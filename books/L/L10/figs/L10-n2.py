import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, dot, label

# 例 7 的数据与拟合直线 y=-0.5+1.6t
t = np.array([1.0, 2.0, 3.0, 4.0])
y = np.array([1.0, 3.0, 4.0, 6.0])
yhat = -0.5 + 1.6 * t
e = y - yhat                      # 残差 -0.1, 0.3, -0.3, 0.1
tbar, ybar = 2.5, 3.5

fig, (ax, ax2) = new_fig(13.5, 6.4, ncols=2, gridspec_kw={"width_ratios": [1.15, 1.0], "wspace": 0.35})

# 左图：数据点、拟合直线、平均点、竖直残差（虚线）
ax.set_xlim(0, 5); ax.set_ylim(0, 7)
ax.set_xticks(range(0, 6)); ax.set_yticks(range(0, 8))
ax.grid(True, color=C.LIGHT, lw=0.6)
ax.set_xlabel("$t$"); ax.set_ylabel("$y$")
tt = np.array([0.4, 4.7])
ax.plot(tt, -0.5 + 1.6 * tt, color=C.INK, lw=1.8)
label(ax, r"$y=-0.5+1.6t$", (0.75, -0.5 + 1.6 * 0.75), offset=(8, -4))
for ti, yi, yh in zip(t, y, yhat):
    ax.plot([ti, ti], [yi, yh], color=C.INK, lw=1.4, ls="--", zorder=3)
    dot(ax, (ti, yi), color=C.INK, size=26)
ax.scatter([tbar], [ybar], s=46, marker="s", facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.4, zorder=5)
label(ax, r"$(\bar t,\bar y)$", (tbar, ybar), offset=(-38, 0))

# 右图：把同样的残差单独画出来（纵轴放大），看清正负抵消
ax2.set_xlim(0.4, 4.6); ax2.set_ylim(-0.42, 0.42)
ax2.set_xticks([1, 2, 3, 4]); ax2.set_yticks([-0.3, -0.1, 0, 0.1, 0.3])
ax2.axhline(0, color=C.INK, lw=1.0)
ax2.grid(True, color=C.LIGHT, lw=0.6)
ax2.set_xlabel("$t$"); ax2.set_ylabel("残差 $e_i$（放大）")
for ti, ei in zip(t, e):
    ax2.plot([ti, ti], [0, ei], color=C.INK, lw=1.6, ls="--")
    ax2.scatter([ti], [ei], s=26, color=C.INK, zorder=4)
    label(ax2, f"{ei:+.1f}".replace("+", "+").replace("-", "−"), (ti, ei), offset=(6, -4 if ei < 0 else 2))
label(ax2, "四个残差之和为 0", (2.95, 0.36), offset=(0, 0))

save(fig, "L10-n2")
