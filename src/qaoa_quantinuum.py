from pytket import Circuit
from pytket.extensions.quantinuum import QuantinuumBackend
from pytket.extensions.qiskit import qiskit_to_tk
from qiskit import ClassicalRegister
from graphs import make_grid_graph
from qaoa import qaoa_ansatz
from optimize import optimize_qaoa
from analysis import approximation_ratio
import json

def run_quantinuum_qaoa(grid_size=2, p=1, shots=1000, device_name="H1-1"):
    # 1. Build the graph
    G = make_grid_graph(grid_size, grid_size)

    # 2. Optimize parameters (classical part)
    gammas, betas, _ = optimize_qaoa(G, p)

    # 3. Build QAOA ansatz circuit (Qiskit)
    qc_qiskit = qaoa_ansatz(G, gammas, betas)
    
    # Add measurements
    n_qubits = qc_qiskit.num_qubits
    cr = ClassicalRegister(n_qubits, 'c')
    qc_qiskit.add_register(cr)
    qc_qiskit.measure(range(n_qubits), range(n_qubits))
    
    # Convert to pytket
    qc: Circuit = qiskit_to_tk(qc_qiskit)

    # 4. Select Quantinuum backend (emulator or hardware if you have access)
    # Available devices: 'H1-1', 'H2-1', 'H2-2' (hardware), or 'H1-1E', 'H2-1E', 'H2-2E' (emulators)
    backend = QuantinuumBackend(device_name=device_name)

    # 5. Compile circuit for Quantinuum (ensures gate set & constraints)
    qc_compiled = backend.get_compiled_circuit(qc)

    # 6. Submit job / run circuit with specified shots
    handle = backend.process_circuit(qc_compiled, n_shots=shots)
    # Wait / poll until result is ready (or block until completed)
    result = backend.get_result(handle)
    pytket_counts = result.get_counts()
    
    # Convert pytket counts to standard format
    counts = {}
    for bit_tuple, count in pytket_counts.items():
        bitstring = ''.join(str(b) for b in bit_tuple)
        counts[bitstring] = count

    # 7. Compute approximation ratio
    alpha = approximation_ratio(G, counts)

    # 8. Save results
    out = {
      "graph": f"{grid_size}x{grid_size}_grid",
      "platform": f"Quantinuum {device_name}",
      "p": p,
      "gammas": gammas.tolist(),
      "betas": betas.tolist(),
      "approx_ratio": alpha,
      "counts": counts
    }
    filename = f"quantinuum_{grid_size}x{grid_size}_p{p}.json"
    with open(filename, "w") as f:
      json.dump(out, f, indent=2)
    print("Saved results to", filename)
    print("Approximation ratio:", alpha)

if __name__ == "__main__":
    run_quantinuum_qaoa(grid_size=2, p=1, shots=1000, device_name="H1-1")
