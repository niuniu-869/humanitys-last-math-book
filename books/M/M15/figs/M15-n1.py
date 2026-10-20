import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

v = np.array([0.4288, 0.5241, 0.7358])
assert np.allclose(v, [0.4288, 0.5241, 0.7358])
fig, ax = new_fig(17, 6)
xs = [1, 3.6, 6.2, 8.8]
for i, x in enumerate(xs):
    ax.add_patch(Rectangle((x-.8, 0), 1.6, 1.25, facecolor=C.LIGHT if i == 3 else C.PAPER, edgecolor=C.INK, lw=1.2))
    label(ax, ["格 1", "格 2", "格 3", "终点"][i], (x, .63), ha="center", va="center", fontsize=11)
for x1, x2 in zip(xs[:-1], xs[1:]):
    ax.add_patch(FancyArrowPatch((x1+.82,.78),(x2-.82,.78),arrowstyle="<->",mutation_scale=11,lw=1.1,color=C.INK))
    label(ax, "左", ((x1+x2)/2, .98), ha="center", fontsize=8)
    label(ax, "右", ((x1+x2)/2, .55), ha="center", fontsize=8)
    label(ax, "奖励 1" if x1 == xs[2] else "奖励 0", ((x1+x2)/2, .16), ha="center", fontsize=8)
ax.add_patch(FancyArrowPatch((.55,.25),(.55,1.0),connectionstyle="arc3,rad=-.75",arrowstyle="-|>",mutation_scale=11,lw=1.1,color=C.INK))
label(ax, "左：留在原地", (.05,.1), ha="left", fontsize=8)
for x, val in zip(xs[:3], v): label(ax, f"{val:.4f}", (x,-.34), ha="center", fontsize=9)
for x, val in zip(xs[:3], [0.81, .9, 1]): label(ax, f"{val:g}", (x,-.72), ha="center", fontsize=9)
label(ax, "随机策略（左右各 0.5），$\\gamma=0.9$：$V$", (-.25,-.34), ha="right", fontsize=9)
label(ax, "最优策略（一路向右）：$V^*$", (-.25,-.72), ha="right", fontsize=9)
ax.set(xlim=(-1.8,10), ylim=(-1.05,1.55)); ax.axis("off")
save(fig, "M15-n1")
