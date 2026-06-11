import json
from pathlib import Path
from typing import List, Dict, Any

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        print(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        print("Embedding model loaded successfully.")

    def generate_embedding(self, text: str) -> List[float]:
        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )
        return embedding.tolist()

    def generate_embeddings_for_chunks(
        self,
        chunks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:

        embedded_chunks = []

        for chunk in chunks:
            embedding = self.generate_embedding(chunk["text"])

            embedded_chunks.append(
                {
                    "chunk_id": chunk["chunk_id"],
                    "document_id": chunk["document_id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                    "entities": chunk.get("entities", {}),
                    "embedding_model": self.model_name,
                    "embedding_dimension": len(embedding),
                    "embedding": embedding,
                }
            )

        return embedded_chunks


if __name__ == "__main__":

    input_path = Path("data/processed/enriched_chunks.json")
    output_path = Path("data/processed/embedded_chunks.json")

    if not input_path.exists():
        raise FileNotFoundError(
            "enriched_chunks.json not found. Run entity_extractor.py first."
        )

    with open(input_path, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    generator = EmbeddingGenerator()
    embedded_chunks = generator.generate_embeddings_for_chunks(chunks)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(embedded_chunks, file, indent=4, ensure_ascii=False)

    print("\nEmbedding Generator Results")
    print("=" * 40)
    print(f"Total chunks embedded: {len(embedded_chunks)}")
    print(f"Embedding model: {generator.model_name}")

    if embedded_chunks:
        print(f"Embedding dimension: {embedded_chunks[0]['embedding_dimension']}")

    print(f"Output saved to: {output_path}")