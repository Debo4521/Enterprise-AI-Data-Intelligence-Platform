import json
import re
from pathlib import Path
from typing import Dict, Any, List


class ComparisonEngine:

    def __init__(
        self,
        chunks_path: str = "data/processed/enriched_chunks.json"
    ):
        self.chunks_path = Path(chunks_path)

        if not self.chunks_path.exists():
            raise FileNotFoundError("enriched_chunks.json not found.")

        with open(self.chunks_path, "r", encoding="utf-8") as file:
            self.chunks = json.load(file)

    def compare_files(self, file_a: str, file_b: str) -> Dict[str, Any]:
        data_a = self._extract_file_summary(file_a)
        data_b = self._extract_file_summary(file_b)

        return {
            "file_a": file_a,
            "file_b": file_b,
            "summary_a": data_a,
            "summary_b": data_b,
            "comparison": self._build_comparison(data_a, data_b),
        }

    def _extract_file_summary(self, file_name: str) -> Dict[str, Any]:
        matched_chunks = [
            chunk for chunk in self.chunks
            if chunk["metadata"].get("file_name", "").lower() == file_name.lower()
        ]

        full_text = "\n".join(chunk["text"] for chunk in matched_chunks)

        return {
            "file_name": file_name,
            "revenue": self._find_metric(full_text, "revenue"),
            "customer_satisfaction": self._find_metric(full_text, "customer satisfaction"),
            "ai_projects": self._find_ai_projects(full_text),
            "markets": self._find_market_expansion(full_text),
            "raw_text": full_text,
        }

    def _find_metric(self, text: str, metric_name: str) -> str:
        pattern = rf"{metric_name}[^.]*\."
        match = re.search(pattern, text, flags=re.IGNORECASE)

        if match:
            return match.group(0)

        return "Not found"

    def _find_ai_projects(self, text: str) -> str:
        patterns = [
            r"AI department[^.]*projects[^.]*\.",
            r"AI department[^.]*automation[^.]*\.",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(0)

        return "Not found"

    def _find_market_expansion(self, text: str) -> str:
        patterns = [
            r"sales department[^.]*regions[^.]*\.",
            r"marketing department[^.]*markets[^.]*\.",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(0)

        return "Not found"

    def _build_comparison(
        self,
        data_a: Dict[str, Any],
        data_b: Dict[str, Any]
    ) -> List[Dict[str, str]]:

        return [
            {
                "metric": "Revenue",
                data_a["file_name"]: data_a["revenue"],
                data_b["file_name"]: data_b["revenue"],
            },
            {
                "metric": "Customer Satisfaction",
                data_a["file_name"]: data_a["customer_satisfaction"],
                data_b["file_name"]: data_b["customer_satisfaction"],
            },
            {
                "metric": "AI Projects",
                data_a["file_name"]: data_a["ai_projects"],
                data_b["file_name"]: data_b["ai_projects"],
            },
            {
                "metric": "Market Expansion",
                data_a["file_name"]: data_a["markets"],
                data_b["file_name"]: data_b["markets"],
            },
        ]


if __name__ == "__main__":

    engine = ComparisonEngine()

    result = engine.compare_files(
        "company_notes.txt",
        "quarterly_report.txt",
    )

    print("\nMulti-Document Comparison Results")
    print("=" * 50)

    for row in result["comparison"]:
        print(row)