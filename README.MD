# Helix Threader — Profile (PSSM) + Contact Energy + Loop Constraints

This project implements a **protein helix threading** algorithm: given a protein sequence and three helix models (H1, H2, H3), the code finds the **best locations** of these helices on the sequence by maximizing a combined objective:

- **Profile similarity score** (from MSAs → PSSMs / profile matrices)
- **Contact energy** (from a contact table + a contact energy matrix, e.g., Jernigan-like)
- **Loop constraints** between helices (min/max loop lengths)
- **No overlap** between helices

It produces a full report including:
- chosen helix placements and loop lengths
- per-position profile score breakdown
- per-contact energy breakdown (with residue mapping and energies)
- total scores

---

## Why this exists (bioinformatics context)

In helix threading, you want to place secondary structure elements (helices) onto a sequence such that:
1) each helix “looks like” known helices in your training set (via profile/PSSM)
2) helices interact favorably (via contact energies)
3) helices are connected realistically (via loop length constraints)

This mimics a simplified structural bioinformatics scoring model used in fold recognition and threading.

---

## Inputs

You provide 5 inputs:

1) **Full sequence** (FASTA)
- `sequence.fasta` (single record)

2) **Three helix MSAs** (FASTA)
- `helix1_msa.fasta`
- `helix2_msa.fasta`
- `helix3_msa.fasta`

Each MSA file contains multiple aligned helix sequences of the same length.  
That length is the helix length `L1`, `L2`, `L3`.

3) **Contact table** (TSV)
A list of contacts defined **in helix coordinate space**:

hA posA hB posB
1 1 2 1
1 2 2 2


- `hA`, `hB` are helix IDs: 1, 2, 3
- `posA`, `posB` are **1-based positions within each helix**

4) **Contact energy matrix** (TSV)
A square matrix `C[a,b]` giving energy (or compatibility) for residues `a` and `b`.

- Can be a full 20×20 amino acid matrix
- Or a reduced alphabet (like the toy example: B / z / x)

Example reduced alphabet:

  B    z    x
B 20  -10   -15
z -10  8     2
x -15  2     10


5) **Loop constraints** (JSON)
Defines realistic spacing constraints between helices:

```json
{
  "12": {"min": 2, "max": 20},
  "23": {"min": 2, "max": 20}
}
```

Meaning:

- loop12 = start2 - (start1 + L1) must be in [min, max]

- loop23 = start3 - (start2 + L2) must be in [min, max]


Search algorithm (threading)

We search for starts (start1, start2, start3) that maximize total score under constraints.

Constraints enforced

Ordering: H1 before H2 before H3 (typical threading chain)

No overlap: helix intervals must not intersect

Loop constraints: enforced exactly

Method A — Fix-and-search (fast, recommended)

Pre-scan each helix across the sequence to compute profile score for all possible starts

Choose the helix with the strongest best profile hit (most confident)

Fix that helix and search placements for others using loop constraints to shrink search space

Evaluate total score for each valid placement

Return the best placement

Method B — Brute force (validation)

Try all valid combinations that satisfy constraints (slower but exact).

Example run (from this repo)

Run the included demo:

```bash
helix-thread \
  --seq data/example/sequence.fasta \
  --msa1 data/example/helix1_msa.fasta \
  --msa2 data/example/helix2_msa.fasta \
  --msa3 data/example/helix3_msa.fasta \
  --contacts data/example/contact_table.tsv \
  --cmat data/example/contact_matrix.tsv \
  --loops data/example/loops.json \
  --lambda 1.0 \
  --method fix \
  --out outputs/run_001
```

Example result (Report Summary)

Best placement

H1: start=2, end=5, window=BzxB

H2: start=8, end=11, window=Bzzz

H3: start=14, end=17, window=xxxB

Loop lengths

loop12 = 2 (constraint (2, 20))

loop23 = 2 (constraint (2, 20))

Totals

Profile total = 109

Contact total = 9.0

TOTAL = 118.0

What the tool outputs

Inside outputs/run_001/:

report.md
Human-readable report (placements + per-position profile breakdown + contact breakdown)

result.json
Machine-readable full result (same content as report, structured)

contact_breakdown.tsv
One row per contact, showing:

helix positions → mapped sequence indices → symbols → energy values

Understanding the example output (step-by-step)
1) Profile scoring (why these windows are chosen)

Each helix placement produces a per-position sum:

H1 total = 45

B (12) + z (9) + x (12) + B (12)

H2 total = 45

B (12) + z (12) + z (12) + z (9)

H3 total = 19

x (12) + x (12) + x (9) + B (-14)

Total profile = 45 + 45 + 19 = 109

Even though H3 position 4 has a strong penalty, the combined profile + contact + constraints still makes this placement optimal under the given toy data.

2) Contact breakdown (how energy is computed)

Each contact entry is mapped from helix coordinates to sequence residues:

Example row:

(H1,1) is at sequence index 2 → residue B

(H2,1) is at sequence index 8 → residue B

energy C(B,B)=20

Summing all contacts yields 9.0 total contact energy:

Contact	Residues	Energy
H1,1–H2,1	B–B	20
H1,2–H2,2	z–z	8
H1,3–H2,3	x–z	2
H1,4–H2,4	B–z	-10
H2,2–H3,2	z–x	2
H2,3–H3,3	z–x	2
H1,1–H3,1	B–x	-15
Total = 9.0		