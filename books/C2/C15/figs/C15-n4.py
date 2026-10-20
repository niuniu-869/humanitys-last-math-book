import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc

fig, ax = new_fig(10, 9)
ax.set_aspect("equal")
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color=C.INK, lw=1.0)
label(ax, "单位圆", (np.cos(-0.6), np.sin(-0.6)), offset=(4, -6))
ax.axhline(0, color=C.GRAY, lw=0.8); ax.axvline(0, color=C.GRAY, lw=0.8)
label(ax, "实轴", (2.35, 0), offset=(-14, 5)); label(ax, "虚轴", (0, 2.45), offset=(5, -8))
th = np.pi / 3
E = (np.cos(th), np.sin(th))
ax.plot([0, E[0]], [0, E[1]], color=C.INK, lw=1.0)
ax.scatter(*E, s=28, color=C.INK, zorder=5)
label(ax, r"$e^{i\theta}$", E, offset=(-4, 7))
ax.plot([E[0], E[0]], [0, E[1]], color=C.INK, lw=0.9, ls=":")
label(ax, r"$\cos\theta$", (E[0], 0), offset=(-12, -14))
label(ax, r"$\sin\theta$", (E[0], 0.62), offset=(3, 0))
ax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=60, color=C.INK, lw=1))
label(ax, r"$\theta$", (0.3, 0.12), offset=(0, 0))
# z 与 z e^{iθ}
z = (np.sqrt(3), 1.0); w = (0.0, 2.0)
for p in (z, w):
    ax.annotate("", xy=p, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.6, shrinkA=0, shrinkB=0, mutation_scale=11))
ax.scatter(*z, s=30, color=C.INK, zorder=5)
ax.scatter(*w, s=34, marker="s", color=C.INK, zorder=5)
label(ax, "$z$", z, offset=(5, 2)); label(ax, r"$z\,e^{i\theta}$", w, offset=(-44, -2))
label(ax, "$r$", (z[0] * 0.62, z[1] * 0.62), offset=(2, -12))
label(ax, "$r$", (0, 1.35), offset=(4, 0))
ax.add_patch(Arc((0, 0), 1.25, 1.25, theta1=0, theta2=30, color=C.INK, lw=1))
label(ax, r"$\varphi$", (0.75, 0.16), offset=(2, 0))
arc_t = np.linspace(np.pi / 6, np.pi / 2, 120)
ax.plot(2 * np.cos(arc_t), 2 * np.sin(arc_t), color=C.INK, lw=1.2, ls="--")
ax.annotate("", xy=(2 * np.cos(np.pi / 2), 2 * np.sin(np.pi / 2)),
            xytext=(2 * np.cos(1.40), 2 * np.sin(1.40)),
            arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.2, mutation_scale=11))
label(ax, r"转过 $\theta$", (1.35, 1.75), offset=(4, 2))
ax.set_xlim(-1.3, 2.4); ax.set_ylim(-1.25, 2.5)
ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
save(fig, "C15-n4")
