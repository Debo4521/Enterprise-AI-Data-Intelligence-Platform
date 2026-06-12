import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class SemanticSearchEngine:

    def __init__(
        self,
        index_path: str = "data/processed/faiss_index.bin",
        chunks_path: str = "data/processed/embedded_chunks.json",
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):
        self.index_path = Path(index_path)
        self.chunks_path = Path(chunks_path)
        self.model_name = model_name

        if not self.index_path.exists():
            raise FileNotFoundError("FAISS index not found. Run faiss_index.py first.")

        if not self.chunks_path.exists():
            raise FileNotFoundError(
                "embedded_chunks.json not found. Run embedding_generator.py first."
            )

        self.index = faiss.read_index(str(self.index_path))

        with open(self.chunks_path, "r", encoding="utf-8") as file:
            self.chunks = json.load(file)

        self.model = SentenceTransformer(self.model_name)

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        filename_filter = self._extract_filename_from_query(query)

        if filename_filter:
            return self._search_by_filename(filename_filter, top_k)

        return self._semantic_search(query, top_k)

    def _semantic_search(self, query: str, top_k: int) -> List[Dict[str, Any]]:
        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        query_vector = np.array([query_embedding], dtype=np.float32)

        scores, indices = self.index.search(query_vector, top_k)

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append(
                {
                    "score": float(score),
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "entities": chunk.get("entities", {}),
                }
            )

        return results

    def _search_by_filename(
        self,
        filename: str,
        top_k: int
    ) -> List[Dict[str, Any]]:

        results = []

        for chunk in self.chunks:
            file_name = chunk["metadata"].get("file_name", "").lower()

            if filename.lower() in file_name:
                results.append(
                    {
                        "score": 1.0,
                        "chunk_id": chunk["chunk_id"],
                        "document_id": chunk["document_id"],
                        "text": chunk["text"],
                        "metadata": chunk["metadata"],
                        "entities": chunk.get("entities", {}),
                    }
                )

        return results[:top_k]

    def _extract_filename_from_query(self, query: str) -> Optional[str]:
        match = re.search(
            r"[\w\-]+\.(txt|csv|pdf|docx|xlsx|xls)",
            query.lower()
        )

        if match:
            return match.group(0)

        return None


if __name__ == "__main__":

    search_engine = SemanticSearchEngine()

    query = "What happened in quarterly_report.txt?"

    results = search_engine.search(query, top_k=2)

    print("\nSemantic Search Results")
    print("=" * 40)
    print(f"Query: {query}")

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("-" * 30)
        print(f"Score: {result['score']:.4f}")
        print(f"File Name: {result['metadata'].get('file_name')}")
        print(f"Chunk ID: {result['chunk_id']}")
        print(f"Text: {result['text']}")
        print(f"Entities: {result['entities']}")