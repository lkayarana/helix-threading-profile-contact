from __future__ import annotations
from dataclasses import dataclass
from helix_threader.models.profile import Profile
from helix_threader.io.contact_table import ContactPair
from helix_threader.io.contact_matrix import ContactMatrix

@dataclass
class ThreadingProblem:
    sequence: str
    profiles: dict[int, Profile]           # helix_id -> Profile
    contacts: list[ContactPair]            # contact table
    contact_matrix: ContactMatrix
    loop12: tuple[int, int]                # (min,max)
    loop23: tuple[int, int]                # (min,max)
    lam: float = 1.0
