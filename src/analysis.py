import numpy as np
from qiskit.quantum_info import Statevector

def energy_expectation(qc, H):
    """
    Compute <psi|H|psi> using the statevector.
    H should be a SparsePauliOp (from your hamiltonian.py)
    """
    state = Statevector.from_instruction(qc)
    return state.expectation_value(H).real

def classical_maxcut_value(G, bitstring):
    """
    Compute the MaxCut value of a given bitstring assignment.
    """
    cut = 0
    for i, j in G.edges():
        if bitstring[i] != bitstring[j]:
            cut += 1
    return cut

def approximation_ratio(G, counts):
    """
    Compute the approximation ratio from bitstring counts (probabilities).
    counts: dict of bitstring -> probability
    """
    best_possible = G.number_of_edges()  # Grid graphs are bipartite
    total = 0
    for bitstring, prob in counts.items():
        bits = list(reversed([int(b) for b in bitstring]))  # Qiskit uses LSB first
        cut = classical_maxcut_value(G, bits)
        total += prob * cut
    return total / best_possible

def sample_bitstrings(qc, shots=1000):
    """
    Sample bitstrings from the statevector to simulate measurement shots.
    Returns a dictionary: bitstring -> probability.
    """
    state = Statevector.from_instruction(qc)
    probs = np.abs(state.data)**2
    n = qc.num_qubits
    indices = np.arange(2**n)
    samples = np.random.choice(indices, size=shots, p=probs)

    counts = {}
    for s in samples:
        bstr = format(s, f"0{n}b")
        counts[bstr] = counts.get(bstr, 0) + 1 / shots
    return counts
