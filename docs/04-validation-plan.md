# 04. Validation plan

Version 0.1 · November 2026 · Status: draft

The owner can review a few hours a week, not every paper. So quality comes from three layers: **automatic checks on everything**, **model-vs-model disagreement to find likely errors**, and **small random human samples** to estimate error rates honestly. Every review decision is saved in `data/reviews/` so anyone can audit it.

## Layer 1: automatic checks (every record, free)

| Check | What fails |
|---|---|
| Schema validation | Any missing field, wrong type or value not on the allowed list |
| Exact-quote match | Any quote that is not word for word in the abstract |
| Registry check | Unknown theory or phenomenon ids |
| Consistency rules | e.g. "tests_prediction" with no result claim; theory links on excluded papers |
| Deduplication tests | Known duplicate pairs must merge; known look-alike pairs must not |

Failures go to quarantine, never into the accepted data. Quarantine rate is reported for every run. A run with more than 5% quarantined records is stopped and investigated before continuing.

## Layer 2: disagreement flags (cheap)

A second, independent screening pass on a slice of papers (for example Claude Sonnet 5.5 on 10% of what Claude Haiku 5.5 screened) shows where the models disagree. Disagreements are the most likely errors, so they go to the front of the human review queue. This focuses the owner's limited time where it matters most.

## Layer 3: human spot checks (sampled)

### What gets sampled each batch

| Sample | Size per batch | Why |
|---|---|---|
| Random included papers (core, substantial) | 20 | Estimates how often we include things wrongly |
| **Random excluded papers** (incidental, unrelated) | 30 | Estimates how often we miss real consciousness research. The outline insists on checking exclusions too |
| Random "unclear" | 10 | Checks whether unclear is being overused |
| Model disagreements | up to 20 | Finds systematic rubric problems |
| Random full codings: theory roles and claims | 10 | Checks the richer fields |

Reviewing one batch takes about 2 to 3 hours, so roughly one batch a week.

### How the owner reviews

A spreadsheet per batch (generated automatically) with the title, abstract, the AI's answer, and columns for "agree / disagree / unsure" and a note. The owner never edits the AI's coding directly; their decision is stored as a separate human record, and the published data shows both.

### What the numbers can and cannot tell us

Samples are small, so we report error rates with honest ranges. A useful rule of thumb: if we check *n* excluded papers and find **zero** errors, the true error rate is still plausibly up to about 3 / *n* (the "rule of three"). Thirty clean exclusions means "probably under 10%", not "zero". To claim under 5% we need about 60 clean exclusions, which means pooling two batches. The coverage report will always state these ranges.

## Thresholds for scaling up

Measured on the pilot, then re-checked on every new batch.

| Measure | Target | If missed |
|---|---|---|
| Relevance agreement with owner (core+substantial vs the rest) | ≥ 85% | Revise rubric or prompt, re-run pilot slice |
| Wrongly excluded relevant papers (in excluded sample) | ≤ 5% (pooled) | Loosen screening, or send "incidental" to a second model |
| Wrongly included papers (in included sample) | ≤ 10% | Tighten rubric |
| Exact-quote match rate | ≥ 99% | Fix prompt; never accept unmatched quotes |
| Theory role correct ("tests" vs "mentions") | ≥ 80% on sampled codings | Restrict roles, add examples, or use Sonnet for theory links |
| Quarantine rate | ≤ 5% | Stop the run and investigate |

## Things the plan guards against

- **Treating counts as evidence strength.** The site will never say "theory X has the most support" because more papers mention it.
- **Silent drift.** Any change to the prompt, model, schema or rubric gets a new version number, and a small re-test on the pilot gold set before use.
- **Owner as single point of view.** Where possible, invite a second reviewer (for example the RAND contact) for 20 papers per quarter to measure human agreement.
- **Publishing restricted text.** See abstract policy in [Risks and open questions](06-risks-and-open-questions.md).
