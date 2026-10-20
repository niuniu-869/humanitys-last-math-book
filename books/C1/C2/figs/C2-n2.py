import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
x = np.geomspace(1e-3, 1, 3000)
# Equivalent expressions keep every exponential nonpositive.
e = np.exp(-1/x)
ax.plot(-x, 1/(1+e), color=C.INK, ls='-')
ax.plot(x, e/(1+e), color=C.INK, ls='-')
ax.axvline(0, color=C.GRAY, ls='--', lw=0.9)
ax.scatter([0, 0], [1, 0], s=40, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, '左极限 1', (0.08, 0.92))
label(ax, '右极限 0', (-0.08, 0.12), ha='right')
ax.set(xlim=(-1, 1), ylim=(-0.1, 1.1), xlabel='$x$', ylabel='$y$')
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
fig.subplots_adjust(left=0.14, right=0.97, bottom=0.19, top=0.96)
save(fig, "C2-n2")
