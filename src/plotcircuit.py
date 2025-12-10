# plotcircuit.py
from graphs import make_grid_graph       # graph generation
from qaoa import qaoa_ansatz             # QAOA ansatz
import matplotlib.pyplot as plt

# Define grid sizes
grid_sizes = [(2, 2), (3, 3), (4, 4)]

# Example optimized parameters for p=2
gammas_dict = {
    (2, 2): [1.178, 0.95],
    (3, 3): [1.12, 0.97],
    (4, 4): [1.09, 0.92]
}
betas_dict = {
    (2, 2): [0.393, 0.42],
    (3, 3): [0.41, 0.38],
    (4, 4): [0.42, 0.39]
}

for size in grid_sizes:
    rows, cols = size
    G = make_grid_graph(rows, cols)
    gammas = gammas_dict[size]
    betas = betas_dict[size]

    # Build QAOA circuit for p=2
    qc = qaoa_ansatz(G, gammas, betas)

    # Draw circuit with Matplotlib
    fig = qc.draw(output='mpl')
    fig.axes[0].set_title(f"QAOA Circuit for {rows}x{cols} Grid (p=2)")

    # Save figure
    filename = f"{rows}x{cols}_circuit_p2.png"
    fig.savefig(filename)
    plt.close(fig)  # close figure to avoid overlapping plots
    print(f"Saved circuit diagram for {rows}x{cols} grid to {filename}")
