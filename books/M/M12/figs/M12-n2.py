import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle


def table(ax, x, y, title, shade):
    cols, rows, cw = 4, 3, 1.25
    width = cols * cw
    ax.add_patch(Rectangle((x, y), width, rows, facecolor=C.PAPER, edgecolor="none"))
    if shade == "col":
        sx, sy, sw, sh = x + cw, y, cw, rows
    else:
        sx, sy, sw, sh = x, y + 1, width, 1
    ax.add_patch(Rectangle((sx, sy), sw, sh, facecolor=C.LIGHT, edgecolor="none"))

    # 网格线画在阴影之上，阴影里的 3/4 个格子仍然看得见。
    for i in range(1, cols):
        ax.plot([x + i * cw, x + i * cw], [y, y + rows], color=C.GRAY, lw=0.6, zorder=3)
    for j in range(1, rows):
        ax.plot([x, x + width], [y + j, y + j], color=C.GRAY, lw=0.6, zorder=3)

    ax.add_patch(Rectangle((x, y), width, rows, facecolor="none",
                           edgecolor=C.INK, lw=1.1, zorder=4))
    # 两幅图的阴影边框使用同一粗细，且与外框/网格严格对齐。
    ax.add_patch(Rectangle((sx, sy), sw, sh, facecolor="none",
                           edgecolor=C.INK, lw=1.3, zorder=5))

    for i in range(cols):
        label(ax, f"特征 {i + 1}", (x + (i + 0.5) * cw, y + rows + 0.14),
              ha="center", va="bottom", fontsize=7.5)
    for j in range(rows):
        label(ax, f"样本 {j + 1}", (x - 0.18, y + rows - j - 0.5),
              ha="right", va="center", fontsize=8.5)
    label(ax, title, (x + width / 2, y + rows + 0.62), ha="center", va="bottom",
          fontsize=11)
    return x + width / 2


fig, ax = new_fig(15, 7.0)
ax.set_xlim(-0.8, 14.4); ax.set_ylim(0.4, 6.9); ax.axis("off")

left_mid = table(ax, 0.8, 2.7, "批归一化：沿列", "col")
ax.annotate("", xy=(2.675, 5.45), xytext=(2.675, 2.95),
            arrowprops=dict(arrowstyle="<->", color=C.INK, lw=1.2, mutation_scale=9))
# 两处说明都放在整张表下方居中，位于底线与底部图例文字之间。
label(ax, "均值、方差", (left_mid, 2.25), ha="center", va="center")

right_mid = table(ax, 8.4, 2.7, "层归一化：沿行", "row")
ax.annotate("", xy=(13.15, 4.2), xytext=(8.65, 4.2),
            arrowprops=dict(arrowstyle="<->", color=C.INK, lw=1.2, mutation_scale=9))
label(ax, "均值、方差", (right_mid, 2.25), ha="center", va="center")

label(ax, "阴影的格子就是求统计量的那一组数", (7.5, 1.05), ha="center", va="center")
save(fig, "M12-n2")
