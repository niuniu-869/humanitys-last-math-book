import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

a = [1, 2, 3, 5, 8, 9]
lo, hi, target = 1, len(a), 9
states = []
for _ in range(5):
    mid = (lo + hi) // 2
    states.append((lo, hi, mid))
    assert a[mid-1] < target
    lo = mid
assert states == [(1, 6, 3), (3, 6, 4), (4, 6, 5), (5, 6, 5), (5, 6, 5)]

fig, ax = new_fig(18, 14)
for i in range(1, 7):
    label(ax, str(i), (i-.5, 1.3), ha='center', fontsize=9)
label(ax, '下标', (-.3, 1.3), ha='right', fontsize=9)
label(ax, '查找 9', (7, 1.3), fontsize=10)
for row, (lo, hi, mid) in enumerate(states):
    y = -row * 1.95
    label(ax, f'第 {row+1} 轮', (-.35, y), ha='right', va='center')
    for i, value in enumerate(a, 1):
        ax.add_patch(Rectangle((i-1, y-.27), 1, .54,
                     facecolor=C.LIGHT if i == mid else C.PAPER,
                     edgecolor=C.INK, lw=.8))
        label(ax, str(value), (i-.5, y), ha='center', va='center')
    left, right = lo-1-.10, hi+.10
    ax.plot([left, left, right, right],
            [y+.32, y+.62, y+.62, y+.32],
            color=C.INK, ls='-', lw=1)
    label(ax, f'mid={mid}', (mid-.5, y+.78), ha='center', fontsize=8)
    for index, name in ((lo, 'lo'), (hi, 'hi')):
        ax.plot(index-.5, y-.43, marker='^', color=C.INK, ms=5)
        label(ax, name, (index-.5, y-.75), ha='center', fontsize=8)
    action = f'{a[mid-1]}<9，lo←{mid}'
    if lo == mid:
        action += '（没变）'
    label(ax, action, (6.55, y), va='center', fontsize=10)
label(ax, r'$\vdots$ 以后每轮相同', (3, -9.3), ha='center', va='center')
ax.set(xlim=(-1.3, 11), ylim=(-9.65, 1.8))
ax.axis('off')
fig.tight_layout()
save(fig, "K36-n3")
