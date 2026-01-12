from __future__ import annotations
import json

def read_loops_json(path: str) -> dict[str, dict[str, int]]:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    for key in ("12", "23"):
        if key not in obj or "min" not in obj[key] or "max" not in obj[key]:
            raise ValueError(f"loops.json must contain {key}.min and {key}.max")
    return obj
