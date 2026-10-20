import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle
from itertools import permutations

expected = [("上海", "北京", "成都", "广州"), ("上海", "广州", "成都", "北京"),
            ("广州", "上海", "成都", "北京"), ("广州", "成都", "上海", "北京")]
valid = [p for p in permutations(["北京", "上海", "广州", "成都"])
         if (p[1] != "北京" or p[3] == "广州") and p[0] not in ("北京", "成都")
         and p[2] in ("成都", "上海") and p[3] != "上海"]
assert set(valid) == set(expected)
fig, ax = new_fig(19, 13)
ax.set(xlim=(-.1, 13.1), ylim=(-.3, 10.3))
ax.axis("off")

def box(x, y, text, w=2, h=.62, fs=10):
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h, facecolor=C.PAPER, edgecolor=C.INK, lw=1, zorder=3))
    label(ax, text, (x, y), ha="center", va="center", fontsize=fs)

def edge(a, b, ls="-"):
    ax.plot([a[0], b[0]], [a[1], b[1]], color=C.INK, ls=ls, lw=1, zorder=1)

box(6, 9.6, "例 5 的四条条件", w=3.5)
for x in (3, 9):
    edge((6, 9.29), (x, 8.31))
box(3, 8, "甲上海")
box(9, 8, "甲广州")
edge((3, 7.69), (3, 6.81))
edge((9, 7.69), (7.1, 6.81))
edge((9, 7.69), (10.7, 6.81))
box(3, 6.5, "丙成都")
box(7.1, 6.5, "丙成都")
box(10.7, 6.5, "丙上海")
label(ax, "上海已被甲占", (1.25, 7.15), ha="center", fontsize=8)
leaf_x = [1.5, 4.3, 7.1, 10.7]
for i, x in enumerate(leaf_x):
    parent = 3 if i < 2 else x
    edge((parent, 6.19), (x, 3.25))
    p = expected[i]
    box(x, 2.25, f"安排 {i+1}\n甲{p[0]}  乙{p[1]}\n丙{p[2]}  丁{p[3]}", w=2.65, h=2, fs=9)
label(ax, "丁不去上海", (7.1, 4.8), (8, 0), ha="left", fontsize=8)
# A rejected candidate is a side branch, not a fifth feasible leaf.
edge((10.7, 6.19), (12.35, 5.45), ls="--")
label(ax, r"$\times$", (12.45, 5.3), ha="center", va="center", fontsize=18)
label(ax, "乙北京\n⇒ 丁广州\n（甲已占）", (12.1, 4.6), ha="center", va="top", fontsize=8)
save(fig, "K13-n6")
