import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

groups = np.array([[8, 10, 9, 11, 12], [13, 12, 15, 14, 16], [10, 12, 11, 13, 14]])
means = groups.mean(axis=1)
grand = groups.mean()
assert np.allclose(means, [10, 14, 12]) and grand == 12
fig, ax = new_fig(17, 10)
centers = [0, 2, 5]
offsets = np.array([-.24, -.12, 0, .12, .24])
ax.axhline(grand, color=C.GRAY, ls='--', lw=1.2)
for i, (center, values, marker) in enumerate(zip(centers, groups, ['o', 's', '^'])):
    ax.scatter(center + offsets, values, marker=marker, s=33,
               facecolor=C.PAPER if i == 1 else C.INK, edgecolor=C.INK, zorder=5)
    ax.plot([center - .4, center + .4], [means[i]] * 2, color=C.INK, lw=1.8)
    label(ax, f'均值 {means[i]:.0f}', (center, 7), ha='center')
ax.plot([2, 2], [12, 14], color=C.INK, lw=3.2)
ax.plot([2, 2], [14, 15], color=C.INK, lw=1)
label(ax, r'组间 $\bar X_i-\bar X$', (2.25, 12.8), offset=(4, 0))
label(ax, r'组内 $X_{ij}-\bar X_i$', (2.25, 15.4), offset=(4, 0))
ax.annotate('', xy=(3.8, 15), xytext=(3.8, 12),
            arrowprops=dict(arrowstyle=']-[', color=C.INK, lw=1, mutation_scale=6))
label(ax, r'$X_{ij}-\bar X$', (3.8, 13.5), offset=(8, 0), va='center')
label(ax, '全体均值 12', (-.65, 12), offset=(0, 8))
ax.set(xlim=(-.8, 5.65), ylim=(6, 18), ylabel='停留时长', xlabel='组别')
ax.set_xticks(centers, ['A', 'B', 'C'])
fig.subplots_adjust(left=.1, right=.98, bottom=.14, top=.96)
save(fig, "P13-n1")
