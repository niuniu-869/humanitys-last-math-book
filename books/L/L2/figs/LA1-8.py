import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, np, plt, save

fig, ax = new_fig(11.0, 7.5)

idx = np.array([1.0, 2.0, 3.0])
val = np.array([3.0, 0.0, 3.0])
m = 2.0                                   # 均值 = 投影系数 t

# 均值线（投影 p=(2,2,2)）
ax.plot([0.5, 3.75], [m, m], color=C.TEAL, lw=1.8, zorder=2)
# 离差（残差 e=(1,-2,1)）
for x, y in zip(idx, val):
    ax.plot([x, x], [m, y], color=C.TEAL, lw=1.7, ls=(0, (4, 2.5)), zorder=3)

# 数据点与垂足
ax.scatter(idx, val, s=40, color=C.BLUE, zorder=5)
ax.scatter(idx, np.full(3, m), s=16, color=C.TEAL, zorder=5)

# 标注
label(ax, r"均值 $\bar x=2$", (0.5, 2.0), offset=(0, -12), ha="left", va="top", color=C.TEAL)
label(ax, r"$\boldsymbol{b}=(3,0,3)$", (2, 0), offset=(12, -2), ha="left", va="center", color=C.BLUE)
label(ax, "$+1$", (1, 2.5), offset=(8, 0), ha="left", va="center", color=C.TEAL)
label(ax, "$-2$", (2, 1.0), offset=(8, 0), ha="left", va="center", color=C.TEAL)
label(ax, "$+1$", (3, 2.5), offset=(8, 0), ha="left", va="center", color=C.TEAL)

ax.set_xlim(0.35, 4.15)
ax.set_ylim(-0.95, 3.95)
ax.set_xticks([1, 2, 3])
ax.set_yticks([0, 1, 2, 3])
ax.set_xlabel("分量编号 $i$")
ax.set_ylabel("数值 $x_i$")

save(fig, "LA1-8")
