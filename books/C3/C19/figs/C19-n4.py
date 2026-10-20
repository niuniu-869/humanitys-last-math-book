import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from _geometry import setup, line, vector, text, axes, fill, point, bounds
from itertools import product

fig, ax = setup(13, 12)
o = np.zeros(3); a = np.array([3., 0, 0]); b = np.array([1., 2, 0]); c = np.array([1., 1, 4.])
n = np.cross(a, b); foot = c.copy(); foot[2] = 0
fill(ax, [o, a, a+b, b])
bits = list(product([0, 1], repeat=3))
verts = [i*a+j*b+k*c for i, j, k in bits]
for i, p in enumerate(verts):
    for j in range(i+1, len(verts)):
        if sum(x != y for x, y in zip(bits[i], bits[j])) == 1:
            hidden = bits[i] == (0, 0, 0) or bits[j] == (0, 0, 0)
            line(ax, [p, verts[j]], ls='--' if hidden else '-', lw=1.2)
vector(ax, o, n, lw=2.5)
line(ax, [c, foot], ls=':', lw=2)
line(ax, [foot+[.2, 0, 0], foot+[.2, 0, .2], foot+[0, 0, .2]], lw=1)
point(ax, c, hollow=True)
axes(ax, [4.6, 3.4, 6.6])
text(ax, n, r'$\boldsymbol{a}\times\boldsymbol{b}$', (10, -5), fontsize=12)
text(ax, (foot+c)/2, '$h=4$', (72, 10))
text(ax, (a+b)/2, '底面积 $6$', (12, -24))
text(ax, a, r'$\boldsymbol{a}$', (-6, 12))
text(ax, b, r'$\boldsymbol{b}$', (6, 6))
text(ax, c, r'$\boldsymbol{c}$', (6, 6))
assert np.allclose(n, [0, 0, 6])
assert np.isclose(n @ c, 24)
assert np.isclose(c @ (n/np.linalg.norm(n)), 4)
bounds(ax, verts+[n, [0, 3.4, 0], [0, 0, 6.6]], 1)
save(fig, 'C19-n4')
