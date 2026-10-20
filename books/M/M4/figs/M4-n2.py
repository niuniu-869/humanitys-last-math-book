import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# Independent uniform query and 2000 training points in each unit cube.
# Batches bound memory without changing the sample size or distance definition.
seed = 20261017
rng = np.random.default_rng(seed)
dimensions = np.array([2, 10, 100, 1000, 10000])
ratios = []
for dimension in dimensions:
    query = rng.random(dimension)
    distances = []
    for start in range(0, 2000, 100):
        delta = rng.random((100, dimension)) - query
        distances.extend(np.sqrt(np.einsum('ij,ij->i', delta, delta)))
    ratios.append(np.min(distances) / np.max(distances))
ratios = np.array(ratios)
assert np.all((ratios > 0) & (ratios < 1))
print('M4-n2 seed:', seed, 'dimensions:', dimensions.tolist(), 'ratios:', ratios.tolist())

fig, (left, right) = new_fig(18, 8, ncols=2)
d = np.linspace(1, 100, 1000)
left.plot(d, 1 - 0.95**d, color=C.INK, ls='-')
for x, offset, align, fmt in [(2, (-18, 25), 'left', '.4f'),
                               (10, (7, -15), 'left', '.3f'),
                               (100, (-8, -42), 'right', '.3f')]:
    y = 1 - 0.95**x
    dot(left, (x, y))
    left.collections[-1].set_clip_on(False)
    label(left, f'({x}, {y:{fmt}})', (x, y), offset, ha=align, fontsize=8)
left.set(xscale='log', xlim=(1, 100), ylim=(0, 1), xlabel='维数 $d$', ylabel='比例')
left.set_title(r'$1-0.95^d$', pad=10)
right.plot(dimensions, ratios, color=C.INK, ls='--', marker='s', markersize=4,
           clip_on=False, zorder=4)
right.set(xscale='log', xlim=(2, 10000), ylim=(0, 1), xlabel='维数 $d$',
          ylabel='最近距离 ÷ 最远距离')
right.set_title('2000 个均匀随机点', pad=10)
for ax in (left, right):
    ax.axhline(1, color=C.GRAY, ls=':', lw=0.8)
    ax.set_yticks(np.linspace(0, 1, 6))
fig.tight_layout(w_pad=2)
save(fig, "M4-n2")
