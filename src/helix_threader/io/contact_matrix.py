from __future__ import annotations

class ContactMatrix:
    def __init__(self, alphabet: list[str], values: dict[tuple[str, str], float]):
        self.alphabet = alphabet
        self._values = values

    def get(self, a: str, b: str) -> float:
        if (a, b) in self._values:
            return self._values[(a, b)]
        if (b, a) in self._values:
            return self._values[(b, a)]
        raise KeyError(f"Missing contact matrix entry for ({a},{b})")

def read_contact_matrix_tsv(path: str) -> ContactMatrix:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip() and not ln.strip().startswith("#")]
    if len(lines) < 2:
        raise ValueError(f"Contact matrix file too small: {path}")

    header = lines[0].split()
    alphabet = header  # assumes first row is like: A R N ...
    values: dict[tuple[str, str], float] = {}

    for row in lines[1:]:
        parts = row.split()
        if len(parts) != len(alphabet) + 1:
            raise ValueError(f"Row length mismatch in {path}: {row}")
        row_aa = parts[0]
        nums = parts[1:]
        for col_aa, v in zip(alphabet, nums):
            values[(row_aa, col_aa)] = float(v)

    return ContactMatrix(alphabet=alphabet, values=values)
