import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))

from crip.openalex import (reconstruct_abstract, abstract_hash, title_similarity,
                           slim_record, usable_abstract)


def test_reconstruct_abstract_orders_words():
    inv = {"world": [1], "hello": [0], "again": [3], "hello,": [2]}
    assert reconstruct_abstract(inv) == "hello world hello, again"


def test_reconstruct_abstract_empty():
    assert reconstruct_abstract(None) is None
    assert reconstruct_abstract({}) is None


def test_hash_ignores_whitespace_and_curly_quotes():
    assert abstract_hash("A  “quoted” text") == abstract_hash('A "quoted" text')


def test_title_similarity():
    assert title_similarity("Theories of consciousness", "Theories of Consciousness.") == 1.0
    assert title_similarity("Theories of consciousness", "Rubber hands feel touch") == 0.0


def test_slim_record_withholds_closed_abstract():
    words = {f"w{i}": [i] for i in range(50)}
    work = {"id": "W1", "display_name": "T", "abstract_inverted_index": words,
            "primary_location": {"license": None, "source": {"display_name": "J"}}}
    rec = slim_record(work)
    assert rec["has_abstract"] is True
    assert rec["abstract_hash"].startswith("sha256:")
    assert rec["abstract_open_text"] is None


def test_slim_record_keeps_open_abstract():
    words = {f"w{i}": [i] for i in range(50)}
    work = {"id": "W2", "display_name": "T", "abstract_inverted_index": words,
            "best_oa_location": {"license": "cc-by"}}
    assert slim_record(work)["abstract_open_text"].startswith("w0 w1")


def test_short_abstract_not_usable():
    assert usable_abstract("too short") is False
