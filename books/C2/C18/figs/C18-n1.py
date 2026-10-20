import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(0.0, 4.0 * np.pi, 1601)
y_star = 0.5 * x * np.sin(x)
y_upper = 0.5 * x
y_lower = -0.5 * x
y_hom = np.sin(x)

fig, ax = new_fig(14.5, 7.8)
ax.set_xlim(0.0, 4.0 * np.pi)
ax.set_ylim(-7.0, 7.0)
ax.set_xticks(np.arange(5) * np.pi)
ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])
ax.set_yticks([-6, -3, 0, 3, 6])
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.7, zorder=0)
ax.axhline(0.0, color=C.GRAY, lw=0.8, zorder=1)

ax.plot(x, y_star, color=C.BLUE, lw=2.0, ls="-", zorder=3, label=r"$y^*=\frac{x}{2}\sin x$")
ax.plot(x, y_upper, color=C.GRAY, lw=1.25, ls="--", zorder=2, label=r"$y=\pm\frac{x}{2}$")
ax.plot(x, y_lower, color=C.GRAY, lw=1.25, ls="--", zorder=2)
ax.plot(x, y_hom, color=C.RED, lw=1.35, ls=":", zorder=2, label=r"$y=\sin x$（摆幅不变）")

# 两条虚线外侧的空白处：文字底/顶边与虚线保持约 0.4–0.5 个 y 单位的净空，
# 水平方向落在 2π 与 3π 两条网格线之间，不压线也不出界。
x_lab = 2.3 * np.pi
y_lab = 0.5 * x_lab
label(ax, r"$y=\frac{x}{2}$", (x_lab, y_lab), offset=(0, 8), ha="center", va="bottom", color=C.INK)
label(ax, r"$y=-\frac{x}{2}$", (x_lab, -y_lab), offset=(0, -8), ha="center", va="top", color=C.INK)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)

ax.set_xlabel(r"$x$")
ax.set_ylabel(r"$y$")
save(fig, "C18-n1")
