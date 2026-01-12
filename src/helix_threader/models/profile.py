from __future__ import annotations
from dataclasses import dataclass
import math
from collections import Counter

@dataclass
class Profile:
    name: str
    length: int
    alphabet: list[str]
    # scores[aa][pos] -> int
    scores: dict[str, list[int]]

    def score_window(self, seq: str, start: int) -> int:
        if start < 0 or start + self.length > len(seq):
            raise ValueError("Window out of bounds")
        total = 0
        for k in range(self.length):
            aa = seq[start + k]
            if aa not in self.scores:
                # unknown symbol: heavy penalty
                total += -10_000
            else:
                total += self.scores[aa][k]
        return total

def build_pssm_from_msa(
    msa: list[str],
    alphabet: list[str],
    name: str,
    pseudocount: float = 1.0,
    background: dict[str, float] | None = None,
    scale: float = 10.0,
) -> Profile:
    """
    Build a log-odds PSSM from an MSA:
      score(aa,pos) = round(scale * log2( P(aa|pos) / bg(aa) ))

    - msa: list of equal-length strings
    - alphabet: list of allowed symbols
    """
    if not msa:
        raise ValueError("Empty MSA")
    L = len(msa[0])
    for s in msa:
        if len(s) != L:
            raise ValueError("All MSA sequences must have the same length")

    # background default: uniform over alphabet
    if background is None:
        background = {aa: 1.0 / len(alphabet) for aa in alphabet}

    # initialize scores
    scores: dict[str, list[int]] = {aa: [0] * L for aa in alphabet}

    # column-wise counts
    for pos in range(L):
        col = [s[pos] for s in msa]
        counts = Counter(col)

        denom = 0.0
        for aa in alphabet:
            denom += counts.get(aa, 0) + pseudocount

        for aa in alphabet:
            p = (counts.get(aa, 0) + pseudocount) / denom
            bg = background.get(aa, 1e-12)
            val = math.log2(p / bg)
            scores[aa][pos] = int(round(scale * val))

    return Profile(name=name, length=L, alphabet=alphabet, scores=scores)
