import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def main():
    fig, ax = new_fig(13, 8)
    x = np.linspace(0, 2, 500)
    y = x ** 2
    y0 = 2.25
    x0 = np.sqrt(y0)
    ax.plot(x, y, color=C.INK, ls="-", lw=2.0, zorder=3)
    ax.axhline(y0, color=C.GRAY, ls="--", lw=1.2, zorder=1)
    ax.plot([x0, x0], [0, y0], color=C.GRAY, ls=":", lw=1.2, zorder=1)
    ax.add_patch(plt.Rectangle((0, -0.055), x0, 0.11, facecolor=C.LIGHT,
                               edgecolor="none", zorder=0))
    ax.plot([0, x0], [0, 0], color=C.INK, lw=3.0, solid_capstyle="butt", zorder=4)
    dot(ax, (x0, 0), size=24)
    dot(ax, (x0, y0), size=15)
    label(ax, r"$y$", (1.88, y0), offset=(0, 6), ha="center", va="bottom")
    label(ax, r"$X\leq\sqrt{y}$", (1.18, 0), offset=(0, 14), ha="center", va="bottom")
    label(ax, r"$X\sim U(0,2)$，$x\in(0,2)$", (0.95, 3.4), offset=(0, 0),
          ha="center", va="center", color=C.INK)
    ax.set_xlim(-0.18, 2.18)
    ax.set_ylim(-0.18, 4.25)
    ax.set_xlabel("$x$")
    ax.set_ylabel("$y$")
    ax.set_xticks([0, 1, x0, 2])
    ax.set_xticklabels(["0", "1", r"$\sqrt{y}$", "2"])
    ax.set_yticks([0, 1, y0, 4])
    ax.set_yticklabels(["0", "1", "$y$", "4"])
    ax.grid(color=C.LIGHT, lw=0.55)
    fig.tight_layout()
    save(fig, "P5-n2")


if __name__ == "__main__":
    main()
