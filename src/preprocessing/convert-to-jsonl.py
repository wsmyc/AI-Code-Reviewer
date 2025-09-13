import pandas as pd
import json
from pathlib import Path

# Input CSV (from Day 2)
csv_file = Path("../../data/first_200_codes.csv")
# Output JSONL
jsonl_file = Path("../../data/first_200_codes.jsonl")

def convert_csv_to_jsonl(csv_path: Path, jsonl_path: Path):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Only keep the relevant columns
    if not {"code", "docstring"}.issubset(df.columns):
        raise ValueError("CSV must contain 'code' and 'docstring' columns")

    # Write to JSONL
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            record = {
                "code": row["code"],
                "docstring": row["docstring"]
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ Converted {len(df)} rows → {jsonl_path}")

if __name__ == "__main__":
    convert_csv_to_jsonl(csv_file, jsonl_file)
