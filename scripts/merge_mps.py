#!/usr/bin/env python3
"""Merge NEW_MPS from scripts/enrich_all.py into scripts/generate_datasets.py,
ensuring all 47 counties are represented, no 'Hon.' prefix, and no phone numbers.
"""
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GEN_SCRIPT = ROOT / "scripts" / "generate_datasets.py"
ENRICH_SCRIPT = ROOT / "scripts" / "enrich_all.py"

# Import NEW_MPS from enrich_all.py
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from enrich_all import NEW_MPS

# Read generate_datasets.py
content = GEN_SCRIPT.read_text(encoding="utf-8")

# Parse existing MPS
import generate_datasets
existing_mps = generate_datasets.MPS

existing_ids = {m["id"] for m in existing_mps}
merged = list(existing_mps)

added = 0
for m in NEW_MPS:
    if m["id"] not in existing_ids:
        # Sanitize name and notes just in case
        m["name"] = m["name"].replace("Hon. ", "").replace("Hon ", "").strip()
        m["notes"] = m["notes"].replace("Hon. ", "").replace("Hon ", "").strip()
        m.pop("phone", None)
        m.pop("whatsapp", None)
        merged.append(m)
        existing_ids.add(m["id"])
        added += 1

# Check county coverage
counties = sorted(list(set(m["county"] for m in merged if m.get("county"))))
print(f"Total MPs after merge: {len(merged)} (Added {added})")
print(f"Counties covered: {len(counties)}/47 counties")

# Re-serialize MPS array in generate_datasets.py
mps_json = json.dumps(merged, indent=2, ensure_ascii=False)

# Replace MPS = [ ... ] in generate_datasets.py
pattern = re.compile(r"MPS = \[.*?\]\n\n# ====", re.DOTALL)
replacement = f"MPS = {mps_json}\n\n# ===="

new_content = pattern.sub(replacement, content)
GEN_SCRIPT.write_text(new_content, encoding="utf-8")
print(f"Updated scripts/generate_datasets.py with {len(merged)} MPs.")
