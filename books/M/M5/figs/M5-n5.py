import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

X = np.array([[1, 2], [2, 3], [3, 5], [4, 6], [5, 9]], dtype=float)
centered = X - X.mean(axis=0)
scaled = centered * [1, 10]
Z = centered / X.std(axis=0, ddof=1)
values, vectors = np.linalg.eigh(np.cov(scaled, rowvar=False))
w = vectors[:, -1]
w *= np.sign(w[1])
assert np.allclose(scaled, [[-2, -30], [-1, -20], [0, 0], [1, 10], [2, 40]])
assert np.allclose(np.diag(np.cov(Z, rowvar=False)), 1)
assert np.allclose(np.cov(Z, rowvar=False) @ np.ones(2), np.repeat(np.cov(Z, rowvar=False).sum(axis=1)[0], 2))
fig, (left, right) = new_fig(17.5, 9, ncols=2)
left.scatter(*scaled.T, s=26, color=C.INK, zorder=4)
left.plot(*np.outer([-44, 44], w).T, ls='-', color=C.INK, label='第一主成分')
left.set(xlim=(-3, 3), ylim=(-45, 45), xlabel=r'$x-\bar{x}$', ylabel=r'$10(y-\bar{y})$',
         title='中心化后（y 放大十倍）')
left.set_xticks([-3, -2, -1, 0, 1, 2, 3])
left.set_yticks([-40, -20, 0, 20, 40])
right.scatter(*Z.T, s=26, color=C.INK, zorder=4)
u = np.array([1., 1.]) / np.sqrt(2)
v = np.array([-1., 1.]) / np.sqrt(2)
right.plot(*np.outer([-2.2, 2.2], u).T, ls='-', color=C.INK, label='第一主成分')
right.plot(*np.outer([-.9, .9], v).T, ls='--', color=C.INK, label='第二主成分')
right.set(xlim=(-1.8, 1.8), ylim=(-1.8, 1.8), xlabel='$z_x$', ylabel='$z_y$', title='标准化后')
right.set_aspect('equal')
for ax in (left, right):
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.21), fontsize=9)
fig.tight_layout(w_pad=2)
save(fig, "M5-n5")
