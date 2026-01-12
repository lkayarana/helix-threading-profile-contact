from helix_threader.io.contact_matrix import ContactMatrix
from helix_threader.io.contact_table import ContactPair
from helix_threader.scoring.contact_energy import contact_energy

def test_contact_energy_simple():
    C = ContactMatrix(["A","B"], {("A","A"): 1.0, ("A","B"): 2.0, ("B","B"): 3.0, ("B","A"): 2.0})
    seq = "AABB"
    starts = {1: 0, 2: 2, 3: 0}
    lengths = {1: 2, 2: 2, 3: 2}
    contacts = [ContactPair(1,1,2,1), ContactPair(1,2,2,2)]  # A-B and A-B
    e = contact_energy(seq, starts, lengths, contacts, C)
    assert e == 2.0 + 2.0
