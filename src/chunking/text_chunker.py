import json
from pathlib import Path
from typing import List, Dict, Any


class TextChunker:

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

    def chunk_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += self.chunk_size - self.chunk_overlap

        return chunks

    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        chunked_documents = []

        for document in documents:
            document_id = document["document_id"]
            content = document["content"]

            chunks = self.chunk_text(content)

            for index, chunk in enumerate(chunks):
                chunked_documents.append(
                    {
                        "chunk_id": f"{document_id}_chunk_{index + 1:04d}",
                        "document_id": document_id,
                        "chunk_index": index + 1,
                        "text": chunk,
                        "metadata": document["metadata"],
                    }
                )

        return chunked_documents


if __name__ == "__main__":

    input_path = Path("data/processed/ingested_documents.json")
    output_path = Path("data/processed/chunked_documents.json")

    if not input_path.exists():
        raise FileNotFoundError(
            "ingested_documents.json not found. Run ingestion_pipeline.py first."
        )

    with open(input_path, "r", encoding="utf-8") as file:
        documents = json.load(file)

    chunker = TextChunker(chunk_size=300, chunk_overlap=50)
    chunks = chunker.chunk_documents(documents)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, indent=4, ensure_ascii=False)

    print("\nText Chunking Results")
    print("=" * 40)
    print(f"Total documents: {len(documents)}")
    print(f"Total chunks created: {len(chunks)}")
    print(f"Output saved to: {output_path}")

    if chunks:
        print("\nSample Chunk:")
        print(chunks[0])