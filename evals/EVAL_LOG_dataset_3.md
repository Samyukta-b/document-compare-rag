# Retrieval eval log

**Note:** This eval currently is not for checking if the final answer is correct or not, but to check if it retrieved information from the correct location in the pdf.

Append-only history of retrieval evals. Each run is written by `python evals/eval_retrieval.py --log "note"`.

- **Evidence page**: the page in `evidence`, plus any `alt_pages` (other pages containing the same phrase) when the dataset lists them.
- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks returned (1 = best match, k = last). k is shown in each run's config.
- **Recall@k**: share of evidence pages found in the top k retrieved chunks.
- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).
- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step (chunks per PDF, number of PDFs).
- **Fully answerable**: questions where ALL needed evidence reaches the LLM.

## Run 1 - 2026-10-25 17:20

- **What changed:** First run on dataset_3 (63 questions, 96 evidence items; a cleaned merge of dataset_1 and dataset_2, every evidence phrase verified on its page, some evidence items list alt_pages that also contain the phrase). Setup: embedding BAAI/bge-small-en-v1.5 (384 dims, normalized, no query instruction), per-PDF search k=25 each, 5 chunks per PDF go to the LLM, chunk size 800 / overlap 80, 1,958 chunks (654 Tesla, 1,304 Uber), Chroma default L2 distance.
- **Git commit:** b57ca78 (+ uncommitted changes)
- **Dataset:** 63 questions (30 comparison, 3 multi_page, 30 single), 96 evidence items
- **Evidence found within the top 25 (k):** 81/96 (84%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding BAAI/bge-small-en-v1.5; Chroma default distance (L2); search = separate per PDF, k=25 each; context = 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@25 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 63 | 0.52 | 0.65 | 0.79 | 0.84 | 0.47 | 0.65 | 35/63 | 56% |
| comparison | 30 | 0.43 | 0.55 | 0.72 | 0.80 | 0.40 | 0.55 | 9/30 | 30% |
| multi_page | 3 | 0.50 | 0.67 | 0.83 | 0.83 | 0.48 | 0.67 | 1/3 | 33% |
| single | 30 | 0.70 | 0.83 | 0.93 | 0.93 | 0.60 | 0.83 | 25/30 | 83% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 25) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-deliveries` | single | TSLA 2/25 | 1/1 |
| `tsla-net-income` | single | TSLA 5/25 | 1/1 |
| `tsla-rnd` | single | TSLA 1/25 | 1/1 |
| `tsla-total-assets` | single | TSLA 1/25 | 1/1 |
| `tsla-eps-diluted` | single | TSLA 1/25 | 1/1 |
| `tsla-us-revenue` | single | TSLA 4/25 | 1/1 |
| `tsla-warranty` | single | TSLA 2/25 | 1/1 |
| `tsla-total-cash-investments` | single | TSLA 6/25 | 0/1 |
| `tsla-energy-gross-margin` | single | TSLA 1/25 | 1/1 |
| `tsla-mission` | single | TSLA 1/25 | 1/1 |
| `tsla-key-person-risk` | single | TSLA 2/25 | 1/1 |
| `tsla-revenue-recognition` | single | TSLA 2/25 | 1/1 |
| `tsla-self-driving` | single | TSLA 1/25 | 1/1 |
| `tsla-manufacturing-sites` | single | TSLA 2/25 | 1/1 |
| `uber-revenue` | single | UBER 2/25 | 1/1 |
| `uber-employees` | single | UBER 1/25 | 1/1 |
| `uber-net-loss` | single | UBER 6/25 | 0/1 |
| `uber-rnd` | single | UBER not in top 25 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/25 | 1/1 |
| `uber-trips` | single | UBER 1/25 | 1/1 |
| `uber-mobility-revenue` | single | UBER 6/25 | 0/1 |
| `uber-total-assets` | single | UBER 1/25 | 1/1 |
| `uber-goodwill` | single | UBER 1/25 | 1/1 |
| `uber-us-revenue` | single | UBER not in top 25 | 0/1 |
| `uber-segments` | single | UBER 4/25 | 1/1 |
| `uber-revenue-recognition` | single | UBER 2/25 | 1/1 |
| `uber-proposition-22` | single | UBER 4/25 | 1/1 |
| `uber-one` | single | UBER 2/25 | 1/1 |
| `uber-aurora-gain` | single | UBER 2/25 | 1/1 |
| `cmp-revenue` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp-rnd` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-cash` | comparison | TSLA 2/25, UBER 2/25 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 25, UBER 1/25 | 1/2 |
| `cmp-headcount` | comparison | TSLA 2/25, UBER 5/25 | 2/2 |
| `cmp-total-assets` | comparison | TSLA 1/25, UBER 2/25 | 2/2 |
| `cmp-operating-result` | comparison | TSLA 2/25, UBER 7/25 | 1/2 |
| `cmp-eps` | comparison | TSLA 2/25, UBER 1/25 | 2/2 |
| `cmp-operating-cashflow` | comparison | TSLA 7/25, UBER not in top 25 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 4/25, UBER 13/25 | 1/2 |
| `cmp-financing-cashflow` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-capex` | comparison | TSLA 3/25, UBER 13/25 | 1/2 |
| `cmp-long-term-debt` | comparison | TSLA 3/25, UBER 22/25 | 1/2 |
| `cmp-geographic-revenue` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp-sga` | comparison | TSLA 3/25, UBER 13/25 | 1/2 |
| `cmp-trips-vs-deliveries` | comparison | UBER 5/25, TSLA not in top 25 | 1/2 |
| `cmp-goodwill` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp-energy-vs-freight` | comparison | TSLA 1/25, UBER 6/25 | 1/2 |
| `cmp-mobility-vs-automotive` | comparison | TSLA 1/25, UBER 7/25 | 1/2 |
| `cmp-warranty-vs-insurance` | comparison | TSLA 1/25, UBER 9/25 | 1/2 |
| `cmp-segments` | comparison | TSLA 1/25, UBER 4/25 | 2/2 |
| `cmp-headquarters` | comparison | TSLA 25/25, UBER 4/25 | 1/2 |
| `cmp-exchange` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp-incorporation` | comparison | TSLA not in top 25, UBER 24/25 | 0/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 25, UBER 14/25 | 0/2 |
| `cmp-dividends` | comparison | TSLA 8/25, UBER 19/25 | 0/2 |
| `cmp-self-driving` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-revenue-recognition` | comparison | TSLA 4/25, UBER 5/25 | 2/2 |
| `cmp-footprint` | comparison | TSLA 24/25, UBER not in top 25 | 0/2 |
| `tsla-cash-and-investments` | multi_page | TSLA 1/25, TSLA 8/25 | 1/2 |
| `tsla-us-and-energy-revenue` | multi_page | TSLA 4/25, TSLA 1/25 | 2/2 |
| `uber-loss-vs-ebitda` | multi_page | UBER not in top 25, UBER 2/25 | 1/2 |

---

## Run 2 - 2026-10-25 17:21

- **What changed:** Same dataset_3 and same setup as Run 1, only the embedding model changed back to sentence-transformers/all-MiniLM-L12-v2 (384 dims, normalized) and the index was rebuilt with 'python database.py --reset'. Everything else unchanged: per-PDF search k=25 each, 5 chunks per PDF go to the LLM, chunk size 800 / overlap 80, 1,958 chunks (654 Tesla, 1,304 Uber), Chroma default L2 distance.
- **Git commit:** b57ca78 (+ uncommitted changes)
- **Dataset:** 63 questions (30 comparison, 3 multi_page, 30 single), 96 evidence items
- **Evidence found within the top 25 (k):** 70/96 (73%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search = separate per PDF, k=25 each; context = 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@25 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 63 | 0.45 | 0.54 | 0.68 | 0.73 | 0.38 | 0.54 | 28/63 | 44% |
| comparison | 30 | 0.35 | 0.47 | 0.58 | 0.65 | 0.30 | 0.47 | 7/30 | 23% |
| multi_page | 3 | 0.50 | 0.50 | 0.67 | 0.83 | 0.44 | 0.50 | 0/3 | 0% |
| single | 30 | 0.63 | 0.70 | 0.87 | 0.87 | 0.52 | 0.70 | 21/30 | 70% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 25) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 1/25 | 1/1 |
| `tsla-deliveries` | single | TSLA 4/25 | 1/1 |
| `tsla-net-income` | single | TSLA 15/25 | 0/1 |
| `tsla-rnd` | single | TSLA 1/25 | 1/1 |
| `tsla-total-assets` | single | TSLA 1/25 | 1/1 |
| `tsla-eps-diluted` | single | TSLA 2/25 | 1/1 |
| `tsla-us-revenue` | single | TSLA not in top 25 | 0/1 |
| `tsla-warranty` | single | TSLA 1/25 | 1/1 |
| `tsla-total-cash-investments` | single | TSLA 11/25 | 0/1 |
| `tsla-energy-gross-margin` | single | TSLA 6/25 | 0/1 |
| `tsla-mission` | single | TSLA not in top 25 | 0/1 |
| `tsla-key-person-risk` | single | TSLA 2/25 | 1/1 |
| `tsla-revenue-recognition` | single | TSLA 3/25 | 1/1 |
| `tsla-self-driving` | single | TSLA 2/25 | 1/1 |
| `tsla-manufacturing-sites` | single | TSLA 1/25 | 1/1 |
| `uber-revenue` | single | UBER 2/25 | 1/1 |
| `uber-employees` | single | UBER 3/25 | 1/1 |
| `uber-net-loss` | single | UBER 2/25 | 1/1 |
| `uber-rnd` | single | UBER not in top 25 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/25 | 1/1 |
| `uber-trips` | single | UBER 1/25 | 1/1 |
| `uber-mobility-revenue` | single | UBER 6/25 | 0/1 |
| `uber-total-assets` | single | UBER 1/25 | 1/1 |
| `uber-goodwill` | single | UBER 1/25 | 1/1 |
| `uber-us-revenue` | single | UBER not in top 25 | 0/1 |
| `uber-segments` | single | UBER 13/25 | 0/1 |
| `uber-revenue-recognition` | single | UBER 2/25 | 1/1 |
| `uber-proposition-22` | single | UBER 1/25 | 1/1 |
| `uber-one` | single | UBER 1/25 | 1/1 |
| `uber-aurora-gain` | single | UBER 5/25 | 1/1 |
| `cmp-revenue` | comparison | TSLA 1/25, UBER 2/25 | 2/2 |
| `cmp-rnd` | comparison | TSLA 2/25, UBER not in top 25 | 1/2 |
| `cmp-cash` | comparison | TSLA 2/25, UBER 2/25 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 25, UBER 5/25 | 1/2 |
| `cmp-headcount` | comparison | TSLA 2/25, UBER 1/25 | 2/2 |
| `cmp-total-assets` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp-operating-result` | comparison | TSLA 3/25, UBER 25/25 | 1/2 |
| `cmp-eps` | comparison | TSLA 5/25, UBER 11/25 | 1/2 |
| `cmp-operating-cashflow` | comparison | TSLA 20/25, UBER not in top 25 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 3/25, UBER 10/25 | 1/2 |
| `cmp-financing-cashflow` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 3/25, UBER not in top 25 | 1/2 |
| `cmp-capex` | comparison | TSLA 3/25, UBER not in top 25 | 1/2 |
| `cmp-long-term-debt` | comparison | TSLA 1/25, UBER 5/25 | 2/2 |
| `cmp-geographic-revenue` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp-sga` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp-trips-vs-deliveries` | comparison | UBER 12/25, TSLA not in top 25 | 0/2 |
| `cmp-goodwill` | comparison | TSLA 1/25, UBER 1/25 | 2/2 |
| `cmp-energy-vs-freight` | comparison | TSLA 5/25, UBER 9/25 | 1/2 |
| `cmp-mobility-vs-automotive` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-warranty-vs-insurance` | comparison | TSLA 1/25, UBER 16/25 | 1/2 |
| `cmp-segments` | comparison | TSLA 2/25, UBER 4/25 | 2/2 |
| `cmp-headquarters` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp-exchange` | comparison | TSLA 11/25, UBER not in top 25 | 0/2 |
| `cmp-incorporation` | comparison | TSLA not in top 25, UBER not in top 25 | 0/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 25, UBER 4/25 | 1/2 |
| `cmp-dividends` | comparison | TSLA 13/25, UBER not in top 25 | 0/2 |
| `cmp-self-driving` | comparison | TSLA 1/25, UBER not in top 25 | 1/2 |
| `cmp-revenue-recognition` | comparison | TSLA 4/25, UBER 20/25 | 1/2 |
| `cmp-footprint` | comparison | TSLA not in top 25, UBER 10/25 | 0/2 |
| `tsla-cash-and-investments` | multi_page | TSLA 1/25, TSLA 16/25 | 1/2 |
| `tsla-us-and-energy-revenue` | multi_page | TSLA 13/25, TSLA 1/25 | 1/2 |
| `uber-loss-vs-ebitda` | multi_page | UBER not in top 25, UBER 2/25 | 1/2 |

---

