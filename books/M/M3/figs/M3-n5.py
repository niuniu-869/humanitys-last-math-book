import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

vertices = np.array([[0, 0], [0, 1/2], [1/3, 1/2], [1/3, 1], [2/3, 1], [1, 1]])
area = np.sum(np.diff(vertices[:, 0])*(vertices[:-1, 1]+vertices[1:, 1])/2)
assert np.isclose(area, 5/6)
fig, ax = new_fig(13, 12)
ax.fill_between(vertices[:, 0], vertices[:, 1], color=C.LIGHT, alpha=0.55)
ax.plot(*vertices.T, ls='-', color=C.INK, lw=2, clip_on=False, zorder=4)
ax.plot([0, 1], [0, 1], ls='--', color=C.GRAY, lw=1.2, label='随机猜测')
ax.scatter(*vertices[1:].T, s=18, color=C.INK, zorder=5, clip_on=False)
offsets = [(7, 9), (-8, -20), (8, -17), (8, -17), (-7, -82)]
aligns = ['left', 'right', 'left', 'left', 'right']
for xy, text, offset, ha in zip(vertices[1:],
        ['0.826（正例）', '0.615（负例）', '0.349（正例）',
         '0.153（负例）', '0.057（负例）'], offsets, aligns):
    label(ax, text, xy, offset=offset, ha=ha, fontsize=9)
label(ax, r'$\mathrm{AUC}=5/6$', (0.67, 0.27), ha='center', fontsize=13)
ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='FPR', ylabel='TPR')
ax.set_aspect('equal')
ax.set_xticks([0, 1/3, 2/3, 1], ['0', '$1/3$', '$2/3$', '1'])
ax.set_yticks([0, 0.5, 1], ['0', '$1/2$', '1'])
ax.legend(loc='lower right', fontsize=9)
fig.tight_layout()
save(fig, "M3-n5")
