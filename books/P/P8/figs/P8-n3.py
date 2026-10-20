import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
import math

p = 0.7
q = 1 - p
fig, axes = new_fig(15, 5.3, ncols=3, sharex=True)
z = np.linspace(-4, 4, 500)
normal = np.exp(-z**2 / 2) / np.sqrt(2 * np.pi)
for ax, n in zip(axes, [5, 20, 100]):
    s = math.sqrt(n * p * q)
    ks = np.arange(n + 1)
    zk = (ks - n * p) / s
    pmf = np.array([math.comb(n, int(k)) * p**k * q**(n-k) for k in ks])
    ax.bar(zk, s * pmf, width=1 / s, color=C.LIGHT, edgecolor=C.INK, linewidth=0.8, align='center')
    ax.plot(z, normal, color=C.GRAY, ls='--', lw=1.5)
    ax.set_title(f'$n={n}$')
    ax.set_xlim(-4, 4)
    ax.set_ylim(bottom=0)
    ax.set_xlabel('$z$')
    ax.set_ylabel('密度')
fig.subplots_adjust(wspace=0.35)
save(fig, 'P8-n3')
