from pathlib import Path
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel, Field


class DocumentMetadata(BaseModel):
    document_id: str
    file_name: str
    file_type: str
    file_path: str
    file_size_kb: float
    created_at: str
    status: str = Field(default="loaded")


class EnterpriseFileLoader:
    SUPPORTED_EXTENSIONS = {
        ".pdf": "pdf",
        ".docx": "docx",
        ".csv": "csv",
        ".xlsx": "excel",
        ".xls": "excel",
        ".json": "json",
        ".txt": "text",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
    }

    def __init__(self, raw_data_path: str = "data/raw"):
        self.raw_data_path = Path(raw_data_path)

        if not self.raw_data_path.exists():
            raise FileNotFoundError(f"Raw data folder not found: {self.raw_data_path}")

    def scan_files(self) -> List[DocumentMetadata]:
        documents = []

        for index, file_path in enumerate(self.raw_data_path.rglob("*"), start=1):
            if file_path.is_file():
                extension = file_path.suffix.lower()

                if extension in self.SUPPORTED_EXTENSIONS:
                    document = DocumentMetadata(
                        document_id=f"doc_{index:04d}",
                        file_name=file_path.name,
                        file_type=self.SUPPORTED_EXTENSIONS[extension],
                        file_path=str(file_path),
                        file_size_kb=round(file_path.stat().st_size / 1024, 2),
                        created_at=datetime.now().isoformat(),
                        status="loaded",
                    )
                    documents.append(document)

        return documents

    def to_dict(self, documents: List[DocumentMetadata]) -> List[Dict]:
        return [doc.model_dump() for doc in documents]


if __name__ == "__main__":
    loader = EnterpriseFileLoader()
    documents = loader.scan_files()

    print("\nEnterprise File Loader Results")
    print("=" * 40)

    if not documents:
        print("No supported files found in data/raw.")
    else:
        for doc in documents:
            print(doc.model_dump())