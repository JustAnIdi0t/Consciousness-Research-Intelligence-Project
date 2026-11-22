# Pilot data

Produced by `scripts/build_pilot.py` from `config/pilot_queries.yaml`, run on GitHub Actions (`.github/workflows/pilot-harvest.yml`). Uses the free OpenAlex API only. No AI calls.

| File | What it is |
|---|---|
| `anchor_verification.csv` | The 20 anchor papers as listed from memory, next to what OpenAlex actually holds. `check` or `not_found` rows need a human look |
| `candidate_pools.jsonl` | For every query: the exact search, filters, total matches and the ranked pool of OpenAlex ids the random draw was made from. With the seed, this makes the draw reproducible even if OpenAlex changes |
| `pilot_sample.csv` | The selected papers: 20 anchors (A), 50 domain draws (B), 30 trap draws (C), 10 no-abstract records (D) |
| `source_records.jsonl` | OpenAlex metadata for each selected paper, plus an abstract fingerprint. Full abstract text only when openly licensed (docs/06 abstract policy) |
| `balance_report.md` | Balance checks against docs/03 minimums, anchor results, query sizes |
| `run_receipt.json` | When it ran, config checksum, seed, request count, cost ($0) |

The owner's labeling sheet contains full abstracts, so it is not committed. It is kept for 7 days as a workflow artifact named `private-labeling-sheet`.
