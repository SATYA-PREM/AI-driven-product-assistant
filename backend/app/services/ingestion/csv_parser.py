from __future__ import annotations

import csv
import io
from app.services.ingestion.file_parser import FileParser
from app.core.exceptions import FileProcessingError

class CSVParser(FileParser):
    """Parser for CSV files."""

    def parse(self, file_bytes: bytes) -> list[dict]:
        """Parse CSV bytes to list of dicts with robust encoding detection and key cleaning."""
        content = ""
        for enc in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
            try:
                content = file_bytes.decode(enc)
                break
            except UnicodeDecodeError:
                continue

        if not content and file_bytes:
            content = file_bytes.decode('utf-8', errors='replace')

        if not content.strip():
            return []

        sniffer = csv.Sniffer()
        try:
            dialect = sniffer.sniff(content[:4096])
        except csv.Error:
            dialect = csv.excel

        try:
            reader = csv.DictReader(io.StringIO(content), dialect=dialect)
            rows = []
            for row in reader:
                clean_row = {}
                for k, v in row.items():
                    if k is not None:
                        clean_k = str(k).lstrip("\ufeff\uffef").strip().strip("\"'").strip()
                        clean_row[clean_k] = v.strip() if isinstance(v, str) else v
                rows.append(clean_row)
            return rows
        except Exception as e:
            raise FileProcessingError(f"Failed to parse CSV: {str(e)}")

CSVParser.parse_csv = CSVParser.parse
CsvParser = CSVParser
csv_parser = CSVParser()
