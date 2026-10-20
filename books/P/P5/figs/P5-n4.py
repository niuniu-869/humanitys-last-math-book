import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def main():
    fig, ax = new_fig(13, 8)
    x = np.linspace(0.2, 4, 600)
    ax.plot(x, np.sqrt(x), color=C.INK, lw=2.0, zorder=3)
    intervals = [(0.5, 0.4, 0.28, "陡"), (3.0, 0.4, 0.12, "平")]
    for center, dx, dy, _ in intervals:
        left, right = center - dx / 2, center + dx / 2
        yleft, yright = np.sqrt(left), np.sqrt(right)
        ax.add_patch(plt.Rectangle((left, -0.055), dx, 0.11, facecolor=C.LIGHT,
                                   edgecolor="none", zorder=0))
        ax.plot([left, right], [0, 0], color=C.INK, lw=3.0, solid_capstyle="butt", zorder=4)
        ax.plot([0, 0], [yleft, yright], color=C.INK, lw=3.0, solid_capstyle="butt", zorder=4)
        for xx, yy in [(left, yleft), (right, yright)]:
            ax.plot([xx, xx, 0], [0, yy, yy], color=C.GRAY, ls=":", lw=1.0, zorder=1)
        label(ax, r"$\Delta x$", ((left + right) / 2, 0), offset=(0, 13), ha="center", va="bottom")
    label(ax, r"陡处：长约 $g'(x)\Delta x$，较长", (0, 1.1), offset=(9, 0), ha="left", va="center")
    label(ax, "平处：同样的质量，较短", (0, 1.95), offset=(9, 0), ha="left", va="center")
    label(ax, "两小段上的质量相同", (1.8, 0.45), offset=(0, 0), ha="center", va="center")
    ax.set_xlim(-0.22, 4.25)
    ax.set_ylim(-0.18, 2.35)
    ax.set_xlabel("$x$")
    ax.set_ylabel(r"$y=g(x)=\sqrt{x}$")
    ax.set_xticks([0, 0.5, 1, 2, 3, 4])
    ax.set_yticks([0, 1, np.sqrt(3), 2])
    ax.grid(color=C.LIGHT, lw=0.55)
    fig.tight_layout()
    save(fig, "P5-n4")


if __name__ == "__main__":
    main()
