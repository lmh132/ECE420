from qiskit.quantum_info import SparsePauliOp

def maxcut_hamiltonian(G):
    """
    Build the MaxCut Hamiltonian H = sum (1 - ZiZj)/2, but we omit constant shift.
    Only returns the ZZ terms since constant offsets don't change optimization.
    """
    num_nodes = G.number_of_nodes()
    paulis = []
    coeffs = []

    for i, j in G.edges():
        p = ["I"] * num_nodes
        p[i] = "Z"
        p[j] = "Z"
        paulis.append("".join(p))
        coeffs.append(1.0)

    return SparsePauliOp.from_list(list(zip(paulis, coeffs)))
