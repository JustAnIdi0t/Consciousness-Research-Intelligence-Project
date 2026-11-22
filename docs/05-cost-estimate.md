# 05. Cost estimate

Version 0.1 · November 2026 · Status: draft. Prices checked November 2026; they change, so the pipeline reads them from a config file.

**Budget ceiling: $20 per month, all APIs combined.**

## Free parts

| Item | Cost |
|---|---|
| OpenAlex (free key, $1/day usage budget) | $0 |
| Crossref, PubMed, arXiv | $0 |
| Semantic Scholar (free key, optional) | $0 |
| GitHub repo, GitHub Actions (public repos), GitHub Pages | $0 |
| SQLite, Python | $0 |

So in practice **the only paid item is the Claude API.**

Note: the Claude API is billed separately from a Claude Pro subscription. The owner needs an account on the Claude Console (platform.claude.com) with prepaid credit, and should set a monthly spend limit there as a second safety net.

## Claude API prices used

| Model | Input per million tokens | Output per million tokens | Role |
|---|---|---|---|
| Claude Haiku 5.5 | $0.10 | $0.50 | Bulk screening and coding |
| Claude Sonnet 5.5 | $2.00 | $10.00 | Pilot comparison, hard cases, second opinions |

The Message Batches API halves these prices in exchange for results within 24 hours, which suits this project. Prompt caching cuts the cost of the repeated instructions further, but the estimates below ignore it to stay conservative.

## Assumptions per paper

- Instructions, rubric and schema: about 3,000 tokens (the same for every paper).
- Title, metadata and abstract: about 450 tokens.
- Output: about 150 tokens for screening, about 600 for full coding.
- The models think before answering, which adds output tokens. We run them at low effort and **double the output estimate** as a safety margin.

## Estimated cost per paper (batch prices, with the safety margin)

| Task | Haiku 5.5 | Sonnet 5.5 |
|---|---|---|
| Screening (pass A) | about $0.00025 | about $0.005 |
| Full coding (pass B) | about $0.00050 | about $0.010 |

## What that means in practice

| Job | Papers | Model | Estimated cost |
|---|---|---|---|
| Pilot, both models, full coding | 100 | Haiku + Sonnet | about $1.10 (say $3 with retries and prompt testing) |
| Screen a large candidate set | 20,000 | Haiku | about $5 |
| Full-code the relevant share (assume 40%) | 8,000 | Haiku | about $4 |
| Second opinion on 10% | 2,000 | Sonnet | about $10 |
| Screen 100,000 candidates | 100,000 | Haiku | about $25 (spread over two months) |

We do not yet know how many candidates the broad searches will return. Phase 1 measures it before any large run.

**Rough timeline under the cap:** the pilot costs a few dollars. After that, $15 a month is enough to screen and code tens of thousands of papers, so the realistic limit on pace is human review time, not money.

## How the cap is enforced

1. **Monthly ceiling: $20,** with $15 for planned runs and $5 kept in reserve for retries and experiments.
2. **Per-run cap:** every run declares an estimated cost and a hard maximum (default $5) before it starts. The script counts the real tokens returned and stops before crossing the cap.
3. **Cost ledger:** every run's actual cost is written to `data/runs/` and summed per month in a public file.
4. **Approval:** any single run estimated above $5 needs the owner's explicit OK.
5. **Console spend limit:** set the Anthropic Console monthly limit to $20 so a bug cannot overspend.

## Computing needs

Very light. Harvesting and checks run on GitHub's free servers. The database for a few hundred thousand papers is a few hundred megabytes at most. Nothing needs to run on the owner's Windows computer, though everything can.
