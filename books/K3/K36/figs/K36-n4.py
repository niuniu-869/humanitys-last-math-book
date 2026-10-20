import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

a = [1, 2, 3, 5, 8, 9]

def trace(target):
    lo, hi = 1, len(a)
    result = []
    while lo < hi:
        total = a[lo-1] + a[hi-1]
        result.append((lo, hi, total))
        if total == target:
            break
        if total < target:
            lo += 1
        else:
            hi -= 1
    return result, (lo, hi)

assert trace(12) == ([(1, 6, 10), (2, 6, 11), (3, 6, 12)], (3, 6))
assert trace(15) == ([(1, 6, 10), (2, 6, 11), (3, 6, 12), (4, 6, 14), (5, 6, 17)], (5, 5))
assert not any(a[i]+a[j] in (15, 16) for i in range(6) for j in range(i+1, 6))

fig, axes = new_fig(19, 21, nrows=2, gridspec_kw={'height_ratios': [3.4, 5.4]})
for ax, target in zip(axes, (12, 15)):
    states, final = trace(target)
    label(ax, f't = {target}', (6.45, .85), fontsize=11)
    for i in range(1, 7):
        label(ax, str(i), (i-.5, .85), ha='center', fontsize=8)
    label(ax, '下标', (-.2, .85), ha='right', fontsize=8)
    for row, (lo, hi, total) in enumerate(states):
        y = -row * 1.25
        label(ax, f'第 {row+1} 轮', (-.3, y), ha='right', va='center', fontsize=9)
        for i, value in enumerate(a, 1):
            discarded = not lo <= i <= hi
            ax.add_patch(Rectangle((i-1, y-.25), 1, .5,
                         facecolor=C.LIGHT if discarded else C.PAPER,
                         edgecolor=C.INK, lw=.8, hatch='//' if discarded else None))
            label(ax, str(value), (i-.5, y), ha='center', va='center', fontsize=10)
        left, right = lo-1-.1, hi+.1
        ax.plot([left, left, right, right],
                [y+.3, y+.5, y+.5, y+.3], color=C.INK, ls='-', lw=1)
        for index, name in ((lo, 'lo'), (hi, 'hi')):
            label(ax, name, (index-.5, y-.52), ha='center', fontsize=8)
        if total == target:
            for i in (lo, hi):
                ax.add_patch(Rectangle((i-1, y-.25), 1, .5, facecolor='none', edgecolor=C.INK, lw=2))
            action = f'和={total}={target}，找到'
        elif total < target:
            action = f'和={total}<{target}，丢左'
        else:
            action = f'和={total}>{target}，丢右（hi 减 1）\nlo=hi=5，结束，没有答案'
        label(ax, action, (6.45, y), va='center', fontsize=9, linespacing=1.6)
    ax.set(xlim=(-1.5, 12.1), ylim=(-len(states)*1.25+.35, 1.35))
    ax.axis('off')
label(axes[0], '斜线灰格：已丢弃', (6.45, -3.05), fontsize=9)
fig.subplots_adjust(hspace=.22, left=.04, right=.98, top=.98, bottom=.03)
save(fig, "K36-n4")
