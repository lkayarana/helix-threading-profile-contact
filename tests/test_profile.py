from helix_threader.models.profile import build_pssm_from_msa

def test_pssm_shapes():
    msa = ["AAAA", "AAAA", "AAAB", "AAAA"]
    alphabet = ["A","B"]
    P = build_pssm_from_msa(msa, alphabet=alphabet, name="H1", pseudocount=1.0, scale=10.0)
    assert P.length == 4
    assert set(P.scores.keys()) == set(alphabet)
    assert len(P.scores["A"]) == 4
