from __future__ import annotations
from helix_threader.models.problem import ThreadingProblem
from helix_threader.io.contact_table import ContactPair

def explain(problem: ThreadingProblem, starts: dict[int, int]) -> dict:
    seq = problem.sequence
    profiles = problem.profiles
    lengths = {hid: prof.length for hid, prof in profiles.items()}

    # helix windows
    windows = {}
    for hid in (1, 2, 3):
        st = starts[hid]
        windows[hid] = {
            "start_0based": st,
            "start_1based": st + 1,
            "end_1based": st + lengths[hid],
            "window": seq[st : st + lengths[hid]],
        }

    # loops
    loop12 = starts[2] - (starts[1] + lengths[1])
    loop23 = starts[3] - (starts[2] + lengths[2])

    # profile breakdown
    profile_breakdown = {}
    for hid in (1, 2, 3):
        prof = profiles[hid]
        st = starts[hid]
        contrib = []
        total = 0
        for k in range(prof.length):
            aa = seq[st + k]
            sc = prof.scores.get(aa, [-10_000] * prof.length)[k]
            total += sc
            contrib.append({"helix_pos": k + 1, "seq_index_1based": st + k + 1, "aa": aa, "score": sc})
        profile_breakdown[hid] = {"total": total, "contrib": contrib}

    # contact breakdown
    contact_rows = []
    contact_total = 0.0
    for c in problem.contacts:
        i = starts[c.hA] + (c.posA - 1)
        j = starts[c.hB] + (c.posB - 1)
        aaA = seq[i]
        aaB = seq[j]
        e = problem.contact_matrix.get(aaA, aaB)
        contact_total += e
        contact_rows.append({
            "hA": c.hA, "posA": c.posA, "seq_i_1based": i + 1, "aaA": aaA,
            "hB": c.hB, "posB": c.posB, "seq_j_1based": j + 1, "aaB": aaB,
            "energy": e
        })

    prof_total = sum(profile_breakdown[h]["total"] for h in (1, 2, 3))
    total = float(prof_total) + problem.lam * float(contact_total)

    return {
        "windows": windows,
        "loops": {"12": loop12, "23": loop23, "constraints": {"12": problem.loop12, "23": problem.loop23}},
        "profile": profile_breakdown,
        "contact": {"total": contact_total, "rows": contact_rows},
        "totals": {"profile_total": prof_total, "contact_total": contact_total, "lambda": problem.lam, "total": total},
    }
