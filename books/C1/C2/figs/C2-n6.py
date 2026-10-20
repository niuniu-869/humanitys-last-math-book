import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(17, 9)
z = np.array([2., 1., 0.])
temps = np.array([0.25, 1., 10.])
weights = np.exp((z[None, :] - z.max())/temps[:, None])
p = weights/weights.sum(axis=1, keepdims=True)
assert np.allclose(p.sum(axis=1), 1)
groups = np.arange(3)*1.35
width = 0.29
for j, hatch in enumerate(['///', '\\\\', '...']):
    positions = groups+(j-1)*width
    ax.bar(positions, p[:, j], width=width, facecolor=C.PAPER, edgecolor=C.INK, hatch=hatch, linewidth=1, label='分数 '+str(int(z[j])))
    for pos, v in zip(positions, p[:, j]):
        # The near-unit bar gets its value above the axes, inside the figure margin.
        label(ax, f'{v:.4f}', (pos, v), offset=(0, 5), ha='center', va='bottom', fontsize=9, annotation_clip=False)
ax.axhline(1/3, color=C.GRAY, ls=':', lw=1)
label(ax, r'$\frac{1}{3}$', (3.22, 1/3), offset=(0, 5), ha='center')
ax.set(xlim=(-0.62, 3.35), ylim=(0, 1), ylabel='概率')
ax.set_xticks(groups, ['$T=0.25$', '$T=1$', '$T=10$'])
ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax.legend(loc='upper center', bbox_to_anchor=(0.58, 1.17), ncol=3, fontsize=9)
fig.subplots_adjust(left=0.1, right=0.98, bottom=0.13, top=0.83)
save(fig, "C2-n6")
