import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle
from itertools import permutations

solutions = [p for p in permutations(range(4))
             if p[1] == 0 and p[0] != 2 and p[2] not in (1, 2)]
assert solutions == [(1, 0, 3, 2)]
steps = [[4, 6, 2, 5], [1, 4, 4, 4], [4, 3, 3, 5], [4, 6, 7, 5]]
direct = {(1, 0), (0, 2), (2, 1), (2, 2)}
fig, ax = new_fig(13, 10)
ax.set(xlim=(-.7, 4.25), ylim=(-1.05, 4.65))
ax.axis("off")
for j, city in enumerate(["北京", "上海", "广州", "成都"]):
    label(ax, city, (j + .5, 4.22), ha="center", va="center")
for i, person in enumerate("甲乙丙丁"):
    y = 3 - i
    label(ax, person, (-.3, y + .5), ha="center", va="center")
    for j in range(4):
        ax.add_patch(Rectangle((j, y), 1, 1, facecolor=C.LIGHT if (i, j) in direct else C.PAPER,
                               edgecolor=C.INK, lw=.9))
        ax.text(j + .45, y + .43, "✓" if solutions[0][i] == j else r"$\times$",
                ha="center", va="center", fontsize=19, color=C.INK)
        ax.text(j + .84, y + .82, "①②③④⑤⑥⑦"[steps[i][j] - 1],
                ha="center", va="center", fontsize=10, color=C.INK)
ax.add_patch(Rectangle((.03, -.62), .25, .25, facecolor=C.LIGHT, edgecolor=C.INK, lw=.8))
label(ax, "条件给出（①—③）", (.38, -.5), va="center", fontsize=9)
ax.add_patch(Rectangle((2.23, -.62), .25, .25, facecolor=C.PAPER, edgecolor=C.INK, lw=.8))
label(ax, "推出（④—⑦）", (2.58, -.5), va="center", fontsize=9)
label(ax, "圈内数字：填写顺序", (2, -.91), ha="center", fontsize=9)
save(fig, "K13-n1")
