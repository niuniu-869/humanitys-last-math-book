import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axs = new_fig(19.0, 7.0, ncols=4)

# ① 可去间断
ax = axs[0]
x = np.linspace(-1, 1, 1200)
xl, xr = x[x < -1e-4], x[x > 1e-4]
ax.plot(xl, np.sin(xl) / xl, color=C.INK, lw=1.5, ls="-")
ax.plot(xr, np.sin(xr) / xr, color=C.INK, lw=1.5, ls="-")
ax.scatter([0], [1], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
ax.set_title("① 可去\n$y=\\sin x/x$", pad=12)

# ② 跳跃间断
ax = axs[1]
ax.plot([-1, 0], [-1, -1], color=C.INK, lw=1.5, ls="-")
ax.plot([0, 1], [1, 1], color=C.INK, lw=1.5, ls="-")
ax.scatter([0, 0], [-1, 1], s=32, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
ax.set_title("② 跳跃\n$y=|x|/x$", pad=12)

# ③ 无穷间断
ax = axs[2]
xl = np.linspace(-1, -0.08, 600)
xr = np.linspace(0.08, 1, 600)
ax.plot(xl, 1/xl, color=C.INK, lw=1.5, ls="-")
ax.plot(xr, 1/xr, color=C.INK, lw=1.5, ls="-")
ax.axvline(0, color=C.GRAY, lw=1.0, ls="--")
ax.set_title("③ 无穷\n$y=1/x$", pad=12)

# ④ 振荡间断：在零点附近用对数加密采样
ax = axs[3]
xp = np.geomspace(0.001, 0.3, 20000)
for xo in (-xp[::-1], xp):
    ax.plot(xo, np.sin(1/xo), color=C.INK, lw=0.65, ls="-")
ax.axhline(1, color=C.GRAY, lw=0.8, ls=":")
ax.axhline(-1, color=C.GRAY, lw=0.8, ls=":")
ax.set_title("④ 振荡\n$y=\\sin(1/x)$", pad=12)

for ax in axs:
    if ax is not axs[2]:
        ax.axvline(0, color=C.GRAY, lw=0.7, ls=":", zorder=0)
    ax.axhline(0, color=C.GRAY, lw=0.7, zorder=0)
    ax.set_xlim(-1, 1)
    ax.set_xticks([-1, 0, 1])
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
axs[0].set_ylim(-0.15, 1.25); axs[0].set_yticks([0, 1])
axs[1].set_ylim(-1.45, 1.45)
axs[1].set_yticks([-1, 0, 1])
axs[2].set_ylim(-6, 6)
axs[2].set_yticks([-6, 0, 6])
axs[3].set_xlim(-0.3, 0.3); axs[3].set_ylim(-1.45, 1.45)
axs[3].set_xticks([-0.3, 0, 0.3]); axs[3].set_yticks([-1, 0, 1])
for ax, note in zip(axs, ["缺一点，两侧都趋于 1", "左 $-1$，右 $1$", "$x=0$ 是渐近线", "在 $\\pm1$ 间来回摆动"]):
    label(ax, note, (0.5, -0.62), xycoords="axes fraction", ha="center", fontsize=8.5, annotation_clip=False)
fig.subplots_adjust(wspace=0.45, left=0.05, right=0.98, bottom=0.36, top=0.78)
save(fig, "C3-n2")
