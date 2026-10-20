import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def main():
    fig, ax = new_fig(13, 8)
    x = np.linspace(0, 1.5, 600)
    F = 1 - np.exp(-3 * x)
    ax.plot(x, F, color=C.INK, lw=2.0, zorder=3)
    us = np.arange(0.1, 1.0, 0.1)
    for u in us:
        xx = -np.log(1 - u) / 3
        special = np.isclose(u, 0.5)
        ls = "-" if special else ":"
        lw = 1.8 if special else 0.9
        ax.plot([0, xx], [u, u], color=C.GRAY if not special else C.INK, ls=ls, lw=lw, zorder=1)
        ax.plot([xx, xx], [0, u], color=C.GRAY if not special else C.INK, ls=ls, lw=lw, zorder=1)
        ax.scatter([0], [u], s=28, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.0, zorder=5)
        ax.scatter([xx], [0], s=24, color=C.INK, zorder=5)
    xmid = -np.log(0.5) / 3
    label(ax, "$u=0.5\\ \\to\\ x\\approx0.231$", (0, 0.5), offset=(8, 6), ha="left", va="bottom")
    label(ax, "落点密", (0.17, -0.085), offset=(0, 0), ha="center", va="center")
    label(ax, "落点疏", (0.95, -0.085), offset=(0, 0), ha="center", va="center")
    ax.set_xlim(-0.12, 1.62)
    ax.set_ylim(-0.14, 1.08)
    ax.set_xlabel("$x$（小时）")
    ax.set_ylabel("$u$")
    ax.set_xticks([0, 0.231, 0.5, 1.0, 1.5])
    ax.set_xticklabels(["0", "0.231", "0.5", "1.0", "1.5"])
    ax.set_yticks(np.linspace(0, 1, 6))
    ax.grid(color=C.LIGHT, lw=0.55)
    fig.tight_layout()
    save(fig, "P5-n5")


if __name__ == "__main__":
    main()
