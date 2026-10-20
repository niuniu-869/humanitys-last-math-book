import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(15, 15, nrows=2, sharex=True, sharey=True)
for ax, times, title in zip(axes, [[0, 10, 20], [0, 5, 20]], ['间隔都是 10 分钟', '间隔 5 与 15 分钟交替']):
    gaps = np.diff(times)
    areas = gaps**2/2
    total, mean = areas.sum(), areas.sum()/(times[-1]-times[0])
    for start, end in zip(times[:-1], times[1:]):
        ax.fill([start, start, end], [0, end-start, 0], color=C.LIGHT)
        ax.plot([start, end], [end-start, 0], color=C.INK, ls='-', lw=1.6)
        ax.scatter(start, end-start, s=24, facecolor=C.PAPER, edgecolor=C.INK, zorder=4)
    ax.scatter(times, np.zeros(3), marker='^', s=42, color=C.INK, zorder=5, clip_on=False)
    for t in times:
        label(ax, '车', (t, 0), offset=(0, 9), ha='center', fontsize=8)
    terms = r'2\times'+f'{areas[0]:g}' if areas[0] == areas[1] else '+'.join(f'{a:g}' for a in areas)
    label(ax, f'面积 ${terms}={total:g}$，平均等 ${total:g}/20={mean:g}$', (10, 15.8), ha='center', fontsize=9)
    ax.set(xlim=(-.5, 20.5), ylim=(-.5, 17), xticks=[0, 5, 10, 15, 20], yticks=[0, 5, 10, 15], ylabel='$w$（分钟）', title=title)
    ax.tick_params(labelbottom=True)
    ax.set_xlabel('$t$（分钟）')
    print(f'K41-n4: gaps={gaps.tolist()}, areas={areas.tolist()}, mean={mean}')
fig.subplots_adjust(left=.13, right=.96, bottom=.09, top=.94, hspace=.45)
save(fig, 'K41-n4')
