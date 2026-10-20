import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from itertools import combinations, product
from matplotlib.patches import Patch

lines = np.array([[.4, 1], [-.6, 3], [2, -3], [-1.2, 1.5]])
box = np.array([[-4., -5.], [6., -5.], [6., 7.], [-4., 7.]])

def clip(poly, m, b, sign):
    out = []
    for p, q in zip(poly, np.roll(poly, -1, axis=0)):
        fp, fq = sign * (p[1] - m*p[0] - b), sign * (q[1] - m*q[0] - b)
        if fp >= -1e-10:
            out.append(p)
        if (fp > 0) != (fq > 0):
            out.append(p + fp/(fp-fq)*(q-p))
    return np.array(out)

crossings = []
for i, j in combinations(range(4), 2):
    m, b = lines[i]
    u, v = lines[j]
    assert m != u
    x = (v-b)/(m-u)
    crossings.append([x, m*x+b])
crossings = np.array(crossings)
assert all(np.linalg.norm(p-q) > 1e-6 for p, q in combinations(crossings, 2))
assert np.all((crossings > [-4, -5]) & (crossings < [6, 7]))
regions = {}
for signs in product([-1, 1], repeat=3):
    poly = box.copy()
    for (m, b), sign in zip(lines[:3], signs):
        if len(poly):
            poly = clip(poly, m, b, sign)
    if len(poly) >= 3:
        regions[signs] = poly
assert len(regions) == 7
m, b = lines[3]
hits = sorted((v-b)/(m-u) for u, v in lines[:3])
ends = [-4, *hits, (b+5)/(-m)]
samples = np.array([(a+c)/2 for a, c in zip(ends[:-1], ends[1:])])
keys = [tuple(np.sign(m*x+b-lines[:3, 0]*x-lines[:3, 1]).astype(int)) for x in samples]
assert len(set(keys)) == 4
fig, ax = new_fig(13, 13)
for key in keys:
    p = regions[key]
    ax.fill(p[:, 0], p[:, 1], color=C.LIGHT, zorder=0)
for i, (u, v) in enumerate(lines):
    x = np.array([-4, 6])
    ax.plot(x, u*x+v, color=C.INK, ls='-', lw=2.4 if i == 3 else .9)
for x in hits:
    dot(ax, (x, m*x+b), size=24)
for text, x, offset in zip('①②③④', samples, [(12, 7), (-12, -10), (12, 7), (12, 7)]):
    label(ax, text, (x, m*x+b), offset=offset, fontsize=11)
label(ax, '第 4 条', (4.3, m*4.3+b), offset=(12, 5))
for i, x in enumerate([5.3, 5.3, 4.3]):
    label(ax, f'$L_{i+1}$', (x, lines[i, 0]*x+lines[i, 1]), offset=(-18, 0) if i == 2 else (0, 8))
ax.set(xlim=(-4, 6), ylim=(-5, 7), aspect='equal', xticks=[], yticks=[])
ax.set_axis_off()
ax.legend(handles=[Patch(facecolor=C.LIGHT, edgecolor=C.GRAY, label='阴影：被第 4 条切开的 4 块')], loc='upper center', bbox_to_anchor=(.5, -.015))
fig.text(.5, .035, f'$f(3)={len(regions)}$，加第 4 条后多 {len(keys)} 块，$f(4)={len(regions)+len(keys)}$', ha='center')
fig.subplots_adjust(bottom=.16, top=.98)
print('K41-n1: intersections=', crossings.tolist(), 'regions=7; split=4; total=11')
save(fig, 'K41-n1')
