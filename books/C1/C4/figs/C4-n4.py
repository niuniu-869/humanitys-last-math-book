import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 8, ncols=3)
fig.subplots_adjust(left=0.07, right=0.99, bottom=0.29, top=0.85, wspace=0.46)

ax = axes[0]
x = np.linspace(-0.5, 0.5, 800)
ax.plot(x, np.abs(x), color=C.INK, lw=1.7, ls="-")
label(ax, "左导数 -1，右导数 1", (0.5, -0.35),
      xycoords="axes fraction", ha="center", fontsize=9, annotation_clip=False)
ax.set_title("① $y=|x|$")
ax.set_xlim(-0.5, 0.5); ax.set_ylim(-0.08, 0.55)

ax = axes[1]
# Log sampling resolves the shrinking oscillations; additional uniform phase
# samples prevent aliasing before the oscillations become subpixel.
x_right = np.unique(np.concatenate((
    np.geomspace(1e-5, 0.5, 16000),
    1 / np.linspace(2, 100000, 180000),
)))
x_left = -x_right[::-1]
ax.plot(x_left, x_left * np.sin(1 / x_left), color=C.INK, lw=1.0, ls="-")
ax.plot(x_right, x_right * np.sin(1 / x_right), color=C.INK, lw=1.0, ls="-")
xx = np.linspace(-0.5, 0.5, 900)
ax.plot(xx, np.abs(xx), color=C.GRAY, lw=0.9, ls=":")
ax.plot(xx, -np.abs(xx), color=C.GRAY, lw=0.9, ls=":")
dot(ax, (0, 0), color=C.INK, size=22)
label(ax, "来回摆动\n" + r"差商 $\sin\frac{1}{h}$ 无极限", (0.5, -0.35),
      xycoords="axes fraction", ha="center", va="center", fontsize=9, annotation_clip=False)
ax.set_title(r"② $y=x\sin\frac{1}{x}$")
ax.set_xlim(-0.5, 0.5); ax.set_ylim(-0.55, 0.55)

ax = axes[2]
ax.plot(x_left, x_left**2 * np.sin(1 / x_left), color=C.INK, lw=1.0, ls="-")
ax.plot(x_right, x_right**2 * np.sin(1 / x_right), color=C.INK, lw=1.0, ls="-")
xx = np.linspace(-0.3, 0.3, 900)
ax.plot(xx, xx**2, color=C.GRAY, lw=0.9, ls=":")
ax.plot(xx, -xx**2, color=C.GRAY, lw=0.9, ls=":")
dot(ax, (0, 0), color=C.INK, size=22)
ax.plot([-0.16, 0.16], [0, 0], color=C.INK, lw=1.4, ls="--", zorder=4)
label(ax, "被 $\\pm x^2$ 夹住\n$f'(0)=0$", (0.5, -0.35),
      xycoords="axes fraction", ha="center", va="center", fontsize=9, annotation_clip=False)
ax.set_title(r"③ $y=x^2\sin\frac{1}{x}$")
ax.set_xlim(-0.3, 0.3); ax.set_ylim(-0.1, 0.1)

for ax in axes:
    if ax is axes[2]:
        ax.plot([-0.3, -0.16], [0, 0], color=C.GRAY, lw=0.8)
        ax.plot([0.16, 0.3], [0, 0], color=C.GRAY, lw=0.8)
    else:
        ax.axhline(0, color=C.GRAY, lw=0.8, ls="-")
    ax.axvline(0, color=C.GRAY, lw=0.8, ls="-")
    ax.set_xlabel("$x$")
axes[0].set_ylabel("$y$")
save(fig, "C4-n4")
