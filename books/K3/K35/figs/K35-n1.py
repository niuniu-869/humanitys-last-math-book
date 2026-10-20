import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, FancyArrowPatch

a = [5, 2, 8, 1, 9, 3]
d = []
for i, value in enumerate(a):
    d.append(1 + max([d[j] for j in range(i) if a[j] < value], default=0))
assert d == [1, 1, 2, 1, 3, 2]
fig, ax = new_fig(16, 7)
for i, value in enumerate(a):
    x = 1.4 * i
    ax.add_patch(Rectangle((x-.43, 0), .86, .8, facecolor=C.LIGHT if i in (2, 4) else C.PAPER,
                           edgecolor=C.INK, lw=1.2))
    label(ax, str(value), (x, .4), ha='center', va='center', fontsize=14)
    label(ax, str(i+1), (x, .98), ha='center', va='center')
    label(ax, str(d[i]), (x, -.4), ha='center', va='center', fontsize=12)
label(ax, '$i$', (-.85, .98), ha='center', va='center')
label(ax, '$d[i]$', (-.85, -.4), ha='center', va='center')
# 每个 i 只在满足 a[j] < a[i] 且 d[j] + 1 == d[i] 的前驱里取下标最小的 j，
# 不满足条件的 j 一律不连弧。粗实线标出 LIS 5,8,9，其余合法前驱弧用细虚线。
pred = {}
for i in range(len(a)):
    cand = [j for j in range(i) if a[j] < a[i] and d[j] + 1 == d[i]]
    if cand:
        pred[i] = min(cand)
assert pred == {2: 0, 4: 2, 5: 1}
for end, start in pred.items():
    assert a[start] < a[end] and d[start] + 1 == d[end]
# 从 d 最大的格子沿最小下标前驱倒走，得到最长上升子序列 5,8,9。
end = max(range(len(d)), key=lambda k: d[k])
lis_arcs = set()
while end in pred:
    start = pred[end]
    lis_arcs.add((start, end))
    end = start
assert lis_arcs == {(0, 2), (2, 4)}
for start, end in lis_arcs:
    ax.add_patch(FancyArrowPatch((1.4*start, 1.2), (1.4*end, 1.2),
        connectionstyle='arc3,rad=-.62', arrowstyle='-|>', mutation_scale=14,
        lw=2.3, ls='-', color=C.INK))
for end, start in pred.items():
    if (start, end) in lis_arcs:
        continue
    ax.add_patch(FancyArrowPatch((1.4*start+.16, 1.12), (1.4*end-.16, 1.12),
        connectionstyle='arc3,rad=-.50', arrowstyle='-|>', mutation_scale=12,
        lw=1.1, ls='--', color=C.GRAY))
label(ax, '$d[5]=3$', (5.6, -.93), ha='center', va='center')
ax.set(xlim=(-1.2, 7.65), ylim=(-1.25, 3.0), aspect='equal')
ax.axis('off')
save(fig, 'K35-n1')
