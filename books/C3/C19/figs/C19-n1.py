import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from _geometry import setup, line, vector, text, point, axes, bounds
from itertools import product

fig, ax = setup(13, 11)
P1, Q, P2 = np.array([0., 0., 0.]), np.array([3., 2., 0.]), np.array([3., 2., 4.])
vertices = np.array(list(product([0., 3.], [0., 2.], [0., 4.])))
for i, p in enumerate(vertices):
    for q in vertices[i+1:]:
        if np.count_nonzero(p != q) == 1:
            line(ax, [p, q], lw=1)
line(ax, [P1, Q], ls='--', lw=1.8)
line(ax, [Q, P2], lw=2.5)
line(ax, [P1, P2], lw=2.5)
u = (P1-Q)/np.linalg.norm(P1-Q)*0.27
v = np.array([0, 0, 0.27])
line(ax, [Q+u, Q+u+v, Q+v], lw=1)
axes(ax, [3.65, 2.65, 4.7], origin='')
text(ax, [0, 0, 0], r'$P_1=O$', (-8, 9), fontsize=9, ha='right')
point(ax, P2, hollow=True)
point(ax, Q, square=True)
P2label = np.array([1.55, 2.0, 4.95])
line(ax, [P2, P2label], lw=.8, ls=':')
text(ax, P2label, r'$P_2;\ d(P_1,P_2)=\sqrt{29}$', (4, -2), fontsize=10)
text(ax, Q, '$Q$：底面上与 $P_1$ 相对的顶点；\n虚线是 $P_1Q$', (6, -12), fontsize=9.2, ha='left', va='top')
# Three edge lengths are consolidated outside the solid to limit annotation clutter.
text(ax, [3, 0, 4], r'$|x_2-x_1|=3$'+'\n'+r'$|y_2-y_1|=2$'+'\n'+r'$|z_2-z_1|=4$', (-18, 14), ha='right', fontsize=10)
assert np.isclose(np.dot(Q-P1, P2-Q), 0)
assert np.isclose(np.linalg.norm(P2-P1)**2, 29)
bounds(ax, np.vstack([vertices, [0, 0, 4.8], [0, 3.1, 0]]), 1)
save(fig, 'C19-n1')
