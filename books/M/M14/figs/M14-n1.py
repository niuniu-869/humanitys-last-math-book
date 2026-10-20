import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(22, 6.5)
fig.subplots_adjust(left=0.04, right=0.97, bottom=0.12, top=0.96)
ax.set(xlim=(-0.02, 1.025), ylim=(-0.36, 1.4))
ax.axis("off")
cuts = np.array([0, 0.6652, 0.9099, 1.0])
shown = [0.6652, 0.2447, 0.0900]
# Requested rounded cuts are retained; the final interval has length 0.0901.
for i, (left, right) in enumerate(zip(cuts[:-1], cuts[1:])):
    ax.add_patch(Rectangle((left, 0), right-left, 0.48,
                           facecolor=C.LIGHT if i != 1 else C.PAPER,
                           edgecolor=C.INK, lw=1.1))
    label(ax, f"第 {i+1} 个词\n{shown[i]:.4f}", ((left+right)/2, 0.24),
          ha="center", va="center", fontsize=8.5)
for x, text in zip(cuts, ["0", "0.6652", "0.9099", "1"]):
    ax.plot([x, x], [-0.045, 0], color=C.INK)
    label(ax, text, (x, -0.08), ha="center", va="top", fontsize=8.5)
dot(ax, (0.70, 0.48), size=30)
ax.scatter([0.95], [0.48], s=34, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
arrow(ax, (0.58, 1.09), (0.12, -0.53), color=C.INK, lw=1.0)
label(ax, r"$u=0.70$ → 第 2 个词", (0.57, 1.18), ha="center", va="center")
arrow(ax, (0.90, 0.91), (0.05, -0.35), color=C.INK, lw=1.0)
label(ax, r"$u=0.95$ → 第 3 个词", (0.88, 1.02), ha="center", va="center")
assert cuts[1] <= 0.70 < cuts[2]
assert cuts[2] <= 0.95 < cuts[3]
save(fig, "M14-n1")
