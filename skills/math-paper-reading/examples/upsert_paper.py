#!/usr/bin/env python3
import json
import sys
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "local_reference_db.json")

# 1. 读取现有数据库
try:
    with open(DB_PATH, "r", encoding="utf-8") as f:
        db = json.load(f)
except FileNotFoundError:
    db = {"total_entries": 0, "papers": [], "conflicts_detected": [], "overdue_review": []}
except json.JSONDecodeError as e:
    print(f"Error: Database file is corrupted. {e}", file=sys.stderr)
    sys.exit(1)

# 2. 从 stdin 安全读取输入
input_data = sys.stdin.read().strip()
if not input_data:
    print("Error: Empty input received from stdin", file=sys.stderr)
    sys.exit(1)

try:
    new_entry = json.loads(input_data)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input format. {e}", file=sys.stderr)
    sys.exit(1)

if "global_uri" not in new_entry:
    print("Error: 'global_uri' is strictly required in the input JSON", file=sys.stderr)
    sys.exit(1)

# 3. UPSERT 逻辑
existing = next((p for p in db["papers"] if p["global_uri"] == new_entry["global_uri"]), None)
if existing:
    old_status = existing.get("status", "")
    existing.update(new_entry)
    action = "~"
    print(f"~ {new_entry['global_uri']} status: {old_status} -> {new_entry.get('status', '状态未定义')}")
else:
    db["papers"].append(new_entry)
    db["total_entries"] += 1
    action = "+"
    print(f"+ {new_entry['global_uri']} ({new_entry.get('status', '状态未定义')})")

# 4. 安全写回
try:
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Error: Failed to write to database. {e}", file=sys.stderr)
    sys.exit(1)
