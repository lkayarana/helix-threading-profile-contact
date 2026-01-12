from helix_threader.io.contact_matrix import read_contact_matrix_tsv
from helix_threader.io.contact_table import read_contact_table_tsv

def test_read_contact_matrix(tmp_path):
    p = tmp_path / "cmat.tsv"
    p.write_text("\tA\tB\nA\t1\t2\nB\t2\t3\n")
    cm = read_contact_matrix_tsv(str(p))
    assert cm.get("A","A") == 1
    assert cm.get("A","B") == 2
    assert cm.get("B","A") == 2

def test_read_contact_table(tmp_path):
    p = tmp_path / "ct.tsv"
    p.write_text("hA\tposA\thB\tposB\n1\t1\t2\t3\n")
    cs = read_contact_table_tsv(str(p))
    assert len(cs) == 1
    assert cs[0].hA == 1 and cs[0].posB == 3
