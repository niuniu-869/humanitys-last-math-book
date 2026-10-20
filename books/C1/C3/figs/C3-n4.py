import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axs = new_fig(17.5, 6.0, ncols=3)

# ① 区间不含左端点，函数无界
ax = axs[0]
x = np.linspace(0.06, 1, 700)
ax.plot(x, 1/x, color=C.INK, lw=1.7, ls="-")
dot(ax, (1, 1), size=28)
ax.scatter([0], [0], s=32, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
ax.set_title("① $y=1/x$，$(0,1]$", pad=12)
label(ax, "无界", (0.55, 4.8), offset=(0, 0), ha="center")
label(ax, "$0$ 不在区间内", (0.15, 0.45), offset=(0, 0), fontsize=8.5)

# ② 开区间导致上确界取不到
ax = axs[1]
x = np.linspace(0, 0.999, 600)
ax.plot(x, x, color=C.INK, lw=1.7, ls="-")
dot(ax, (0, 0), size=28)
ax.scatter([1], [1], s=32, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
ax.axhline(1, color=C.GRAY, lw=1.0, ls=":")
ax.set_title("② $y=x$，$[0,1)$", pad=12)
label(ax, "上确界 1，取不到", (0.5, 1.20), offset=(0, 0), ha="center", fontsize=9)

# ③ 不连续导致最高点不存在
ax = axs[2]
x = np.linspace(0, 0.999, 600)
ax.plot(x, x, color=C.INK, lw=1.7, ls="-")
dot(ax, (0, 0), size=28)
ax.scatter([1], [1], s=32, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
dot(ax, (1, 0), size=28)
ax.axhline(1, color=C.GRAY, lw=1.0, ls=":")
ax.set_title("③ 不连续，$[0,1]$", pad=12)
label(ax, "上确界 1，取不到", (0.5, 1.20), offset=(0, 0), ha="center", fontsize=9)

for ax in axs:
    ax.set_xlim(-0.12, 1.12); ax.set_ylim(-0.18, 5.7 if ax is axs[0] else 1.48)
    ax.set_xticks([0, 0.5, 1]); ax.set_yticks([0, 1] if ax is not axs[0] else [0, 1, 3, 5])
    ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
    ax.axhline(0, color=C.GRAY, lw=0.7, zorder=0)
    ax.axvline(0, color=C.GRAY, lw=0.7, zorder=0)
fig.subplots_adjust(wspace=0.36, left=0.06, right=0.98, bottom=0.19, top=0.82)
save(fig, "C3-n4")
