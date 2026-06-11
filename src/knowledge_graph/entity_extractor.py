import json
import re
from pathlib import Path
from typing import Dict, List, Any


class EntityExtractor:
    """
    Rule-based business entity extractor.

    This is our first version.
    Later we will upgrade it with LLM-based extraction.
    """

    def __init__(self):
        self.department_keywords = [
            "AI department",
            "sales department",
            "marketing department",
            "finance department",
            "engineering department",
            "HR department",
            "operations department",
        ]

        self.metric_patterns = [
            r"revenue increased by \d+%",
            r"revenue decreased by \d+%",
            r"customer satisfaction reached \d+%",
            r"sales increased by \d+%",
            r"sales decreased by \d+%",
            r"profit increased by \d+%",
            r"profit decreased by \d+%",
        ]

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        text_lower = text.lower()

        companies = self._extract_companies(text)
        departments = self._extract_departments(text_lower)
        business_metrics = self._extract_business_metrics(text_lower)

        return {
            "companies": companies,
            "departments": departments,
            "business_metrics": business_metrics,
        }

    def _extract_companies(self, text: str) -> List[str]:
        pattern = r"\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\s(?:Corporation|Corp|Inc|LLC|Ltd|Company)\b"
        matches = re.findall(pattern, text)
        return list(set(matches))

    def _extract_departments(self, text_lower: str) -> List[str]:
        departments = []

        for department in self.department_keywords:
            if department.lower() in text_lower:
                departments.append(department)

        return departments

    def _extract_business_metrics(self, text_lower: str) -> List[str]:
        metrics = []

        for pattern in self.metric_patterns:
            matches = re.findall(pattern, text_lower)
            metrics.extend(matches)

        return list(set(metrics))

    def extract_from_chunks(self, chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched_chunks = []

        for chunk in chunks:
            entities = self.extract_entities(chunk["text"])

            enriched_chunk = {
                **chunk,
                "entities": entities,
            }

            enriched_chunks.append(enriched_chunk)

        return enriched_chunks


if __name__ == "__main__":

    input_path = Path("data/processed/chunked_documents.json")
    output_path = Path("data/processed/enriched_chunks.json")

    if not input_path.exists():
        raise FileNotFoundError(
            "chunked_documents.json not found. Run text_chunker.py first."
        )

    with open(input_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    extractor = EntityExtractor()
    enriched_chunks = extractor.extract_from_chunks(chunks)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(enriched_chunks, file, indent=4, ensure_ascii=False)

    print("\nEntity Extraction Results")
    print("=" * 40)
    print(f"Total chunks processed: {len(chunks)}")
    print(f"Output saved to: {output_path}")

    if enriched_chunks:
        print("\nSample Enriched Chunk:")
        print(enriched_chunks[0])