from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class MetadataExtractor:

    def extract_metadata(self, file_path: str) -> Dict[str, Any]:

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_stats = path.stat()

        metadata = {
            "file_name": path.name,
            "file_extension": path.suffix.lower(),
            "file_size_kb": round(file_stats.st_size / 1024, 2),
            "created_time": datetime.fromtimestamp(
                file_stats.st_ctime
            ).isoformat(),
            "modified_time": datetime.fromtimestamp(
                file_stats.st_mtime
            ).isoformat(),
            "absolute_path": str(path.resolve())
        }

        return metadata


if __name__ == "__main__":

    extractor = MetadataExtractor()

    sample_file = "data/raw/company_notes.txt"

    metadata = extractor.extract_metadata(sample_file)

    print("\nMetadata Extraction Results")
    print("=" * 40)
    print(metadata)