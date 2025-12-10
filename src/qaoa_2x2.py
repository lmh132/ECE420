from graphs import make_grid_graph
from qaoa import qaoa_ansatz
from optimize import optimize_qaoa
from analysis import energy_expectation, sample_bitstrings, approximation_ratio
from utils import save_json, timestamp

if __name__ == "__main__":
    G = make_grid_graph(2, 2)
    p = 1

    # Optimize parameters
    gammas, betas, energy = optimize_qaoa(G, p)

    print("Gammas:", gammas)
    print("Betas:", betas)
    print("Energy:", energy)

    # Sample bitstrings
    qc = qaoa_ansatz(G, gammas, betas)
    counts = sample_bitstrings(qc, shots=1000)

    alpha = approximation_ratio(G, counts)
    print("Approximation ratio:", alpha)

    # Save results
    out = {
        "graph": "2x2_grid",
        "p": p,
        "gammas": gammas.tolist(),
        "betas": betas.tolist(),
        "energy": energy,
        "approx_ratio": alpha,
        "counts": {k: float(v) for k, v in counts.items()}
    }

    filename = f"../data/results_2x2_p{p}_{timestamp()}.json"
    save_json(out, filename)
    print("Saved to", filename)
