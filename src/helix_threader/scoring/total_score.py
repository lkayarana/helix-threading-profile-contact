from __future__ import annotations
from helix_threader.models.problem import ThreadingProblem
from helix_threader.scoring.profile_score import profile_score
from helix_threader.scoring.contact_energy import contact_energy

def total_score(problem: ThreadingProblem, starts: dict[int, int]) -> tuple[float, int, float]:
    """
    Returns: (total, profile_total, contact_total)
    """
    seq = problem.sequence
    profiles = problem.profiles
    helix_lengths = {hid: prof.length for hid, prof in profiles.items()}

    prof_total = 0
    for hid, prof in profiles.items():
        prof_total += profile_score(seq, starts[hid], prof)

    cont_total = contact_energy(
        seq=seq,
        starts=starts,
        helix_lengths=helix_lengths,
        contacts=problem.contacts,
        C=problem.contact_matrix,
    )

    total = float(prof_total) + problem.lam * float(cont_total)
    return total, prof_total, cont_total
