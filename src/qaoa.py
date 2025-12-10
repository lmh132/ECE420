from qiskit import QuantumCircuit

def qaoa_ansatz(G, gammas, betas):
    """
    Build the QAOA circuit of depth p for grid-graph MaxCut.
    gammas, betas are length-p arrays.
    """
    p = len(gammas)
    n = G.number_of_nodes()

    qc = QuantumCircuit(n)
    qc.h(range(n))  # prepare |+...+>

    for layer in range(p):
        gamma = gammas[layer]
        beta = betas[layer]

        # Cost layer: ZZ rotations
        for i, j in G.edges():
            qc.rzz(2 * gamma, i, j)

        # Mixer layer: RX rotations
        for qubit in range(n):
            qc.rx(2 * beta, qubit)

    return qc

# --- PYTKET VERSION OF QAOA ANSATZ (for Quantinuum hardware) ---

from pytket import Circuit
from pytket.extensions.quantinuum import QuantinuumBackend

def qaoa_ansatz_pytket(G, gammas, betas):
    """
    Builds a pytket Circuit implementing p-layer QAOA for MaxCut.
    G: NetworkX graph
    gammas, betas: lists of angles of length p
    """

    p = len(gammas)
    n = G.number_of_nodes()
    qc = Circuit(n)

    # --- Initial |+> state ---
    for i in range(n):
        qc.H(i)

    # --- Apply p QAOA layers ---
    for layer in range(p):

        gamma = gammas[layer]
        beta = betas[layer]

        # Cost Hamiltonian (ZZ on edges)
        for (u, v) in G.edges():
            qc.CX(u, v)
            qc.Rz(2 * gamma, v)
            qc.CX(u, v)

        # Mixer Hamiltonian (Rx on all qubits)
        for i in range(n):
            qc.Rx(2 * beta, i)

    # Add all qubit measurements
    qc.measure_all()

    return qc
