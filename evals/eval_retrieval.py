"""
Retrieval eval: did the right chunks come back from Chroma?

Run from the project root:
    python evals/eval_retrieval.py                        # just print results
    python evals/eval_retrieval.py --log "what I changed"  # also append to evals/EVAL_LOG.md

For each question in golden_dataset.json we ask Chroma for the top K chunks,
then check whether each piece of evidence (source file + page) is among them.
No LLM is involved, so this tests ONLY the retrieval half of RAG.
"""
import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_chroma import Chroma
from embedding import get_embedding_function
import database

# Chunking comes from database.py and the embedding model from embedding.py.
# The three settings below MUST MATCH query.py (K_PER_SOURCE, CHUNKS_PER_SOURCE, NUM_SOURCES)
# and search_per_source() below mirrors query.py's function of the same name.
# If you change them in query.py, change them here too, otherwise the eval tests something else.
CHROMA_PATH = database.CHROMA_PATH
DATASET_PATH = "evals/dataset_3.json"
LOG_PATH = "evals/EVAL_LOG_dataset_3.md"
MAX_K = 25                 # query.py K_PER_SOURCE: chunks fetched from EACH PDF; ranks are within that PDF's list
CHUNKS_PER_SOURCE = 5      # query.py CHUNKS_PER_SOURCE
NUM_SOURCES = 2            # query.py NUM_SOURCES
K_VALUES = sorted({k for k in (3, 5, 15, MAX_K) if k <= MAX_K})   # we report recall at each of these


def is_match(doc, evidence):
    """A chunk is relevant if it comes from the evidence's file AND page (or one of its optional 'alt_pages',
    other pages that contain the same phrase)."""
    pages = [evidence["page"], *evidence.get("alt_pages", [])]
    return doc.metadata.get("source") == evidence["source"] and doc.metadata.get("page") in pages


def first_rank(docs, evidence):
    """1-based position of the first matching chunk, or None if not found."""
    for rank, doc in enumerate(docs, start=1):
        if is_match(doc, evidence):
            return rank
    return None


def search_per_source(db, query_text):
    """Mirror of query.py's search_per_source: each PDF is searched on its own (metadata filter on 'source').
    Returns {source: [(Document, score), ...]} with MAX_K results per PDF, best first."""
    sources = sorted({m["source"] for m in db.get(include=["metadatas"])["metadatas"]})
    return {s: db.similarity_search_with_score(query_text, k=MAX_K, filter={"source": s}) for s in sources}


def pipeline_context(per_source):
    """The chunks query.py sends to the LLM: the NUM_SOURCES PDFs with the closest best chunk,
    CHUNKS_PER_SOURCE chunks from each."""
    closest = sorted(per_source, key=lambda s: per_source[s][0][1])[:NUM_SOURCES]
    return [doc for s in closest for doc, _score in per_source[s][:CHUNKS_PER_SOURCE]]


def new_totals():
    return {"items": 0, "questions": 0, "full": 0, "pipeline": 0, "rr": 0.0, **{f"r{k}": 0 for k in K_VALUES}}


def add_row(totals, row):
    totals["questions"] += 1
    totals["items"] += row["n"]
    totals["full"] += row["pipeline"] == row["n"]
    totals["pipeline"] += row["pipeline"]
    totals["rr"] += row["rr"]
    for k in K_VALUES:
        totals[f"r{k}"] += row[f"r{k}"]


def summarize(t):
    n = t["items"]
    out = {f"Recall@{k}": t[f"r{k}"] / n for k in K_VALUES}
    out["MRR"] = t["rr"] / n
    out["Pipeline recall"] = t["pipeline"] / n
    out["Fully answerable"] = f"{t['full']}/{t['questions']}"
    out["Fully answerable %"] = f"{t['full'] / t['questions']:.0%}"
    return out


def evaluate(dataset, db):
    rows = []
    for q in dataset:
        per_source = search_per_source(db, q["question"])
        context_docs = pipeline_context(per_source)

        row = {"id": q["id"], "type": q["type"], "n": len(q["evidence"]), "pipeline": 0, "rr": 0.0,
               "ranks": [], "labels": [], **{f"r{k}": 0 for k in K_VALUES}}
        for ev in q["evidence"]:
            # the evidence is looked for in its own PDF's results, so rank = position within that PDF
            rank = first_rank([doc for doc, _score in per_source.get(ev["source"], [])], ev)
            row["ranks"].append(rank)
            row["labels"].append(os.path.basename(ev["source"]).split("-")[0].upper())  # e.g. TSLA, UBER
            row["rr"] += 1 / rank if rank else 0
            for k in K_VALUES:
                if rank is not None and rank <= k:
                    row[f"r{k}"] += 1
            if any(is_match(d, ev) for d in context_docs):
                row["pipeline"] += 1
        rows.append(row)
    return rows


def git_info():
    def run(*args):
        return subprocess.run(["git", *args], capture_output=True, text=True).stdout.strip()
    commit = run("rev-parse", "--short", "HEAD") or "unknown"
    dirty = " (+ uncommitted changes)" if run("status", "--porcelain") else ""
    return f"{commit}{dirty}"


def pipeline_config():
    """Describe the pipeline from the real values in the code."""
    embeddings = get_embedding_function()
    return (
        f"chunk size {database.CHUNK_SIZE} / overlap {database.CHUNK_OVERLAP}; "
        f"embedding {getattr(embeddings, 'model_name', 'unknown')}; "
        f"Chroma default distance (L2); "
        f"search = separate per PDF, k={MAX_K} each; "
        f"context = {NUM_SOURCES} PDFs x {CHUNKS_PER_SOURCE} chunks each"
    )


def fmt(v):
    return f"{v:.2f}" if isinstance(v, float) else str(v)


def rank_table(rows):
    """Markdown table: for each question, where the evidence landed among the MAX_K retrieved chunks."""
    lines = [
        f"| Question | Type | Rank of evidence (out of {MAX_K}) | Reaches LLM |",
        "|---|---|---|---|",
    ]
    for r in rows:
        cells = [f"{label} {rank}/{MAX_K}" if rank else f"{label} not in top {MAX_K}"
                 for label, rank in zip(r["labels"], r["ranks"])]
        lines.append(f"| `{r['id']}` | {r['type']} | {', '.join(cells)} | {r['pipeline']}/{r['n']} |")
    return lines


def append_log(note, rows, overall, by_type):
    """Append one run to EVAL_LOG.md, creating the file with a header if needed."""
    is_new = not os.path.exists(LOG_PATH)
    run_no = 1
    if not is_new:
        with open(LOG_PATH) as f:
            run_no = sum(1 for line in f if line.startswith("## Run ")) + 1

    metric_names = list(summarize(overall).keys())
    lines = []
    if is_new:
        lines += [
            "# Retrieval eval log",
            "",
            "**Note:** This eval currently is not for checking if the final answer is correct or not, "
            "but to check if it retrieved information from the correct location in the pdf.",
            "",
            "Append-only history of retrieval evals. Each run is written by "
            "`python evals/eval_retrieval.py --log \"note\"`.",
            "",
            "- **Evidence page**: the page in `evidence`, plus any `alt_pages` (other pages containing the same phrase) "
            "when the dataset lists them.",
            "- **Rank**: position of the first retrieved chunk that comes from the evidence page, among the k chunks "
            "returned (1 = best match, k = last). k is shown in each run's config.",
            "- **Recall@k**: share of evidence pages found in the top k retrieved chunks.",
            "- **MRR**: average of 1/rank of the first correct chunk (1.0 = always rank 1, 0 = never found).",
            "- **Pipeline recall**: share of evidence pages that reach the LLM after the context-selection step "
            "(chunks per PDF, number of PDFs).",
            "- **Fully answerable**: questions where ALL needed evidence reaches the LLM.",
            "",
        ]
    n_q = len(rows)
    n_items = overall["items"]
    found = sum(rank is not None for r in rows for rank in r["ranks"])
    counts = ", ".join(f"{t['questions']} {name}" for name, t in sorted(by_type.items()))
    lines += [
        f"## Run {run_no} - {datetime.now():%Y-%m-%d %H:%M}",
        "",
        f"- **What changed:** {note}",
        f"- **Git commit:** {git_info()}",
        f"- **Dataset:** {n_q} questions ({counts}), {n_items} evidence items",
        f"- **Evidence found within the top {MAX_K} (k):** {found}/{n_items} ({found / n_items:.0%})",
        f"- **Setup (read from the code):** {pipeline_config()}",
        "",
        "| Group | Questions | " + " | ".join(metric_names) + " |",
        "|---|---|" + "---|" * len(metric_names),
    ]
    for name, t in [("All", overall)] + sorted(by_type.items()):
        s = summarize(t)
        lines.append(f"| {name} | {t['questions']} | " + " | ".join(fmt(s[m]) for m in metric_names) + " |")

    lines += ["", "**Where the evidence landed per question:**", ""]
    lines += rank_table(rows)
    lines += ["", "---", ""]

    with open(LOG_PATH, "a") as f:
        f.write("\n".join(lines) + "\n")
    print(f"\nAppended Run {run_no} to {LOG_PATH}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", metavar="NOTE", help="append this run to evals/EVAL_LOG.md with a note on what changed")
    args = parser.parse_args()

    with open(DATASET_PATH) as f:
        dataset = json.load(f)

    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    rows = evaluate(dataset, db)

    overall = new_totals()
    by_type = defaultdict(new_totals)
    print(f"{'id':<24} {'type':<11} " + " ".join(f"@{k:<3}" for k in K_VALUES) + "  pipeline  ranks")
    print("-" * 84)
    for r in rows:
        add_row(overall, r)
        add_row(by_type[r["type"]], r)
        n = r["n"]
        cols = " ".join(f"{r[f'r{k}']}/{n}".ljust(4) for k in K_VALUES)
        print(f"{r['id']:<24} {r['type']:<11} {cols}  {r['pipeline']}/{n}       {r['ranks']}")

    print("-" * 84)
    print(f"Evidence items: {overall['items']}   Questions: {overall['questions']}\n")
    for name, value in summarize(overall).items():
        print(f"{name:<18}: {fmt(value)}")

    if args.log:
        append_log(args.log, rows, overall, by_type)


if __name__ == "__main__":
    main()
