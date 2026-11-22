# 00. Architecture proposal

Version 0.1 · November 2026 · Status: draft for owner review

## The short version

CRIP is a pipeline of small, separate steps. Each step reads data, does one job, and writes its result plus a receipt saying what it did. All of it runs from one public GitHub repository.

1. **Harvest.** Scripts ask free scholarly databases for candidate papers using deliberately broad searches. Raw responses are saved unchanged.
2. **Reconcile.** Records from different sources are matched into one publication record, by DOI first. Uncertain matches are flagged, not merged.
3. **Screen.** A cheap AI model applies the relevance rubric to each title and abstract. This decides relevance, not the keyword search.
4. **Code.** Papers that pass screening get full structured coding: domain, method, theory roles, claims with exact quotes.
5. **Validate.** Automatic checks (schema, exact-quote matching) run on every record. Human spot checks run on samples.
6. **Publish.** Versioned, checksummed exports go to the repository. A small website comes later.

Nothing moves to the next step without passing the checks of the step before it.

## Where things live

| What | Where | Public? |
|---|---|---|
| Code, rubric, schema, prompts, these documents | GitHub repo | Yes |
| Authoritative research database | A single SQLite file, rebuilt from scripts | Yes, as a versioned release file (see note) |
| Raw API responses | Compressed files, attached to releases | Metadata yes; abstract text follows the abstract policy in doc 06 |
| Human review decisions | CSV files in the repo | Yes |
| Coding runs (inputs, raw model output, receipts, cost) | JSONL files in the repo | Yes |
| API keys | GitHub Secrets and a local `.env` file | Never |

**Why SQLite:** it is one file, free, needs no server, and is easy for anyone to download and query. It is plenty for a few hundred thousand papers. A graph view (theories, phenomena, findings) can be generated from it later without making the graph the source of truth.

**Why files plus a database:** git tracks changes well in text files (CSV, JSONL) and badly in a binary database. So the plain-text exports are the reviewable record, and the SQLite file is rebuilt from them and published with each release, along with a checksum.

## Proposed repository layout

```
crip/
  README.md
  docs/                  plans, rubric, decision log
  schema/                versioned JSON schemas (coding-v0.1.json, ...)
  prompts/               versioned prompts (screen-v0.1.md, code-v0.1.md, ...)
  registry/              human-curated theories and phenomena (YAML)
  src/                   harvest, reconcile, screen, code, validate, export
  data/
    pilot/               pilot sample list and gold-standard labels
    reviews/             human spot-check decisions
    runs/                one folder per coding run: receipt, raw outputs, rejects
    exports/             versioned CSV/JSONL snapshots with checksums
  tests/                 deduplication tests, schema tests, quote-match tests
  .github/workflows/     scheduled harvests and checks (GitHub Actions)
```

## Main tables in the database

Plain-language version. The precise columns go in `schema/` once coding starts.

- **publications:** one row per real-world work. Title, year, venue, type, open-access status.
- **identifiers:** DOI, PubMed ID, arXiv ID, OpenAlex ID, linked to a publication.
- **source_records:** every raw record from every source, kept even if the paper is later excluded. Records which search found it (the "discovery pathway").
- **match_conflicts:** possible duplicates the system was not sure about, waiting for a human.
- **authors, institutions, citations:** from OpenAlex, mainly for the field map.
- **abstracts:** text, which source it came from, and its license status. Papers with no usable abstract get a status of `no_abstract` and are never coded as "not relevant".
- **screening_results** and **codings:** one row per paper per run, with schema version, prompt version, model, timestamp, cost and validation status (`accepted`, `quarantined`, `rejected`).
- **claims:** extracted propositions, each with an exact supporting quote and a flag for author-stated vs AI-inferred.
- **theories, phenomena:** the human-curated registry.
- **links:** paper-to-theory and paper-to-phenomenon links, with the role (proposes, tests, mentions...) and whether a human or the AI made the link.

## Literature sources and access constraints

Checked November 2026.

| Source | Use for | Cost | Key needed | Constraints |
|---|---|---|---|---|
| **OpenAlex** | Main discovery, citations, authors, abstracts, field map | Free | Free key recommended | Free key gives a $1/day usage budget (list request about $0.0001, search about $0.001), roughly 10,000 list pages of up to 100 records a day. Data is CC0. Basic paging stops at 10,000 results, so large queries use cursor paging, which needs the key. |
| **Crossref** | DOI checks, metadata reconciliation | Free | No (add a contact email to requests for the faster "polite" pool, using a project address) | Abstracts present only for some publishers. |
| **PubMed (NCBI E-utilities)** | Clinical and neuroscience work: anesthesia, coma, disorders of consciousness | Free | Free key raises the limit from 3 to 10 requests a second | Abstracts may be under publisher copyright. Metadata is fine to share. |
| **arXiv** | AI consciousness, computational models, preprints | Free | No | Polite rate limit (about one request every 3 seconds). Metadata is CC0. Each paper has its own license for the abstract and text. |
| **Semantic Scholar** | Extra citation coverage, optional | Free | Free key on request | License limits redistribution of some fields. Treat as optional in phase 1. |
| **PhilPapers** | Philosophy of mind | Free JSON API | No registration, but they ask to be told | Terms "severely restrict the redistribution" of their data. We can use it to find philosophy papers, then fetch the published metadata from OpenAlex or Crossref. We should email PhilPapers before relying on it. |

**Practical consequence:** OpenAlex does most of the work. PubMed fills clinical gaps. arXiv fills AI gaps. Philosophy coverage will be the weakest area at first, so the coverage report must say so plainly.

## Technology choices

- **Language:** Python. Free, widely used in research, runs on Windows and on GitHub's servers.
- **Running jobs:** GitHub Actions, which is free for public repositories. Harvests and checks can run on a schedule without the owner's computer being on.
- **AI coding:** Claude via the Anthropic API, using the Message Batches API (half price, results within 24 hours) and structured outputs so every response must match the schema. Claude Haiku 5.5 for bulk work, Claude Sonnet 5.5 for the pilot comparison and hard cases. See [Cost estimate](05-cost-estimate.md).
- **Website (later):** GitHub Pages, free, static.

## Safety rails built in from day one

- **Idempotent runs:** running a step twice never duplicates data or spend. Each run has an ID and a receipt.
- **Spend guard:** every coding run states its cost estimate and a hard cap before it starts, and stops if the cap would be crossed.
- **No silent fixes:** invalid AI output is saved in `rejects/` with the reason. It is retried or reviewed, never patched into accepted data.
- **Backups:** each release is a milestone snapshot. GitHub is one copy; the owner keeps one downloaded copy of each milestone release.
- **Approval gates:** large spends, deleting data, changes to the registry, and publishing the website need the owner's explicit OK.

## Suggested build order after this plan is approved

1. Create the repo, commit these documents, and add a decision log.
2. Owner reviews the rubric (doc 01) and labels the pilot (doc 03).
3. Build harvest and reconcile for OpenAlex only. Write deduplication tests.
4. Run the pilot coding and the audit in doc 04.
5. Only then add PubMed and arXiv, and scale coding.
