# Retrieval eval log

**Note:** This eval currently is not for checking if the final answer is correct or not, but to check if it retrieved information from the correct location in the pdf.

Append-only history of retrieval evals. Each run is written by `python evals/eval_retrieval.py --log "note"`.

- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks returned (1 = best match, k = last). k is shown in each run's config.
- **Recall@k**: share of evidence pages found in the top k retrieved chunks.
- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).
- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step in `retrieval.py`.
- **Fully answerable**: questions where ALL needed evidence reaches the LLM.

## Run 1 - 2026-10-25 16:02

- **What changed:** Baseline for dataset_2. Chunk size 800 / overlap 80 (reverted from 500/50, re-indexed with database.py --reset: 1958 chunks), k=50, 5 chunks per PDF.
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

