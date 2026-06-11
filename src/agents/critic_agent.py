from typing import Dict, Any, List


class CriticAgent:

    def evaluate(
        self,
        answer: str,
        vector_context: str,
        graph_context: str
    ) -> Dict[str, Any]:

        checks = {
            "revenue_supported": self._contains_evidence(
                answer,
                vector_context,
                ["revenue", "15"]
            ),
            "customer_satisfaction_supported": self._contains_evidence(
                answer,
                vector_context,
                ["customer satisfaction", "92"]
            ),
            "graph_context_used": bool(graph_context.strip()),
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
            "critic_summary": self._generate_summary(checks, confidence_score, risk_level),
        }

    def _contains_evidence(
        self,
        answer: str,
        context: str,
        required_terms: List[str]
    ) -> bool:

        combined_text = f"{answer} {context}".lower()

        return all(term.lower() in combined_text for term in required_terms)

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
    Revenue increased by 15%.
    Customer satisfaction reached 92%.
    Recommended Business Actions:
    Continue tracking customer satisfaction.
    """

    sample_vector_context = """
    Revenue increased by 15%.
    Customer satisfaction reached 92%.
    """

    sample_graph_context = """
    BusinessMetric: revenue increased by 15%
    BusinessMetric: customer satisfaction reached 92%
    """

    result = critic.evaluate(
        answer=sample_answer,
        vector_context=sample_vector_context,
        graph_context=sample_graph_context,
    )

    print("\nCritic Agent Results")
    print("=" * 40)
    print(result)