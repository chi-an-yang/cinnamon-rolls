from __future__ import annotations
import csv
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_CSV = REPO_ROOT / "google-2025-12-12.csv"
OUTPUT_JSON = REPO_ROOT / "docs" / "data" / "rolls.json"


def load_rows() -> list[dict]:
    with SOURCE_CSV.open(encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)
        rows = []
        for idx, row in enumerate(reader, start=1):
            padded_row = row + [""] * (len(headers) - len(row))
            record = {header: value for header, value in zip(headers, padded_row)}
            record_id = idx
            title = record.get(headers[1], "").strip()
            record["_id"] = record_id
            record["_title"] = title or f"肉桂捲 #{record_id}"
            rows.append(record)
    return headers, rows


def save_json(headers: list[str], rows: list[dict]) -> None:
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"headers": headers, "rows": rows}
    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    headers, rows = load_rows()
    save_json(headers, rows)


if __name__ == "__main__":
    main()
