import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
p = np.linspace(0, 1, 500)
L = p**6 * (1 - p)**4
ax.plot(p, L, color=C.BLUE, ls='-', label=r'$L(p)$')
peak = 0.6**6 * 0.4**4
ax.axvline(0.6, color=C.INK, ls='--', lw=1.1)
label(ax, r'$\hat p=0.6$', (0.6, peak), offset=(6, 8))
for q in (0.5, 0.7):
    val = q**6 * (1-q)**4
    ax.axvline(q, color=C.GRAY, ls=':', lw=1.0)
    label(ax, f'{val:.5f}', (q, val), offset=(4, -16))
ax.set(xlim=(0, 1), ylim=(-0.00012, 0.00135), xlabel=r'$p$', ylabel=r'$L(p)$')
label(ax, '$L(p)$ 不是 $p$ 的分布，\n曲线下面积 $\\ne 1$', (0.03, 0.00130), offset=(0, 0), va='top')
ax.set_yticks([0, 0.0005, 0.0010])
save(fig, "P11-n1")
