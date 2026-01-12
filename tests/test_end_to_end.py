import os
from helix_threader.io.fasta import read_single_fasta_sequence, read_fasta_sequences
from helix_threader.io.contact_table import read_contact_table_tsv
from helix_threader.io.contact_matrix import read_contact_matrix_tsv
from helix_threader.io.loops import read_loops_json
from helix_threader.models.profile import build_pssm_from_msa
from helix_threader.models.problem import ThreadingProblem
from helix_threader.search.fix_and_search import search_fix_and_search

def test_end_to_end_example():
    base = os.path.join("data", "example")
    seq = read_single_fasta_sequence(os.path.join(base, "sequence.fasta"))
    msa1 = read_fasta_sequences(os.path.join(base, "helix1_msa.fasta"))
    msa2 = read_fasta_sequences(os.path.join(base, "helix2_msa.fasta"))
    msa3 = read_fasta_sequences(os.path.join(base, "helix3_msa.fasta"))
    contacts = read_contact_table_tsv(os.path.join(base, "contact_table.tsv"))
    cmat = read_contact_matrix_tsv(os.path.join(base, "contact_matrix.tsv"))
    loops = read_loops_json(os.path.join(base, "loops.json"))

    alphabet = cmat.alphabet
    P1 = build_pssm_from_msa(msa1, alphabet=alphabet, name="H1")
    P2 = build_pssm_from_msa(msa2, alphabet=alphabet, name="H2")
    P3 = build_pssm_from_msa(msa3, alphabet=alphabet, name="H3")

    problem = ThreadingProblem(
        sequence=seq,
        profiles={1:P1,2:P2,3:P3},
        contacts=contacts,
        contact_matrix=cmat,
        loop12=(loops["12"]["min"], loops["12"]["max"]),
        loop23=(loops["23"]["min"], loops["23"]["max"]),
        lam=1.0
    )
    sol = search_fix_and_search(problem)
    assert set(sol.starts.keys()) == {1,2,3}
