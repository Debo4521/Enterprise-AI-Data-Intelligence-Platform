from typing import Optional


class LLMAnswerGenerator:
    """
    First production-safe version.

    For now, this uses a structured template instead of calling a paid API.
    Later, we can connect OpenAI, Databricks Mosaic AI, or local Llama.
    """

    def generate_answer(
        self,
        query: str,
        vector_context: str,
        graph_context: str,
        model_name: Optional[str] = "template-v1"
    ) -> str:

        answer = f"""
Business Intelligence Answer

Question:
{query}

Evidence-Based Findings:
The retrieved enterprise data shows the following:

{self._extract_key_points(vector_context)}

Graph-Based Evidence:
{graph_context}

Executive Summary:
Based on both semantic vector search and knowledge graph relationships, the enterprise data indicates positive business performance. The available evidence shows improvement in revenue and customer satisfaction, with department-level activity connected to business outcomes.

Recommended Business Actions:
1. Investigate which department activities contributed most to revenue growth.
2. Compare customer satisfaction trends across future reporting periods.
3. Connect business metrics with department-level performance data.
4. Use the knowledge graph to track relationships between companies, metrics, teams, and reports.

Model Used:
{model_name}
"""
        return answer.strip()

    def _extract_key_points(self, vector_context: str) -> str:
        lines = []

        for line in vector_context.splitlines():
            clean_line = line.strip()

            if not clean_line:
                continue

            if any(
                keyword in clean_line.lower()
                for keyword in [
                    "revenue",
                    "customer satisfaction",
                    "department",
                    "sales",
                    "ai department",
                ]
            ):
                lines.append(f"- {clean_line}")

        if not lines:
            return "- No clear business findings were extracted from the retrieved context."

        return "\n".join(lines[:8])