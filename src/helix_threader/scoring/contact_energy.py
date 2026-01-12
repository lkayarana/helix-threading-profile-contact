from __future__ import annotations
from helix_threader.io.contact_table import ContactPair
from helix_threader.io.contact_matrix import ContactMatrix

def contact_energy(
    seq: str,
    starts: dict[int, int],               # helix_id -> start (0-based in sequence)
    helix_lengths: dict[int, int],        # helix_id -> L
    contacts: list[ContactPair],
    C: ContactMatrix,
) -> float:
    e = 0.0
    for c in contacts:
        sA = starts[c.hA]
        sB = starts[c.hB]
        # 1-based helix position -> 0-based offset
        i = sA + (c.posA - 1)
        j = sB + (c.posB - 1)
        aaA = seq[i]
        aaB = seq[j]
        e += C.get(aaA, aaB)
    return e
