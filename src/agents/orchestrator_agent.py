import sys
from pathlib import Path
from typing import Dict, Any

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

RAG_DIR = PROJECT_ROOT / "src" / "rag"
EVALUATION_DIR = PROJECT_ROOT / "src" / "evaluation"

sys.path.append(str(RAG_DIR))
sys.path.append(str(EVALUATION_DIR))

from graph_rag import GraphRAG
from rag_evaluator import RAGEvaluator


class OrchestratorAgent:

    def __init__(self):
        self.graph_rag = GraphRAG()
        self.evaluator = RAGEvaluator()

    def run(self, query: str) -> Dict[str, Any]:
        rag_result = self.graph_rag.answer(query)
        evaluation_result = self.evaluator.evaluate(query)

        return {
            "query": query,
            "final_answer": rag_result["answer"],
            "retrieval_strategy": rag_result["retrieval_strategy"],
            "evaluation": {
                "retrieval_score": evaluation_result["retrieval_score"],
                "graph_usage_score": evaluation_result["graph_usage_score"],
                "evidence_coverage_score": evaluation_result["evidence_coverage_score"],
                "critic_confidence_score": evaluation_result["critic_confidence_score"],
                "overall_enterprise_rag_score": evaluation_result[
                    "overall_enterprise_rag_score"
                ],
            },
            "status": "completed",
        }


if __name__ == "__main__":

    agent = OrchestratorAgent()

    query = "What happened to revenue and customer satisfaction?"

    result = agent.run(query)

    print("\nEnterprise AI Orchestrator Results")
    print("=" * 50)
    print(f"Query: {result['query']}")
    print(f"Status: {result['status']}")
    print(f"Retrieval Strategy: {result['retrieval_strategy']}")

    print("\nEvaluation:")
    for key, value in result["evaluation"].items():
        print(f"{key}: {value}")

    print("\nFinal Answer:")
    print(result["final_answer"])