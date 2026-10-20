import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(14, 9); ax.axis("off"); ax.set_xlim(-6.2, 8.2); ax.set_ylim(-0.9, 5.8)
rows = [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1],[1,5,10,10,5,1]]
pos = {}
for n, r in enumerate(rows):
    y = 5.2 - n*0.95
    label(ax, f"$n={n}$", (-5.9, y), ha="left", va="center")
    for k, v in enumerate(r):
        x = (k - n/2)*1.3
        pos[(n,k)] = (x, y)
        label(ax, str(v), (x, y), ha="center", va="center", fontsize=12)
for k in (1,2):
    x, y = pos[(4,k)]
    ax.add_patch(Rectangle((x-.35, y-.3), .7, .6, fill=False, ec=C.INK, lw=2))
x, y = pos[(5,2)]
ax.add_patch(Rectangle((x-.4, y-.3), .8, .6, fc=C.LIGHT, ec=C.INK, lw=2, zorder=0))
for k in (1,2):
    sx, sy = pos[(4,k)]
    ax.add_patch(FancyArrowPatch((sx+(-0.05 if k==1 else 0.05), sy-.33), (x+(-0.25 if k==1 else 0.25), y+.33), arrowstyle="-|>", mutation_scale=12, lw=1.5, color=C.INK))
label(ax, "$4+6=10$", (x, y-.55), ha="center", va="center")
ax.text(3.6, 4.2, "第 $n$ 行是 $(a+b)^n$\n展开的系数，\n如 $n=3$：$1,3,3,1$", ha="left", va="top")
save(fig, "Z5-n5")
