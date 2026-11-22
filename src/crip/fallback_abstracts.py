"""Fill missing abstracts from other free sources, by DOI: PubMed first, then Crossref.

Used when OpenAlex has no abstract for a paper we specifically need (for example an anchor paper).
The source of every abstract is recorded, and the copyright policy in docs/06 still applies.
"""
from __future__ import annotations

import html
import re
import time
import xml.etree.ElementTree as ET

import requests

UA = {"User-Agent": "CRIP research map (public GitHub project)"}


def _bare_doi(doi: str) -> str:
    return re.sub(r"^https?://(dx\.)?doi\.org/", "", doi or "", flags=re.I).strip()


def strip_markup(s: str) -> str:
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"^\s*(Abstract|ABSTRACT)\s*[:.]?\s*", "", s)
    return re.sub(r"\s+", " ", s).strip()


def pubmed_abstract(doi: str, http=None) -> str | None:
    http = http or requests
    d = _bare_doi(doi)
    if not d:
        return None
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    time.sleep(0.4)
    r = http.get(f"{base}/esearch.fcgi", params={"db": "pubmed", "term": f"{d}[doi]", "retmode": "json"},
                 headers=UA, timeout=60)
    if r.status_code != 200:
        return None
    ids = r.json().get("esearchresult", {}).get("idlist", [])
    if len(ids) != 1:
        return None
    time.sleep(0.4)
    r = http.get(f"{base}/efetch.fcgi", params={"db": "pubmed", "id": ids[0], "retmode": "xml"},
                 headers=UA, timeout=60)
    if r.status_code != 200:
        return None
    root = ET.fromstring(r.content)
    parts = []
    for el in root.iter("AbstractText"):
        text = "".join(el.itertext()).strip()
        label = el.get("Label")
        parts.append(f"{label}: {text}" if label else text)
    text = " ".join(p for p in parts if p).strip()
    return text or None


def crossref_abstract(doi: str, http=None) -> str | None:
    http = http or requests
    d = _bare_doi(doi)
    if not d:
        return None
    time.sleep(0.2)
    r = http.get(f"https://api.crossref.org/works/{d}", headers=UA, timeout=60)
    if r.status_code != 200:
        return None
    raw = r.json().get("message", {}).get("abstract")
    return strip_markup(raw) if raw else None


def find_abstract(doi: str | None) -> tuple[str | None, str | None]:
    """Returns (abstract_text, source_name) or (None, None)."""
    if not doi:
        return None, None
    for name, fn in (("pubmed", pubmed_abstract), ("crossref", crossref_abstract)):
        try:
            text = fn(doi)
        except Exception as e:  # network trouble should not stop the run
            print(f"  {name} lookup failed for {doi}: {e}")
            text = None
        if text and len(text.split()) >= 40:
            return text, name
    return None, None
