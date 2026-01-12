# Helix Threader (Profile + Contact Energy + Loop Constraints)

This repository implements a **threading** algorithm for placing **3 helices (H1, H2, H3)** onto a protein sequence.

Objective: find start positions (start1, start2, start3) that maximize:

- **Profile score** (PSSM/profile matrix built from helix MSAs)
- **Contact energy** (from a contact table + a contact energy matrix)
- Subject to **loop constraints** (min/max loop lengths between helices) and **no overlap**.

## Scoring

### Profile score
For helix h with length Lh and start position start_h (0-based):

\[
ProfileScore(h, start_h) = \sum_{k=1}^{L_h} P_h[ S[start_h + k - 1], k]
\]

### Contact energy
Given a contact table list of pairs:
(hA, posA) ↔ (hB, posB)

Map each (helix,pos) to an amino acid in the sequence:
aaA = S[start(hA) + posA - 1]
aaB = S[start(hB) + posB - 1]

Energy:
\[
ContactEnergy = \sum_{(A,B)\in contacts} C[aaA, aaB]
\]

### Total score
\[
Total = \sum_h ProfileScore(h, start_h) + \lambda \cdot ContactEnergy
\]

## Search strategy

1. **Scan** all possible starts for each helix to get profile scores.
2. **Fix** the helix with the strongest best profile hit.
3. **Search** the remaining helix starts under loop constraints.
4. Compute total score for each valid placement; return best.

(Optional) brute-force O(N^3) search exists for validation.

## Input formats

### Sequence (FASTA)
`data/example/sequence.fasta`

### Helix MSA (FASTA)
`data/example/helix1_msa.fasta`, `helix2_msa.fasta`, `helix3_msa.fasta`

All sequences must have the same length per MSA (the helix length).

### Contact table (TSV)
`data/example/contact_table.tsv`

Columns:
- hA, posA, hB, posB
Positions are **1-based within helix**. Helix ids are 1,2,3.

### Contact matrix (TSV)
`data/example/contact_matrix.tsv`

Header row and left column define the alphabet.
Matrix values are numeric.

### Loop constraints (JSON)
`data/example/loops.json`
Example:
```json
{
  "12": {"min": 2, "max": 20},
  "23": {"min": 2, "max": 25}
}
