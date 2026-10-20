import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import PathPatch
from matplotlib.path import Path

results = [("HHH", 3), ("HHT", 2), ("HTH", 2), ("THH", 2),
           ("HTT", 1), ("THT", 1), ("TTH", 1), ("TTT", 0)]
assert [sum(ch == "H" for ch in r) for r, _ in results] == [x for _, x in results]

fig, ax = new_fig(16, 8)
ax.set(xlim=(-0.4, 11.5), ylim=(-0.7, 8.8))
ax.axis("off")

for i, (outcome, value) in enumerate(results):
    y = 8 - i
    ax.add_patch(FancyBboxPatch((0.1, y - 0.38), 1.15, 0.76,
                                boxstyle="round,pad=0.03,rounding_size=0.04",
                                facecolor=C.PAPER, edgecolor=C.INK, lw=0.9))
    label(ax, outcome, (0.675, y), ha="center", va="center", fontsize=9)
    target_x = 7.45 + value * 0.95
    arrow(ax, (1.35, y), (target_x - 1.35, 1.0 - y), color=C.INK, lw=0.85)

ax.plot([7.45, 10.30], [1.0, 1.0], color=C.INK, lw=1.1)
for value in range(4):
    x = 7.45 + value * 0.95
    ax.plot([x, x], [0.9, 1.1], color=C.INK, lw=1.0)
    dot(ax, (x, 1.0), color=C.INK, size=20)
    label(ax, str(value), (x, 0.65), ha="center", va="top", fontsize=10)
counts = {0: 1, 1: 3, 2: 3, 3: 1}
for value in range(4):
    x = 7.45 + value * 0.95
    label(ax, f"{counts[value]} 个", (x, -0.03), ha="center", va="top", fontsize=9)
label(ax, "$X$ 的取值", (10.3, 1.0), offset=(4, 0), va="center", fontsize=10)
label(ax, r"$\{X=2\}$", (9.35, 3.08), ha="center", va="bottom", fontsize=10)
brace = Path([(8.92, 2.75), (8.92, 2.94), (9.25, 2.75), (9.35, 3.0),
              (9.45, 2.75), (9.78, 2.94), (9.78, 2.75)],
             [Path.MOVETO] + [Path.CURVE4] * 6)
ax.add_patch(PathPatch(brace, fill=False, edgecolor=C.INK, lw=0.9))
save(fig, "P3-n1")
