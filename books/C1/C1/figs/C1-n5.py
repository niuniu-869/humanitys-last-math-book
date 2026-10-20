import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

left = [np.sqrt(2)]
for _ in range(7):
    left.append(np.sqrt(2 + left[-1]))
right = [1.0]
for _ in range(6):
    right.append(.5 * (right[-1] + 2 / right[-1]))
assert np.allclose(left[:5], [1.41421356, 1.847759, 1.961571, 1.990369, 1.99759], atol=2e-5)
assert np.allclose(right[1:5], [1.5, 1.4166667, 1.4142157, 1.4142136], atol=2e-5)
fig, axes = new_fig(15, 7.2, ncols=2)
ax, bx = axes
n1 = np.arange(1, 9)
ax.plot(n1, left, color=C.INK, lw=1.2, marker="o", markersize=4.8)
ax.axhline(2, color=C.GRAY, ls="--", lw=1.1)
label(ax, "$A=2$", (1.6, 2.055), ha="center", va="center", fontsize=8.5)
ax.set_xlim(.5, 8.5); ax.set_ylim(1.3, 2.1)
ax.set_xlabel("$n$", labelpad=1); ax.set_ylabel("$x_n$")
ax.set_xticks(np.arange(1, 9)); ax.set_yticks([1.4, 1.6, 1.8, 2.0])
n2 = np.arange(2, 8)
bx.plot(n2, right[1:], color=C.INK, lw=1.2, marker="o", markersize=4.8)
bx.axhline(np.sqrt(2), color=C.GRAY, ls="--", lw=1.1)
label(bx, "$A=\\sqrt{2}$", (6.2, 1.4295), ha="center", va="center", fontsize=9)
label(bx, "$x_1=1$（图外）", (2.1, 1.505), ha="left", va="bottom", fontsize=8.5)
bx.set_xlim(1.5, 7.5); bx.set_ylim(1.40, 1.52)
bx.set_xlabel("$n$"); bx.set_ylabel("$x_n$")
bx.set_xticks(np.arange(2, 8)); bx.set_yticks([1.40, 1.42, 1.46, 1.50])
fig.subplots_adjust(wspace=.35, bottom=.28)
fig.text(.28, .03, "单调增加，上界 2", ha="center")
fig.text(.73, .03, r"从第 2 项起单调减少，下界 $\sqrt{2}$", ha="center")
save(fig, "C1-n5")
