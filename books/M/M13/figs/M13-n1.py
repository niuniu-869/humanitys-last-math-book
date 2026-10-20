import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch
from matplotlib.path import Path

fig, ax = new_fig(19, 13)
ax.set(xlim=(-0.25, 9.6), ylim=(-0.55, 8.1))
ax.axis("off")
xs = np.arange(6) * 1.25
words = ["猫", "坐", "在", "垫子", "上", "。"]
w, h = 0.95, 0.66

for y, masked in [(6.8, False), (2.5, True)]:
    for i, (x, word) in enumerate(zip(xs, words)):
        hidden = masked and i in (3, 5)
        ax.add_patch(Rectangle((x, y), w, h, facecolor=C.LIGHT if hidden else C.PAPER,
                               edgecolor=C.INK, lw=1.1))
        label(ax, "[掩]" if hidden else word, (x+w/2, y+h/2), ha="center", va="center")
    label(ax, "2 个标签" if masked else "5 个标签", (8.05, y+h/2), va="center")

label(ax, "下一个词：第 2 至第 6 个目标位置由前文预测", (0, 7.85), va="center")
for k in range(1, 6):
    y = 6.5 - (k-1)*0.39
    end = xs[k-1]+w
    ax.plot([0, 0, end, end], [y+0.12, y, y, y+0.12], color=C.INK, lw=0.9)
    target = xs[k]+w/2
    path = Path([(end, y), (target, y), (target, 6.25), (target, 6.77)],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(FancyArrowPatch(path=path, arrowstyle="-|>", mutation_scale=11,
                                color=C.INK, lw=1.1))

label(ax, "遮住再猜：用两侧的词猜被遮的位置", (0, 4.1), va="center")
# Four distinct dashed cue arrows, routed above the boxes.
for i, target_i, rad in [(0, 3, -0.22), (1, 3, -0.23), (2, 3, -0.24), (4, 3, 0.24)]:
    ax.add_patch(FancyArrowPatch((xs[i]+w/2, 3.2), (xs[target_i]+w/2, 3.2),
                                connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                mutation_scale=10, ls="--", color=C.INK, lw=1.0))
for i in (3, 5):
    arrow(ax, (xs[i]+w/2, 2.45), (0, -0.72), color=C.INK)
    label(ax, words[i], (xs[i]+w/2, 1.4), ha="center", va="center")
label(ax, "阴影方框 = 被遮住的词；实线箭头指向被预测的词；虚线箭头 = 作为线索被读到",
      (4.6, 0.15), ha="center", va="center", fontsize=8)
save(fig, "M13-n1")
