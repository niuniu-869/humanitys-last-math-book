import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

fig, axes = new_fig(19, 5.8, ncols=4)
fig.subplots_adjust(left=0.015, right=0.985, bottom=0.22, top=0.86, wspace=0.10)
states = [([3, 2, 1], [], []), ([3], [2, 1], []),
          ([], [2, 1], [3]), ([], [], [3, 2, 1])]
titles = ["开始", "第一段", "第二段", "第三段"]
positions = [0, 3.6, 7.2]
fills = {3: C.LIGHT, 2: C.AMBER, 1: C.PAPER}
for ax, stacks, title in zip(axes, states, titles):
    ax.set(xlim=(-1.8, 9), ylim=(-0.75, 4.5), aspect="equal")
    ax.axis("off")
    ax.set_title(title, pad=8)
    ax.plot([-1.6, 8.8], [0, 0], color=C.INK, lw=1.2, ls="-")
    for x, name, stack in zip(positions, "ABC", stacks):
        ax.plot([x, x], [0, 2.55], color=C.INK, lw=1.2, ls="-", zorder=1)
        label(ax, name, (x, -0.24), ha="center", va="top")
        assert stack == sorted(stack, reverse=True)
        for level, disk in enumerate(stack):
            y = level * 0.75
            ax.add_patch(Rectangle((x - disk / 2, y), disk, 0.75,
                                   facecolor=fills[disk], edgecolor=C.INK, lw=1, zorder=3))
            ax.text(x, y + 0.375, str(disk), ha="center", va="center",
                    fontsize=7, color=C.INK, zorder=6)
    assert sorted(sum((list(s) for s in stacks), [])) == [1, 2, 3]
for ax, start, end, style, text in [
    (axes[1], 0, 3.6, "--", r"$h_2=3$ 步"),
    (axes[2], 0, 7.2, "-", "1 步"),
    (axes[3], 3.6, 7.2, "--", r"$h_2=3$ 步"),
]:
    ax.add_patch(FancyArrowPatch((start, 3.15), (end, 3.15),
                                arrowstyle="-|>", mutation_scale=11,
                                color=C.INK, lw=1.25, linestyle=style))
    label(ax, text, ((start + end) / 2, 3.48), ha="center", va="bottom", fontsize=9)
h2 = 2**2 - 1
assert 2 * h2 + 1 == 7
fig.text(0.5, 0.09, r"共 $3+1+3=7$ 步", ha="center", color=C.INK)
save(fig, "K21-n1")
