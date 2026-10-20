import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

X = np.array([[57, 51, 10], [59, 47, 10], [60, 50, 10], [62, 51, 8], [62, 51, 12]], dtype=float)
W = np.array([[2, 1], [1, -2], [0, 0]], dtype=float) / np.sqrt(5)
scores = (X - X.mean(axis=0)) @ W
a = np.sqrt(5)
assert np.allclose(scores, [[-a, -a], [-a, a], [0, 0], [a, 0], [a, 0]])
fig, ax = new_fig(10, 10)
ax.axhline(0, ls='--', color=C.GRAY, lw=1)
ax.axvline(0, ls='--', color=C.GRAY, lw=1)
for i, name in [(0, '1'), (1, '2'), (2, '3'), (3, '4, 5')]:
    dot(ax, scores[i], name, offset=(8, 8), size=30)
ax.set(xlim=(-3, 3.25), ylim=(-3, 3), xlabel='$t_1$', ylabel='$t_2$')
ax.set_aspect('equal')
ax.set_xticks([-2, -1, 0, 1, 2, 3])
ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])
fig.tight_layout()
save(fig, "M5-n6")
