# How to label the pilot (owner task, about 2.5 hours)

1. Open the latest successful run of **Pilot harvest** under the repo's Actions tab and download the artifact `private-labeling-sheet` (kept for 7 days; re-run the workflow to make a fresh one).
2. Open `labeling_sheet.csv` in Excel or Google Sheets. It has 100 papers in random order. It deliberately does not say which papers were chosen as anchors or traps.
3. For each row, read the title and abstract and fill `your_label` with one of:
   `core`, `substantial`, `incidental`, `unrelated`, `unclear`, `no_abstract`
   using the decision steps in `docs/01-scope-and-relevance-rubric.md`. Use `your_note` for anything that made you hesitate. Those notes are what improve the rubric.
4. Don't look anything up and don't overthink. About 1.5 minutes per paper is the target. Your first judgment is the useful one.
5. When done, keep only three columns (`openalex_id`, `your_label`, `your_note`) and save it as `data/reviews/pilot_owner_labels_v0.1.csv`. **Delete the abstract column before committing**, so no copyrighted abstracts go into the public repo. Or just send the file to Claude, which will strip it and commit it.

Your labels are the gold standard the AI is measured against, so label before seeing any AI output.
