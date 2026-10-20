import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(15.5, 6.5, ncols=2)
xx = np.linspace(0, 8.5, 600)
upper = np.sqrt(2*xx)
lower = -upper
line = xx - 4
poly_x = np.r_[np.linspace(2, 8, 240), np.linspace(8, 0, 300), np.linspace(0, 2, 120)]
poly_y = np.r_[poly_x[:240]-4, np.sqrt(2*poly_x[240:540]), -np.sqrt(2*poly_x[540:])]

for ax in axes:
    ax.plot(xx, upper, color=C.INK, lw=1.5)
    ax.plot(xx, lower, color=C.INK, lw=1.5)
    ax.plot(xx, line, color=C.INK, lw=1.5)
    ax.fill(poly_x, poly_y, color=C.LIGHT, zorder=0)
    ax.set(xlim=(-0.5, 9), ylim=(-3.5, 5), aspect="equal")
    ax.set_xticks([]); ax.set_yticks([])
    ax.axhline(0, color=C.GRAY, lw=0.55); ax.axvline(0, color=C.GRAY, lw=0.55)
    dot(ax, (2, -2), "(2,-2)", offset=(-34, -15), size=25)
    dot(ax, (8, 4), "(8,4)", offset=(5, 4), size=25)

axes[0].set_title("竖着切")
for xv in (1, 5):
    ytop = xv - 4
    ybottom = -np.sqrt(2*xv) if xv < 2 else ytop
    yhi = -np.sqrt(2*xv) if xv < 2 else np.sqrt(2*xv)
    axes[0].plot([xv, xv], [ytop, yhi], color=C.INK, ls="--", lw=1.3)
    axes[0].plot([xv-0.12, xv+0.12], [ytop, ytop], color=C.INK, ls="--", lw=1.0)
    axes[0].plot([xv-0.12, xv+0.12], [yhi, yhi], color=C.INK, ls="--", lw=1.0)
axes[0].axvline(2, color=C.INK, ls=":", lw=1.2)
label(axes[0], "在这里换边", (2, 4.6), ha="center", va="bottom")

axes[1].set_title("横着切")
yv = 1.0
xl, xr = yv**2/2, yv+4
axes[1].plot([xl, xr], [yv, yv], color=C.INK, ls="--", lw=2.0)
axes[1].plot([xl, xl], [yv-0.11, yv+0.11], color=C.INK, lw=1.0)
axes[1].plot([xr, xr], [yv-0.11, yv+0.11], color=C.INK, lw=1.0)
# 标签放到图形外的空白处，用细线指向对应的曲线，避免压线
label(axes[1], r"左：$x=\frac{y^2}{2}$", (0.2, 4.55), ha="left", va="top")
axes[1].annotate("", xy=(4.6, 3.03), xytext=(2.85, 4.25),
                 arrowprops=dict(arrowstyle="-", color=C.INK, lw=0.7,
                                 shrinkA=0, shrinkB=0))
label(axes[1], r"右：$x=y+4$", (3.5, 1.6), ha="center")
save(fig, "C13-n2")
