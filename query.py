from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from embedding import get_embedding_function
from database import split_documents, add_to_chroma, load_documents
import streamlit as st
import os
import logging


logging.basicConfig(
    filename="rag.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


CHROMA_PATH = "chroma"
K_PER_SOURCE = 25        # chunks fetched from EACH PDF (separate search per PDF)
CHUNKS_PER_SOURCE = 5    # chunks per PDF that go into the prompt
NUM_SOURCES = 2          # how many PDFs go into the prompt

COMPARISON_PROMPT_TEMPLATE = """
Compare the two sources below and answer the question directly with specific facts and figures from each source.

Source 1 {source1}:
{source1_context}

Source 2 {source2}:
{source2_context}

Question: {question}

Using the contexts above, answer with 1-2 relevant findings per source."""

@st.cache_resource
def load_embedding_function():
    return get_embedding_function()

def process_uploaded_pdfs(pdf_files):
    with st.status("📄 Processing uploaded PDFs...", expanded=True) as status:
            for pdf_file in pdf_files:
                # save to /data
                save_path = os.path.join("data", pdf_file.name)
                with open(save_path, "wb") as f:
                    f.write(pdf_file.read())
                status.write(f"Saved {pdf_file.name} to /data")
            
            # reindex the entire /data folder including new files
            documents = load_documents()
            chunks = split_documents(documents)
            add_to_chroma(chunks)
            status.update(label="✅ PDFs indexed into DB")

def search_per_source(db, query_text: str):
    """
    Search each PDF on its own (metadata filter on 'source'), so one PDF can't crowd the other
    out of the results. Returns {source: [chunk text, ...]} for the NUM_SOURCES PDFs whose best
    chunk is closest to the query, with up to CHUNKS_PER_SOURCE chunks each.
    """
    sources = sorted({m["source"] for m in db.get(include=["metadatas"])["metadatas"]})
    per_source = {
        source: db.similarity_search_with_score(query_text, k=K_PER_SOURCE, filter={"source": source})
        for source in sources
    }
    # Lower score = closer match, so the PDFs with the closest best chunk come first.
    closest = sorted(per_source, key=lambda s: per_source[s][0][1])[:NUM_SOURCES]
    return {s: [doc.page_content for doc, _score in per_source[s][:CHUNKS_PER_SOURCE]] for s in closest}

def query_rag(query_text: str, pdf_files=None):
    # Prepare the DB.
    embedding_function: HuggingFaceEmbeddings = load_embedding_function()
    
    with st.status("📚 Connecting to vector database...", expanded=True) as status:
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
        status.update(label="✅ Database connected")

    # If PDF files are uploaded, process each one.
    if pdf_files:
        process_uploaded_pdfs(pdf_files)

    # Search each PDF separately and keep the best chunks from each (we are comparing documents).
    source_chunks = search_per_source(db, query_text)

    logging.info(f"size of source_chunks: {len(source_chunks)}")

    # Extract contexts.
    doc_ids = list(source_chunks.keys())
    context_text_doc1 = "\n\n".join(source_chunks[doc_ids[0]])
    context_text_doc2 = "\n\n".join(source_chunks[doc_ids[1]])

    # Create the comparison prompt.
    prompt_template = ChatPromptTemplate.from_template(COMPARISON_PROMPT_TEMPLATE)
    prompt = prompt_template.format(source1={doc_ids[0]}, source1_context=context_text_doc1, source2={doc_ids[1]}, source2_context=context_text_doc2, question=query_text)

    # Invoke the model.
    with st.status("🤖 Generating response with AI...", expanded=True) as status:
        model = OllamaLLM(model="llama3.2:3b")
        response_text = model.invoke(prompt)
        status.update(label="✅ Response generated")

    formatted_response = f"Response: {response_text}\nSources: {doc_ids}"
    return formatted_response

def main():
    st.title("RAG Chatbot for Document Comparison")

    with st.form("query_form"):
        query_text = st.text_input("Enter your query:", placeholder="Type your question here...")
        pdf_files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)
        submitted = st.form_submit_button("Submit Query", use_container_width=True)

    if submitted:
        try:
            if query_text.strip() == "":
                st.error("Please enter a query.")
                return

            response: str = query_rag(query_text, pdf_files=pdf_files if pdf_files else None)
            st.text(response)
        except ValueError as e:
            st.error(str(e))

if __name__ == "__main__":
    main()
