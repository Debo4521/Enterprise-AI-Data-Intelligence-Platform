import json
from pathlib import Path

import faiss
import numpy as np


class FaissIndexBuilder:

    def __init__(self):
        self.index = None

    def build_index(self, embedded_chunks):

        embeddings = np.array(
            [chunk["embedding"] for chunk in embedded_chunks],
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        return self.index

    def save_index(self, output_path):

        faiss.write_index(self.index, str(output_path))


if __name__ == "__main__":

    input_path = Path("data/processed/embedded_chunks.json")
    output_path = Path("data/processed/faiss_index.bin")

    if not input_path.exists():
        raise FileNotFoundError(
            "embedded_chunks.json not found."
        )

    with open(input_path, "r", encoding="utf-8") as file:
        embedded_chunks = json.load(file)

    builder = FaissIndexBuilder()

    index = builder.build_index(embedded_chunks)

    builder.save_index(output_path)

    print("\nFAISS Index Builder Results")
    print("=" * 40)
    print(f"Vectors indexed: {index.ntotal}")
    print(f"Vector dimension: {index.d}")
    print(f"Output saved to: {output_path}")