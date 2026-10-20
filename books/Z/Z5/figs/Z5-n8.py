import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(15, 8.5); ax.axis("off"); ax.set_xlim(-0.2, 9.2); ax.set_ylim(-4.6, 2.2)
for i, v in enumerate([4,7,5]):
    x = 0.4 + i*1.5
    ax.add_patch(Rectangle((x-.6, 0.6), 1.2, .8, fc=C.PAPER, ec=C.INK, lw=1.6))
    label(ax, f"$a_{i+1}={v}$", (x, 1.0), ha="center", va="center")
ax.text(5.0, 1.0, "前缀和 $S_j$ = 前 $j$ 项之和：\n$S_1=4,\\ S_2=11,\\ S_3=16$", ha="left", va="center")
label(ax, "按被 3 除的余数分盒", (0.4, -0.5), ha="left")
names = [("余数 0", "（空）", False), ("余数 1", "$S_1=4$，$S_3=16$", True), ("余数 2", "$S_2=11$", False)]
for i, (t, c, shade) in enumerate(names):
    x = 0.2 + i*3.0
    ax.add_patch(Rectangle((x, -2.8), 2.6, 1.6, fc=C.LIGHT if shade else C.PAPER, ec=C.INK, lw=1.8))
    label(ax, t, (x+1.3, -1.55), ha="center", va="center", fontsize=11)
    label(ax, c, (x+1.3, -2.3), ha="center", va="center", fontsize=10)
ax.text(3.5, -3.3, "$S_1$ 与 $S_3$ 同盒：$S_3-S_1=16-4=12=a_2+a_3$，被 3 整除", ha="center", va="top")
save(fig, "Z5-n8")
