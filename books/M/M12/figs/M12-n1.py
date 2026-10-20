import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, C, new_fig, save, arrow, label
from matplotlib.patches import Rectangle
from matplotlib.colors import to_rgba

# 头 1 与头 2 用两级浅灰；仍然只取 figstyle 的灰阶。
LIGHT2 = to_rgba(C.LIGHT, 0.45)

# 尺寸：3 行 × 4 列，单元 0.68；每段 3×2，权重 3×3。
CW = 0.68
W4, H3, W2 = 4 * CW, 3 * CW, 2 * CW

# 三条水平带：头 1 在上、X/QKV 在中、头 2 在下。
YC, YH1, YH2 = 5.00, 8.04, 1.96


def matrix(ax, x, y, rows, cols, title=None, fill=C.PAPER, halves=None,
           split=False, title_fs=8.5, title_va="bottom", title_gap=0.12,
           lw=1.05):
    w, h = cols * CW, rows * CW
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fill, edgecolor="none",
                           zorder=1))
    if halves is not None:
        ax.add_patch(Rectangle((x, y), w / 2, h, facecolor=halves[0],
                               edgecolor="none", zorder=1))
        ax.add_patch(Rectangle((x + w / 2, y), w / 2, h, facecolor=halves[1],
                               edgecolor="none", zorder=1))

    # 网格线；中缝留给虚线，避免实线与虚线叠在一起。
    for i in range(1, cols):
        if split and cols == 4 and i == 2:
            continue
        ax.plot([x + i * w / cols] * 2, [y, y + h], color=C.GRAY, lw=0.5,
                zorder=3)
    for j in range(1, rows):
        ax.plot([x, x + w], [y + j * h / rows] * 2, color=C.GRAY, lw=0.5,
                zorder=3)

    if split:
        sx = x + w / 2
        ax.plot([sx, sx], [y, y + h], color=C.INK, lw=1.0,
                ls=(0, (3.2, 2.6)), zorder=5)

    ax.add_patch(Rectangle((x, y), w, h, facecolor="none", edgecolor=C.INK,
                           lw=lw, zorder=4))

    if title:
        ty = y + h + title_gap if title_va == "bottom" else y - title_gap
        label(ax, title, (x + w / 2, ty), ha="center", va=title_va,
              fontsize=title_fs)


def connect(ax, p0, p1, lw=1.2):
    arrow(ax, p0, (p1[0] - p0[0], p1[1] - p0[1]), color=C.INK, lw=lw)


fig, ax = new_fig(29.5, 9.7)
ax.set_xlim(0, 29.5)
ax.set_ylim(1.2, 10.9)
ax.axis("off")

# ---------------- 中间一行：X -> Q, K, V（各 3×4） ----------------
matrix(ax, 0.40, YC, 3, 4, "X（3×4）", title_fs=8.5)

QX, KX, VX = 5.80, 8.92, 12.04
for xx, name in ((QX, "Q"), (KX, "K"), (VX, "V")):
    matrix(ax, xx, YC, 3, 4, halves=(C.LIGHT, LIGHT2), split=True)
    # 单行标题紧贴方框上沿；向上的短箭头贴左半格左侧走，避开标题。
    label(ax, f"{name}（3×4）", (xx + W4 / 2, YC + H3 + 0.10),
          ha="center", va="bottom", fontsize=8.5)

connect(ax, (3.12, YC + H3 / 2), (QX, YC + H3 / 2), lw=1.3)
label(ax, "乘 $W_Q,W_K,W_V$", (4.46, YC + 1.18), ha="center", va="bottom",
      fontsize=8.0)

# ---------------- 头 1：上支路，取每块的左段 ----------------
for xx, name in ((QX, "$Q_1$"), (KX, "$K_1$"), (VX, "$V_1$")):
    matrix(ax, xx, YH1, 3, 2, name, fill=C.LIGHT, title_fs=8.5)

matrix(ax, 15.70, YH1, 3, 3, "3×3 权重", fill=C.LIGHT, title_fs=8.0)
matrix(ax, 19.10, YH1, 3, 2, "3×2 输出", fill=C.LIGHT, title_fs=8.0)

connect(ax, (VX + W2, YH1 + H3 / 2), (15.70, YH1 + H3 / 2), lw=1.25)
label(ax, "$Q_1,K_1,V_1$", (14.55, YH1 + H3 / 2 + 0.12), ha="center",
      va="bottom", fontsize=7.8)
connect(ax, (17.74, YH1 + H3 / 2), (19.10, YH1 + H3 / 2), lw=1.25)
label(ax, "$O_1$", (18.42, YH1 + H3 / 2 + 0.12), ha="center", va="bottom",
      fontsize=8.0)

# 头 1 的标题放在整个支路的左侧空白处。
label(ax, "头 1（取左段）", (5.45, 9.45), ha="right", va="center", fontsize=10.5)
label(ax, "$Q_1,K_1,V_1$（各 3×2）", (5.45, 8.83), ha="right", va="center",
      fontsize=8.0)

# ---------------- 头 2：下支路，取每块的右段 ----------------
for xx, name in ((QX + W2, "$Q_2$"), (KX + W2, "$K_2$"),
                 (VX + W2, "$V_2$")):
    matrix(ax, xx, YH2, 3, 2, name, fill=LIGHT2, title_fs=8.5,
           title_va="top")

matrix(ax, 15.70, YH2, 3, 3, "3×3 权重", fill=LIGHT2, title_fs=8.0,
       title_va="top")
matrix(ax, 19.10, YH2, 3, 2, "3×2 输出", fill=LIGHT2, title_fs=8.0,
       title_va="top")

connect(ax, (VX + W4, YH2 + H3 / 2), (15.70, YH2 + H3 / 2), lw=1.25)
connect(ax, (17.74, YH2 + H3 / 2), (19.10, YH2 + H3 / 2), lw=1.25)
label(ax, "$O_2$", (18.42, YH2 + H3 / 2 + 0.12), ha="center", va="bottom",
      fontsize=8.0)

label(ax, "头 2（取右段）", (6.80, 3.37), ha="right", va="center", fontsize=10.5)
label(ax, "$Q_2,K_2,V_2$（各 3×2）", (6.80, 2.65), ha="right", va="center",
      fontsize=8.0)

# ---------------- 中缝上下的短箭头：从每块左/右半格进入对应支路 ----------------
for xx in (QX + 0.22, KX + 0.22, VX + 0.22):
    connect(ax, (xx, YC + H3), (xx, YH1), lw=1.2)
for xx in (QX + W2 + W2 / 2, KX + W2 + W2 / 2, VX + W2 + W2 / 2):
    connect(ax, (xx, YC), (xx, YH2 + H3), lw=1.2)

# ---------------- 两个头输出 O1、O2 汇到拼接条，再乘 W_O ----------------
# O1、O2 先到一个竖向汇流条，再单箭头进入 3×4 拼接块。
ax.plot([20.46, 21.05], [YH1 + H3 / 2, YH1 + H3 / 2], color=C.INK, lw=1.0,
        zorder=2)
ax.plot([20.46, 21.05], [YH2 + H3 / 2, YH2 + H3 / 2], color=C.INK, lw=1.0,
        zorder=2)
ax.plot([21.05, 21.05], [YH2 + H3 / 2, YH1 + H3 / 2], color=C.INK, lw=1.0,
        zorder=2)
connect(ax, (21.05, YC + H3 / 2), (22.20, YC + H3 / 2), lw=1.25)
label(ax, "拼接", (21.63, YC + H3 / 2 + 0.14), ha="center", va="bottom",
      fontsize=8.0)

matrix(ax, 22.20, YC, 3, 4, "$3\\times4$（$O_1$｜$O_2$）",
       halves=(C.LIGHT, LIGHT2), split=True, title_fs=8.0)

connect(ax, (24.92, YC + H3 / 2), (26.30, YC + H3 / 2), lw=1.3)
label(ax, "$\\times\\,W_O$", (25.61, YC + H3 / 2 + 0.14), ha="center",
      va="bottom", fontsize=9.0)

matrix(ax, 26.30, YC, 3, 4, "输出（3×4）", title_fs=8.5)

save(fig, "M12-n1")
