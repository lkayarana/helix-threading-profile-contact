from __future__ import annotations

def read_fasta(path: str) -> list[tuple[str, str]]:
    records: list[tuple[str, str]] = []
    header = None
    seq_parts: list[str] = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if header is not None:
                    records.append((header, "".join(seq_parts)))
                header = line[1:].strip()
                seq_parts = []
            else:
                seq_parts.append(line)
        if header is not None:
            records.append((header, "".join(seq_parts)))

    if not records:
        raise ValueError(f"No FASTA records found in {path}")
    return records

def read_single_fasta_sequence(path: str) -> str:
    recs = read_fasta(path)
    if len(recs) != 1:
        raise ValueError(f"Expected 1 FASTA record in {path}, found {len(recs)}")
    return recs[0][1]

def read_fasta_sequences(path: str) -> list[str]:
    return [seq for _, seq in read_fasta(path)]
