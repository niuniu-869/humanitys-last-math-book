import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

before = np.array([12.4, 15.1, 9.8, 13.6, 11.2, 14.0])
after = np.array([11.5, 14.0, 9.1, 12.9, 10.6, 13.1])
fig, axes = new_fig(15, 7.5, ncols=2, sharey=True)
ax, bx = axes

for b, a in zip(before, after):
    ax.plot([0, 1], [b, a], color=C.INK, ls='-', lw=1.1)
    ax.scatter([0], [b], s=34, facecolors=C.PAPER, edgecolors=C.INK, zorder=4)
    ax.scatter([1], [a], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=4)
ax.set_title('按用户连线')
ax.set_xticks([0, 1], ['之前', '之后'])
ax.set_xlim(-.28, 1.28)
ax.set_ylim(8, 16)
ax.set_ylabel('停留时间（分钟）')

rng = np.random.default_rng(12)
j1 = rng.uniform(-.10, .10, len(before))
j2 = rng.uniform(-.10, .10, len(after))
bx.scatter(j1, before, s=34, facecolors=C.PAPER, edgecolors=C.INK, zorder=4)
bx.scatter(1 + j2, after, s=34, facecolors=C.INK, edgecolors=C.INK, zorder=4)
for x0, m in [(0, before.mean()), (1, after.mean())]:
    bx.plot([x0 - .18, x0 + .18], [m, m], color=C.INK, ls='-', lw=3.0, solid_capstyle='butt', zorder=3)
bx.set_title('当成独立两组')
bx.set_xticks([0, 1], ['之前', '之后'])
bx.set_xlim(-.28, 1.28)
label(bx, '两组范围重叠', (.5, 15.5), ha='center')
for a0 in axes:
    a0.grid(axis='y', color=C.LIGHT, lw=.7, ls=':')
fig.subplots_adjust(left=.11, right=.97, bottom=.15, top=.88, wspace=.18)
save(fig, 'P12-n3')
