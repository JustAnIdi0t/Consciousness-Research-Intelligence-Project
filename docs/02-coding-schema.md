# 02. Preliminary coding schema

Version 0.1 · November 2026 · Status: draft, will change after the pilot

"Coding" means turning an abstract into structured fields that can be searched, counted and compared. This is not a summary. Every field has a fixed list of allowed values, and the AI's answer is rejected if it does not match the schema exactly.

Coding happens in two passes:

- **Pass A, screening** (every candidate paper, cheapest model): relevance level, reason, domain guess. About 10 fields.
- **Pass B, full coding** (core and substantial papers only): all fields below.

## Record-level fields

| Field | Allowed values | Notes |
|---|---|---|
| `relevance` | core, substantial, incidental, unrelated, unclear | From the rubric (doc 01) |
| `relevance_reason` | short text | One sentence |
| `relevance_quote` | exact text from the abstract, or null | Checked automatically |
| `work_kind` | empirical, theoretical_model, philosophical, review, methods, commentary | One primary, optional secondary |
| `domains` | D1 to D10 (list) | One or more |
| `discipline` | neuroscience, psychology, psychiatry_neurology_clinical, philosophy, computer_science_ai, biology_animal, physics_math, other | Of the paper, not the topic |
| `consciousness_target` | phenomenal, access, level_or_state, content, self, metacognition, unconscious_processing, not_specified (list) | What aspect of consciousness |
| `population` | human_healthy, human_clinical, nonhuman_animal, artificial_system, simulation, none (list) | `none` for pure philosophy |
| `clinical_condition` | text or null | e.g. "minimally conscious state" |
| `methods` | eeg_meg, fmri, pet, intracranial, tms_stimulation, lesion, pharmacological, behavioral_psychophysics, report_questionnaire, no_report_paradigm, computational_model, formal_analysis, conceptual_argument, literature_review, other (list) | |
| `consciousness_measure` | subjective_report, confidence_rating, forced_choice_performance, no_report_marker, clinical_scale, neural_index, none, not_stated (list) | How consciousness was operationalized. Key for the "report is not experience" lesson |
| `phenomena` | ids from the phenomena registry (list) | e.g. visual_masking, binocular_rivalry, blindsight |
| `outcome_type` | positive_result, null_result, mixed, no_empirical_result, not_stated | As stated by the authors |
| `sample_size` | number or null | Only if stated in the abstract |

## Theory links

A list, one entry per theory the abstract involves. **A mention is not evidence.**

| Field | Allowed values |
|---|---|
| `theory_id` | id from the theory registry, or `unregistered:<name as written>` |
| `roles` | proposes, develops, tests_prediction, reports_bearing_finding, compares, critiques, applies_as_framework, mentions_background (list, compound allowed) |
| `stance_stated_by_authors` | supports, challenges, mixed, neutral, not_stated |
| `quote` | exact text from the abstract |
| `link_origin` | ai_suggested (always, at this stage); later human_confirmed or human_rejected |

`tests_prediction` requires the abstract to describe a prediction and a test of it. Otherwise the strongest allowed role is `reports_bearing_finding` or `mentions_background`.

### Starter theory registry (ids)

Curated by hand, aliases added over time.

| id | Theory or family | Category |
|---|---|---|
| gnwt | Global (Neuronal) Workspace Theory | neuroscientific |
| iit | Integrated Information Theory | neuroscientific / formal |
| rpt | Recurrent Processing Theory | neuroscientific |
| hot | Higher-Order Theories (incl. perceptual reality monitoring, higher-order thought) | neuroscientific / philosophical |
| pp | Predictive Processing and Active Inference accounts | neuroscientific / computational |
| ast | Attention Schema Theory | neuroscientific / computational |
| enactive | Sensorimotor and Enactive approaches | philosophical / cognitive |
| other_sci | Other scientific theories (e.g. dendritic integration, temporo-spatial, unfolding argument responses) | grows from pilot |
| phil_physicalism, phil_illusionism, phil_dualism, phil_panpsychism, phil_idealism, phil_russellian_monism | Metaphysical positions | philosophical (kept separate) |

## Claims (propositions)

For core and substantial papers, up to five claims.

| Field | Allowed values | Notes |
|---|---|---|
| `claim_kind` | question, hypothesis, manipulation_or_measure, result, interpretation, limitation, prediction_evaluated | Mirrors the outline's seven questions |
| `text` | short paraphrase | |
| `quote` | exact text from the abstract | **Required.** If no quote supports it, the claim is not recorded |
| `origin` | author_stated, ai_inferred | ai_inferred claims are allowed only for `claim_kind = interpretation` and are shown separately |

## Provenance and status (filled in by the pipeline, not the AI)

`publication_id`, `abstract_source`, `abstract_hash`, `schema_version`, `rubric_version`, `prompt_version`, `model`, `run_id`, `timestamp`, `input_tokens`, `output_tokens`, `cost_usd`, `validation_status` (accepted, quarantined, rejected), `validation_errors`.

## Example (invented abstract, for format only)

```json
{
  "relevance": "core",
  "relevance_reason": "Contrasts seen and unseen masked stimuli to identify neural markers of conscious perception.",
  "relevance_quote": "trials reported as seen versus unseen",
  "work_kind": ["empirical"],
  "domains": ["D3", "D5"],
  "discipline": "neuroscience",
  "consciousness_target": ["content"],
  "population": ["human_healthy"],
  "methods": ["eeg_meg", "behavioral_psychophysics"],
  "consciousness_measure": ["subjective_report"],
  "phenomena": ["visual_masking"],
  "outcome_type": "positive_result",
  "sample_size": 24,
  "theory_links": [
    {
      "theory_id": "gnwt",
      "roles": ["tests_prediction"],
      "stance_stated_by_authors": "supports",
      "quote": "consistent with the late ignition predicted by global workspace theory",
      "link_origin": "ai_suggested"
    }
  ],
  "claims": [
    {
      "claim_kind": "result",
      "text": "A late, widespread EEG response distinguished seen from unseen trials.",
      "quote": "a late (300-500 ms) widespread positivity distinguished seen from unseen trials",
      "origin": "author_stated"
    }
  ]
}
```

## Automatic checks on every coded record

1. The JSON matches the schema exactly (enforced by the API's structured outputs, then checked again locally).
2. **Every `quote` appears word for word in the abstract** (after normalizing spaces and quote marks). One failed quote puts the whole record in quarantine.
3. Every `theory_id` and phenomenon id exists in the registry, or is marked `unregistered:`.
4. `tests_prediction` without a `prediction_evaluated` or `result` claim is flagged.
5. Excluded papers (incidental, unrelated) must not have theory links with roles beyond `mentions_background`.

Records that fail go to quarantine with the reason. They are never edited into shape by hand or by script.
