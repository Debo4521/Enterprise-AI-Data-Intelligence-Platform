import sys
from pathlib import Path
from typing import Dict, Any

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

RAG_DIR = PROJECT_ROOT / "src" / "rag"
AGENTS_DIR = PROJECT_ROOT / "src" / "agents"

sys.path.append(str(RAG_DIR))
sys.path.append(str(AGENTS_DIR))

from graph_rag import GraphRAG
from critic_agent import CriticAgent


class RAGEvaluator:

    def __init__(self):
        self.graph_rag = GraphRAG()
        self.critic = CriticAgent()

    def evaluate(self, query: str) -> Dict[str, Any]:
        rag_result = self.graph_rag.answer(query)

        critic_result = self.critic.evaluate(
            answer=rag_result["answer"],
            vector_context=rag_result["vector_context"],
            graph_context=rag_result["graph_context"],
        )

        retrieval_score = self._score_retrieval(rag_result)
        graph_score = self._score_graph_usage(rag_result)
        evidence_score = self._score_evidence_coverage(critic_result)
        critic_score = critic_result["confidence_score"]

        overall_score = round(
            (
                retrieval_score
                + graph_score
                + evidence_score
                + critic_score
            ) / 4,
            2,
        )

        return {
            "query": query,
            "retrieval_score": retrieval_score,
            "graph_usage_score": graph_score,
            "evidence_coverage_score": evidence_score,
            "critic_confidence_score": critic_score,
            "overall_enterprise_rag_score": overall_score,
            "critic_result": critic_result,
            "answer": rag_result["answer"],
        }

    def _score_retrieval(self, rag_result: Dict[str, Any]) -> float:
        vector_context = rag_result.get("vector_context", "")

        if len(vector_context.strip()) > 100:
            return 1.0

        if len(vector_context.strip()) > 0:
            return 0.5

        return 0.0

    def _score_graph_usage(self, rag_result: Dict[str, Any]) -> float:
        graph_context = rag_result.get("graph_context", "")

        if "BusinessMetric" in graph_context and "HAS_METRIC" in graph_context:
            return 1.0

        if graph_context.strip():
            return 0.5

        return 0.0

    def _score_evidence_coverage(self, critic_result: Dict[str, Any]) -> float:
        checks = critic_result.get("checks", {})

        if not checks:
            return 0.0

        passed = sum(1 for value in checks.values() if value)
        total = len(checks)

        return round(passed / total, 2)


if __name__ == "__main__":

    evaluator = RAGEvaluator()

    query = "What happened to revenue and customer satisfaction?"

    evaluation = evaluator.evaluate(query)

    print("\nEnterprise RAG Evaluation Results")
    print("=" * 50)
    print(f"Query: {evaluation['query']}")
    print(f"Retrieval Score: {evaluation['retrieval_score']}")
    print(f"Graph Usage Score: {evaluation['graph_usage_score']}")
    print(f"Evidence Coverage Score: {evaluation['evidence_coverage_score']}")
    print(f"Critic Confidence Score: {evaluation['critic_confidence_score']}")
    print(f"Overall Enterprise RAG Score: {evaluation['overall_enterprise_rag_score']}")

    print("\nCritic Summary:")
    print(evaluation["critic_result"]["critic_summary"])