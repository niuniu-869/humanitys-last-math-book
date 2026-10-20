import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

points = np.array([[1, 2], [2, 3], [3, 5], [4, 6], [5, 9]], dtype=float)
mean = points.mean(axis=0)
values, vectors = np.linalg.eigh(np.cov(points, rowvar=False))
w = vectors[:, 1]
w *= np.sign(w[0])
v = np.array([-w[1], w[0]])
projected = mean + np.outer((points - mean) @ w, w)
assert np.allclose((points - projected) @ w, 0)
fig, ax = new_fig(12, 13)
for point, foot in zip(points, projected):
    ax.plot(*np.array([point, foot]).T, ls=':', color=C.GRAY, lw=1.2)
ax.plot(*(mean + np.outer([-4.0, 4.8], w)).T, ls='-', color=C.INK,
        label=f'第一主成分，方差 {values[1]:.2f}')
ax.plot(*(mean + np.outer([-2, 2], v) * np.sqrt(values[0])).T,
        ls='--', color=C.INK, lw=1.8, label=f'第二主成分，方差 {values[0]:.2f}')
ax.scatter(*points.T, s=25, color=C.INK, zorder=4)
ax.scatter(*mean, marker='+', s=180, linewidths=1.8, color=C.INK, zorder=5)
label(ax, '平均值', mean, offset=(25, -18), fontsize=9)
ax.set(xlim=(0, 6), ylim=(0, 10), xlabel='$x$', ylabel='$y$')
ax.set_aspect('equal')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), fontsize=9)
fig.tight_layout()
save(fig, "M5-n1")
