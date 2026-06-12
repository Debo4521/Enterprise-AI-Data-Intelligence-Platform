import re
from typing import Dict, Any


class CriticAgent:

    def evaluate(
        self,
        answer: str,
        vector_context: str,
        graph_context: str
    ) -> Dict[str, Any]:

        combined_text = f"{answer}\n{vector_context}\n{graph_context}".lower()

        checks = {
            "revenue_supported": self._metric_supported(
                combined_text,
                metric_name="revenue",
            ),
            "customer_satisfaction_supported": self._metric_supported(
                combined_text,
                metric_name="customer satisfaction",
            ),
            "graph_context_available": bool(graph_context.strip()),
            "has_recommendations": "recommended business actions" in answer.lower(),
        }

        passed_checks = sum(1 for value in checks.values() if value)
        total_checks = len(checks)

        confidence_score = round(passed_checks / total_checks, 2)

        if confidence_score >= 0.85:
            risk_level = "low"
        elif confidence_score >= 0.6:
            risk_level = "medium"
        else:
            risk_level = "high"

        return {
            "checks": checks,
            "confidence_score": confidence_score,
            "risk_level": risk_level,
            "critic_summary": self._generate_summary(
                checks,
                confidence_score,
                risk_level
            ),
        }

    def _metric_supported(
        self,
        text: str,
        metric_name: str
    ) -> bool:

        if metric_name not in text:
            return False

        percentage_pattern = r"\d+%"

        return bool(re.search(percentage_pattern, text))

    def _generate_summary(
        self,
        checks: Dict[str, bool],
        confidence_score: float,
        risk_level: str
    ) -> str:

        failed_checks = [
            check for check, passed in checks.items()
            if not passed
        ]

        if not failed_checks:
            return (
                f"Answer passed all critic checks. "
                f"Confidence score: {confidence_score}. "
                f"Risk level: {risk_level}."
            )

        return (
            f"Answer failed checks: {failed_checks}. "
            f"Confidence score: {confidence_score}. "
            f"Risk level: {risk_level}."
        )


if __name__ == "__main__":

    critic = CriticAgent()

    sample_answer = """
    Revenue increased by 22%.
    Customer satisfaction reached 95%.

    Recommended Business Actions:
    Continue tracking business metrics.
    """

    sample_vector_context = """
    Revenue increased by 22%.
    Customer satisfaction reached 95%.
    """

    sample_graph_context = """
    BusinessMetric: revenue increased by 22%
    BusinessMetric: customer satisfaction reached 95%
    """

    result = critic.evaluate(
        answer=sample_answer,
        vector_context=sample_vector_context,
        graph_context=sample_graph_context,
    )

    print("\nCritic Agent Results")
    print("=" * 40)
    print(result)