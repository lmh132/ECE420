from pytket import Circuit
from pytket.extensions.cirq import CirqDensityMatrixSampleBackend
from pytket.extensions.qiskit import qiskit_to_tk
from graphs import make_grid_graph
from qaoa import qaoa_ansatz
from optimize import optimize_qaoa
from analysis import approximation_ratio
from utils import save_json, timestamp
import os

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

def run_qaoa_pytket_cirq(grid_size, p=1, shots=1000):
    """Run QAOA using pytket + Cirq backend simulator."""

    # 1️⃣ Build grid graph
    G = make_grid_graph(grid_size, grid_size)

    # 2️⃣ Optimize QAOA parameters
    gammas, betas, _ = optimize_qaoa(G, p)

    # 3️⃣ Build Qiskit QAOA ansatz circuit
    qc_qiskit = qaoa_ansatz(G, gammas, betas)
    
    # Add measurements to the circuit
    from qiskit import ClassicalRegister
    n_qubits = qc_qiskit.num_qubits
    cr = ClassicalRegister(n_qubits, 'c')
    qc_qiskit.add_register(cr)
    qc_qiskit.measure(range(n_qubits), range(n_qubits))

    # 4️⃣ Convert Qiskit circuit to pytket
    qc = qiskit_to_tk(qc_qiskit)

    # 5️⃣ Initialize Cirq backend simulator (supports shot-based sampling)
    backend = CirqDensityMatrixSampleBackend()

    # 6️⃣ Run simulation
    counts_result = backend.run_circuit(qc, n_shots=shots)
    # Extract counts from BackendResult and convert to standard format
    # pytket returns Counter({(bit_tuple): count, ...})
    pytket_counts = counts_result.get_counts()
    counts = {}
    for bit_tuple, count in pytket_counts.items():
        # Convert tuple of bits to binary string (e.g., (1, 0, 1) -> "101")
        bitstring = ''.join(str(b) for b in bit_tuple)
        counts[bitstring] = count

    # 6️⃣ Compute approximation ratio
    alpha = approximation_ratio(G, counts)

    # 7️⃣ Save results to JSON
    out = {
        "graph": f"{grid_size}x{grid_size}_grid",
        "platform": "pytket-Cirq",
        "p": p,
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "approx_ratio": alpha,
        "counts": counts,
        "shots": shots
    }

    filename = f"data/pytket_cirq_{grid_size}x{grid_size}_p{p}_{timestamp()}.json"
    save_json(out, filename)
    print(f"Saved results to {filename}")


if __name__ == "__main__":
    run_qaoa_pytket_cirq(2)
    run_qaoa_pytket_cirq(3)
    run_qaoa_pytket_cirq(4)
