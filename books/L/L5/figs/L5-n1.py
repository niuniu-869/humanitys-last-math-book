import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# 技术系数矩阵与工业部门增加 1 元的最终需求
A = np.array([[0.2, 0.4],
              [0.4, 0.3]], dtype=float)
d = np.array([0.0, 1.0], dtype=float)

# S_k = d + A d + ... + A^k d，分量 1 为农业，分量 2 为工业
ks = np.arange(16)
terms = []
term = d.copy()
cumulative = np.zeros(2, dtype=float)
for k in ks:
    if k == 0:
        term = d.copy()
    elif k > 0:
        term = A @ term
    cumulative = cumulative + term
    terms.append(cumulative.copy())
S = np.asarray(terms)
agriculture = S[:, 0]
industry = S[:, 1]

fig, ax = new_fig(14.5, 8.5)
ax.set_xlim(-0.25, 15.75)
ax.set_ylim(0.0, 2.2)
ax.set_xticks(np.arange(0, 16, 1))
ax.set_yticks(np.arange(0, 2.21, 0.2))
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.65, zorder=0)

# 两条累计曲线：工业实线实心圆，农业虚线空心圆
ax.plot(ks, industry, color=C.BLUE, lw=2.2, ls="-", zorder=3)
ax.scatter(ks, industry, s=27, marker="o", facecolors=C.BLUE, edgecolors=C.BLUE, linewidths=0.8, zorder=4)
ax.plot(ks, agriculture, color=C.RED, lw=1.9, ls="--", zorder=3)
ax.scatter(ks, agriculture, s=29, marker="o", facecolors=C.PAPER, edgecolors=C.RED, linewidths=1.4, zorder=4)

# 极限水平线，用点线与曲线区分
ax.axhline(2.0, color=C.GRAY, lw=1.25, ls=":", zorder=1)
ax.axhline(1.0, color=C.GRAY, lw=1.25, ls=":", zorder=1)
label(ax, "2：工业的极限", (15.0, 2.0), offset=(-2, 7), color=C.INK, ha="right")
label(ax, "1：农业的极限", (15.0, 1.0), offset=(-2, 7), color=C.INK, ha="right")

# 必要的短标签
label(ax, "工业", (9.0, industry[9]), offset=(7, 7), color=C.BLUE)
label(ax, "农业", (9.0, agriculture[9]), offset=(7, -15), color=C.RED)

# 首轮直接消耗注释，置于 k=0 与 k=1 之间的空白区域
label(ax, "第 1 轮：直接消耗 $A\\boldsymbol{e}_2=(0.4,0.3)$", (0.35, 2.14),
      offset=(0, 0), color=C.INK, ha="left", va="top")

ax.set_xlabel("轮数 $k$")
ax.set_ylabel("累计总产出（元）")

save(fig, "L5-n1")
