import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def main():
    fig, (ax1, ax2) = new_fig(14, 10, nrows=2)
    x = np.linspace(-1, 2, 600)
    ax1.plot(x, np.abs(x), color=C.INK, lw=2.0, ls="-", zorder=3)
    levels = [(0.6, "-", -0.6, 0.6), (1.5, ":", -1, 1.5)]
    for lev, ls, left, right in levels:
        ax1.axhline(lev, color=C.GRAY, ls="--", lw=1.0, zorder=1)
        ax1.plot([left, right], [-0.12 if lev < 1 else -0.38] * 2,
                 color=C.INK, ls=ls, lw=3.0, solid_capstyle="butt", zorder=4)
    label(ax1, "y=0.6 时 [-y,y]", (0.68, 0.07), offset=(5, 0),
          ha="left", va="bottom")
    label(ax1, "y=1.5 时 [-1,y]（左端被 x=-1 截断）", (0.25, -0.52),
          offset=(0, -3), ha="center", va="top")
    ax1.axvline(-1, color=C.GRAY, ls=":", lw=1.2)
    label(ax1, "$X$ 的左端点", (-1, 2.30), offset=(5, 0), ha="left", va="center")
    ax1.set_xlim(-1.45, 2.35)
    ax1.set_ylim(-1.2, 2.6)
    ax1.set_xlabel("$x$")
    ax1.set_ylabel("$y=|x|$")
    ax1.set_xticks([-1, 0, 1, 2])
    ax1.set_yticks([0, 0.6, 1.5, 2])
    ax1.set_yticklabels(["0", "0.6", "1.5", "2"])
    ax1.grid(color=C.LIGHT, lw=0.55)

    yy = np.linspace(0, 2, 500)
    dens = np.where((yy > 0) & (yy < 1), 2 / 3, np.where((yy >= 1) & (yy < 2), 1 / 3, 0))
    ax2.fill_between(yy, 0, dens, step="post", facecolor=C.LIGHT, edgecolor=C.INK, linewidth=1.1)
    ax2.step(yy, dens, where="post", color=C.INK, lw=1.8)
    ax2.axvline(1, color=C.GRAY, ls="--", lw=1.1)
    ax2.set_xlim(-0.08, 2.08)
    ax2.set_ylim(0, 0.82)
    ax2.set_xlabel("$y$")
    ax2.set_ylabel(r"$f_Y(y)$")
    ax2.set_xticks([0, 1, 2])
    ax2.set_yticks([0, 1 / 3, 2 / 3])
    ax2.set_yticklabels(["0", r"$1/3$", r"$2/3$"])
    label(ax2, r"$2/3$", (0.45, 2 / 3), offset=(0, 5), ha="center", va="bottom")
    label(ax2, r"$1/3$", (1.5, 1 / 3), offset=(0, 5), ha="center", va="bottom")
    ax2.grid(color=C.LIGHT, lw=0.55)
    fig.tight_layout(h_pad=2.0)
    save(fig, "P5-n3")


if __name__ == "__main__":
    main()
