from pathlib import Path
from typing import List, Dict, Any
import json

from file_loader import EnterpriseFileLoader
from metadata_extractor import MetadataExtractor
from document_parser import DocumentParser


class IngestionPipeline:

    def __init__(
        self,
        raw_data_path: str = "data/raw",
        output_path: str = "data/processed/ingested_documents.json"
    ):
        self.raw_data_path = raw_data_path
        self.output_path = Path(output_path)

        self.file_loader = EnterpriseFileLoader(raw_data_path=self.raw_data_path)
        self.metadata_extractor = MetadataExtractor()
        self.document_parser = DocumentParser()

    def run(self) -> List[Dict[str, Any]]:

        documents = self.file_loader.scan_files()
        ingested_documents = []

        print("\nStarting Enterprise Data Ingestion Pipeline")
        print("=" * 50)

        for document in documents:
            print(f"Processing: {document.file_name}")

            metadata = self.metadata_extractor.extract_metadata(document.file_path)
            parsed_content = self.document_parser.parse(document.file_path)

            ingested_document = {
                "document_id": document.document_id,
                "metadata": metadata,
                "content": parsed_content["content"],
                "content_length": parsed_content["content_length"],
                "status": "ingested"
            }

            ingested_documents.append(ingested_document)

        self._save_output(ingested_documents)

        print("=" * 50)
        print(f"Ingestion completed. Total documents: {len(ingested_documents)}")
        print(f"Output saved to: {self.output_path}")

        return ingested_documents

    def _save_output(self, documents: List[Dict[str, Any]]) -> None:

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as file:
            json.dump(documents, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":

    pipeline = IngestionPipeline()
    pipeline.run()