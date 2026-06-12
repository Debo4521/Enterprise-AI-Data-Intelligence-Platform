import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[1]

AGENTS_DIR = PROJECT_ROOT / "src" / "agents"
PIPELINE_DIR = PROJECT_ROOT / "src" / "pipeline"
RAG_DIR = PROJECT_ROOT / "src" / "rag"

sys.path.insert(0, str(AGENTS_DIR))
sys.path.insert(0, str(PIPELINE_DIR))
sys.path.insert(0, str(RAG_DIR))

from orchestrator_agent import OrchestratorAgent
from auto_pipeline import AutoPipeline
from comparison_engine import ComparisonEngine


def extract_section(text: str, section_title: str) -> list[str]:
    lines = text.splitlines()
    capture = False
    items = []

    for line in lines:
        clean = line.strip()

        if clean.startswith(section_title):
            capture = True
            continue

        if capture and clean.endswith(":") and clean != section_title:
            break

        if capture and clean.startswith("-"):
            items.append(clean.replace("-", "").strip())

    return items


def render_bullets(items: list[str]):
    if not items:
        st.caption("No items detected.")
        return

    for item in items:
        st.markdown(f"- {item}")


def save_uploaded_file(uploaded_file, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    file_path = target_dir / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path


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
        "Auto Pipeline",
        "Graph Visualization",
        "Document Comparison",
    ]

    for module in modules:
        st.success(module)

    st.divider()
    st.info("Version: MVP v1.7")


tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Ask AI",
        "Evaluation Dashboard",
        "Retrieved Evidence",
        "Knowledge Graph",
        "Compare Documents",
        "System Architecture",
    ]
)

with tab1:
    st.subheader("Upload Enterprise Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF, DOCX, CSV, TXT, or Excel files",
        type=["pdf", "docx", "csv", "txt", "xlsx"],
        accept_multiple_files=True,
        key="ask_ai_uploader",
    )

    if uploaded_files:
        raw_data_path = PROJECT_ROOT / "data" / "raw"

        for uploaded_file in uploaded_files:
            save_uploaded_file(uploaded_file, raw_data_path)

        st.success(f"Uploaded {len(uploaded_files)} file(s) to data/raw.")

        with st.spinner("Running automatic enterprise pipeline..."):
            pipeline = AutoPipeline()
            pipeline_success = pipeline.run()

        if pipeline_success:
            st.success(
                "Enterprise pipeline completed successfully. You can now ask questions."
            )
        else:
            st.error("Pipeline failed. Please check your uploaded files.")

    st.divider()

    st.subheader("Ask a Business Question")

    query = st.text_input(
        "Enter your question",
        value="What happened in quarterly_report.txt?",
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
        st.info(result["final_answer"])

with tab2:
    st.subheader("Evaluation Dashboard")

    if "result" not in st.session_state:
        st.warning("Run an analysis first from the Ask AI tab.")
    else:
        result = st.session_state["result"]
        evaluation = result["evaluation"]
        critic = result["critic_result"]

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Retrieval", evaluation["retrieval_score"])
        col2.metric("Graph Usage", evaluation["graph_usage_score"])
        col3.metric("Evidence", evaluation["evidence_coverage_score"])
        col4.metric("Critic", evaluation["critic_confidence_score"])
        col5.metric("Overall", evaluation["overall_enterprise_rag_score"])

        st.divider()

        risk_level = critic["risk_level"]

        if risk_level == "low":
            st.success("Low-risk answer: strong retrieval and evidence support.")
        elif risk_level == "medium":
            st.warning("Medium-risk answer: review retrieved evidence.")
        else:
            st.error("High-risk answer: weak evidence support.")

        st.subheader("AI Critic Summary")
        st.write(critic["critic_summary"])

        st.subheader("System Status")
        st.json(
            {
                "query": result["query"],
                "status": result["status"],
                "retrieval_strategy": result["retrieval_strategy"],
                "risk_level": critic["risk_level"],
            }
        )

with tab3:
    st.subheader("Retrieved Evidence")

    if "result" not in st.session_state:
        st.warning("Run an analysis first from the Ask AI tab.")
    else:
        result = st.session_state["result"]
        final_answer = result["final_answer"]
        critic = result["critic_result"]

        st.markdown("### Vector Search Evidence")

        with st.expander("Open vector context"):
            st.text(result["vector_context"])

        st.markdown("### Structured Knowledge Graph Evidence")

        companies = extract_section(final_answer, "Companies:")
        departments = extract_section(final_answer, "Departments:")
        metrics = extract_section(final_answer, "Business Metrics:")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### Companies")
            render_bullets(companies)

        with col2:
            st.markdown("#### Departments")
            render_bullets(departments)

        with col3:
            st.markdown("#### Business Metrics")
            render_bullets(metrics)

        st.markdown("### Raw Knowledge Graph Context")

        with st.expander("Open graph context"):
            st.text(result["graph_context"])

        st.markdown("### AI Critic Evidence")

        col1, col2 = st.columns(2)

        col1.metric("Confidence Score", critic["confidence_score"])
        col2.metric("Risk Level", critic["risk_level"])

        st.json(critic["checks"])

        st.markdown("### Final Business Answer")

        with st.expander("Open final answer"):
            st.write(result["final_answer"])

with tab4:
    st.subheader("Interactive Knowledge Graph")

    graph_path = PROJECT_ROOT / "data" / "processed" / "knowledge_graph.html"

    if graph_path.exists():
        with open(graph_path, "r", encoding="utf-8") as file:
            graph_html = file.read()

        components.html(
            graph_html,
            height=700,
            scrolling=True,
        )
    else:
        st.warning(
            "Knowledge graph visualization not found. Run graph_visualizer.py first."
        )

with tab5:
    st.subheader("Compare Enterprise Documents")
    st.info("Upload two enterprise documents, then compare their business metrics.")

    compare_file_1 = st.file_uploader(
        "Upload first document",
        type=["pdf", "docx", "csv", "txt", "xlsx"],
        key="compare_file_1",
    )

    compare_file_2 = st.file_uploader(
        "Upload second document",
        type=["pdf", "docx", "csv", "txt", "xlsx"],
        key="compare_file_2",
    )

    compare_button = st.button("Compare Uploaded Documents", type="primary")

    if compare_button:
        if compare_file_1 is None or compare_file_2 is None:
            st.warning("Please upload two documents before comparing.")
        else:
            raw_data_path = PROJECT_ROOT / "data" / "raw"

            save_uploaded_file(compare_file_1, raw_data_path)
            save_uploaded_file(compare_file_2, raw_data_path)

            st.success("Both files uploaded successfully.")

            with st.spinner("Running enterprise pipeline before comparison..."):
                pipeline = AutoPipeline()
                pipeline_success = pipeline.run()

            if pipeline_success:
                with st.spinner("Comparing documents..."):
                    engine = ComparisonEngine()
                    result = engine.compare_files(
                        compare_file_1.name,
                        compare_file_2.name,
                    )

                st.success("Comparison completed.")

                st.markdown("### Comparison Table")
                st.table(result["comparison"])

                st.markdown("### Compared Files")
                col1, col2 = st.columns(2)

                with col1:
                    st.info(result["file_a"])

                with col2:
                    st.info(result["file_b"])
            else:
                st.error("Pipeline failed. Please check your uploaded files.")

with tab6:
    st.subheader("System Architecture")

    st.code(
        """
Enterprise Files
        |
        v
Auto Pipeline
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