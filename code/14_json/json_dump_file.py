# json_dump_file.py - write a JSON summary file
import json
from pathlib import Path

with open("data/json/loans.json", encoding="utf-8") as f:
    loans = json.load(f)

defaults = [x for x in loans if x["status"] == "Default"]
summary = {
    "report": "defaulted loans",
    "as_of": "2025-12-31",
    "count": len(defaults),
    "loan_ids": [x["loan_id"] for x in defaults[:5]],
}

Path("output").mkdir(exist_ok=True)
with open("output/defaults_summary.json", "w",
          encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print(Path("output/defaults_summary.json").read_text())
