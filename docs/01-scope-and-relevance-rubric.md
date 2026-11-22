# 01. Research scope and relevance rubric

Version 0.1 · November 2026 · Status: draft, needs owner review

This is the most important document in the project. The keyword search will pull in thousands of papers that use words like "awareness", "attention", "arousal" or "conscious" in an unrelated sense. This rubric is how we (and the AI) decide what actually belongs in the map.

## 1. What CRIP covers

Consciousness research is work whose **object of study** is consciousness itself: subjective experience, the difference between conscious and unconscious processing, states and levels of consciousness, or explanations of any of these.

### Research domains (version 0.1)

| Code | Domain | In scope when the work... | Typical examples |
|---|---|---|---|
| D1 | Phenomenal consciousness | addresses subjective experience, "what it is like" | hard problem, qualia, phenomenal concepts |
| D2 | Access consciousness | addresses which information becomes available for report, reasoning and control, *as a question about consciousness* | access vs phenomenal debate, overflow, report paradigms |
| D3 | Neural correlates (NCC) | measures brain activity that tracks conscious vs unconscious conditions | contrastive EEG or fMRI, "no-report" paradigms, P3b and ignition debates |
| D4 | States and levels | studies wakefulness, sleep, anesthesia, coma, vegetative or minimally conscious states, seizures, as changes in consciousness | perturbational complexity, covert awareness, anesthetic loss of responsiveness |
| D5 | Contents of consciousness | studies what is consciously perceived or experienced, with conscious vs unconscious contrast | masking, binocular rivalry, inattentional blindness, blindsight, imagery, dreams |
| D6 | Self-consciousness and metacognition | studies self-experience, body ownership, introspection, confidence about one's own experience | rubber hand illusion, metacognitive sensitivity tied to awareness, depersonalization |
| D7 | Theories of consciousness | proposes, develops, tests or criticizes an explanation of consciousness | workspace, integrated information, higher-order, recurrent processing, predictive processing, attention schema |
| D8 | Artificial consciousness | asks whether or how artificial systems could be conscious, or how we would know | indicator-property approaches, machine consciousness models |
| D9 | Altered states | studies psychedelics, meditation, hypnosis and similar *as changes in experience* | ego dissolution, altered perception |
| D10 | Animal consciousness | asks which non-human animals are conscious, or how to tell | markers in fish, insects, cephalopods |

D9 and D10 are additions to the original outline. Both are active areas a field map should show.

### Kinds of work (always recorded, never mixed up)

| Code | Kind | Meaning |
|---|---|---|
| W1 | Empirical study | collects new data |
| W2 | Theoretical or computational model | proposes a formal or mechanistic account, may simulate it |
| W3 | Philosophical argument | conceptual or argumentative work |
| W4 | Review or meta-analysis | summarizes existing work |
| W5 | Methods or measurement | proposes or evaluates a way to measure consciousness |
| W6 | Commentary or opinion | short responses, editorials, target-article replies |

Philosophical work is in scope, but it is **not judged by empirical criteria**, and the map keeps it visibly separate from empirical findings.

## 2. What CRIP does not cover

These are the main false-positive traps. A paper in one of these categories is excluded **unless** it explicitly treats consciousness as its object of study.

| Trap | Why it appears | Usually excluded |
|---|---|---|
| Attention | attention and consciousness overlap but are not the same | spatial cueing studies with no awareness measure |
| "Awareness" as knowledge | everyday sense of being informed | "awareness of diabetes risk", "brand awareness", "situational awareness" in pilots |
| "Consciousness" as attitude | social science usage | "environmental consciousness", "class consciousness", "health consciousness" |
| Arousal | emotion and physiology research | arousal ratings of images |
| AI and "attention" | transformer attention mechanisms | ML papers about attention layers |
| Intelligence and cognition | general cognitive science | working memory capacity, IQ |
| Clinical procedures | "loss of consciousness" as a side note | trauma triage scores, sedation dosing for procedures, unless consciousness itself is measured or theorized |
| Implicit learning, priming | unconscious processing, but often without an awareness test | priming studies with no awareness check |

**Edge rule:** studies of unconscious processing ARE in scope when they explicitly test or measure awareness to establish that processing was unconscious (for example, subliminal priming with a visibility test). That contrast is central to the science.

## 3. Relevance levels

Every paper gets exactly one level. The AI must give a one-sentence reason and, where possible, quote the words that justify it.

| Level | Definition | Test question |
|---|---|---|
| **core** | Consciousness is the main object of study. | Would a consciousness researcher put this in a reading list on the topic? |
| **substantial** | Consciousness is a major secondary aim, or an explicit measure or contrast in the design. | Is there an awareness measure, a conscious vs unconscious contrast, or a section-level argument about consciousness? |
| **incidental** | Consciousness or a related word appears, but is not studied. | Could you delete the consciousness mention without changing the paper's findings? |
| **unrelated** | A different sense of the word, or no real connection. | Is "awareness/consciousness/attention" used in a non-experiential sense? |
| **unclear** | The title and abstract do not give enough information. | Would you need the full text to decide? |
| *(status)* **no_abstract** | Not a relevance level. The paper lacks a usable abstract and has not been judged. | |

**Inclusion in the main map:** core and substantial. Incidental, unrelated and unclear records are kept in the database with their reasons, and are audited (see [Validation plan](04-validation-plan.md)).

### Decision steps (the order the AI and the human both follow)

1. Is there a usable abstract? If not, set status `no_abstract` and stop.
2. Is the key word used in the experiential sense (subjective experience, conscious vs unconscious, states of consciousness)? If clearly not, mark **unrelated**.
3. Is consciousness the main object of study? If yes, **core**.
4. Is there an explicit awareness measure, consciousness contrast, consciousness theory being proposed or tested, or a developed argument about consciousness? If yes, **substantial**.
5. Is consciousness only mentioned as background, motivation or speculation? **incidental**.
6. Still not sure? **unclear**. Never guess upward.

### Worked examples (invented for illustration)

| Abstract gist | Level | Why |
|---|---|---|
| Participants saw masked faces; visibility ratings separated seen from unseen trials; EEG differed after 300 ms. | core | Conscious vs unconscious contrast is the design. |
| Rubber hand illusion strength predicted by interoceptive accuracy. | core | Body ownership, a self-consciousness phenomenon (D6). |
| Propofol dose-response study of hemodynamic stability, loss of consciousness as an endpoint. | incidental | Consciousness is a timing marker, not studied. |
| Propofol-induced unconsciousness reduced cortical complexity measured by TMS-EEG. | core | Measures a level of consciousness (D4). |
| Visual search reaction times with spatial cues. | unrelated | Attention only, no awareness measure. |
| Situational awareness of nurses in emergency wards. | unrelated | Non-experiential sense. |
| A transformer with a global broadcast module improves reasoning; authors note links to workspace theory in the discussion. | incidental | Theory mentioned, consciousness not studied. |
| Argument that large language models lack the indicator properties for consciousness. | core | D8, philosophical (W3). |
| Subliminal word priming, no visibility test reported. | unclear | Cannot tell if awareness was controlled. |

## 4. Versioning and change rules

- This file is versioned. Every coding run records which rubric version it used.
- Changes are logged in `docs/decision-log.md` with the reason and the examples that prompted them.
- After the pilot, expect version 0.2. The owner signs off on each version before it is used at scale.

## Owner review checklist

- [ ] Are the ten domains the right top-level split? Anything missing (for example, development and infancy, psychiatric disorders)?
- [ ] Should D9 (altered states) and D10 (animal consciousness) stay?
- [ ] Is "substantial" too generous or too strict?
- [ ] Do the worked examples match your own judgement?
