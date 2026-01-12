from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ContactPair:
    hA: int
    posA: int  # 1-based within helix
    hB: int
    posB: int  # 1-based within helix

def read_contact_table_tsv(path: str) -> list[ContactPair]:
    contacts: list[ContactPair] = []
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()
        if not header:
            raise ValueError(f"Empty contact table: {path}")
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split()
            if len(parts) != 4:
                raise ValueError(f"Bad contact row (need 4 columns): {line}")
            hA, posA, hB, posB = map(int, parts)
            contacts.append(ContactPair(hA, posA, hB, posB))
    if not contacts:
        raise ValueError(f"No contacts parsed from: {path}")
    return contacts
