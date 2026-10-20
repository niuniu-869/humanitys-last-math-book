import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label

J = np.array([[1.0, 1.0], [0.0, 1.0]])
O = np.array([0.0, 0.0])
fig, ax = new_fig(13, 8.2)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-1.5, 2.3); ax.set_ylim(-0.35, 1.95)
ax.set_xticks(np.arange(-1.5, 2.01, 0.5)); ax.set_yticks(np.arange(0, 1.51, 0.5))
ax.grid(True, color=C.LIGHT, lw=0.7, zorder=0)
ax.axhline(0, color=C.GRAY, lw=0.9, zorder=1); ax.axvline(0, color=C.GRAY, lw=0.9, zorder=1)

# 水平方向：不转向
arrow(ax, O, np.array([1.0, 0.0]), color=C.INK, lw=2.6)
label(ax, "水平方向：不转向", (1.0, 0.0), offset=(-30, -16), fontsize=9)

for v, push, lo in [((1.0, 0.5), "推 0.5", (-38, 3)), ((0.0, 1.0), "推 1", (-30, 3)), ((-1.0, 1.5), "推 1.5", (-34, 3))]:
    v = np.array(v); w = J @ v
    ax.annotate("", xy=v, xytext=O, arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.5, linestyle="--",
                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=3)
    ax.annotate("", xy=w, xytext=O, arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.8,
                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=4)
    ax.annotate("", xy=w, xytext=v, arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.1, linestyle=":",
                shrinkA=3, shrinkB=3, mutation_scale=9), zorder=4)
    if v[1] != 0.5:  # 高度 0.5 那一对靠得太近，坐标从网格读
        label(ax, f"$({v[0]:g},{v[1]:g})$", v, offset=lo, fontsize=8.5, color=C.GRAY)
        label(ax, f"$({w[0]:g},{w[1]:g})$", w, offset=(5, 2), fontsize=8.5)
    label(ax, push, (v + w) / 2 + np.array([0.12, 0]), offset=(0, 4), fontsize=8.5)

ax.text(0.99, 0.99, "虚线：原来的箭头\n实线：剪切后的箭头\n点线：水平推动", transform=ax.transAxes,
        ha="right", va="top", fontsize=8.5,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor=C.GRAY, lw=0.6))
save(fig, "L12-n4")
