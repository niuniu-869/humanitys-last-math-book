import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(11.5, 8.0)
eps = 0.5
delta = min(1.0, eps / 3.0)
x = np.linspace(0.5, 1.5, 800)

ax.add_patch(Rectangle((1 - delta, 1 - eps), 2 * delta, 2 * eps,
                       facecolor=C.LIGHT, edgecolor="none", zorder=0))
ax.plot(x, x**2, color=C.INK, lw=1.8, ls="-", zorder=3)
ax.axhline(1 + eps, color=C.GRAY, lw=1.0, ls="--", zorder=1)
ax.axhline(1 - eps, color=C.GRAY, lw=1.0, ls="--", zorder=1)
ax.axvline(1 - delta, color=C.GRAY, lw=1.0, ls="--", zorder=1)
ax.axvline(1 + delta, color=C.GRAY, lw=1.0, ls="--", zorder=1)
dot(ax, (1, 1), size=30)

label(ax, r"$y=x^2$", (1.28, 2.07), offset=(0, 0))
label(ax, r"$\delta=1/6$", (0.61, 1.73), offset=(0, 0))
label(ax, "小方框", (1.0, 0.58), offset=(0, 0), ha="center")

ax.set_xlim(0.45, 1.57); ax.set_ylim(0.25, 2.28)
ax.set_xticks([0.5, 5/6, 1, 7/6, 1.5])
ax.set_xticklabels(["0.5", "$1-\\delta$\n$5/6$", "1", "$1+\\delta$\n$7/6$", "1.5"])
ax.set_yticks([0.5, 1.0, 1.5, 2.0])
ax.set_yticklabels([r"$1-\varepsilon=0.5$", "1", r"$1+\varepsilon=1.5$", "2"])
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
assert np.isclose(delta, 1/6)
assert (1-delta)**2 > 1-eps and (1+delta)**2 < 1+eps
fig.subplots_adjust(left=0.25, bottom=0.20, right=0.97, top=0.96)
save(fig, "C3-n1")
