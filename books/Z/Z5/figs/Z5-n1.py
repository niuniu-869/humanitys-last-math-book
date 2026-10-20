import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 8)
ax.axis("off")
levels = [[(0, 0, "甲")], [(1, 2, "乙"), (1, 1, "乙"), (1, 0, "乙")]]
ends = []
for i, y in enumerate([2, 1, 0]):
    for j, dy in enumerate([0.28, -0.28]):
        ends.append((2, y + dy, str(i * 2 + j + 1)))
for y in [2, 1, 0]:
    ax.plot([0.8, 1.8], [0, y], color=C.INK, ls="-")
    label(ax, f"路 {3-y:.0f}", (1.25, y/2), offset=(0, 4), ha="center")
for i, y in enumerate([2, 1, 0]):
    for j, dy in enumerate([0.28, -0.28]):
        yy = y + dy
        ax.plot([1.8, 2.8], [y, yy], color=C.INK, ls="-")
        label(ax, "a" if j == 0 else "b", (2.3, (y+yy)/2), offset=(2, 2), ha="center")
        dot(ax, (2.8, yy), ends[i*2+j][2], offset=(5, -4), size=18)
label(ax, "甲", (0.8, 0), offset=(-18, -4)); ax.scatter([0.8], [0], s=22, color=C.INK)
for y in [2, 1, 0]: dot(ax, (1.8, y), "乙", offset=(5, -4), size=18)
label(ax, "丙", (3.05, 1), offset=(0, 0), ha="left")
ax.text(1.8, -0.55, r"$3\times2=6$", ha="center", va="top")
ax.set_xlim(0.3, 3.7); ax.set_ylim(-0.9, 2.55)
save(fig, "Z5-n1")
