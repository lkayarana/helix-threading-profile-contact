from __future__ import annotations
import json
import os

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def write_json(path: str, obj: dict) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def write_contact_tsv(path: str, rows: list[dict]) -> None:
    cols = ["hA","posA","seq_i_1based","aaA","hB","posB","seq_j_1based","aaB","energy"]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")

def write_report_md(path: str, explained: dict) -> None:
    w = explained["windows"]
    loops = explained["loops"]
    totals = explained["totals"]
    prof = explained["profile"]
    contact = explained["contact"]

    lines = []
    lines.append("# Helix Threading Report\n")
    lines.append("## Best placement\n")
    for hid in (1,2,3):
        lines.append(f"- **H{hid}**: start={w[hid]['start_1based']}, end={w[hid]['end_1based']}, window=`{w[hid]['window']}`")
    lines.append("")
    lines.append("## Loop lengths\n")
    lines.append(f"- loop12 = {loops['12']} (constraint {loops['constraints']['12']})")
    lines.append(f"- loop23 = {loops['23']} (constraint {loops['constraints']['23']})")
    lines.append("")
    lines.append("## Totals\n")
    lines.append(f"- Profile total: **{totals['profile_total']}**")
    lines.append(f"- Contact total: **{totals['contact_total']}**")
    lines.append(f"- Lambda: **{totals['lambda']}**")
    lines.append(f"- TOTAL: **{totals['total']}**")
    lines.append("")
    lines.append("## Profile breakdown\n")
    for hid in (1,2,3):
        lines.append(f"### H{hid} (total={prof[hid]['total']})")
        lines.append("| HelixPos | SeqIndex(1-based) | AA | Score |")
        lines.append("|---:|---:|:--:|---:|")
        for r in prof[hid]["contrib"]:
            lines.append(f"| {r['helix_pos']} | {r['seq_index_1based']} | {r['aa']} | {r['score']} |")
        lines.append("")
    lines.append("## Contact breakdown\n")
    lines.append(f"Total contact energy = **{contact['total']}**\n")
    lines.append("| hA | posA | i | aaA | hB | posB | j | aaB | energy |")
    lines.append("|---:|---:|---:|:--:|---:|---:|---:|:--:|---:|")
    for r in contact["rows"]:
        lines.append(f"| {r['hA']} | {r['posA']} | {r['seq_i_1based']} | {r['aaA']} | {r['hB']} | {r['posB']} | {r['seq_j_1based']} | {r['aaB']} | {r['energy']} |")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
