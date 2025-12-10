from graphs import make_grid_graph
from qaoa import qaoa_ansatz
from optimize import optimize_qaoa
from analysis import sample_bitstrings, approximation_ratio
from utils import save_json, timestamp

if __name__ == "__main__":
    # Build 4x4 grid
    G = make_grid_graph(4, 4)
    p = 1  # QAOA depth

    # Optimize QAOA parameters
    gammas, betas, energy = optimize_qaoa(G, p)

    print("Gammas:", gammas)
    print("Betas:", betas)
    print("Energy:", energy)

    # Sample bitstrings and compute approximation ratio
    qc = qaoa_ansatz(G, gammas, betas)
    counts = sample_bitstrings(qc, shots=1000)
    alpha = approximation_ratio(G, counts)
    print("Approximation ratio:", alpha)

    # Save results
    out = {
        "graph": "4x4_grid",
        "p": p,
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "energy": energy,
        "approx_ratio": alpha,
        "counts": {k: float(v) for k, v in counts.items()}
    }

    filename = f"results_4x4_p{p}_{timestamp()}.json"
    save_json(out, filename)
    print("Saved to src/data/", filename)
