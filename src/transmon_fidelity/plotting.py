import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_fidelity_heatmap(F, T1_vals, T2_vals, gate, ax):
    T1_us = T1_vals / 1e3
    T2_us = T2_vals / 1e3
    masked = np.ma.masked_invalid(F)

    im = ax.pcolormesh(T2_us, T1_us, masked, cmap='viridis', vmin=0.9, vmax=1.0)
    plt.colorbar(im, ax=ax, label='Average Gate Fidelity $\\bar{F}$')

    # T2 = 2 T1 boundary
    t_diag = np.linspace(T2_us.min(), T2_us.max(), 200)
    ax.plot(t_diag, t_diag/2, 'w--', lw=1.5, label='$T_2 = 2T_1$')

    duration = 20 if gate == 'X' else 30
    ax.set_title(f'{gate}-Gate Average Fidelity\n(gate duration = {duration} ns)')
    ax.set_xlabel('$T_2$ [µs]')
    ax.set_ylabel('$T_1$ [µs]')
    ax.legend()
