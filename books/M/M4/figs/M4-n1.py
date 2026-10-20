import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle

circles = np.array([(1, 1), (2, 1), (1, 3), (2, 2), (5, 4)])
squares = np.array([(4, 4), (5, 5), (4, 5), (6, 4)])
q = np.array([4.6, 4.2])
distances = np.linalg.norm(np.vstack([circles, squares]) - q, axis=1)
assert (np.count_nonzero(distances < 0.5), np.count_nonzero(distances < 0.9)) == (1, 3)
assert np.allclose(np.sort(distances)[:3], np.sqrt([0.2, 0.4, 0.8]))

fig, ax = new_fig(12, 11)
ax.scatter(*circles.T, s=46, marker='o', facecolors=C.PAPER,
           edgecolors=C.INK, linewidths=1.3, zorder=4, label='空心圆（○ 类）')
ax.scatter(*squares.T, s=42, marker='s', color=C.INK, zorder=4, label='实心方块（□ 类）')
ax.scatter(*q, s=110, marker='*', color=C.INK, zorder=5, label='新点')
for radius in (0.5, 0.9):
    ax.add_patch(Circle(q, radius, fill=False, edgecolor=C.GRAY, ls=':', lw=1.4))
label(ax, '$q$', q, (-10, 7), ha='right')
ax.annotate('$k=1$', xy=q + [0.32, -0.384], xytext=(3.3, 2.8),
            color=C.INK, arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.8))
ax.annotate('$k=3$', xy=q + [0.65, 0.6225], xytext=(5.65, 5.8),
            color=C.INK, arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.8))
ax.annotate('噪声点（○）', xy=(5, 3.94), xytext=(5.0, 3.05),
            color=C.INK, fontsize=9,
            arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.8))
ax.set(xlim=(0, 7), ylim=(0, 7), xlabel='$x$', ylabel='$y$')
ax.set_aspect('equal')
ax.set_xticks(range(8)); ax.set_yticks(range(8))
ax.legend(loc='upper left', fontsize=9)
fig.tight_layout()
save(fig, "M4-n1")
