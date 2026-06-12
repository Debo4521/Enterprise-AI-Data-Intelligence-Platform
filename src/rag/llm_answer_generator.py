from typing import Optional, List


class LLMAnswerGenerator:
    """
    Template-based answer generator.

    Later this can be replaced with OpenAI, Databricks Mosaic AI,
    or a local Llama model.
    """

    def generate_answer(
        self,
        query: str,
        vector_context: str,
        graph_context: str,
        model_name: Optional[str] = "template-v1",
    ) -> str:

        key_findings = self._extract_key_findings(vector_context)
        companies = self._extract_entity_values(vector_context, "companies")
        departments = self._extract_entity_values(vector_context, "departments")
        metrics = self._extract_entity_values(vector_context, "business_metrics")

        answer = f"""
Business Intelligence Answer

Question:
{query}

Key Findings:
{self._format_bullets(key_findings)}

Detected Business Entities:

Companies:
{self._format_bullets(companies)}

Departments:
{self._format_bullets(departments)}

Business Metrics:
{self._format_bullets(metrics)}

Graph-Based Evidence:
{graph_context}

Executive Summary:
The retrieved enterprise data shows positive business performance. Revenue and customer satisfaction improved, and department-level activities indicate active business expansion and AI-driven operational progress.

Recommended Business Actions:
1. Investigate which AI automation projects contributed most to business performance.
2. Compare customer satisfaction across future reporting periods.
3. Track international market expansion by the Marketing department.
4. Connect revenue growth with department-level initiatives in the knowledge graph.

Model Used:
{model_name}
"""
        return answer.strip()

    def _extract_key_findings(self, vector_context: str) -> List[str]:
        findings = []

        important_keywords = [
            "revenue",
            "customer satisfaction",
            "department",
            "automation",
            "international",
            "operating costs",
            "invest",
            "expanded",
            "launched",
            "increased",
            "decreased",
        ]

        for line in vector_context.splitlines():
            clean_line = line.strip()

            if not clean_line:
                continue

            if clean_line.lower().startswith("entities:"):
                continue

            if clean_line.lower().startswith("source chunk"):
                continue

            if clean_line.lower().startswith("text:"):
                clean_line = clean_line.replace("Text:", "").strip()

            if any(keyword in clean_line.lower() for keyword in important_keywords):
                findings.append(clean_line)

        return self._deduplicate(findings)[:8]

    def _extract_entity_values(self, vector_context: str, entity_key: str) -> List[str]:
        values = []

        for line in vector_context.splitlines():
            clean_line = line.strip()

            if not clean_line.startswith("Entities:"):
                continue

            try:
                entity_text = clean_line.replace("Entities:", "").strip()
                entity_dict = eval(entity_text)

                if entity_key in entity_dict:
                    values.extend(entity_dict[entity_key])

            except Exception:
                continue

        return self._deduplicate(values)

    def _format_bullets(self, items: List[str]) -> str:
        if not items:
            return "- No specific items detected."

        return "\n".join(f"- {item}" for item in items)

    def _deduplicate(self, items: List[str]) -> List[str]:
        seen = set()
        unique_items = []

        for item in items:
            normalized = item.lower().strip()

            if normalized not in seen:
                unique_items.append(item)
                seen.add(normalized)

        return unique_items