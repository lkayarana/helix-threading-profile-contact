from __future__ import annotations
from dataclasses import dataclass
from math import inf
from helix_threader.models.problem import ThreadingProblem
from helix_threader.search.scan_profiles import scan_profile
from helix_threader.scoring.total_score import total_score

@dataclass
class Solution:
    starts: dict[int, int]
    total: float
    profile_total: int
    contact_total: float
    fixed_helix: int

def choose_fixed_helix(profile_scans: dict[int, list[int]]) -> int:
    best = None
    best_h = None
    for hid, scan in profile_scans.items():
        m = max(scan)
        if best is None or m > best:
            best = m
            best_h = hid
    assert best_h is not None
    return best_h

def _valid_nonoverlap(starts: dict[int, int], lengths: dict[int, int]) -> bool:
    intervals = []
    for hid, st in starts.items():
        intervals.append((st, st + lengths[hid] - 1, hid))
    intervals.sort()
    for (a1, b1, _), (a2, b2, _) in zip(intervals, intervals[1:]):
        if a2 <= b1:
            return False
    return True

def search_fix_and_search(problem: ThreadingProblem) -> Solution:
    seq = problem.sequence
    profiles = problem.profiles
    lengths = {hid: prof.length for hid, prof in profiles.items()}

    scans = {hid: scan_profile(seq, prof) for hid, prof in profiles.items()}
    fixed = choose_fixed_helix(scans)

    N = len(seq)
    best_total = -inf
    best_starts: dict[int, int] | None = None
    best_prof = 0
    best_cont = 0.0

    # helper: iterate allowed windows for a helix
    def all_starts(hid: int):
        L = lengths[hid]
        return range(0, N - L + 1)

    # We'll enforce ordering H1 -> H2 -> H3 by loop constraints (typical threading).
    # If your problem allows different order, we can generalize later.
    min12, max12 = problem.loop12
    min23, max23 = problem.loop23

    # Try all placements for fixed helix, then constrained ranges for others.
    # We always maintain H1 < H2 < H3 order.
    for s1 in all_starts(1):
        # constrain s2 from loop12
        s2_min = s1 + lengths[1] + min12
        s2_max = s1 + lengths[1] + max12
        for s2 in range(max(0, s2_min), min(N - lengths[2] + 1, s2_max + 1)):
            # constrain s3 from loop23
            s3_min = s2 + lengths[2] + min23
            s3_max = s2 + lengths[2] + max23
            for s3 in range(max(0, s3_min), min(N - lengths[3] + 1, s3_max + 1)):
                starts = {1: s1, 2: s2, 3: s3}
                if not _valid_nonoverlap(starts, lengths):
                    continue
                total, prof_total, cont_total = total_score(problem, starts)
                if total > best_total:
                    best_total = total
                    best_starts = dict(starts)
                    best_prof = prof_total
                    best_cont = cont_total

    if best_starts is None:
        raise RuntimeError("No valid placement found under loop constraints.")

    return Solution(
        starts=best_starts,
        total=best_total,
        profile_total=best_prof,
        contact_total=best_cont,
        fixed_helix=fixed,
    )
