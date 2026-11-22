"""Runs the whole pilot builder against a fake OpenAlex, so it can be checked without network."""
import csv, json, pathlib, random, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import build_pilot  # noqa: E402


class FakeOA:
    def __init__(self):
        self.api_key = None
        self.requests_made = 0
        self.n = 0

    def works(self, search=None, filters=None, per_page=100, page=1, sort=None):
        self.requests_made += 1
        no_abs = (filters or {}).get("has_abstract") == "false"
        results = []
        for _ in range(per_page if page <= 2 else 0):
            self.n += 1
            words = {} if no_abs else {f"w{i}": [i] for i in range(60)}
            results.append({
                "id": f"https://openalex.org/W{self.n}", "display_name": search, "publication_year": 1975 + self.n % 50,
                "type": "review" if self.n % 7 == 0 else "article", "abstract_inverted_index": words,
                "authorships": [{"author": {"display_name": "Chalmers Block Dehaene"}}],
                "primary_topic": {"field": {"display_name": random.choice(["Medicine", "Computer Science", "Arts and Humanities", "Neuroscience"])},
                                   "subfield": {"display_name": "Philosophy"}},
                "primary_location": {"license": "cc-by" if self.n % 3 == 0 else None, "source": {"display_name": "J"}},
                "cited_by_count": 5,
            })
        return {"meta": {"count": 1234}, "results": results}


def test_offline_build(tmp_path, monkeypatch):
    monkeypatch.setattr(build_pilot, "OpenAlex", FakeOA)
    monkeypatch.setattr(build_pilot.fallback_abstracts, "find_abstract", lambda doi: ("pubmed text " * 30, "pubmed"))
    monkeypatch.setattr(build_pilot, "OUT", tmp_path / "pilot")
    monkeypatch.setattr(build_pilot, "PRIVATE", tmp_path / "private")
    build_pilot.main()
    rows = list(csv.DictReader(open(tmp_path / "pilot" / "pilot_sample.csv", encoding="utf-8")))
    blocks = [r["block"] for r in rows]
    assert blocks.count("A_anchor") == 20
    assert blocks.count("B_domain") == 50
    assert blocks.count("C_trap") == 30
    assert blocks.count("D_no_abstract") == 10
    assert len({r["openalex_id"] for r in rows}) == 110  # no duplicates
    # Closed-license abstracts never reach public files
    for line in open(tmp_path / "pilot" / "source_records.jsonl", encoding="utf-8"):
        rec = json.loads(line)
        if rec["license"] != "cc-by":
            assert rec["abstract_open_text"] is None
    # Labeling sheet is blind to blocks
    sheet = list(csv.DictReader(open(tmp_path / "private" / "labeling_sheet.csv", encoding="utf-8-sig")))
    assert len(sheet) == 100 and "block" not in sheet[0] and "pilot_id" not in sheet[0]
