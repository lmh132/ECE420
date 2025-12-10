from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2, Batch
from qiskit import ClassicalRegister, transpile
from qaoa import qaoa_ansatz
from graphs import make_grid_graph
import time
from collections import Counter
import json
import os

def ibm_sampler_counts(result):
    """Extract bit counts from IBM Sampler result."""
    # In newer Qiskit, result[0].data.c is a BitArray with get_counts() method
    bitarray = result[0].data.c
    return bitarray.get_counts()

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

# load API key
service = QiskitRuntimeService()

backend = service.backend("ibm_fez")   # any 7- or 27-qubit Falcon device

G = make_grid_graph(2, 2)
gammas = [0.5]  # Reduced from 1.2 to fit IBM's rzz gate constraints (angle must be in [0, pi/2])
betas = [0.3]   # Reduced from 0.4

qc = qaoa_ansatz(G, gammas, betas)

# Add measurements
n_qubits = qc.num_qubits
cr = ClassicalRegister(n_qubits, 'c')
qc.add_register(cr)
qc.measure(range(n_qubits), range(n_qubits))

# Transpile to match backend
qc = transpile(qc, backend=backend, optimization_level=2)

# Run using Batch mode (available on free plan)
print("Submitting job to IBM backend...")
start_time = time.time()

with Batch(backend=backend) as batch:
    sampler = SamplerV2(mode=batch)
    job = sampler.run([qc])
    
    print(f"Job ID: {job.job_id()}")
    print(f"Waiting for results...")
    
    # Poll for status updates
    while not job.done():
        elapsed = time.time() - start_time
        status = job.status()
        print(f"[{elapsed:6.1f}s] Status: {status}")
        time.sleep(5)  # Check every 5 seconds
    
    elapsed = time.time() - start_time
    print(f"[{elapsed:6.1f}s] Job completed!")
    
    result = job.result()
    
    # Extract and print bit counts
    counts = ibm_sampler_counts(result)
    print(f"\nBit string counts:")
    for bitstring, count in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {bitstring}: {count}")
    
    # Save results to file
    from utils import timestamp
    output = {
        "job_id": job.job_id(),
        "backend": backend.name,
        "grid_size": "2x2",
        "p": 1,
        "gammas": gammas,
        "betas": betas,
        "counts": counts,
        "elapsed_time": elapsed
    }
    filename = f"data/ibm_qaoa_2x2_p1_{timestamp()}.json"
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {filename}")
