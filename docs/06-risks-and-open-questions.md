# 06. Risks and open questions

Version 0.1 · November 2026

## Main risks

| Risk | Why it matters | Mitigation |
|---|---|---|
| **Abstract copyright in a public repo** | Many publisher abstracts are copyrighted. Committing tens of thousands of them publicly may break terms, especially PubMed and publisher sources | Proposed abstract policy below |
| **Keyword flood** | "Awareness", "attention", "consciousness" have many non-experiential meanings | Broad search, then rubric-based AI screening, with excluded papers audited |
| **Philosophy under-covered** | PhilPapers restricts redistribution; many philosophy works lack abstracts in open databases | State coverage gaps openly; ask PhilPapers about permitted use; record `no_abstract` papers rather than dropping them |
| **Mentions mistaken for evidence** | The biggest scientific integrity risk in any field map | Separate theory roles; "tests_prediction" needs a described test; no support/refute judgments without a separate, documented evaluation step |
| **Report treated as experience** | Many studies measure report, not experience | `consciousness_measure` field records how consciousness was operationalized |
| **Owner review bottleneck** | Only a few hours a week | Sampling, disagreement-first review queue, honest error ranges |
| **AI model changes** | Model versions are retired and behavior shifts | Model name and prompt version stored on every record; re-test on the pilot gold set before switching |
| **Budget overrun from a bug** | A loop could submit the same batch twice | Idempotent runs, per-run cap, Console spend limit |
| **Leaked API key in a public repo** | Anyone could spend the budget | Keys only in GitHub Secrets and a local `.env` that git ignores; enable GitHub secret scanning |
| **Scope creep** | The outline has nine phases | Ship small: pilot, then one atlas slice (for example, global workspace theory and visual masking) before broadening |

## Proposed abstract policy (needs owner decision)

**Recommended:** publish everything except full publisher abstracts.

- Publish in the repo: all metadata (OpenAlex is CC0), all AI codings, all human review decisions, and the short supporting quotes the coding relies on (a sentence or less each, with attribution and a link to the source).
- Publish full abstracts only where the license allows it (for example CC BY open-access papers, or arXiv papers with a permissive license).
- For all other papers, store the abstract's source and a fingerprint (hash), so anyone can fetch the same abstract from OpenAlex or PubMed and confirm that our quotes match.

This keeps every step auditable without republishing copyrighted text in bulk.

Alternatives: commit every abstract (most transparent, legally risky), or commit no abstract text at all, even quotes (safest, but harder to audit).

## Open questions for the owner

1. Approve or change the abstract policy above.
2. Review the rubric in doc 01 (checklist at the end).
3. Would your RAND contact label 20 pilot papers? It would give a human-agreement baseline.
4. Is there a theory or phenomenon you want as the first atlas slice?
5. When you set up the Claude Console account, set a $20 monthly limit, and keep the key private. Claude will tell you when it is needed; nothing in this plan needs it yet.
