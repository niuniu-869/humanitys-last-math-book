import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(12, 7.5)
u, v, du, dv = 3.0, 2.0, 1.0, 0.8
ax.add_patch(Rectangle((0, 0), u, v, facecolor=C.PAPER, edgecolor=C.INK, lw=1.4, ls="-"))
ax.add_patch(Rectangle((u, 0), du, v, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.0, ls="-"))
ax.add_patch(Rectangle((0, v), u, dv, facecolor=C.LIGHT, edgecolor=C.INK, lw=1.0, ls="-"))
ax.add_patch(Rectangle((u, v), du, dv, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0, ls="--"))
label(ax, "$v\\,\\Delta u$", (u + du / 2, v / 2), offset=(0, 0), ha="center", va="center")
label(ax, "$u\\,\\Delta v$", (u / 2, v + dv / 2), offset=(0, 0), ha="center", va="center")
label(ax, "$\\Delta u\\,\\Delta v$", (u + du / 2, v + dv / 2),
      ha="center", va="center", fontsize=9)
label(ax, "除以 $h$ 后趋于 0", (3.1, 3.34), ha="center", fontsize=9)
ax.plot([3.5, 3.5, 3.1], [2.85, 3.08, 3.25], color=C.GRAY, lw=0.8)
label(ax, "$u$", (u / 2, 0), offset=(0, -19), ha="center")
label(ax, "$v$", (0, v / 2), offset=(-18, 0), ha="right", va="center")
label(ax, "$\\Delta u$", (u + du / 2, 0), offset=(0, -19), ha="center")
label(ax, "$\\Delta v$", (0, v + dv / 2), offset=(-18, 0), ha="right", va="center")
assert np.isclose((u + du) * (v + dv) - u * v, v * du + u * dv + du * dv)
ax.set_xlim(-0.65, 4.35); ax.set_ylim(-0.5, 3.65)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")
save(fig, "C4-n5")
