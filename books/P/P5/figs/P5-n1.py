import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def main():
    fig, (ax1, ax2) = new_fig(14, 10, nrows=2, sharex=False)
    s = np.arange(2, 13)
    h = (6 - np.abs(s - 7)) / 36
    hatch_for_k = {1: "///", 2: "...", 3: "---", 4: "|||", 5: "\\\\"}
    for x, height in zip(s, h):
        k = abs(x - 7)
        hatch = None if k == 0 else hatch_for_k[k]
        ax1.bar(x, height, width=0.82, facecolor=C.PAPER if k == 0 else C.LIGHT,
                edgecolor=C.INK, linewidth=0.9, hatch=hatch, zorder=2)
    ax1.axvline(7, color=C.GRAY, ls="--", lw=1.1, zorder=1)
    ax1.set_ylabel(r"$P(S=s)$")
    ax1.set_xticks(s)
    ax1.set_yticks(np.arange(0, 7) / 36)
    ax1.set_yticklabels(["0"] + [rf"${k}/36$" for k in range(1, 7)])
    ax1.set_xlim(1.3, 12.7)
    ax1.set_ylim(0, 0.19)
    ax1.grid(axis="y", color=C.LIGHT, lw=0.6)
    ax1.set_title("$S$ 的分布（虚线是对称轴 $s=7$）")

    y = np.arange(6)
    hy = np.array([6, 10, 8, 6, 4, 2]) / 36
    for k, height in zip(y, hy):
        hatch = None if k == 0 else hatch_for_k[k]
        ax2.bar(k, height, width=0.82, facecolor=C.PAPER if k == 0 else C.LIGHT,
                edgecolor=C.INK, linewidth=0.9, hatch=hatch, zorder=2)
        label(ax2, rf"${int(height * 36)}/36$", (k, height), offset=(0, 4), ha="center", va="bottom")
    ax2.set_xlabel(r"$y=|S-7|$")
    ax2.set_ylabel(r"$P(Y=y)$")
    ax2.set_xticks(y)
    ax2.set_yticks(np.arange(0, 6) * 2 / 36)
    ax2.set_yticklabels(["0"] + [rf"${2 * k}/36$" for k in range(1, 6)])
    ax2.set_xlim(-0.7, 5.7)
    ax2.set_ylim(0, 0.34)
    ax2.grid(axis="y", color=C.LIGHT, lw=0.6)
    ax2.set_title("$Y=|S-7|$ 的分布（成对柱高相加）")
    fig.tight_layout(h_pad=2.0)
    save(fig, "P5-n1")


if __name__ == "__main__":
    main()
