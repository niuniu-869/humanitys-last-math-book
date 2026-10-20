import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(16, 8)
xs = np.arange(1, 6)
ax.set_xlim(-1.0, 5.65); ax.set_ylim(-2.6, 2.6); ax.axis("off")
def nodes(y, bold):
    for x in xs:
        b = bold and x <= 2
        ax.scatter([x], [y], s=520 if b else 380, facecolors=C.PAPER, edgecolors=C.INK, linewidths=2.6 if b else 1.4, zorder=4)
        label(ax, f"$a_{x}$", (x, y), ha="center", va="center")
def arr(y, s, e, rad, **kw):
    ax.add_patch(FancyArrowPatch((s+.2, y), (e-.2, y), connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>", mutation_scale=12, lw=1.5, **kw))
# 上排：普通归纳
nodes(1.5, False)
for s in range(1, 5):
    arr(1.5, s, s+1, 0, ls="--", color=C.GRAY)
label(ax, "普通归纳：\n只靠前一项", (-.95, 1.5), ha="left", va="center")
# 下排：本数列
nodes(-1.0, True)
for s, e in [(3, 4), (4, 5)]:
    arr(-1.0, s, e, 0, color=C.INK)
for s, e in [(2, 4), (3, 5)]:
    ax.add_patch(FancyArrowPatch((s+.1, -.7), (e-.1, -.7), connectionstyle="arc3,rad=-.45", arrowstyle="-|>", mutation_scale=12, lw=1.5, color=C.INK))
label(ax, "这个数列：\n$a_{m+1}$ 靠\n$a_m$ 和 $a_{m-1}$", (-.95, -1.0), ha="left", va="center")
label(ax, "$a_1,a_2$ 粗圈：直接验证（奠基两项）；$a_3$ 起由递推式得到", (3.0, -2.2), ha="center")
save(fig, "Z4-n4")
