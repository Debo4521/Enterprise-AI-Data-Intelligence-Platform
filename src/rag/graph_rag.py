import sys
from pathlib import Path
from typing import Dict, Any, List

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

RETRIEVAL_DIR = PROJECT_ROOT / "src" / "retrieval"
RAG_DIR = PROJECT_ROOT / "src" / "rag"

sys.path.append(str(RETRIEVAL_DIR))
sys.path.append(str(RAG_DIR))

from hybrid_retriever import HybridRetriever
from llm_answer_generator import LLMAnswerGenerator


class GraphRAG:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.answer_generator = LLMAnswerGenerator()

    def answer(self, query: str) -> Dict[str, Any]:

        retrieval_results = self.retriever.retrieve(
            query,
            top_k=2
        )

        vector_context = self._build_vector_context(
            retrieval_results["vector_results"]
        )

        graph_context = self._build_graph_context(
            retrieval_results["graph_results"]
        )

        final_answer = self.answer_generator.generate_answer(
            query=query,
            vector_context=vector_context,
            graph_context=graph_context,
        )

        return {
            "query": query,
            "answer": final_answer,
            "vector_context": vector_context,
            "graph_context": graph_context,
            "retrieval_strategy": retrieval_results["retrieval_strategy"],
        }

    def _build_vector_context(
        self,
        vector_results: List[Dict[str, Any]]
    ) -> str:

        context_parts = []

        for result in vector_results:
            context_parts.append(
                f"Source Chunk: {result['chunk_id']}\n"
                f"Text: {result['text']}\n"
                f"Entities: {result['entities']}"
            )

        return "\n\n".join(context_parts)

    def _build_graph_context(
        self,
        graph_results: Dict[str, Any]
    ) -> str:

        matched_nodes = graph_results.get(
            "matched_nodes",
            []
        )

        matched_edges = graph_results.get(
            "matched_edges",
            []
        )

        node_lines = []
        edge_lines = []

        for node in matched_nodes:
            node_lines.append(
                f"{node['type']}: {node['name']}"
            )

        for edge in matched_edges:
            edge_lines.append(
                f"{edge['source']} --{edge['relationship']}--> {edge['target']}"
            )

        return (
            "Matched Graph Nodes:\n"
            + "\n".join(node_lines)
            + "\n\nMatched Graph Relationships:\n"
            + "\n".join(edge_lines)
        )


if __name__ == "__main__":

    graph_rag = GraphRAG()

    query = "What happened to revenue and customer satisfaction?"

    result = graph_rag.answer(query)

    print("\nGraph-RAG Results")
    print("=" * 50)
    print(result["answer"])