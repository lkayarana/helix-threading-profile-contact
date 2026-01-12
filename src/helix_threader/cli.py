from __future__ import annotations
import argparse
import os

from helix_threader.io.fasta import read_single_fasta_sequence, read_fasta_sequences
from helix_threader.io.contact_table import read_contact_table_tsv
from helix_threader.io.contact_matrix import read_contact_matrix_tsv
from helix_threader.io.loops import read_loops_json

from helix_threader.models.profile import build_pssm_from_msa
from helix_threader.models.problem import ThreadingProblem
from helix_threader.models.contacts import validate_contacts

from helix_threader.search.fix_and_search import search_fix_and_search
from helix_threader.search.brute_force import brute_force_search
from helix_threader.reporting.explain_solution import explain
from helix_threader.reporting.writer import ensure_dir, write_json, write_contact_tsv, write_report_md

def main():
    p = argparse.ArgumentParser(description="Thread 3 helices onto a sequence using profile + contact energy.")
    p.add_argument("--seq", required=True, help="FASTA with the full sequence (single record).")
    p.add_argument("--msa1", required=True, help="FASTA MSA for helix 1.")
    p.add_argument("--msa2", required=True, help="FASTA MSA for helix 2.")
    p.add_argument("--msa3", required=True, help="FASTA MSA for helix 3.")
    p.add_argument("--contacts", required=True, help="TSV contact table.")
    p.add_argument("--cmat", required=True, help="TSV contact energy matrix.")
    p.add_argument("--loops", required=True, help="JSON loop constraints.")
    p.add_argument("--lambda", dest="lam", type=float, default=1.0, help="Lambda weight for contact energy.")
    p.add_argument("--pseudocount", type=float, default=1.0, help="Pseudocount for PSSM construction.")
    p.add_argument("--scale", type=float, default=10.0, help="Scale factor for PSSM (log-odds scaled to int).")
    p.add_argument("--method", choices=["fix", "bruteforce"], default="fix", help="Search method.")
    p.add_argument("--out", required=True, help="Output directory for report and result files.")

    args = p.parse_args()

    seq = read_single_fasta_sequence(args.seq)
    msa1 = read_fasta_sequences(args.msa1)
    msa2 = read_fasta_sequences(args.msa2)
    msa3 = read_fasta_sequences(args.msa3)

    contacts = read_contact_table_tsv(args.contacts)
    cmat = read_contact_matrix_tsv(args.cmat)
    loops = read_loops_json(args.loops)

    alphabet = cmat.alphabet

    P1 = build_pssm_from_msa(msa1, alphabet=alphabet, name="H1", pseudocount=args.pseudocount, scale=args.scale)
    P2 = build_pssm_from_msa(msa2, alphabet=alphabet, name="H2", pseudocount=args.pseudocount, scale=args.scale)
    P3 = build_pssm_from_msa(msa3, alphabet=alphabet, name="H3", pseudocount=args.pseudocount, scale=args.scale)

    helix_lengths = {1: P1.length, 2: P2.length, 3: P3.length}
    validate_contacts(contacts, helix_lengths)

    problem = ThreadingProblem(
        sequence=seq,
        profiles={1: P1, 2: P2, 3: P3},
        contacts=contacts,
        contact_matrix=cmat,
        loop12=(loops["12"]["min"], loops["12"]["max"]),
        loop23=(loops["23"]["min"], loops["23"]["max"]),
        lam=args.lam,
    )

    ensure_dir(args.out)

    if args.method == "fix":
        sol = search_fix_and_search(problem)
        starts = sol.starts
        meta = {"method": "fix", "fixed_helix": sol.fixed_helix}
    else:
        sol2 = brute_force_search(problem)
        starts = sol2.starts
        meta = {"method": "bruteforce"}

    explained = explain(problem, starts)

    # add meta
    explained["meta"] = meta
    explained["meta"]["starts_0based"] = starts
    explained["meta"]["starts_1based"] = {k: v + 1 for k, v in starts.items()}

    write_json(os.path.join(args.out, "result.json"), explained)
    write_contact_tsv(os.path.join(args.out, "contact_breakdown.tsv"), explained["contact"]["rows"])
    write_report_md(os.path.join(args.out, "report.md"), explained)

    print(f"[OK] Wrote outputs to: {args.out}")
    print(f"Best starts (1-based): {explained['meta']['starts_1based']}")
    print(f"TOTAL score: {explained['totals']['total']}")
