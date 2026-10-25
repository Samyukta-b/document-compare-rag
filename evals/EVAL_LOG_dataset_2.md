# Retrieval eval log

**Note:** This eval currently is not for checking if the final answer is correct or not, but to check if it retrieved information from the correct location in the pdf.

Append-only history of retrieval evals. Each run is written by `python evals/eval_retrieval.py --log "note"`.

- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks returned (1 = best match, k = last). k is shown in each run's config.
- **Recall@k**: share of evidence pages found in the top k retrieved chunks.
- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).
- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step in `retrieval.py`.
- **Fully answerable**: questions where ALL needed evidence reaches the LLM.

## Run 1 - 2026-10-25 16:02

- **What changed:** Baseline for dataset_2. Retrieval: one similarity_search over both PDFs mixed, k=50, then group by source (5 chunks per doc, first 2 docs). Chunk size 800 / overlap 80 (reverted from 500/50 and re-indexed with database.py --reset: 1958 chunks = 654 Tesla + 1304 Uber), all-MiniLM-L12-v2, Chroma default L2. Dataset has 50 questions (25 single, 25 comparison). At the time these settings lived in retrieval.py (since removed); query.py itself had k=15 and 3 per doc.
- **Git commit:** dd28e4b (+ uncommitted changes)
- **Dataset:** 50 questions (25 comparison, 25 single), 75 evidence items
- **Evidence found within the top 50 (k):** 53/75 (71%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search k=50; context = first 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@50 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 50 | 0.36 | 0.39 | 0.56 | 0.71 | 0.31 | 0.49 | 20/50 | 40% |
| comparison | 25 | 0.24 | 0.24 | 0.42 | 0.60 | 0.18 | 0.40 | 3/25 | 12% |
| single | 25 | 0.60 | 0.68 | 0.84 | 0.92 | 0.55 | 0.68 | 17/25 | 68% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 50) | Reaches LLM |
|---|---|---|---|
| `tsla-total-assets` | single | TSLA 1/50 | 1/1 |
| `tsla-stockholders-equity` | single | TSLA 2/50 | 1/1 |
| `tsla-eps-diluted` | single | TSLA 2/50 | 1/1 |
| `tsla-sga` | single | TSLA 15/50 | 0/1 |
| `tsla-automotive-revenue` | single | TSLA 1/50 | 1/1 |
| `tsla-energy-revenue` | single | TSLA 1/50 | 1/1 |
| `tsla-services-revenue` | single | TSLA 1/50 | 1/1 |
| `tsla-operating-income` | single | TSLA 2/50 | 1/1 |
| `tsla-financing-cashflow` | single | TSLA 1/50 | 1/1 |
| `tsla-deferred-revenue` | single | TSLA 4/50 | 1/1 |
| `tsla-warranty` | single | TSLA 39/50 | 0/1 |
| `tsla-us-revenue` | single | TSLA not in top 50 | 0/1 |
| `tsla-china-revenue` | single | TSLA not in top 50 | 0/1 |
| `tsla-dividends` | single | TSLA 10/50 | 0/1 |
| `tsla-energy-gross-margin` | single | TSLA 6/50 | 0/1 |
| `tsla-total-cash-investments` | single | TSLA 18/50 | 0/1 |
| `uber-gross-bookings-mobility` | single | UBER 1/50 | 1/1 |
| `uber-gross-bookings-delivery` | single | UBER 1/50 | 1/1 |
| `uber-trips` | single | UBER 1/50 | 1/1 |
| `uber-mapc` | single | UBER 1/50 | 1/1 |
| `uber-adjusted-ebitda` | single | UBER 3/50 | 1/1 |
| `uber-freight-revenue` | single | UBER 10/50 | 0/1 |
| `uber-total-assets` | single | UBER 1/50 | 1/1 |
| `uber-long-term-debt` | single | UBER 4/50 | 1/1 |
| `uber-goodwill` | single | UBER 1/50 | 1/1 |
| `cmp2-total-assets` | comparison | TSLA 2/50, UBER 1/50 | 2/2 |
| `cmp2-operating-income` | comparison | TSLA 9/50, UBER not in top 50 | 1/2 |
| `cmp2-eps` | comparison | TSLA 26/50, UBER not in top 50 | 1/2 |
| `cmp2-sga` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp2-dividends` | comparison | TSLA 36/50, UBER not in top 50 | 0/2 |
| `cmp2-financing-cashflow` | comparison | TSLA 3/50, UBER 44/50 | 1/2 |
| `cmp2-geographic-revenue` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp2-debt` | comparison | TSLA not in top 50, UBER 6/50 | 1/2 |
| `cmp2-trips-vs-deliveries` | comparison | UBER 12/50, TSLA not in top 50 | 0/2 |
| `cmp2-adjusted-vs-gaap` | comparison | TSLA 13/50, UBER not in top 50 | 1/2 |
| `cmp2-autonomous-investment` | comparison | TSLA 2/50, UBER not in top 50 | 1/2 |
| `cmp2-gross-margin` | comparison | TSLA 16/50, UBER not in top 50 | 1/2 |
| `cmp2-countries` | comparison | TSLA not in top 50, UBER 33/50 | 0/2 |
| `cmp2-goodwill` | comparison | TSLA 1/50, UBER 2/50 | 2/2 |
| `cmp2-delivery-segment-ebitda` | comparison | UBER 9/50, UBER 9/50 | 0/2 |
| `cmp2-cash-page33-vs-page49` | comparison | TSLA not in top 50, TSLA 3/50 | 1/2 |
| `cmp2-revenue-growth` | comparison | TSLA 13/50, UBER 2/50 | 2/2 |
| `cmp2-insurance` | comparison | TSLA not in top 50, UBER 26/50 | 0/2 |
| `cmp2-energy-vs-freight` | comparison | TSLA 15/50, UBER not in top 50 | 0/2 |
| `cmp2-deferred-revenue-vs-bookings` | comparison | TSLA 24/50, UBER not in top 50 | 1/2 |
| `cmp2-trips-page50-vs-page5` | comparison | UBER 10/50, UBER 3/50 | 1/2 |
| `cmp2-employees-page13-vs-page12` | comparison | TSLA 1/50, TSLA 37/50 | 1/2 |
| `cmp2-capex-intensity` | comparison | TSLA 1/50, UBER not in top 50 | 1/2 |
| `cmp2-stock-based-comp-page` | comparison | TSLA 1/50, UBER not in top 50 | 1/2 |
| `cmp2-mobility-revenue-vs-automotive` | comparison | TSLA 36/50, UBER not in top 50 | 1/2 |

---

## Run 2 - 2026-10-25 16:36

- **What changed:** Per-document retrieval (branch per-document-retrieval): each PDF searched separately with a metadata filter on source, k=25 per PDF, 5 chunks per PDF go to the LLM (was, in Run 1: one mixed search k=50, 5 per PDF). NOTE: rank is now the position within that PDF's own 25 results, not within one shared list, and 'found within k' is out of 25 per PDF. Chunking unchanged (800/80).
- **Git commit:** e774878 (+ uncommitted changes)
- **Dataset:** 50 questions (25 comparison, 25 single), 75 evidence items
- **Evidence found within the top 25 (k):** 50/75 (67%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search = separate per PDF, k=25 each; context = 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@25 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 50 | 0.41 | 0.49 | 0.64 | 0.67 | 0.39 | 0.49 | 20/50 | 40% |
| comparison | 25 | 0.32 | 0.40 | 0.52 | 0.56 | 0.31 | 0.40 | 3/25 | 12% |
| single | 25 | 0.60 | 0.68 | 0.88 | 0.88 | 0.55 | 0.68 | 17/25 | 68% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 25) | Reaches LLM |
|---|---|---|---|
| `tsla-total-assets` | single | TSLA 1/25 | 1/1 |
| `tsla-stockholders-equity` | single | TSLA 2/25 | 1/1 |
| `tsla-eps-diluted` | single | TSLA 2/25 | 1/1 |
| `tsla-sga` | single | TSLA 14/25 | 0/1 |
| `tsla-automotive-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-energy-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-services-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-operating-income` | single | TSLA 2/25 | 1/1 |
| `tsla-financing-cashflow` | single | TSLA 1/25 | 1/1 |
| `tsla-deferred-revenue` | single | TSLA 4/25 | 1/1 |
| `tsla-warranty` | single | TSLA not in top 25 | 0/1 |
| `tsla-us-revenue` | single | TSLA not in top 25 | 0/1 |
| `tsla-china-revenue` | single | TSLA not in top 25 | 0/1 |
| `tsla-dividends` | single | TSLA 9/25 | 0/1 |
| `tsla-energy-gross-margin` | single | TSLA 6/25 | 0/1 |
| `tsla-total-cash-investments` | single | TSLA 15/25 | 0/1 |
| `uber-gross-bookings-mobility` | single | UBER 1/25 | 1/1 |
| `uber-gross-bookings-delivery` | single | UBER 1/25 | 1/1 |
| `uber-trips` | single | UBER 1/25 | 1/1 |
| `uber-mapc` | single | UBER 1/25 | 1/1 |
| `uber-adjusted-ebitda` | single | UBER 3/25 | 1/1 |
| `uber-freight-revenue` | single | UBER 10/25 | 0/1 |
| `uber-total-assets` | single | UBER 1/25 | 1/1 |
| `uber-long-term-debt` | single | UBER 4/25 | 1/1 |
| `uber-goodwill` | single | UBER 1/25 | 1/1 |
| `cmp2-total-assets` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp2-operating-income` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp2-eps` | comparison | TSLA 5/25, UBER not in top 25 | 1/2 |
| `cmp2-sga` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-dividends` | comparison | TSLA 13/25, UBER not in top 25 | 0/2 |
| `cmp2-financing-cashflow` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-geographic-revenue` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-debt` | comparison | TSLA not in top 25, UBER 5/25 | 1/2 |
| `cmp2-trips-vs-deliveries` | comparison | UBER 12/25, TSLA not in top 25 | 0/2 |
| `cmp2-adjusted-vs-gaap` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-autonomous-investment` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-gross-margin` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-countries` | comparison | TSLA not in top 25, UBER 19/25 | 0/2 |
| `cmp2-goodwill` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp2-delivery-segment-ebitda` | comparison | UBER 9/25, UBER 9/25 | 0/2 |
| `cmp2-cash-page33-vs-page49` | comparison | TSLA not in top 25, TSLA 2/25 | 1/2 |
| `cmp2-revenue-growth` | comparison | TSLA 1/25, UBER 2/25 | 2/2 |
| `cmp2-insurance` | comparison | TSLA not in top 25, UBER 17/25 | 0/2 |
| `cmp2-energy-vs-freight` | comparison | TSLA 12/25, UBER not in top 25 | 0/2 |
| `cmp2-deferred-revenue-vs-bookings` | comparison | TSLA 5/25, UBER not in top 25 | 1/2 |
| `cmp2-trips-page50-vs-page5` | comparison | UBER 10/25, UBER 3/25 | 1/2 |
| `cmp2-employees-page13-vs-page12` | comparison | TSLA 1/25, TSLA not in top 25 | 1/2 |
| `cmp2-capex-intensity` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-stock-based-comp-page` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-mobility-revenue-vs-automotive` | comparison | TSLA 4/25, UBER not in top 25 | 1/2 |

---

## Run 3 - 2026-10-25 16:46

- **What changed:** Embedding code from the main branch instead of this branch (comparison run). Same chunking 800/80 (1958 chunks, separate index built in /tmp/chroma_main), same retrieval as Run 2: each PDF searched separately, k=25 per PDF, 5 chunks per PDF to the LLM. Only change vs Run 2: embedding. Main-branch way = transformers AutoModel, CLS-token pooling (first token only, not mean pooling), no normalization, no 128-token truncation. Same model name all-MiniLM-L12-v2, Chroma default L2.
- **Git commit:** e774878 (+ uncommitted changes)
- **Dataset:** 50 questions (25 comparison, 25 single), 75 evidence items
- **Evidence found within the top 25 (k):** 51/75 (68%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding all-MiniLM-L12-v2 run the main-branch way (transformers AutoModel, CLS-token pooling, no normalization, no 128-token truncation); Chroma default distance (L2); search = separate per PDF, k=25 each; context = 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@25 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 50 | 0.31 | 0.37 | 0.57 | 0.68 | 0.22 | 0.37 | 14/50 | 28% |
| comparison | 25 | 0.28 | 0.34 | 0.50 | 0.62 | 0.21 | 0.34 | 3/25 | 12% |
| single | 25 | 0.36 | 0.44 | 0.72 | 0.80 | 0.26 | 0.44 | 11/25 | 44% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 25) | Reaches LLM |
|---|---|---|---|
| `tsla-total-assets` | single | TSLA 3/25 | 1/1 |
| `tsla-stockholders-equity` | single | TSLA 14/25 | 0/1 |
| `tsla-eps-diluted` | single | TSLA 16/25 | 0/1 |
| `tsla-sga` | single | TSLA not in top 25 | 0/1 |
| `tsla-automotive-revenue` | single | TSLA 2/25 | 1/1 |
| `tsla-energy-revenue` | single | TSLA 4/25 | 1/1 |
| `tsla-services-revenue` | single | TSLA 9/25 | 0/1 |
| `tsla-operating-income` | single | TSLA 11/25 | 0/1 |
| `tsla-financing-cashflow` | single | TSLA 1/25 | 1/1 |
| `tsla-deferred-revenue` | single | TSLA 5/25 | 1/1 |
| `tsla-warranty` | single | TSLA not in top 25 | 0/1 |
| `tsla-us-revenue` | single | TSLA 6/25 | 0/1 |
| `tsla-china-revenue` | single | TSLA 10/25 | 0/1 |
| `tsla-dividends` | single | TSLA 24/25 | 0/1 |
| `tsla-energy-gross-margin` | single | TSLA not in top 25 | 0/1 |
| `tsla-total-cash-investments` | single | TSLA not in top 25 | 0/1 |
| `uber-gross-bookings-mobility` | single | UBER 2/25 | 1/1 |
| `uber-gross-bookings-delivery` | single | UBER 2/25 | 1/1 |
| `uber-trips` | single | UBER 2/25 | 1/1 |
| `uber-mapc` | single | UBER 3/25 | 1/1 |
| `uber-adjusted-ebitda` | single | UBER 6/25 | 0/1 |
| `uber-freight-revenue` | single | UBER not in top 25 | 0/1 |
| `uber-total-assets` | single | UBER 3/25 | 1/1 |
| `uber-long-term-debt` | single | UBER 7/25 | 0/1 |
| `uber-goodwill` | single | UBER 1/25 | 1/1 |
| `cmp2-total-assets` | comparison | TSLA 2/25, UBER 3/25 | 2/2 |
| `cmp2-operating-income` | comparison | TSLA 2/25, UBER 2/25 | 2/2 |
| `cmp2-eps` | comparison | TSLA 7/25, UBER 4/25 | 1/2 |
| `cmp2-sga` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-dividends` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-financing-cashflow` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-geographic-revenue` | comparison | TSLA 22/25, UBER not in top 25 | 0/2 |
| `cmp2-debt` | comparison | TSLA not in top 25, UBER 10/25 | 0/2 |
| `cmp2-trips-vs-deliveries` | comparison | UBER 17/25, TSLA not in top 25 | 0/2 |
| `cmp2-adjusted-vs-gaap` | comparison | TSLA 3/25, UBER 20/25 | 1/2 |
| `cmp2-autonomous-investment` | comparison | TSLA 5/25, UBER not in top 25 | 1/2 |
| `cmp2-gross-margin` | comparison | TSLA 13/25, UBER 13/25 | 0/2 |
| `cmp2-countries` | comparison | TSLA 25/25, UBER 16/25 | 0/2 |
| `cmp2-goodwill` | comparison | TSLA 1/25, UBER 2/25 | 2/2 |
| `cmp2-delivery-segment-ebitda` | comparison | UBER not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-cash-page33-vs-page49` | comparison | TSLA not in top 25, TSLA 5/25 | 1/2 |
| `cmp2-revenue-growth` | comparison | TSLA 2/25, UBER 9/25 | 1/2 |
| `cmp2-insurance` | comparison | TSLA not in top 25, UBER 13/25 | 0/2 |
| `cmp2-energy-vs-freight` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-deferred-revenue-vs-bookings` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp2-trips-page50-vs-page5` | comparison | UBER 11/25, UBER 2/25 | 1/2 |
| `cmp2-employees-page13-vs-page12` | comparison | TSLA 1/25, TSLA 20/25 | 1/2 |
| `cmp2-capex-intensity` | comparison | TSLA 6/25, UBER not in top 25 | 0/2 |
| `cmp2-stock-based-comp-page` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp2-mobility-revenue-vs-automotive` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |

---

