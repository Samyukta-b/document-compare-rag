# Retrieval eval log

**Note:** This eval currently is not for checking if the final answer is correct or not, but to check if it retrieved information from the correct location in the pdf.

Append-only history of retrieval evals. Each run is written by `python evals/eval_retrieval.py --log "note"`.

- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks returned (1 = best match, k = last). k is shown in each run's config.
- **Recall@k**: share of evidence pages found in the top k retrieved chunks.
- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).
- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step (chunks per PDF, number of PDFs).
- **Fully answerable**: questions where ALL needed evidence reaches the LLM.

## Run 1 - 2026-10-25 17:00

- **What changed:** Embedding model changed from sentence-transformers/all-MiniLM-L12-v2 to BAAI/bge-small-en-v1.5 (384 dims, normalized, no query instruction); index rebuilt with 'python database.py --reset'. Everything else is the same as dataset_2 Run 2 (the MiniLM per-PDF baseline, 20/50 fully answerable): per-PDF search, k=25 each, 5 chunks per PDF go to the LLM, chunk size 800 / overlap 80, 1,958 chunks (654 Tesla, 1,304 Uber), Chroma default L2 distance, dataset_2 (50 questions, 75 evidence items).
- **Git commit:** b57ca78 (+ uncommitted changes)
- **Dataset:** 50 questions (25 comparison, 25 single), 75 evidence items
- **Evidence found within the top 25 (k):** 52/75 (69%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding BAAI/bge-small-en-v1.5; Chroma default distance (L2); search = separate per PDF, k=25 each; context = 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@25 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 50 | 0.44 | 0.51 | 0.60 | 0.69 | 0.41 | 0.51 | 22/50 | 44% |
| comparison | 25 | 0.34 | 0.38 | 0.50 | 0.58 | 0.28 | 0.38 | 3/25 | 12% |
| single | 25 | 0.64 | 0.76 | 0.80 | 0.92 | 0.65 | 0.76 | 19/25 | 76% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 25) | Reaches LLM |
|---|---|---|---|
| `tsla-total-assets` | single | TSLA 1/25 | 1/1 |
| `tsla-stockholders-equity` | single | TSLA 3/25 | 1/1 |
| `tsla-eps-diluted` | single | TSLA 1/25 | 1/1 |
| `tsla-sga` | single | TSLA 5/25 | 1/1 |
| `tsla-automotive-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-energy-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-services-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-operating-income` | single | TSLA 1/25 | 1/1 |
| `tsla-financing-cashflow` | single | TSLA 1/25 | 1/1 |
| `tsla-deferred-revenue` | single | TSLA 4/25 | 1/1 |
| `tsla-warranty` | single | TSLA 23/25 | 0/1 |
| `tsla-us-revenue` | single | TSLA not in top 25 | 0/1 |
| `tsla-china-revenue` | single | TSLA not in top 25 | 0/1 |
| `tsla-dividends` | single | TSLA 4/25 | 1/1 |
| `tsla-energy-gross-margin` | single | TSLA 1/25 | 1/1 |
| `tsla-total-cash-investments` | single | TSLA 9/25 | 0/1 |
| `uber-gross-bookings-mobility` | single | UBER 1/25 | 1/1 |
| `uber-gross-bookings-delivery` | single | UBER 1/25 | 1/1 |
| `uber-trips` | single | UBER 1/25 | 1/1 |
| `uber-mapc` | single | UBER 1/25 | 1/1 |
| `uber-adjusted-ebitda` | single | UBER 1/25 | 1/1 |
| `uber-freight-revenue` | single | UBER 24/25 | 0/1 |
| `uber-total-assets` | single | UBER 1/25 | 1/1 |
| `uber-long-term-debt` | single | UBER 17/25 | 0/1 |
| `uber-goodwill` | single | UBER 1/25 | 1/1 |
| `cmp2-total-assets` | comparison | TSLA 1/25, UBER 2/25 | 2/2 |
| `cmp2-operating-income` | comparison | TSLA 2/25, UBER 7/25 | 1/2 |
| `cmp2-eps` | comparison | TSLA 2/25, UBER 7/25 | 1/2 |
| `cmp2-sga` | comparison | TSLA 24/25, UBER not in top 25 | 0/2 |
| `cmp2-dividends` | comparison | TSLA 8/25, UBER not in top 25 | 0/2 |
| `cmp2-financing-cashflow` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-geographic-revenue` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-debt` | comparison | TSLA not in top 25, UBER 22/25 | 0/2 |
| `cmp2-trips-vs-deliveries` | comparison | UBER 5/25, TSLA not in top 25 | 1/2 |
| `cmp2-adjusted-vs-gaap` | comparison | TSLA 2/25, UBER 24/25 | 1/2 |
| `cmp2-autonomous-investment` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-gross-margin` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp2-countries` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-goodwill` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp2-delivery-segment-ebitda` | comparison | UBER 15/25, UBER 15/25 | 0/2 |
| `cmp2-cash-page33-vs-page49` | comparison | TSLA not in top 25, TSLA 2/25 | 1/2 |
| `cmp2-revenue-growth` | comparison | TSLA 1/25, UBER 3/25 | 2/2 |
| `cmp2-insurance` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp2-energy-vs-freight` | comparison | TSLA 8/25, UBER not in top 25 | 0/2 |
| `cmp2-deferred-revenue-vs-bookings` | comparison | TSLA 22/25, UBER not in top 25 | 0/2 |
| `cmp2-trips-page50-vs-page5` | comparison | UBER not in top 25, UBER 4/25 | 1/2 |
| `cmp2-employees-page13-vs-page12` | comparison | TSLA 1/25, TSLA not in top 25 | 1/2 |
| `cmp2-capex-intensity` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp2-stock-based-comp-page` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp2-mobility-revenue-vs-automotive` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |

---

