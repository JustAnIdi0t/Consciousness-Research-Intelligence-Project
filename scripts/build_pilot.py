"""Build the pilot candidate list (docs/03-pilot-plan.md, step 1).

Free API only (OpenAlex). No AI calls, no paid services.

Public outputs (committed to the repo), in data/pilot/:
  anchor_verification.csv   each anchor paper as remembered vs as found in OpenAlex
  candidate_pools.jsonl     the full ranked candidate pool for every query, so draws are reproducible
  pilot_sample.csv          the 100 + 10 selected papers (metadata only)
  source_records.jsonl      OpenAlex metadata for every selected paper (abstract text only if openly licensed)
  balance_report.md         balance checks and run summary
  run_receipt.json          when, how, how many requests, config checksum

Private output (NOT committed, may contain copyrighted abstracts), in private/:
  labeling_sheet.csv        shuffled, block-blind sheet for the owner's relevance labels
"""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import pathlib
import random
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from crip.openalex import OpenAlex, slim_record, title_similarity, reconstruct_abstract  # noqa: E402
from crip import fallback_abstracts  # noqa: E402

CONFIG = ROOT / "config" / "pilot_queries.yaml"
OUT = ROOT / "data" / "pilot"
PRIVATE = ROOT / "private"
MIN_ABSTRACT_WORDS = 40


def abstract_words(work: dict) -> int:
    return len((reconstruct_abstract(work.get("abstract_inverted_index")) or "").split())


def search_pool(oa: OpenAlex, search: str, size: int, filters: dict) -> tuple[list[dict], int]:
    works, total, page = [], 0, 1
    while len(works) < size:
        res = oa.works(search=search, filters=filters, per_page=min(100, size), page=page)
        total = res["meta"]["count"]
        batch = res["results"]
        works.extend(batch)
        if len(batch) < min(100, size):
            break
        page += 1
    return works[:size], total


def verify_anchor(oa: OpenAlex, a: dict) -> tuple[dict, dict | None]:
    res = oa.works(search=a["title"], filters={"publication_year": f"{a['year'] - 2}-{a['year'] + 2}"}, per_page=10)
    best, best_score = None, 0.0
    for w in res["results"]:
        score = title_similarity(a["title"], w.get("display_name") or "")
        authors = " ".join((au.get("author") or {}).get("display_name") or "" for au in w.get("authorships") or [])
        if a["author"] and a["author"].lower() not in authors.lower():
            score -= 0.3
        # Tie-breakers: prefer the record with an abstract, then the most cited
        score += 0.01 * (abstract_words(w) >= MIN_ABSTRACT_WORDS)
        score += 0.001 * min(w.get("cited_by_count") or 0, 1000) / 1000
        if score > best_score:
            best, best_score = w, score
    status = "verified" if best_score >= 0.85 else ("check" if best_score >= 0.5 else "not_found")
    row = {
        "anchor_id": a["id"], "expected_title": a["title"], "expected_author": a["author"],
        "expected_year": a["year"], "status": status, "match_score": round(best_score, 3),
        "found_title": best.get("display_name") if best else "",
        "found_first_author": ((best.get("authorships") or [{}])[0].get("author") or {}).get("display_name") if best and best.get("authorships") else "",
        "found_year": best.get("publication_year") if best else "",
        "found_doi": best.get("doi") if best else "", "openalex_id": best.get("id") if best else "",
        "found_has_abstract": (abstract_words(best) >= MIN_ABSTRACT_WORDS) if best else "",
    }
    return row, (best if status != "not_found" else None)


def _count(items) -> dict:
    out: dict = {}
    for i in items:
        out[i] = out.get(i, 0) + 1
    return out


def classify_balance(rec: dict) -> set[str]:
    tags = set()
    field, sub = (rec.get("field") or ""), (rec.get("subfield") or "")
    if "Philosophy" in sub or field == "Arts and Humanities":
        tags.add("philosophy")
    if rec.get("type") == "review":
        tags.add("review")
    if field == "Computer Science" or "Artificial Intelligence" in sub:
        tags.add("ai_computational")
    if field in ("Medicine", "Nursing", "Health Professions") or sub in (
            "Neurology", "Anesthesiology and Pain Medicine", "Psychiatry and Mental health"):
        tags.add("clinical")
    return tags


def main() -> None:
    cfg_bytes = CONFIG.read_bytes()
    cfg = yaml.safe_load(cfg_bytes)
    rng = random.Random(cfg["seed"])
    oa = OpenAlex()
    OUT.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(exist_ok=True)

    selected: list[dict] = []   # each: {pilot_id, block, query_id, work}
    seen: set[str] = set()
    pools_out = []

    # Block A: anchors
    anchor_rows = []
    for a in cfg["anchors"]:
        row, work = verify_anchor(oa, a)
        anchor_rows.append(row)
        if work and work["id"] not in seen:
            seen.add(work["id"])
            selected.append({"pilot_id": a["id"], "block": "A_anchor", "query_id": a["id"], "work": work})
        print(f"{a['id']} {row['status']:9} {row['match_score']:.2f}  {row['found_title'][:70]}")

    # Anchors without an OpenAlex abstract: try PubMed, then Crossref, by DOI
    for s_ in selected:
        if s_["block"] == "A_anchor" and abstract_words(s_["work"]) < MIN_ABSTRACT_WORDS:
            text, src = fallback_abstracts.find_abstract(s_["work"].get("doi"))
            s_["fallback"] = (text, src)
            print(f"  {s_['pilot_id']} abstract from fallback: {src or 'none found'}")
        for row in anchor_rows:
            if row["anchor_id"] == s_["pilot_id"] and s_.get("fallback"):
                row["fallback_abstract_source"] = s_["fallback"][1] or "none"
    for row in anchor_rows:
        row.setdefault("fallback_abstract_source", "")

    base_filters = {"language": "en", "has_abstract": "true", "publication_year": f">{cfg['year_min'] - 1}"}

    def draw_block(block_name: str, spec: dict) -> None:
        for q in spec["queries"]:
            pool, total = search_pool(oa, q["search"], cfg["pool_size"], base_filters)
            pools_out.append({"block": block_name, "query_id": q["id"], "label": q["label"], "search": q["search"],
                              "filters": base_filters, "total_matches": total, "pool_ids": [w["id"] for w in pool]})
            eligible = [w for w in pool if w["id"] not in seen and abstract_words(w) >= MIN_ABSTRACT_WORDS]
            picks = rng.sample(eligible, min(spec["per_query"], len(eligible)))
            for n, w in enumerate(picks, 1):
                seen.add(w["id"])
                selected.append({"pilot_id": f"{q['id']}-{n}", "block": block_name, "query_id": q["id"], "work": w})
            print(f"{q['id']:4} matches={total:>8} pool={len(pool)} eligible={len(eligible)} picked={len(picks)}")

    draw_block("B_domain", cfg["domain_draws"])
    draw_block("C_trap", cfg["trap_draws"])

    # Block D: no-abstract records
    na = cfg["no_abstract_draws"]
    na_filters = {"language": "en", "has_abstract": "false", "type": "article",
                  "publication_year": f">{cfg['year_min'] - 1}"}
    pool, total = search_pool(oa, na["search"], cfg["pool_size"], na_filters)
    pools_out.append({"block": "D_no_abstract", "query_id": "NA", "label": "No abstract", "search": na["search"],
                      "filters": na_filters, "total_matches": total, "pool_ids": [w["id"] for w in pool]})
    na_eligible = [w for w in pool if w["id"] not in seen]
    for n, w in enumerate(rng.sample(na_eligible, min(na["count"], len(na_eligible))), 1):
        seen.add(w["id"])
        selected.append({"pilot_id": f"NA-{n}", "block": "D_no_abstract", "query_id": "NA", "work": w})

    # ---- public outputs ----
    with open(OUT / "anchor_verification.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=list(anchor_rows[0].keys()))
        wr.writeheader()
        wr.writerows(anchor_rows)

    with open(OUT / "candidate_pools.jsonl", "w", encoding="utf-8") as f:
        for p in pools_out:
            f.write(json.dumps(p) + "\n")

    records = []
    for s in selected:
        rec = slim_record(s["work"], *(s.get("fallback") or (None, None)))
        rec.update({"pilot_id": s["pilot_id"], "block": s["block"], "query_id": s["query_id"]})
        rec["balance_tags"] = sorted(classify_balance(rec))
        records.append(rec)

    with open(OUT / "source_records.jsonl", "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    cols = ["pilot_id", "block", "query_id", "openalex_id", "doi", "title", "year", "type", "venue",
            "first_author", "field", "subfield", "cited_by_count", "has_abstract", "abstract_words", "license",
            "balance_tags"]
    with open(OUT / "pilot_sample.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        wr.writeheader()
        for r in records:
            wr.writerow({**r, "balance_tags": ";".join(r["balance_tags"])})

    # Balance checks on the coded papers (blocks A to C)
    coded = [r for r in records if r["block"] != "D_no_abstract"]
    counts = {k: sum(1 for r in coded if k in r["balance_tags"])
              for k in ("philosophy", "review", "ai_computational", "clinical")}
    decades = sorted({(r["year"] // 10) * 10 for r in coded if r.get("year")})
    mins = cfg["balance_minimums"]
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    lines = ["# Pilot balance report", "",
             f"Generated {now} from `config/pilot_queries.yaml` v{cfg['version']} (seed {cfg['seed']}).", "",
             "Tags come from OpenAlex metadata (primary topic field and work type). They are rough proxies, not our coding.",
             "", "| Block | Papers |", "|---|---|"]
    for b in ("A_anchor", "B_domain", "C_trap", "D_no_abstract"):
        lines.append(f"| {b} | {sum(1 for r in records if r['block'] == b)} |")
    lines += ["", "| Check | Minimum | Found | Pass |", "|---|---|---|---|"]
    for k in ("philosophy", "review", "ai_computational", "clinical"):
        lines.append(f"| {k} | {mins[k]} | {counts[k]} | {'yes' if counts[k] >= mins[k] else 'NO'} |")
    lines.append(f"| decades | {mins['decades']} | {len(decades)} ({', '.join(str(d) + 's' for d in decades)}) | "
                 f"{'yes' if len(decades) >= mins['decades'] else 'NO'} |")
    a_status: dict[str, int] = {}
    for r in anchor_rows:
        a_status[r["status"]] = a_status.get(r["status"], 0) + 1
    lines += ["", "## Anchor verification", "", ", ".join(f"{k}: {v}" for k, v in sorted(a_status.items())),
              "", "Anchors marked `check` or `not_found` need a human look before the pilot is frozen.",
              "", "Abstract sources for anchors: " + ", ".join(
                  f"{k}: {v}" for k, v in sorted(_count(r['abstract_source'] or 'none' for r in records if r['block'] == 'A_anchor').items())),
              "", "## Query sizes", "", "| Query | Label | Total OpenAlex matches |", "|---|---|---|"]
    for p in pools_out:
        lines.append(f"| {p['query_id']} | {p['label']} | {p['total_matches']:,} |")
    (OUT / "balance_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    receipt = {
        "run": "build_pilot", "finished_at": now,
        "config": "config/pilot_queries.yaml", "config_sha256": hashlib.sha256(cfg_bytes).hexdigest(),
        "seed": cfg["seed"], "openalex_requests": oa.requests_made, "used_api_key": bool(oa.api_key),
        "papers_selected": len(records), "paid_api_cost_usd": 0.0,
    }
    (OUT / "run_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    # ---- private, block-blind labeling sheet (shuffled, abstracts included, never committed) ----
    sheet = [s for s in selected if s["block"] != "D_no_abstract"]  # includes anchors even if no abstract was found
    random.Random(cfg["seed"] + 1).shuffle(sheet)
    with open(PRIVATE / "labeling_sheet.csv", "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["row", "openalex_id", "title", "year", "venue", "abstract", "your_label", "your_note"])
        for i, s in enumerate(sheet, 1):
            w = s["work"]
            venue = (((w.get("primary_location") or {}).get("source")) or {}).get("display_name")
            wr.writerow([i, w.get("id"), w.get("display_name"), w.get("publication_year"), venue,
                         reconstruct_abstract(w.get("abstract_inverted_index"))
                         or (s.get("fallback") or (None, None))[0] or "(no abstract found)",
                         "", ""])
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
