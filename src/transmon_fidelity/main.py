import numpy as np
import matplotlib.pyplot as plt
from .physics import GATE_DURATION_X, GATE_DURATION_H
from .fidelity import average_gate_fidelity
from .plotting import plot_fidelity_heatmap

def main():
    print("=" * 65)
    print("  Transmon Gate Fidelity Simulation  (QuTiP / Lindblad)")
    print("=" * 65)

    # Single point demo
    T1_DEFAULT = 50_000.0
    T2_DEFAULT = 80_000.0
    print(f"\nSingle-point demo (T1={T1_DEFAULT/1e3:.0f} µs, T2={T2_DEFAULT/1e3:.0f} µs)")
    for gate in ('X', 'H'):
        F = average_gate_fidelity(gate, T1_DEFAULT, T2_DEFAULT)
        dur = GATE_DURATION_X if gate == 'X' else GATE_DURATION_H
        print(f"  {gate}-gate (t={dur:.0f} ns):  F̄ = {F:.6f}  error = {1-F:.2e}")

    # Grid sweep
    print("\nGenerating fidelity heatmaps...")
    T1_vals = np.array([10, 20, 30, 50, 80, 100]) * 1e3
    T2_vals = np.array([10, 20, 30, 50, 80, 100, 150, 200]) * 1e3

    fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
    for ax, gate in zip(axes, ('X', 'H')):
        print(f"  → Computing {gate}-gate grid...")
        F = np.full((len(T1_vals), len(T2_vals)), np.nan)
        for i, T1 in enumerate(T1_vals):
            for j, T2 in enumerate(T2_vals):
                if T2 <= 2 * T1:
                    F[i, j] = average_gate_fidelity(gate, T1, T2)
        plot_fidelity_heatmap(F, T1_vals, T2_vals, gate, ax)

    plt.suptitle('Average Gate Fidelity across $(T_1, T_2)$ plane\nTransmon qubit — Lindblad master equation (QuTiP)', 
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.savefig('figures/fidelity_heatmap.png', dpi=200, bbox_inches='tight')
    print("\n✅ Saved: figures/fidelity_heatmap.png")
    plt.show()

    print("\nSimulation completed successfully!")
