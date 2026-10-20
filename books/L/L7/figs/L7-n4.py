import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, dot, label
from matplotlib.patches import Polygon

fig, axs = new_fig(17, 7, ncols=3)
titles = ["对称伸缩①：秩 2", "投影④：秩 1", "零矩阵：秩 0"]
for ax, ttl in zip(axs, titles):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-0.5, 3.5); ax.set_ylim(-0.5, 3.5)
    ax.set_xticks([0, 1, 2, 3]); ax.set_yticks([0, 1, 2, 3])
    for v in range(0, 4):
        ax.plot([v, v], [-0.5, 3.5], color=C.LIGHT, lw=0.7, ls=":", zorder=0)
        ax.plot([-0.5, 3.5], [v, v], color=C.LIGHT, lw=0.7, ls=":", zorder=0)
    ax.axhline(0, color=C.GRAY, lw=0.8); ax.axvline(0, color=C.GRAY, lw=0.8)
    ax.add_patch(Polygon([(0, 0), (1, 0), (1, 1), (0, 1)], closed=True, fill=False, ec=C.INK, lw=1.0, ls=(0, (3, 2)), zorder=2))
    ax.set_title(ttl)
axs[0].text(0.0, -0.2, "虚线：原来的正方形", transform=axs[0].transAxes, fontsize=9, va="top")
axs[0].add_patch(Polygon([(0, 0), (2, 1), (3, 3), (1, 2)], closed=True, fc=C.LIGHT, ec=C.INK, lw=1.6, zorder=1))
axs[0].text(0.0, -0.32, "阴影：像，还是一块面积", transform=axs[0].transAxes, fontsize=9, va="top")
for p in [(2, 1), (3, 3), (1, 2)]:
    dot(axs[0], p, size=14)
label(axs[0], "$(2,1)$", (2, 1), offset=(4, -10), fontsize=9)
label(axs[0], "$(1,2)$", (1, 2), offset=(-26, 2), fontsize=9)
label(axs[0], "$(3,3)$", (3, 3), offset=(-30, 2), fontsize=9)
axs[1].plot([-0.5, 3.5], [-0.5, 3.5], color=C.GRAY, lw=0.9)
axs[1].plot([0, 1], [0, 1], color=C.INK, lw=3.2, zorder=3)
dot(axs[1], (1, 1), size=14)
axs[1].text(0.0, -0.2, "粗实线：像，压成一条线段", transform=axs[1].transAxes, fontsize=9, va="top")
label(axs[1], "$(1,1)$", (1, 1), offset=(6, -6), fontsize=9)
label(axs[1], "$y=x$", (2.8, 2.8), offset=(4, -10), fontsize=9, color=C.GRAY)
dot(axs[2], (0, 0), size=30)
axs[2].text(0.0, -0.2, "像只剩原点一个点", transform=axs[2].transAxes, fontsize=9, va="top")
fig.subplots_adjust(wspace=0.3)
save(fig, "L7-n4")
