import numpy as np
import qutip as qt
from qutip import basis, ket2dm, sigmax, sigmaz, Qobj

OMEGA_Q = 2 * np.pi * 5.0  # 5 GHz

GATE_DURATION_X = 20.0
GATE_DURATION_H = 30.0

def collapse_ops(T1: float, T2: float) -> list[Qobj]:
    """Return Lindblad collapse operators for T1 and T2."""
    sm = qt.destroy(2)
    gamma1 = 1.0 / T1
    gamma_phi = max(1.0/T2 - 1.0/(2.0*T1), 0.0)

    c_ops = [np.sqrt(gamma1) * sm]
    if gamma_phi > 0:
        c_ops.append(np.sqrt(gamma_phi) * sigmaz() / 2.0)
    return c_ops


def drive_hamiltonian(gate: str, duration: float) -> Qobj:
    """Drive Hamiltonian in rotating frame."""
    omega_drive = np.pi / duration

    if gate == 'X':
        return omega_drive * sigmax() / 2.0
    elif gate == 'H':
        axis = (sigmax() + sigmaz()) / (2.0 * np.sqrt(2.0))
        return omega_drive * axis
    else:
        raise ValueError("Gate must be 'X' or 'H'")


IDEAL_X = qt.sigmax()
IDEAL_H = Qobj([[1, 1], [1, -1]]) / np.sqrt(2)

def ideal_unitary(gate: str) -> Qobj:
    return IDEAL_X if gate == 'X' else IDEAL_H
