import json
import matplotlib.pyplot as plt

def plot_bitstring_histogram(json_file, title):
    with open(json_file, "r") as f:
        data = json.load(f)
    counts = data["counts"]
    bitstrings = list(counts.keys())
    probabilities = list(counts.values())
    
    plt.figure(figsize=(10,5))
    plt.bar(bitstrings, probabilities, color='skyblue')
    plt.xlabel("Bitstring")
    plt.ylabel("Probability")
    plt.title(title)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

# Example usage
plot_bitstring_histogram("src/data/ibm_qaoa_2x2_p1_2025-12-07_20-52-01.json", "IBM Hardware QAOA Bitstring Probabilities, 2x2 Grid, p=1")
# plot_bitstring_histogram("src/data/results_3x3_p2_2025-12-07_16-45-32.json", "3x3 QAOA Bitstring Probabilities, p=2")
# plot_bitstring_histogram("src/data/results_4x4_p2_2025-12-07_16-45-40.json", "4x4 QAOA Bitstring Probabilities, p=2")
