from __future__ import annotations
from helix_threader.models.profile import Profile

def profile_score(seq: str, start: int, profile: Profile) -> int:
    return profile.score_window(seq, start)
