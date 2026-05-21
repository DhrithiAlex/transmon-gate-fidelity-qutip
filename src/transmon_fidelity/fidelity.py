import numpy as np
import qutip as qt
from .simulation import simulate_channel
from .physics import ideal_unitary

def average_gate_fidelity(gate: str, T1: float, T2: float) -> float:
    """Compute average gate fidelity."""
    U = ideal_unitary(gate)
    output_states = simulate_channel(gate, T1, T2)

    fid_sum = 0.0
    for rho_in, rho_out in zip(PROBE_STATES, output_states):
        rho_ideal = U * rho_in * U.dag()
        fid_sum += (qt.fidelity(rho_ideal, rho_out) ** 2)

    F_e = fid_sum / len(PROBE_STATES)
    F_avg = (2 * F_e + 1) / 3
    return float(np.real(F_avg))
