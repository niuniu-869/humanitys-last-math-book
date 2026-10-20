import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(15, 8); ax.axis("off"); ax.set_xlim(-0.3, 10.3); ax.set_ylim(-1.6, 4.3)
pairs = ["{1,10}","{2,9}","{3,8}","{4,7}","{5,6}"]
for i, p in enumerate(pairs):
    x = 1 + i*2
    ax.add_patch(Rectangle((x-.8, 2.0), 1.6, 1.2, fc=C.LIGHT if i==1 else C.PAPER, ec=C.INK, lw=1.8))
    label(ax, p, (x, 2.6), ha="center", va="center", fontsize=12)
    label(ax, f"盒 {i+1}", (x, 3.55), ha="center")
    label(ax, "和 = 11", (x, 1.75), ha="center", va="top", fontsize=9)
taken = {0:[1], 1:[2,9], 2:[3], 3:[4], 4:[5]}
for i, v in taken.items():
    x = 1 + i*2
    xs = [x] if len(v)==1 else [x-.4, x+.4]
    for xx, num in zip(xs, v):
        ax.add_patch(FancyArrowPatch((xx, .15), (xx, 1.45), arrowstyle="-|>", mutation_scale=11, lw=1.4, color=C.INK))
        ax.scatter([xx],[0],s=40,color=C.INK,zorder=5)
        label(ax, str(num), (xx,-.15), ha="center", va="top")
label(ax, "取出的 6 个数 1,2,3,4,5,9；盒 2 收到 2 和 9，两数之和 $2+9=11$（阴影）", (5, -1.1), ha="center", va="top")
save(fig, "Z5-n7")
