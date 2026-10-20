import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 8)
b = np.geomspace(1, 100, 500)
for rho, style in [(0.8, '-'), (0.5, '--'), (0.2, ':')]:
    variance = rho + (1-rho)/b
    assert np.isclose(variance[0], 1)
    ax.plot(b, variance, color=C.INK, ls=style, lw=1.8)
    ax.axhline(rho, color=C.GRAY, ls=style, lw=0.7)
    label(ax, rf'$\rho={rho}$', (95, rho), (0, 9), ha='right')
ax.set(xscale='log', xlim=(1, 100), ylim=(0, 1),
       xlabel='树数 $B$', ylabel=r'$\mathrm{Var}/\sigma^2$')
ax.set_yticks(np.linspace(0, 1, 6))
fig.tight_layout()
save(fig, "M4-n4")
