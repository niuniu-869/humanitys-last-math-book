import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
import math

def gamma_standardized(z, n):
    x = n + np.sqrt(n) * z
    out = np.zeros_like(z, dtype=float)
    mask = x > 0
    xm = x[mask]
    out[mask] = np.sqrt(n) * np.exp((n - 1) * np.log(xm) - xm - math.lgamma(n))
    return out

z = np.linspace(-3.5, 4.5, 900)
fig, ax = new_fig(13, 7.4)
ax.plot(z, gamma_standardized(z, 1), color=C.GRAY, ls=':', lw=1.6, label='$n=1$（点线）')
ax.plot(z, gamma_standardized(z, 5), color=C.GRAY, ls='--', lw=1.8, label='$n=5$（短划虚线）')
ax.plot(z, gamma_standardized(z, 30), color=C.INK, ls='-', lw=2.0, label='$n=30$（实线）')
ax.plot(z, np.exp(-z**2 / 2) / np.sqrt(2 * np.pi), color=C.INK, ls='-', lw=3.0, label='标准正态（粗实线）')
ax.set(xlim=(-3.5, 4.5), ylim=(0, 0.44), xlabel='$z$', ylabel='密度')
ax.legend(loc='upper right', fontsize=9)
save(fig, 'P8-n5')
