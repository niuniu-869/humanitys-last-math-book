import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

alpha = np.log(1.6) / np.log(100)
def loss(n):
    return 4.0 * (np.asarray(n) / 1e7) ** (-alpha)

points = np.array([1e7, 1e8, 1e9, 1e10])
values = loss(points)
assert np.allclose(values[[0, 2]], [4, 2.5])
assert np.isclose(values[3], 2.5 / np.sqrt(1.6))
fig, axes = new_fig(19, 9, ncols=2)
fig.subplots_adjust(left=0.08, right=0.98, bottom=0.2, top=0.88, wspace=0.32)
n = np.geomspace(10**6.5, 10**10.5, 600)
left, right = axes
nl_s = n[n <= 1e9]; nl_e = n[n >= 1e9]
left.plot(nl_s/1e9, loss(nl_s), color=C.INK, ls="-")
left.plot(nl_e/1e9, loss(nl_e), color=C.INK, ls="--")
left.set(xlim=(0, 12), ylim=(1, 5), xlabel=r"$N$（单位 $10^9$）", ylabel=r"$L$", title="普通坐标")
label(left, "曲线形状不便直接读取指数", (3.4, 4.35), fontsize=9)
right.set_xscale("log")
right.set_yscale("log")
solid = np.geomspace(10**6.5, 1e9, 400)
extra = np.geomspace(1e9, 10**10.5, 200)
right.plot(solid, loss(solid), color=C.INK, ls="-")
right.plot(extra, loss(extra), color=C.INK, ls="--")
right.set(xlim=(10**6.5, 10**10.5), ylim=(1.65, 5), xlabel=r"$N$", ylabel=r"$L$", title="双对数坐标")
right.set_xticks(points, [r"$10^7$", r"$10^8$", r"$10^9$", r"$10^{10}$"])
right.yaxis.set_major_locator(FixedLocator([2, 3, 4]))
right.yaxis.set_major_formatter(FixedFormatter(["2", "3", "4"]))
right.yaxis.set_minor_locator(NullLocator())
right.xaxis.set_minor_locator(NullLocator())
# In log coordinates these legs have lengths log(100) and log(1.6).
right.plot([1e7, 1e9, 1e9], [4, 4, 2.5], color=C.GRAY, ls=":", lw=1.1)
right.plot([7e8, 7e8, 1e9], [4, 3.86, 3.86], color=C.GRAY, lw=0.8)
label(right, "×100", (1e8, 4), offset=(0, 10), ha="center", fontsize=9)
label(right, "÷1.6", (1e9, np.sqrt(10)), offset=(8, 0), va="center", fontsize=9)
label(right, r"斜率 $-\alpha\approx-0.10$", (1.2e7, 2.3), fontsize=9)
for ax, xx in [(left, points/1e9), (right, points)]:
    ax.scatter(xx[[0,2]], values[[0,2]], s=25, facecolors=C.INK, edgecolors=C.INK, zorder=5, clip_on=False, label="已知点")
    ax.scatter(xx[3:], values[3:], s=36, facecolors=C.PAPER, edgecolors=C.INK, zorder=5, label="外推点")
left.legend(loc="upper right", bbox_to_anchor=(1, 0.78), fontsize=8)
label(right, r"$1.98$", (1e10, values[3]), offset=(-4, -17), ha="center", fontsize=8)
save(fig, "M13-n2")
