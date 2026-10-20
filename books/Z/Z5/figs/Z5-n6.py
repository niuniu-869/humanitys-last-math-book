import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(14, 12); ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-3.0, 3.0); ax.set_ylim(-2.6, 3.6)
R = 1.5
for (cx, cy), nm in [((-0.8,0),"A"), ((0.8,0),"B"), ((0,1.4),"C")]:
    ax.add_patch(Circle((cx,cy), R, fill=False, ec=C.INK, lw=1.8))
ax.add_patch(Circle((0,0.45), .5, fc=C.LIGHT, ec="none", zorder=0))
label(ax, "$A$", (-2.1,-1.1), fontsize=13); label(ax, "$B$", (2.1,-1.1), fontsize=13); label(ax, "$C$", (1.4,2.6), fontsize=13)
def reg(x, y, a, b, fs=8): label(ax, f"{a}\n{b}", (x, y), ha="center", va="center", fontsize=fs)
reg(-1.65,-0.45,"1","净 1"); reg(1.65,-0.45,"1","净 1"); reg(0,2.4,"1","净 1")
reg(0,-0.75,"2","2−1=1"); reg(-0.95,1.0,"2","2−1=1"); reg(0.95,1.0,"2","2−1=1")
label(ax, "3\n3−3=0\n加回 1", (0,0.45), ha="center", va="center", fontsize=7.5)
ax.text(0,-2.2,"上行：在 $|A|+|B|+|C|$ 中被数的遍数\n下行：减两两交（中心再加三重交）之后", ha="center", va="top")
save(fig, "Z5-n6")
