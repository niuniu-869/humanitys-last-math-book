import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle, Circle


X = 3.6          # 竖直主干所在位置
RX = 7.4         # 残差连线绕行所在的竖线
PLUS_R = 0.30

fig, ax = new_fig(9.8, 13.4)
ax.set_xlim(0, 9.4)
ax.set_ylim(0.25, 12.45)
ax.axis("off")


def box(y, h, w, text, fontsize=9.2):
    ax.add_patch(Rectangle((X - w / 2, y), w, h, facecolor=C.LIGHT,
                           edgecolor=C.INK, lw=1.1, zorder=2))
    label(ax, text, (X, y + h / 2), ha="center", va="center",
          fontsize=fontsize, linespacing=1.3)


def plus(y):
    ax.add_patch(Circle((X, y), PLUS_R, facecolor=C.PAPER,
                        edgecolor=C.INK, lw=1.2, zorder=5))
    label(ax, "+", (X, y), ha="center", va="center", fontsize=13)


def trunk(y0, y1):
    arrow(ax, (X, y0), (0, y1 - y0), color=C.INK, lw=1.8)


def nd(y):
    label(ax, "$n\\times d$", (X - 0.18, y), ha="right", va="center", fontsize=8)


def residual(y0, y1):
    # 从分叉点向右绕过 LN 与子层，再向左从右侧进入加号。
    ax.plot([X, RX, RX, 4.55], [y0, y0, y1, y1],
            color=C.INK, lw=1.0, ls="--", zorder=1)
    ax.annotate("", xy=(X + PLUS_R, y1), xytext=(4.55, y1),
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.0,
                                ls="--", shrinkA=0, shrinkB=0,
                                mutation_scale=9), zorder=1)


# ---------------- 第一个子层：LN -> 多头注意力 -> 加 ----------------
label(ax, "输入 X", (X, 0.55), ha="center", va="center", fontsize=10.5)
trunk(0.85, 2.15)
nd(1.20)
ax.add_patch(Circle((X, 1.60), 0.075, facecolor=C.INK,
                    edgecolor="none", zorder=7))

box(2.15, 0.80, 2.2, "LN", fontsize=10)
trunk(2.95, 3.55)
nd(3.25)
box(3.55, 1.40, 3.5, "多头注意力\n（带因果掩码）")
trunk(4.95, 5.55)
nd(5.25)
plus(5.85)
label(ax, "$X'$", (X - 0.42, 5.85), ha="right", va="center", fontsize=10.5)

residual(1.60, 5.85)
label(ax, "残差", (RX + 0.16, 3.55), ha="left", va="center", fontsize=8.5)

# ---------------- 第二个子层：LN -> 前馈层 -> 加 ----------------
trunk(6.15, 7.00)
nd(6.72)
ax.add_patch(Circle((X, 6.45), 0.075, facecolor=C.INK,
                    edgecolor="none", zorder=7))

box(7.00, 0.80, 2.2, "LN", fontsize=10)
trunk(7.80, 8.40)
nd(8.10)
box(8.40, 1.50, 3.5, "前馈层\n$d\\to 4d\\to d$")
trunk(9.90, 10.50)
nd(10.20)
plus(10.80)

residual(6.45, 10.80)
label(ax, "残差", (RX + 0.16, 8.45), ha="left", va="center", fontsize=8.5)

trunk(11.10, 11.75)
nd(11.42)
label(ax, "输出 Y", (X, 12.05), ha="center", va="center", fontsize=10.5)

save(fig, "M12-n5")
