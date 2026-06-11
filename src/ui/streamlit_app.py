import sys
from pathlib import Path

import streamlit as st

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]
AGENTS_DIR = PROJECT_ROOT / "src" / "agents"

sys.path.insert(0, str(AGENTS_DIR))

from orchestrator_agent import OrchestratorAgent


st.set_page_config(
    page_title="Enterprise AI Data Intelligence Platform",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Enterprise AI Data Intelligence Platform")
st.caption(
    "A Multi-Agent Graph-RAG System for Enterprise Knowledge Management and Business Intelligence"
)

with st.sidebar:
    st.header("System Modules")

    modules = [
        "Data Ingestion",
        "Text Chunking",
        "Entity Extraction",
        "Knowledge Graph",
        "BGE Embeddings",
        "FAISS Vector Search",
        "Hybrid Retrieval",
        "Graph-RAG",
        "AI Critic",
        "RAG Evaluation",
        "Orchestrator Agent",
    ]

    for module in modules:
        st.success(module)

    st.divider()
    st.info("Version: MVP v1.0")


tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Ask AI",
        "Evaluation Dashboard",
        "Retrieved Evidence",
        "System Architecture",
    ]
)

with tab1:
    st.subheader("Upload Enterprise Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, CSV, TXT, or Excel files",
        type=["pdf", "docx", "csv", "txt", "xlsx"],
        accept_multiple_files=True,
    )

    if uploaded_files:
        raw_data_path = PROJECT_ROOT / "data" / "raw"
        raw_data_path.mkdir(parents=True, exist_ok=True)

        for uploaded_file in uploaded_files:
            file_path = raw_data_path / uploaded_file.name

            with open(file_path, "wb") as file:
                file.write(uploaded_file.getbuffer())

        st.success(f"Uploaded {len(uploaded_files)} file(s) to data/raw.")
        st.info(
            "Next step: rerun the backend pipeline scripts to update ingestion, chunks, graph, embeddings, and FAISS index."
        )

    st.divider()

    st.subheader("Ask a Business Question")

    query = st.text_input(
        "Enter your question",
        value="What happened to revenue and customer satisfaction?",
    )

    run_button = st.button("Run Enterprise AI Analysis", type="primary")

    if run_button:
        with st.spinner("Running Hybrid Retrieval + Graph-RAG + AI Critic..."):
            agent = OrchestratorAgent()
            result = agent.run(query)

        st.session_state["result"] = result

    if "result" in st.session_state:
        result = st.session_state["result"]

        st.subheader("Business Intelligence Answer")
        st.write(result["final_answer"])

with tab2:
    st.subheader("Evaluation Dashboard")

    if "result" not in st.session_state:
        st.warning("Run an analysis first from the Ask AI tab.")
    else:
        result = st.session_state["result"]
        evaluation = result["evaluation"]

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Retrieval", evaluation["retrieval_score"])
        col2.metric("Graph Usage", evaluation["graph_usage_score"])
        col3.metric("Evidence", evaluation["evidence_coverage_score"])
        col4.metric("Critic", evaluation["critic_confidence_score"])
        col5.metric("Overall", evaluation["overall_enterprise_rag_score"])

        st.divider()

        st.subheader("System Status")
        st.json(
            {
                "query": result["query"],
                "status": result["status"],
                "retrieval_strategy": result["retrieval_strategy"],
            }
        )

with tab3:
    st.subheader("Retrieved Evidence")

    if "result" not in st.session_state:
        st.warning("Run an analysis first from the Ask AI tab.")
    else:
        final_answer = st.session_state["result"]["final_answer"]

        with st.expander("Full Answer Evidence"):
            st.write(final_answer)

        st.info(
            "Next upgrade: we will show vector chunks and knowledge graph evidence separately."
        )

with tab4:
    st.subheader("System Architecture")

    st.code(
        """
Enterprise Files
        |
        v
Data Ingestion
        |
        v
Text Chunking
        |
        v
Entity Extraction
        |
        v
Knowledge Graph Builder
        |
        v
BGE Embedding Engine
        |
        v
FAISS Vector Search
        |
        v
Hybrid Retrieval
        |
        v
Graph-RAG
        |
        v
AI Critic Agent
        |
        v
RAG Evaluator
        |
        v
Orchestrator Agent
        |
        v
Enterprise UI
        """,
        language="text",
    )