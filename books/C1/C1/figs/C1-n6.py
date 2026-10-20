import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 7.5)
n = np.arange(1, 31)
a = (1 + 1 / n) ** n
assert np.isclose(a[0], 2) and np.isclose(a[1], 2.25)
assert np.isclose(a[11], 2.6130, atol=5e-4) and np.isclose(a[-1], 2.6743, atol=5e-4)
ax.plot(n, a, color=C.INK, lw=1.2, marker="o", markersize=3.7)
ax.axhline(np.e, color=C.GRAY, ls="--", lw=1.1)
ax.axhline(3, color=C.GRAY, ls=":", lw=1.1)
label(ax, "$y=e$", (30.8, np.e), offset=(0, 5), ha="right", va="bottom", fontsize=9)
label(ax, "上界 3", (30.8, 2.96), ha="right", va="top", fontsize=9)
label(ax, "2", (1, a[0]), offset=(0, -9), ha="center", va="top", fontsize=9)
label(ax, "2.25", (2, a[1]), offset=(3, -7), ha="left", va="top", fontsize=9)
label(ax, "2.613", (12, 2.49), ha="center", va="center", fontsize=9)
# 从 2.613 的标注向上用短线指向 n=12 的数据点
ax.annotate("", xy=(12, a[11]), xytext=(12, 2.545),
            arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=.9,
                            shrinkA=2.5, shrinkB=2, mutation_scale=7))
ax.set_xlim(.5, 31.5); ax.set_ylim(1.8, 3.1)
ax.set_xlabel("$n$"); ax.set_ylabel("$a_n$")
ax.set_xticks([1, 5, 10, 15, 20, 25, 30]); ax.set_yticks([1.8, 2.0, 2.2, 2.4, 2.6, 2.718, 3.0])
fig.tight_layout()
save(fig, "C1-n6")
