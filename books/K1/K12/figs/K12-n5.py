import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from collections import Counter

rows = [("甲", "丁第 3", "丙第 4"), ("乙", "丁第 1", "丙第 4"),
        ("丙", "甲第 2", "丙第 4"), ("丁", "丙第 2", "乙第 1")]
counts = Counter(t for _, p, q in rows for t in (p, q))
assert counts["丙第 4"] == 3 and sorted(counts.values()) == [1, 1, 1, 1, 1, 3]
fig, ax = new_fig(17, 11)
ax.set(xlim=(0, 12), ylim=(0, 7.5))
ax.axis("off")
for i, (person, left, right) in enumerate(rows):
    y = 6.4 - i*1.7
    label(ax, person, (4.2, y), ha="center", va="center")
    for x, text in [(5.8, left), (8.7, right)]:
        ax.add_patch(FancyBboxPatch((x-1.1, y-.42), 2.2, .84,
                     boxstyle="round,pad=.03,rounding_size=.08",
                     facecolor=C.PAPER, edgecolor=C.INK,
                     lw=2.3 if text == "丙第 4" else 1))
        label(ax, text, (x, y), ha="center", va="center")
for y in (6.4, 4.7):
    ax.add_patch(FancyArrowPatch((9.86, y), (9.86, y-1.7),
                 connectionstyle="arc3,rad=-.5", arrowstyle="-",
                 color=C.INK, ls="--", lw=1.5))
label(ax, "出现 3 次", (10.55, 4.7), va="center")
ax.plot([5.8, 5.8], [5.96, 5.14], color=C.INK, ls="-", lw=1.5)
label(ax, "×", (5.8, 5.55), ha="center", va="center", fontsize=15)
label(ax, "若“丙第 4”为假\n两者须同真\n矛盾", (1.9, 5.55), ha="center", va="center")
save(fig, "K12-n5")
