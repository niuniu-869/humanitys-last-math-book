import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

n = np.arange(1, 5)
S = np.array([1, 1.25, 1.3611, 1.4236])
B = 2 - 1/n
assert np.all(S <= B + 1e-4)
fig, ax = new_fig(12, 8)
ax.set_xlim(.55, 4.65); ax.set_ylim(.0, 2.28)
ax.set_xticks(n); ax.set_xticklabels(["1", "2", "3", "4"]); ax.set_ylabel("数值")
ax.axhline(2, color=C.INK, lw=1.2, ls="--")
label(ax, "2", (4.55, 2), offset=(0, 4), ha="right")
for i in range(4):
    ax.fill_between([n[i]-.12, n[i]+.12], S[i], B[i], color=C.LIGHT, alpha=.75, zorder=1)
ax.plot(n, B, color=C.INK, lw=1.5, ls=":", marker="s", markersize=7, markerfacecolor=C.PAPER, markeredgecolor=C.INK, markeredgewidth=1.2)
ax.plot(n, S, color=C.INK, lw=1.7, ls="-", marker="o", markersize=6, markerfacecolor=C.INK)
for x, y in zip(n, S): label(ax, f"$S_{x}$", (x, y), offset=(6, -3), va="center")
for x, y in zip(n, B): label(ax, "$2-\\frac{1}{n}$" if x == 4 else "", (x, y), offset=(5, 5), va="bottom")
label(ax, "余量 0.326", (4, (S[-1]+B[-1])/2), offset=(12, 0), va="center")
label(ax, "实心点：$S_n$；空心方块：$2-\\frac{1}{n}$", (2.5, .18), ha="center")
save(fig, "Z4-n5")
