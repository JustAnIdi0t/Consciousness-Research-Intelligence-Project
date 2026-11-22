"""Small, polite OpenAlex client (free API, no key needed for the pilot).

Docs: https://help.openalex.org/api/
"""
from __future__ import annotations

import hashlib
import os
import re
import time
import unicodedata

import requests

BASE = "https://api.openalex.org"

# Fields we request for every work. Keeping this fixed makes runs comparable.
WORK_FIELDS = ",".join([
    "id", "doi", "display_name", "publication_year", "type", "language",
    "primary_location", "best_oa_location", "open_access", "authorships",
    "primary_topic", "abstract_inverted_index", "ids", "cited_by_count",
])

# Licenses under which we may republish full abstract text (docs/06 abstract policy).
OPEN_LICENSES = {"cc-by", "cc-by-sa", "cc0", "public-domain", "cc-by-nc", "cc-by-nc-sa"}


class OpenAlex:
    def __init__(self, api_key: str | None = None, pause: float = 0.25, session=None):
        self.api_key = api_key if api_key is not None else os.environ.get("OPENALEX_API_KEY")
        self.pause = pause
        self.http = session or requests.Session()
        self.http.headers["User-Agent"] = "CRIP research map (public GitHub project)"
        self.requests_made = 0

    def get(self, path: str, params: dict) -> dict:
        params = dict(params)
        if self.api_key:
            params["api_key"] = self.api_key
        for attempt in range(5):
            time.sleep(self.pause)
            r = self.http.get(f"{BASE}{path}", params=params, timeout=60)
            self.requests_made += 1
            if r.status_code == 200:
                return r.json()
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"OpenAlex {r.status_code} for {r.url}: {r.text[:300]}")
        raise RuntimeError(f"OpenAlex kept failing for {path} {params}")

    def works(self, *, search: str | None = None, filters: dict | None = None,
              per_page: int = 100, page: int = 1, sort: str | None = None) -> dict:
        params = {"per_page": per_page, "page": page, "select": WORK_FIELDS}
        if search:
            params["search"] = search
        if filters:
            params["filter"] = ",".join(f"{k}:{v}" for k, v in filters.items())
        if sort:
            params["sort"] = sort
        return self.get("/works", params)


# ---------- helpers that do not touch the network (unit-tested) ----------

def reconstruct_abstract(inverted_index: dict | None) -> str | None:
    """OpenAlex stores abstracts as {word: [positions]}. Rebuild the text."""
    if not inverted_index:
        return None
    positions = []
    for word, idxs in inverted_index.items():
        for i in idxs:
            positions.append((i, word))
    positions.sort()
    text = " ".join(w for _, w in positions).strip()
    return text or None


def normalize_text(s: str) -> str:
    """Normalization used for hashing and for exact-quote checks."""
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def abstract_hash(text: str | None) -> str | None:
    if not text:
        return None
    return "sha256:" + hashlib.sha256(normalize_text(text).encode("utf-8")).hexdigest()


def usable_abstract(text: str | None, min_words: int = 40) -> bool:
    return bool(text) and len(text.split()) >= min_words


def work_license(work: dict) -> str | None:
    for key in ("best_oa_location", "primary_location"):
        loc = work.get(key) or {}
        if loc.get("license"):
            return loc["license"]
    return None


def title_similarity(a: str, b: str) -> float:
    """Word-overlap similarity (0 to 1) between two titles, ignoring case and punctuation."""
    def words(s):
        return set(re.findall(r"[a-z0-9]+", normalize_text(s).lower()))
    wa, wb = words(a or ""), words(b or "")
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def slim_record(work: dict) -> dict:
    """Public record: metadata only. Abstract text is included only under an open license."""
    text = reconstruct_abstract(work.get("abstract_inverted_index"))
    lic = work_license(work)
    topic = work.get("primary_topic") or {}
    src = ((work.get("primary_location") or {}).get("source") or {})
    rec = {
        "openalex_id": work.get("id"),
        "doi": work.get("doi"),
        "title": work.get("display_name"),
        "year": work.get("publication_year"),
        "type": work.get("type"),
        "language": work.get("language"),
        "venue": src.get("display_name"),
        "first_author": ((work.get("authorships") or [{}])[0].get("author") or {}).get("display_name")
                         if work.get("authorships") else None,
        "n_authors": len(work.get("authorships") or []),
        "cited_by_count": work.get("cited_by_count"),
        "topic": topic.get("display_name"),
        "subfield": (topic.get("subfield") or {}).get("display_name"),
        "field": (topic.get("field") or {}).get("display_name"),
        "domain": (topic.get("domain") or {}).get("display_name"),
        "is_oa": (work.get("open_access") or {}).get("is_oa"),
        "license": lic,
        "has_abstract": usable_abstract(text),
        "abstract_words": len(text.split()) if text else 0,
        "abstract_hash": abstract_hash(text),
        "abstract_source": "openalex" if text else None,
        "abstract_open_text": text if (text and lic in OPEN_LICENSES) else None,
    }
    return rec
