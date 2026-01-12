from __future__ import annotations
from dataclasses import dataclass
from helix_threader.io.contact_table import ContactPair
from helix_threader.io.contact_matrix import ContactMatrix

@dataclass
class Contacts:
    pairs: list[ContactPair]
    matrix: ContactMatrix

def validate_contacts(contacts: list[ContactPair], helix_lengths: dict[int, int]) -> None:
    for c in contacts:
        if c.hA not in helix_lengths or c.hB not in helix_lengths:
            raise ValueError(f"Unknown helix id in contact: {c}")
        if not (1 <= c.posA <= helix_lengths[c.hA]):
            raise ValueError(f"Contact posA out of range: {c}")
        if not (1 <= c.posB <= helix_lengths[c.hB]):
            raise ValueError(f"Contact posB out of range: {c}")
