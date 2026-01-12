from __future__ import annotations
from dataclasses import dataclass
from math import inf
from helix_threader.models.problem import ThreadingProblem
from helix_threader.scoring.total_score import total_score

@dataclass
class SolutionBF:
    starts: dict[int, int]
    total: float
    profile_total: int
    contact_total: float

def brute_force_search(problem: ThreadingProblem) -> SolutionBF:
    seq = problem.sequence
    profiles = problem.profiles
    lengths = {hid: prof.length for hid, prof in profiles.items()}
    N = len(seq)
    min12, max12 = problem.loop12
    min23, max23 = problem.loop23

    best_total = -inf
    best = None

    for s1 in range(0, N - lengths[1] + 1):
        for s2 in range(0, N - lengths[2] + 1):
            # order + loop constraint
            loop12 = s2 - (s1 + lengths[1])
            if loop12 < min12 or loop12 > max12:
                continue
            for s3 in range(0, N - lengths[3] + 1):
                loop23 = s3 - (s2 + lengths[2])
                if loop23 < min23 or loop23 > max23:
                    continue
                # enforce ordering and no overlap
                if not (s1 + lengths[1] <= s2 and s2 + lengths[2] <= s3):
                    continue

                starts = {1: s1, 2: s2, 3: s3}
                total, prof_total, cont_total = total_score(problem, starts)
                if total > best_total:
                    best_total = total
                    best = (dict(starts), total, prof_total, cont_total)

    if best is None:
        raise RuntimeError("No valid placement found (brute force).")

    starts, total, prof_total, cont_total = best
    return SolutionBF(starts=starts, total=total, profile_total=prof_total, contact_total=cont_total)
