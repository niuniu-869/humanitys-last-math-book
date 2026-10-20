import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import comb

fig, axes = new_fig(18, 8.5, ncols=2)
fig.subplots_adjust(left=.09, right=.98, bottom=.19, top=.89, wspace=.36)
left, right = axes
n = np.arange(31)
for alpha, ls, color in [(.99, "-", C.INK), (.95, "--", C.RED), (.90, ":", C.TEAL)]:
    left.plot(n, alpha**n, ls=ls, color=color, label=rf"$\alpha={alpha:.2f}$")
left.set(xlim=(0, 30), ylim=(0, 1), xlabel="步数 $n$", ylabel="全链正确概率",
         xticks=np.arange(0, 31, 5))
left.legend(loc="lower left", fontsize=9, handlelength=2.7)
for step, offset in [(5, (8, 7)), (10, (9, 4)), (20, (6, 8))]:
    value = .95**step
    dot(left, (step, value), color=C.RED, size=20)
    label(left, f"{value:.3f}", (step, value), offset, fontsize=9)
assert [f"{.95**i:.3f}" for i in (5, 10, 20)] == ["0.774", "0.599", "0.358"]

k = np.arange(1, 22, 2)
def majority(count):
    return sum(comb(count, j)*.6**j*.4**(count-j) for j in range(count//2+1, count+1))
values = np.array([majority(int(count)) for count in k])
right.plot(k, values, color=C.INK, ls="-", marker="o", markersize=3,
           markerfacecolor=C.PAPER, markeredgecolor=C.INK)
right.axhline(.6, color=C.GRAY, ls="--", lw=1.2)
right.set(xlim=(0, 22), ylim=(.5, 1), xlabel="投票条数 $k$", ylabel="多数票正确概率",
          xticks=[1, 5, 9, 13, 17, 21])
for count, offset in [(1, (0, 24)), (5, (-6, 13)), (11, (-10, 13)), (21, (-26, 12))]:
    value = majority(count)
    label(right, "0.6" if count == 1 else f"{value:.3f}", (count, value), offset, fontsize=9)
label(right, "单条链 0.6", (12, .6), (0, -16), ha="center", fontsize=9)
label(right, "$q=0.6$", (12, .95), ha="center", fontsize=10)
assert [f"{majority(i):.3f}" for i in (5, 11, 21)] == ["0.683", "0.753", "0.826"]
assert np.all(np.diff(values) > 0)
save(fig, "K16-n3")
