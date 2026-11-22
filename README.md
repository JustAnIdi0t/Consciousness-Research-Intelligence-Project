# Consciousness Research Intelligence Platform (CRIP)

CRIP is a public, source-grounded map of consciousness research. It collects published work on consciousness, sorts out what each paper is actually about, and links papers to the theories and phenomena they address. Every step, prompt, decision and dataset lives in this repository so anyone can check how a conclusion was reached.

**Status:** Foundation planning (version 0.1, November 2026). No code has been written and no paid API has been called yet.

## Why it exists

- To give researchers (including a contact at RAND) a map of the whole field: which questions are studied, by whom, with which methods, and which theories they bear on.
- To help the project owner orient for PhD applications in consciousness science.
- To be openly available to anyone in the field.
- To be a learning project, done carefully and in the open.

## Ground rules

1. **A mention is not evidence.** A paper that mentions a theory is not a test of it.
2. **Every claim points to its source,** ideally an exact quote from the abstract.
3. **AI output is a draft until validated.** Invalid AI output is quarantined, never quietly accepted.
4. **Missing data is missing,** not a "no".
5. **Everything is versioned:** the rubric, the schema, the prompts, the model used and the review decisions.
6. **Budget ceiling:** $20 per month for all APIs combined.

## Read the plan

| # | Document | What it answers |
|---|---|---|
| 0 | [Architecture proposal](docs/00-architecture-proposal.md) | How the system is built, where data comes from, and what each source allows |
| 1 | [Scope and relevance rubric](docs/01-scope-and-relevance-rubric.md) | What counts as consciousness research, and how a paper is judged relevant |
| 2 | [Coding schema](docs/02-coding-schema.md) | The structured fields extracted from each abstract |
| 3 | [Pilot plan](docs/03-pilot-plan.md) | How the first ~100 papers are chosen and coded |
| 4 | [Validation plan](docs/04-validation-plan.md) | How quality is checked with a few hours of human review per week |
| 5 | [Cost estimate](docs/05-cost-estimate.md) | What it costs to run, and how the $20 cap is enforced |
| 6 | [Risks and open questions](docs/06-risks-and-open-questions.md) | What could go wrong, and decisions still to make |
| – | [Decision log](docs/decision-log.md) | Every decision, with date and reason |

## Licensing (proposed)

- Code: MIT license.
- Our own codings, rubric and documents: CC BY 4.0.
- Third-party metadata keeps its source license (OpenAlex is CC0). Publisher abstracts are handled under the policy in [Risks and open questions](docs/06-risks-and-open-questions.md).
