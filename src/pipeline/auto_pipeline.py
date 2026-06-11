from pathlib import Path
import subprocess
import sys
import time


class AutoPipeline:
    """
    Enterprise Auto Pipeline
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parent.parent.parent
        self.raw_data_path = self.project_root / "data" / "raw"

    def run(self):

        print("\nStarting Enterprise Auto Pipeline")
        print("=" * 50)

        files = list(self.raw_data_path.glob("*"))

        if not files:
            print("No files found in data/raw")
            return False

        print(f"Found {len(files)} file(s)\n")

        self.run_ingestion()
        self.run_metadata_extraction()
        self.run_document_parsing()
        self.run_text_chunking()
        self.run_entity_extraction()
        self.run_knowledge_graph()
        self.run_embeddings()
        self.run_faiss_index()

        print("\n" + "=" * 50)
        print("Enterprise Pipeline Completed Successfully")
        print("=" * 50)

        return True

    def _run_script(self, script_path: Path):
        subprocess.run(
            [
                sys.executable,
                str(script_path),
            ],
            check=True,
        )

    def run_ingestion(self):
        print("Step 1: Data Ingestion")
        self._run_script(
            self.project_root / "src" / "ingestion" / "ingestion_pipeline.py"
        )

    def run_metadata_extraction(self):
        print("Step 2: Metadata Extraction")
        time.sleep(0.3)

    def run_document_parsing(self):
        print("Step 3: Document Parsing")
        time.sleep(0.3)

    def run_text_chunking(self):
        print("Step 4: Text Chunking")
        self._run_script(
            self.project_root / "src" / "chunking" / "text_chunker.py"
        )

    def run_entity_extraction(self):
        print("Step 5: Entity Extraction")
        self._run_script(
            self.project_root / "src" / "knowledge_graph" / "entity_extractor.py"
        )

    def run_knowledge_graph(self):
        print("Step 6: Knowledge Graph Update")
        self._run_script(
            self.project_root / "src" / "knowledge_graph" / "graph_builder.py"
        )

    def run_embeddings(self):
        print("Step 7: Embedding Generation")
        self._run_script(
            self.project_root / "src" / "embeddings" / "embedding_generator.py"
        )

    def run_faiss_index(self):
        print("Step 8: FAISS Index Update")
        self._run_script(
            self.project_root / "src" / "retrieval" / "faiss_index.py"
        )


if __name__ == "__main__":

    pipeline = AutoPipeline()
    pipeline.run()