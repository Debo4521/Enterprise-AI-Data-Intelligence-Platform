from pathlib import Path
from typing import Dict, Any

import pandas as pd
from pypdf import PdfReader
from docx import Document


class DocumentParser:

    def parse(self, file_path: str) -> Dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extension = path.suffix.lower()

        if extension == ".txt":
            content = self._parse_txt(path)
        elif extension == ".csv":
            content = self._parse_csv(path)
        elif extension == ".pdf":
            content = self._parse_pdf(path)
        elif extension == ".docx":
            content = self._parse_docx(path)
        elif extension in [".xlsx", ".xls"]:
            content = self._parse_excel(path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

        return {
            "file_name": path.name,
            "file_type": extension,
            "content": content,
            "content_length": len(content)
        }

    def _parse_txt(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def _parse_csv(self, path: Path) -> str:
        df = pd.read_csv(path)
        return df.to_string(index=False)

    def _parse_pdf(self, path: Path) -> str:
        reader = PdfReader(str(path))
        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text)

    def _parse_docx(self, path: Path) -> str:
        document = Document(str(path))
        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return "\n".join(paragraphs)

    def _parse_excel(self, path: Path) -> str:
        excel_file = pd.ExcelFile(path)
        sheets_text = []

        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(path, sheet_name=sheet_name)
            sheets_text.append(f"Sheet: {sheet_name}")
            sheets_text.append(df.to_string(index=False))

        return "\n\n".join(sheets_text)


if __name__ == "__main__":

    parser = DocumentParser()

    sample_file = "data/raw/company_notes.txt"

    parsed_document = parser.parse(sample_file)

    print("\nDocument Parsing Results")
    print("=" * 40)
    print(f"File Name: {parsed_document['file_name']}")
    print(f"File Type: {parsed_document['file_type']}")
    print(f"Content Length: {parsed_document['content_length']}")
    print("\nContent Preview:")
    print(parsed_document["content"][:500])