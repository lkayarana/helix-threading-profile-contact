from __future__ import annotations
from helix_threader.models.profile import Profile

def scan_profile(seq: str, profile: Profile) -> list[int]:
    N = len(seq)
    L = profile.length
    out: list[int] = []
    for start in range(0, N - L + 1):
        out.append(profile.score_window(seq, start))
    return out
