# ECE420: Quantum Algorithm Implementation

This repository contains implementations of the Quantum Approximate Optimization Algorithm (QAOA) for the MaxCut problem on grid graphs, with support for multiple quantum computing platforms.

## Project Structure

```
src/
├── qaoa.py                 # Core QAOA ansatz implementation (Qiskit)
├── qaoa_ibm.py            # QAOA on IBM Quantum Runtime
├── qaoa_cirq.py           # QAOA using pytket + Cirq backend
├── qaoa_quantinuum.py     # QAOA on Quantinuum devices
├── qaoa_2x2.py            # 2×2 grid specialized implementation
├── qaoa_3x3.py            # 3×3 grid specialized implementation
├── qaoa_4x4.py            # 4×4 grid specialized implementation
├── graphs.py              # Grid graph generation utilities
├── optimize.py            # QAOA parameter optimization (COBYLA)
├── hamiltonian.py         # MaxCut Hamiltonian construction
├── analysis.py            # Approximation ratio & analysis functions
├── ibm.py                 # IBM backend utilities
├── utils.py               # Helper functions (JSON I/O, timestamps)
└── data/                  # Results directory (JSON output files)
```

## Requirements

- Python 3.13+
- Qiskit and Qiskit IBM Runtime
- pytket (with Cirq and Quantinuum extensions)
- NetworkX (graph utilities)
- NumPy, SciPy

## Installation

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install -r requirements.txt
```

## Usage

### Run QAOA on IBM Quantum

```bash
python src/qaoa_ibm.py
```

This submits a QAOA circuit to IBM's quantum backend in batch mode and saves results to `src/data/ibm_qaoa_2x2_p1_*.json`.

### Run QAOA with Cirq (pytket)

```bash
python src/qaoa_cirq.py
```

Runs QAOA on a local Cirq simulator via pytket.

### Run QAOA on Quantinuum

```bash
python src/qaoa_quantinuum.py
```

Requires Quantinuum API credentials. Set up authentication via:
```bash
export QUANTINUUM_API_KEY="your_key"
export QUANTINUUM_USER_ID="your_id"
```

### Grid-Specific Implementations

```bash
python src/qaoa_2x2.py  # 2×2 grid
python src/qaoa_3x3.py  # 3×3 grid
python src/qaoa_4x4.py  # 4×4 grid
```

## Configuration

### IBM Quantum Access

Save your IBM Quantum credentials:
```bash
qiskit-ibm-runtime save-account
```

Free plan users have access to the `ibm_fez` backend via batch mode.

### Parameter Constraints

IBM's RZZ gate has angle constraints: `angle ∈ [0, π/2]`

Since the circuit uses `2*gamma` as the angle, ensure:
- `2*gamma ≤ π/2` → `gamma ≤ π/4 ≈ 0.785`

The default parameters (gamma=0.5, beta=0.3) satisfy these constraints.

## Output Format

Results are saved to `src/data/` as JSON files with the following structure:

```json
{
  "job_id": "...",
  "backend": "ibm_fez",
  "grid_size": "2x2",
  "p": 1,
  "gammas": [0.5],
  "betas": [0.3],
  "counts": {
    "0011": 245,
    "1100": 231,
    ...
  },
  "elapsed_time": 42.5
}
```

## Key Functions

### `qaoa_ansatz(G, gammas, betas)`
Constructs the QAOA quantum circuit for MaxCut on graph G.

### `optimize_qaoa(G, p, initial=None)`
Optimizes QAOA parameters using COBYLA, returns optimized gammas, betas, and minimum energy.

### `approximation_ratio(G, counts)`
Computes the approximation ratio from measurement outcome counts.

### `classical_maxcut_value(G, bitstring)`
Evaluates the MaxCut objective function for a given bitstring assignment.

## Notes

- Optimization for larger grids (4×4+) may take significant time
- Free IBM Quantum plan supports batch execution mode only
- Quantinuum requires valid API credentials and may have quota limits
