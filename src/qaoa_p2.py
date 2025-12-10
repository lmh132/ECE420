import numpy as np
from graphs import make_grid_graph
from qaoa import qaoa_ansatz
from optimize import optimize_qaoa
from analysis import energy_expectation, sample_bitstrings, approximation_ratio
from utils import save_json, timestamp

def run_qaoa(grid_size, p=2, shots=1000):
    # Create grid graph
    G = make_grid_graph(grid_size, grid_size)

    # Optimize parameters
    gammas, betas, energy = optimize_qaoa(G, p)
    print(f"Grid {grid_size}x{grid_size}, p={p}")
    print("Gammas:", gammas)
    print("Betas:", betas)
    print("Energy:", energy)

    # Build ansatz and sample
    qc = qaoa_ansatz(G, gammas, betas)
    counts = sample_bitstrings(qc, shots=shots)

    # Compute approximation ratio
    alpha = approximation_ratio(G, counts)
    print("Approximation ratio:", alpha)

    # Save results
    out = {
        "graph": f"{grid_size}x{grid_size}_grid",
        "p": p,
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "energy": energy,
        "approx_ratio": alpha,
        "counts": {k: float(v) for k, v in counts.items()}
    }
    filename = f"data/results_{grid_size}x{grid_size}_p{p}_{timestamp()}.json"
    save_json(out, filename)
    print("Saved to", filename)
    print("-" * 40)

if __name__ == "__main__":
    for size in [2, 3, 4]:
        run_qaoa(size, p=2)
