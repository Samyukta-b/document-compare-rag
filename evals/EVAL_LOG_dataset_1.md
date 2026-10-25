# Retrieval eval log

**Note:** This eval currently is not for checking if the final answer is correct or not, but to check if it retrieved information from the correct location in the pdf.

Append-only history of retrieval evals. Each run is written by `python evals/eval_retrieval.py --log "note"`.

- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks returned (1 = best match, k = last). k is shown in each run's setup.
- **Recall@k**: share of evidence pages found in the top k retrieved chunks.
- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).
- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step ("3 chunks per document, first 2 documents" in Run 1).
- **Fully answerable**: questions where ALL needed evidence reaches the LLM.

## Run 1 - 2026-10-25 15:07

- **What changed:** Baseline. Original retrieval: similarity_search k=15 over both PDFs mixed, then group by source (3 chunks per doc, first 2 docs). Chunk size 800 / overlap 80, all-MiniLM-L12-v2, Chroma default L2. Dataset has 30 questions (14 single, 16 comparison).
- **Git commit:** dd28e4b (+ uncommitted changes)
- **Dataset:** 30 questions, 46 evidence items
- **Evidence found within the top 15 (k):** 23/46 (50%)
- **Retrieval config:** k=15, results grouped by source (3 per doc, first 2 docs)

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|
| All | 30 | 0.22 | 0.33 | 0.50 | 0.16 | 0.30 | 7/30 | 23% |
| comparison | 16 | 0.16 | 0.25 | 0.34 | 0.12 | 0.28 | 2/16 | 12% |
| single | 14 | 0.36 | 0.50 | 0.86 | 0.26 | 0.36 | 5/14 | 36% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 15) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 8/15 | 0/1 |
| `tsla-deliveries` | single | TSLA 4/15 | 0/1 |
| `tsla-storage` | single | TSLA 5/15 | 0/1 |
| `tsla-net-income` | single | TSLA 15/15 | 0/1 |
| `tsla-rnd` | single | TSLA 8/15 | 0/1 |
| `tsla-gross-margin` | single | TSLA 6/15 | 0/1 |
| `tsla-cash` | single | TSLA 2/15 | 1/1 |
| `uber-revenue` | single | UBER 2/15 | 1/1 |
| `uber-employees` | single | UBER 3/15 | 1/1 |
| `uber-net-loss` | single | UBER not in top 15 | 0/1 |
| `uber-rnd` | single | UBER not in top 15 | 0/1 |
| `uber-segments` | single | UBER 14/15 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/15 | 1/1 |
| `uber-cash` | single | UBER 3/15 | 1/1 |
| `cmp-revenue` | comparison | TSLA not in top 15, UBER 2/15 | 1/2 |
| `cmp-rnd` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-cash` | comparison | TSLA 7/15, UBER 2/15 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-headcount` | comparison | TSLA 3/15, UBER 2/15 | 2/2 |
| `cmp-segments` | comparison | TSLA not in top 15, UBER 5/15 | 0/2 |
| `cmp-headquarters` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-exchange` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-incorporation` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-operating-cashflow` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 13/15, UBER 12/15 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 4/15, UBER not in top 15 | 1/2 |
| `cmp-operating-result` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-capex` | comparison | TSLA 5/15, UBER not in top 15 | 1/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 15, UBER not in top 15 | 0/2 |
| `cmp-ev-tech` | comparison | TSLA 1/15, UBER not in top 15 | 1/2 |

---

## Run 2 - 2026-10-25 15:21

- **What changed:** Raised k from 15 to 50. Only change: retrieval.K. Retrieval and context-selection logic moved into retrieval.py so the eval reads the same code as the app (no logic change). Compare with Run 1 (k=15).
- **Git commit:** dd28e4b (+ uncommitted changes)
- **Dataset:** 30 questions (16 comparison, 14 single), 46 evidence items
- **Evidence found within the top 50 (k):** 30/46 (65%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search k=50; context = first 2 PDFs x 3 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@50 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 30 | 0.22 | 0.33 | 0.50 | 0.65 | 0.17 | 0.33 | 7/30 | 23% |
| comparison | 16 | 0.16 | 0.25 | 0.34 | 0.53 | 0.12 | 0.31 | 2/16 | 12% |
| single | 14 | 0.36 | 0.50 | 0.86 | 0.93 | 0.26 | 0.36 | 5/14 | 36% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 50) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 8/50 | 0/1 |
| `tsla-deliveries` | single | TSLA 4/50 | 0/1 |
| `tsla-storage` | single | TSLA 5/50 | 0/1 |
| `tsla-net-income` | single | TSLA 15/50 | 0/1 |
| `tsla-rnd` | single | TSLA 8/50 | 0/1 |
| `tsla-gross-margin` | single | TSLA 6/50 | 0/1 |
| `tsla-cash` | single | TSLA 2/50 | 1/1 |
| `uber-revenue` | single | UBER 2/50 | 1/1 |
| `uber-employees` | single | UBER 3/50 | 1/1 |
| `uber-net-loss` | single | UBER not in top 50 | 0/1 |
| `uber-rnd` | single | UBER 31/50 | 0/1 |
| `uber-segments` | single | UBER 14/50 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/50 | 1/1 |
| `uber-cash` | single | UBER 3/50 | 1/1 |
| `cmp-revenue` | comparison | TSLA not in top 50, UBER 2/50 | 1/2 |
| `cmp-rnd` | comparison | TSLA 44/50, UBER not in top 50 | 0/2 |
| `cmp-cash` | comparison | TSLA 7/50, UBER 2/50 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-headcount` | comparison | TSLA 3/50, UBER 2/50 | 2/2 |
| `cmp-segments` | comparison | TSLA 23/50, UBER 5/50 | 0/2 |
| `cmp-headquarters` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-exchange` | comparison | TSLA 34/50, UBER not in top 50 | 0/2 |
| `cmp-incorporation` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-operating-cashflow` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 13/50, UBER 12/50 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 4/50, UBER not in top 50 | 1/2 |
| `cmp-operating-result` | comparison | TSLA 19/50, UBER 36/50 | 1/2 |
| `cmp-capex` | comparison | TSLA 5/50, UBER not in top 50 | 1/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 50, UBER 33/50 | 0/2 |
| `cmp-ev-tech` | comparison | TSLA 1/50, UBER not in top 50 | 1/2 |

---

## Run 3 - 2026-10-25 15:36

- **What changed:** CHUNKS_PER_SOURCE 3 -> 5 (k stays 50). Only change vs Run 2.
- **Git commit:** dd28e4b (+ uncommitted changes)
- **Dataset:** 30 questions (16 comparison, 14 single), 46 evidence items
- **Evidence found within the top 50 (k):** 30/46 (65%)
- **Setup (read from the code):** chunk size 800 / overlap 80; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search k=50; context = first 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@50 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 30 | 0.22 | 0.33 | 0.50 | 0.65 | 0.17 | 0.39 | 9/30 | 30% |
| comparison | 16 | 0.16 | 0.25 | 0.34 | 0.53 | 0.12 | 0.34 | 2/16 | 12% |
| single | 14 | 0.36 | 0.50 | 0.86 | 0.93 | 0.26 | 0.50 | 7/14 | 50% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 50) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 8/50 | 0/1 |
| `tsla-deliveries` | single | TSLA 4/50 | 1/1 |
| `tsla-storage` | single | TSLA 5/50 | 1/1 |
| `tsla-net-income` | single | TSLA 15/50 | 0/1 |
| `tsla-rnd` | single | TSLA 8/50 | 0/1 |
| `tsla-gross-margin` | single | TSLA 6/50 | 0/1 |
| `tsla-cash` | single | TSLA 2/50 | 1/1 |
| `uber-revenue` | single | UBER 2/50 | 1/1 |
| `uber-employees` | single | UBER 3/50 | 1/1 |
| `uber-net-loss` | single | UBER not in top 50 | 0/1 |
| `uber-rnd` | single | UBER 31/50 | 0/1 |
| `uber-segments` | single | UBER 14/50 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/50 | 1/1 |
| `uber-cash` | single | UBER 3/50 | 1/1 |
| `cmp-revenue` | comparison | TSLA not in top 50, UBER 2/50 | 1/2 |
| `cmp-rnd` | comparison | TSLA 44/50, UBER not in top 50 | 0/2 |
| `cmp-cash` | comparison | TSLA 7/50, UBER 2/50 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-headcount` | comparison | TSLA 3/50, UBER 2/50 | 2/2 |
| `cmp-segments` | comparison | TSLA 23/50, UBER 5/50 | 1/2 |
| `cmp-headquarters` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-exchange` | comparison | TSLA 34/50, UBER not in top 50 | 0/2 |
| `cmp-incorporation` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-operating-cashflow` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 13/50, UBER 12/50 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 4/50, UBER not in top 50 | 1/2 |
| `cmp-operating-result` | comparison | TSLA 19/50, UBER 36/50 | 1/2 |
| `cmp-capex` | comparison | TSLA 5/50, UBER not in top 50 | 1/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 50, UBER 33/50 | 0/2 |
| `cmp-ev-tech` | comparison | TSLA 1/50, UBER not in top 50 | 1/2 |

---

## Run 4 - 2026-10-25 15:53

- **What changed:** Chunk size 800 -> 500, overlap 80 -> 50 (re-indexed with database.py --reset: 2472 -> 3080 chunks). Retrieval settings unchanged from Run 3 (k=50, 5 chunks per PDF). Only change vs Run 3.
- **Git commit:** dd28e4b (+ uncommitted changes)
- **Dataset:** 30 questions (16 comparison, 14 single), 46 evidence items
- **Evidence found within the top 50 (k):** 33/46 (72%)
- **Setup (read from the code):** chunk size 500 / overlap 50; embedding sentence-transformers/all-MiniLM-L12-v2; Chroma default distance (L2); search k=50; context = first 2 PDFs x 5 chunks each

| Group | Questions | Recall@3 | Recall@5 | Recall@15 | Recall@50 | MRR | Pipeline recall | Fully answerable | Fully answerable % |
|---|---|---|---|---|---|---|---|---|---|
| All | 30 | 0.26 | 0.26 | 0.46 | 0.72 | 0.18 | 0.35 | 9/30 | 30% |
| comparison | 16 | 0.16 | 0.16 | 0.34 | 0.59 | 0.12 | 0.28 | 2/16 | 12% |
| single | 14 | 0.50 | 0.50 | 0.71 | 1.00 | 0.31 | 0.50 | 7/14 | 50% |

**Where the evidence landed per question:**

| Question | Type | Rank of evidence (out of 50) | Reaches LLM |
|---|---|---|---|
| `tsla-revenue` | single | TSLA 8/50 | 0/1 |
| `tsla-deliveries` | single | TSLA 2/50 | 1/1 |
| `tsla-storage` | single | TSLA 3/50 | 1/1 |
| `tsla-net-income` | single | TSLA 7/50 | 0/1 |
| `tsla-rnd` | single | TSLA 17/50 | 0/1 |
| `tsla-gross-margin` | single | TSLA 6/50 | 0/1 |
| `tsla-cash` | single | TSLA 2/50 | 1/1 |
| `uber-revenue` | single | UBER 2/50 | 1/1 |
| `uber-employees` | single | UBER 2/50 | 1/1 |
| `uber-net-loss` | single | UBER 38/50 | 0/1 |
| `uber-rnd` | single | UBER 22/50 | 0/1 |
| `uber-segments` | single | UBER 21/50 | 0/1 |
| `uber-gross-bookings` | single | UBER 1/50 | 1/1 |
| `uber-cash` | single | UBER 3/50 | 1/1 |
| `cmp-revenue` | comparison | TSLA not in top 50, UBER 3/50 | 1/2 |
| `cmp-rnd` | comparison | TSLA 28/50, UBER not in top 50 | 0/2 |
| `cmp-cash` | comparison | TSLA 8/50, UBER 2/50 | 2/2 |
| `cmp-profit` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-headcount` | comparison | TSLA 2/50, UBER 1/50 | 2/2 |
| `cmp-segments` | comparison | TSLA 37/50, UBER 6/50 | 0/2 |
| `cmp-headquarters` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-exchange` | comparison | TSLA 36/50, UBER 15/50 | 0/2 |
| `cmp-incorporation` | comparison | TSLA not in top 50, UBER not in top 50 | 0/2 |
| `cmp-operating-cashflow` | comparison | TSLA 47/50, UBER not in top 50 | 0/2 |
| `cmp-investing-cashflow` | comparison | TSLA 25/50, UBER 16/50 | 1/2 |
| `cmp-stock-comp` | comparison | TSLA 8/50, UBER not in top 50 | 1/2 |
| `cmp-operating-result` | comparison | TSLA 24/50, UBER 10/50 | 1/2 |
| `cmp-capex` | comparison | TSLA 11/50, UBER not in top 50 | 0/2 |
| `cmp-fiscal-year` | comparison | TSLA not in top 50, UBER 48/50 | 0/2 |
| `cmp-ev-tech` | comparison | TSLA 2/50, UBER not in top 50 | 1/2 |

---

