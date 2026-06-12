import sys
from pathlib import Path
from typing import Dict, Any

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent

RAG_DIR = PROJECT_ROOT / "src" / "rag"
EVALUATION_DIR = PROJECT_ROOT / "src" / "evaluation"
AGENTS_DIR = PROJECT_ROOT / "src" / "agents"

sys.path.append(str(RAG_DIR))
sys.path.append(str(EVALUATION_DIR))
sys.path.append(str(AGENTS_DIR))

from graph_rag import GraphRAG
from rag_evaluator import RAGEvaluator
from critic_agent import CriticAgent


class OrchestratorAgent:

    def __init__(self):
        self.graph_rag = GraphRAG()
        self.evaluator = RAGEvaluator()
        self.critic = CriticAgent()

    def run(self, query: str) -> Dict[str, Any]:
        rag_result = self.graph_rag.answer(query)

        critic_result = self.critic.evaluate(
            answer=rag_result["answer"],
            vector_context=rag_result["vector_context"],
            graph_context=rag_result["graph_context"],
        )

        evaluation_result = self.evaluator.evaluate(query)

        return {
            "query": query,
            "final_answer": rag_result["answer"],
            "retrieval_strategy": rag_result["retrieval_strategy"],
            "vector_context": rag_result["vector_context"],
            "graph_context": rag_result["graph_context"],
            "critic_result": critic_result,
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

    query = "What happened in quarterly_report.txt?"

    result = agent.run(query)

    print("\nEnterprise AI Orchestrator Results")
    print("=" * 50)
    print(result["final_answer"])
    print("\nCritic Result:")
    print(result["critic_result"])