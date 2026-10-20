import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 6)
ax.axis("off")
x = np.arange(10); y = np.zeros(10)
ax.scatter(x, y, s=90, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3)
for i in range(9): label(ax, str(i+1), (i+0.5, 0.25), offset=(0, 0), ha="center")
for k in [3, 7]: ax.plot([k-0.5, k-0.5], [-0.38, 0.48], color=C.INK, lw=2.6, ls="-")
for a, b, t in [(0, 2.5, "第一人 3 颗"), (2.5, 6.5, "第二人 4 颗"), (6.5, 9, "第三人 3 颗")]:
    ax.annotate("", xy=(b, -0.55), xytext=(a, -0.55), arrowprops=dict(arrowstyle="-[", lw=1.0, color=C.INK, mutation_scale=10))
    label(ax, t, ((a+b)/2, -0.78), ha="center")
label(ax, "(3,4,3)", (4.5, -1.15), ha="center")
ax.text(4.5, -1.65, r"分法 ↔ 从 9 个空隙选 2 个，$\mathrm{C}_9^2=36$", ha="center")
ax.set_xlim(-0.8, 9.8); ax.set_ylim(-1.95, 0.7)
save(fig, "Z5-n3")
