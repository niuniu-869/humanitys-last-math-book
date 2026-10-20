import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from _geometry import setup, line, text, point, axes, ring, bounds

fig, ax = setup(13, 11)
for r in [.5, 1., 1.8, 2.]:
    line(ax, ring(r, r*r/2), color=C.GRAY, lw=.7)
y = np.linspace(0, 2, 151)
line(ax, np.column_stack((0*y, y, y*y/2)), lw=2.6)
M1 = np.array([0., 1.5, 1.125])
angle = np.deg2rad(215)
M = np.array([1.5*np.cos(angle), 1.5*np.sin(angle), 1.125])
center = np.array([0., 0, 1.125])
line(ax, ring(1.5, M1[2]), ls='--', lw=1.8)
line(ax, [center, M], lw=1.2)
point(ax, M1); point(ax, M, hollow=True)
axes(ax, [2.7, 2.8, 3.1])
text(ax, M1, '$M_1$', (12, -3))
text(ax, M, '$M(x,y,z)$', (-12, 16), ha='right')
label(ax, r'$\sqrt{x^2+y^2}=|y_1|$'+'\n'+'高度 $z$ 不变', (-1.8, -1.85), ha='center', fontsize=10)
assert np.isclose(M1[2], M1[1]**2/2)
assert np.isclose(np.linalg.norm(M[:2]), abs(M1[1])) and M[2] == M1[2]
bounds(ax, np.vstack([ring(2, 2), [0, 0, 3.1], [2.7, 0, 0], [0, 2.8, 0]]), 1)
save(fig, 'C19-n7')
