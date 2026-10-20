import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10, 9)
theta = np.linspace(0, 2*np.pi, 801)
def outer(t):
    r = 2 + 0.4*np.cos(3*t) + 0.3*np.sin(2*t)
    return np.array([r*np.cos(t), r*np.sin(t)])
xy = outer(theta)
assert np.min(np.linalg.norm(xy, axis=0)) > 0.5
ax.fill(*xy, color=C.LIGHT, lw=0)
ax.fill(0.5*np.cos(theta), 0.5*np.sin(theta), color=C.PAPER, lw=0)
ax.axhline(0, color=C.GRAY, lw=0.7)
ax.axvline(0, color=C.GRAY, lw=0.7)
ax.plot(*xy, color=C.INK, ls="-", lw=1.6)
ax.plot(0.5*np.cos(theta), 0.5*np.sin(theta), color=C.INK, ls="--", lw=1.3)
for t in (0.9, 4.1):
    arrow(ax, outer(t), outer(t+0.13)-outer(t), color=C.INK)
t0, t1 = 2.1, 1.65
p0 = 0.5*np.array([np.cos(t0), np.sin(t0)])
p1 = 0.5*np.array([np.cos(t1), np.sin(t1)])
ax.annotate("", xy=p1, xytext=p0, arrowprops=dict(
    arrowstyle="-|>", color=C.INK, lw=1.3, ls="--",
    shrinkA=0, shrinkB=0, mutation_scale=12, connectionstyle="arc3,rad=-0.12"))
ax.scatter([0], [0], s=24, marker="s", color=C.INK, zorder=5)
label(ax, "$O$", (0, 0), offset=(-10, -10), fontsize=9)
label(ax, "$L$", outer(0.35), offset=(9, 3))
label(ax, "$l$（挖掉）", (0.5*np.cos(-0.6), 0.5*np.sin(-0.6)), offset=(8, -11))
label(ax, "$D'$", (-1.1, -1.1), fontsize=13)
label(ax, "$x$", (2.7, 0), offset=(0, 5))
label(ax, "$y$", (0, 2.5), offset=(5, 0))
ax.set_aspect("equal")
ax.set_xlim(-2.8, 2.95)
ax.set_ylim(-2.75, 2.8)
ax.axis("off")
save(fig, "C27-n3")
