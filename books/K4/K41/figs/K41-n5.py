import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from itertools import combinations
from math import comb
from matplotlib.patches import Patch

angles = np.deg2rad([0, 52, 115, 170, 235, 296])
points = np.column_stack([np.cos(angles), np.sin(angles)])
chords = list(combinations(range(6), 2))
crossings = []
for (i, j), (k, l) in combinations(chords, 2):
    if len({i, j, k, l}) < 4:
        continue
    a, b, c, d = points[[i, j, k, l]]
    mat = np.column_stack([b-a, c-d])
    if abs(np.linalg.det(mat)) < 1e-10:
        continue
    t, u = np.linalg.solve(mat, c-a)
    if 0 < t < 1 and 0 < u < 1:
        crossings.append(a+t*(b-a))
crossings = np.array(crossings)
assert len(crossings) == comb(6, 4) == 15
assert np.all(np.linalg.norm(crossings, axis=1) < 1)
assert all(np.linalg.norm(p-q) > 1e-6 for p, q in combinations(crossings, 2))

# Half-plane clipping selects one complete face of the chord arrangement.
seed = .83*(points[0]+points[1])/2
theta = np.linspace(0, 2*np.pi, 1441)
poly = np.column_stack([np.cos(theta[:-1]), np.sin(theta[:-1])])
for i, j in chords:
    a, b = points[[i, j]]
    normal = np.array([-(b-a)[1], (b-a)[0]])
    sign = np.sign((seed-a)@normal)
    out = []
    for p, q in zip(poly, np.roll(poly, -1, axis=0)):
        fp, fq = sign*((p-a)@normal), sign*((q-a)@normal)
        if fp >= -1e-10:
            out.append(p)
        if (fp > 0) != (fq > 0):
            out.append(p+fp/(fp-fq)*(q-p))
    poly = np.array(out)
assert len(poly) >= 3
fig, ax = new_fig(13, 13)
ax.fill(poly[:, 0], poly[:, 1], color=C.LIGHT)
for i, j in chords:
    ax.plot(points[[i, j], 0], points[[i, j], 1], color=C.INK, ls='-', lw=.75)
ax.plot(np.cos(theta), np.sin(theta), color=C.INK, ls='-', lw=1.8)
ax.scatter(crossings[:, 0], crossings[:, 1], s=12, color=C.INK, zorder=4)
ax.scatter(points[:, 0], points[:, 1], s=38, facecolor=C.PAPER, edgecolor=C.INK, zorder=5)
for i, p in enumerate(points):
    label(ax, str(i+1), 1.12*p, ha='center', va='center')
ax.set(xlim=(-1.23, 1.23), ylim=(-1.23, 1.23), aspect='equal')
ax.set_axis_off()
ax.legend(handles=[Patch(facecolor=C.LIGHT, edgecolor=C.GRAY, label='阴影：其中一块')], loc='upper center', bbox_to_anchor=(.5, -.01))
regions = 1+len(chords)+len(crossings)
assert regions == 31
fig.text(.5, .035, rf'$1+\binom{{6}}{{2}}+\binom{{6}}{{4}}=1+{len(chords)}+{len(crossings)}={regions}$', ha='center')
fig.subplots_adjust(bottom=.16, top=.98)
print(f'K41-n5: chords={len(chords)}, distinct crossings={len(crossings)}, regions={regions}, shaded vertices={len(poly)}')
save(fig, 'K41-n5')
