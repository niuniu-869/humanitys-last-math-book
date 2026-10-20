import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from itertools import permutations

solutions = []
for a, b, c, d in permutations(range(1, 5)):
    if sum((a < b, a == 4, a < d, b != 1, b != 3)) == 1:
        solutions.append((a, b, c, d))
assert solutions == [(3, 1, 4, 2)]
fig, ax = new_fig(18, 16)
ax.set(xlim=(0, 12), ylim=(0, 12.3))
ax.axis("off")

def box(x, y, text, w, h=.78, bold=False):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                 boxstyle="round,pad=0.05,rounding_size=0.1",
                 facecolor=C.PAPER, edgecolor=C.INK, lw=2 if bold else 1))
    label(ax, text, (x, y), ha="center", va="center", fontsize=10)

def link(p, q, dashed=False):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11,
                 lw=1.2, ls="--" if dashed else "-", color=C.INK))

box(5.8, 11.65, "恰有一句真话", 3.2)
link((4.7, 11.21), (2.5, 10.45), True)
link((6.9, 11.21), (8.2, 10.45))
box(2.5, 9.9, "假设第 2 句真\n甲第 4", 4.3, 1)
box(8.2, 9.9, "第 2 句假", 3.3, 1)
link((2.5, 9.35), (2.5, 8.75), True)
box(2.5, 7.85, "第 1、3 句假\n第 4、5 句也须假\n乙第 1 且乙第 3", 4.3, 1.65)
label(ax, "× 矛盾", (2.5, 6.55), ha="center", fontsize=12)
link((7.4, 9.35), (6.6, 8.75), True)
link((9, 9.35), (10, 8.75))
box(6.5, 8.1, "假设第 4 句真\n乙不是第 1", 3.2, 1.1)
box(10, 8.1, "第 4 句假\n乙是第 1", 3.2, 1.1)
link((6.5, 7.5), (6.5, 6.95), True)
link((10, 7.5), (10, 6.95))
box(6.5, 5.55, "其余四句全假\n乙、丁都比甲靠前\n乙第 3，甲非第 4\n但甲只能第 4", 3.3, 2.65)
label(ax, "× 矛盾", (6.5, 3.65), ha="center", fontsize=12)
box(10, 5.55, "第 1 句假\n第 5 句是唯一真话\n第 3 句假：丁在甲前\n第 2 句假：甲非第 4", 3.3, 2.65)
link((10, 4.17), (10, 2.65))
box(9.3, 1.95, "名次：乙、丁、甲、丙", 4.9, 1.05, bold=True)
save(fig, "K12-n3")
