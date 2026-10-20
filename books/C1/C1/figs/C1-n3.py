import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Wedge, Arc

x = 0.9
P = (np.cos(x), np.sin(x)); T = (1, np.tan(x))
assert np.allclose(P, (0.6216, 0.7833), atol=5e-4)
assert np.isclose(T[1], 1.2602, atol=5e-4) and np.isclose(np.hypot(*T), 1.6087, atol=5e-4)
fig, ax = new_fig(10, 8.5)
theta = np.linspace(0, 2*np.pi, 400)
ax.plot(np.cos(theta), np.sin(theta), color=C.INK, lw=1.8)
ax.plot([1, 1], [-.15, 1.55], color=C.INK, lw=1.7)
ax.plot([0, T[0]], [0, T[1]], color=C.INK, lw=1.8)
ax.plot([0, P[0]], [0, P[1]], color=C.INK, lw=1.5)
ax.plot([P[0], T[0]], [P[1], T[1]], color=C.INK, lw=1.8)
ax.plot([P[0], 1], [P[1], 0], color=C.INK, ls="--", lw=1.2)
ax.plot([P[0], P[0]], [0, P[1]], color=C.GRAY, ls=":", lw=1.1)
ax.add_patch(Wedge((0, 0), 1, 0, np.degrees(x), facecolor=C.LIGHT, alpha=.38,
                   edgecolor="none", zorder=0))
ax.add_patch(Arc((0, 0), .38, .38, theta1=0, theta2=np.degrees(x), color=C.INK, lw=1.0))
dot(ax, (0, 0), text="$O$", offset=(-13, -14), size=28)
dot(ax, (1, 0), text="$A$", offset=(5, -14), size=28)
dot(ax, P, text="$P$", offset=(-10, 12), size=28)
dot(ax, T, text="$T$", offset=(5, 5), size=28)
label(ax, "1", (.5, 0), offset=(0, -15), ha="center")
label(ax, "$\\tan x$", (1, .60), offset=(7, 0), ha="left", va="center", fontsize=9)
# sec x 标在 OT 中点上方，靠近线段但不压线
label(ax, "$\\sec x$", (.36, .72), ha="center", va="center", fontsize=9)
# sin x 标在 P 到横轴的点线旁（线段左侧的空隙内）
label(ax, "$\\sin x$", (.47, .33), ha="center", va="center", fontsize=9)
label(ax, "$x$", (.24, .085), offset=(3, 2), fontsize=9)
label(ax, "阴影 = 扇形 $OAP$", (-.30, 1.35), ha="left", va="center", fontsize=8.5)
ax.set_xlim(-.35, 1.42); ax.set_ylim(-.25, 1.55); ax.set_aspect("equal")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
fig.tight_layout()
save(fig, "C1-n3")
