import numpy as np
from scipy.optimize import minimize
from qaoa import qaoa_ansatz
from analysis import energy_expectation
from hamiltonian import maxcut_hamiltonian

def qaoa_objective(params, G, H, p):
    """
    Compute QAOA energy for given parameters.
    params: [gamma_1,...,gamma_p, beta_1,...,beta_p]
    """
    gammas = params[:p]
    betas = params[p:]
    qc = qaoa_ansatz(G, gammas, betas)
    return energy_expectation(qc, H)

def optimize_qaoa(G, p, initial=None):
    """
    Optimize QAOA parameters using COBYLA.
    Returns optimized gammas, betas, and the minimum energy.
    """
    H = maxcut_hamiltonian(G)
    if initial is None:
        initial = 0.1 * np.ones(2 * p)

    res = minimize(
        lambda params: qaoa_objective(params, G, H, p),
        initial,
        method="COBYLA",
        options={"maxiter": 200}
    )

    gammas = res.x[:p]
    betas = res.x[p:]
    energy = res.fun
    return gammas, betas, energy
