# 03. Pilot plan (about 100 publications)

Version 0.1 · November 2026 · Status: draft

## Purpose

Before coding thousands of papers, we test the rubric, the schema and the prompts on a small, deliberately varied set where we know the right answers. The pilot answers three questions:

1. Does the AI judge relevance the way the owner would?
2. Are the extracted quotes, theory roles and claims accurate?
3. Is Claude Haiku 5.5 good enough for bulk work, or do some fields need Claude Sonnet 5.5?

## Composition: 100 papers plus 10 extras

| Block | Count | How chosen | Expected relevance |
|---|---|---|---|
| A. Anchor papers | 20 | Well-known works listed below, picked by hand | Mostly core |
| B. Domain draws | 50 | 5 per domain D1 to D10, drawn at random from OpenAlex search results with a recorded random seed | Mixed |
| C. Trap papers | 30 | Random draws from searches built to hit the false-positive traps in the rubric (situational awareness, environmental consciousness, transformer attention, arousal ratings, anesthesia dosing, priming without awareness tests) | Mostly incidental or unrelated |
| D. No-abstract records | 10 (extra) | Records OpenAlex returns without an abstract | Status `no_abstract`, not coded |

**Balance checks** before the pilot is frozen: at least 15 philosophical works, at least 10 reviews, at least 8 AI or computational works, at least 10 clinical works, and publication years spread across at least four decades. If a check fails, swap random draws, and log the swap.

The final list, the exact search queries, the random seed and every swap are committed to `data/pilot/` so anyone can reproduce the selection.

## Candidate anchor papers

These are well-known works chosen to cover the theories and phenomena. **Details are from memory and will be verified against OpenAlex and Crossref (DOI, year, venue) before use.** Any that cannot be verified are replaced.

| # | Work | Covers |
|---|---|---|
| 1 | Chalmers (1995), "Facing up to the problem of consciousness", *Journal of Consciousness Studies* | D1, philosophical |
| 2 | Block (1995), "On a confusion about a function of consciousness", *Behavioral and Brain Sciences* | D1, D2 |
| 3 | Dehaene & Changeux (2011), "Experimental and theoretical approaches to conscious processing", *Neuron* | GNWT, review |
| 4 | Tononi (2004), "An information integration theory of consciousness", *BMC Neuroscience* | IIT, proposes |
| 5 | Lamme (2006), "Towards a true neural stance on consciousness", *Trends in Cognitive Sciences* | RPT |
| 6 | Lau & Rosenthal (2011), "Empirical support for higher-order theories of conscious awareness", *Trends in Cognitive Sciences* | HOT |
| 7 | Graziano & Webb (2015), "The attention schema theory: a mechanistic account of subjective awareness", *Frontiers in Psychology* | AST |
| 8 | O'Regan & Noë (2001), "A sensorimotor account of vision and visual consciousness", *Behavioral and Brain Sciences* | Sensorimotor |
| 9 | Seth & Bayne (2022), "Theories of consciousness", *Nature Reviews Neuroscience* | Review, many theories |
| 10 | Koch, Massimini, Boly & Tononi (2016), "Neural correlates of consciousness: progress and problems", *Nature Reviews Neuroscience* | D3 |
| 11 | Cogitate Consortium (2025), adversarial test of global workspace and integrated information theories, *Nature* | Compares theories, tests predictions |
| 12 | Tsuchiya, Wilke, Frässle & Lamme (2015), "No-report paradigms: extracting the true neural correlates of consciousness", *Trends in Cognitive Sciences* | Methods, report problem |
| 13 | Owen et al. (2006), "Detecting awareness in the vegetative state", *Science* | D4, covert awareness |
| 14 | Casali et al. (2013), "A theoretically based index of consciousness independent of sensory processing and behavior", *Science Translational Medicine* | D4, measurement |
| 15 | Siclari et al. (2017), "The neural correlates of dreaming", *Nature Neuroscience* | Dreaming |
| 16 | Botvinick & Cohen (1998), "Rubber hands 'feel' touch that eyes see", *Nature* | D6, body ownership |
| 17 | Fleming & Lau (2014), "How to measure metacognition", *Frontiers in Human Neuroscience* | Metacognition, methods |
| 18 | Carhart-Harris et al. (2016), neural correlates of the LSD experience, *PNAS* | D9 |
| 19 | Butlin et al. (2023), "Consciousness in artificial intelligence: insights from the science of consciousness", arXiv | D8 |
| 20 | Frankish (2016), "Illusionism as a theory of consciousness", *Journal of Consciousness Studies* | Philosophical position |

Gaps to fill from the domain draws: blindsight, binocular rivalry, inattentional blindness, animal consciousness, predictive processing.

## Steps and who does what

| Step | Who | Owner time |
|---|---|---|
| 1. Build the candidate list (blocks A to D), verify anchors, run balance checks | Claude | none |
| 2. **Owner labels relevance only** for all 100, blind to the AI's answer, using a simple spreadsheet (title, abstract, a dropdown for the level, an optional note) | Owner | about 2.5 hours (about 1.5 minutes per paper) |
| 3. Code all 100 with Claude Sonnet 5.5 and with Claude Haiku 5.5, using the same prompt | Claude | none |
| 4. Run automatic checks (schema, exact quotes, registry ids) | Claude | none |
| 5. Compare: owner vs each model on relevance; Haiku vs Sonnet on every field | Claude | none |
| 6. **Owner reviews disagreements** plus a random 20 of the full codings (theory roles, claims) | Owner | about 2 hours |
| 7. Write the pilot report, propose rubric 0.2 and schema 0.2 | Claude | none |
| 8. Owner approves version 0.2 | Owner | about 30 minutes |

**Total owner time:** about 5 hours, spread over two to three weeks.

The owner's RAND contact could optionally label 20 of the same papers. That would show how much two humans agree, which sets a realistic target for the AI.

## Pilot cost

Under $3 in API charges for both models together. See [Cost estimate](05-cost-estimate.md).

## Exit criteria (when we are ready to scale)

See the thresholds in [Validation plan](04-validation-plan.md). In short: relevance agreement with the owner at least 85%, no more than 1 in 20 relevant papers wrongly excluded, and at least 99% of quotes matching exactly. If Haiku misses the bar but Sonnet passes, we use Haiku for screening and Sonnet for full coding, within budget.
