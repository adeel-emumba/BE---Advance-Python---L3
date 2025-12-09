"""
Utility functions for loading URLs from JSON or CSV files.
"""

import json
import csv
from pathlib import Path
from typing import List


def load_urls(path: Path) -> List[str]:
    """Load URLs from a JSON or CSV file.

    JSON format example:
        ["https://example.com", "https://google.com"]

    CSV format example:
        url
        https://example.com
        https://google.com

    Time Complexity: O(n) where n is the number of URLs in the file.
    - JSON: O(n) for parsing and converting to list
    - CSV: O(n) for reading each row
    Space Complexity: O(n) to store all URLs in memory
    """
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")

    if path.suffix.lower() == ".json":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON file must contain a list of URLs.")
            return [str(item) for item in data]

    elif path.suffix.lower() == ".csv":
        urls: List[str] = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            if "url" not in fieldnames:
                raise ValueError("CSV must contain a 'url' column.")
            for row in reader:
                urls.append(str(row["url"]))
        return urls

    else:
        raise ValueError("Unsupported file format. Use JSON or CSV.")
