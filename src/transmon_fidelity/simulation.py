import numpy as np
import qutip as qt
from .physics import collapse_ops, drive_hamiltonian, ideal_unitary

PROBE_STATES = [
    qt.ket2dm(basis(2, 0)),
    qt.ket2dm(basis(2, 1)),
    qt.ket2dm((basis(2,0) + basis(2,1)).unit()),
    qt.ket2dm((basis(2,0) + 1j*basis(2,1)).unit())
]

def simulate_channel(gate: str, T1: float, T2: float, n_steps: int = 200):
    """Simulate noisy channel for all probe states."""
    duration = 20.0 if gate == 'X' else 30.0
    H = drive_hamiltonian(gate, duration)
    c_ops = collapse_ops(T1, T2)
    tlist = np.linspace(0, duration, n_steps)

    output_states = []
    for rho0 in PROBE_STATES:
        result = qt.mesolve(H, rho0, tlist, c_ops, [])
        output_states.append(result.states[-1])
    return output_states
