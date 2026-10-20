import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Patch

fig, ax = new_fig(19, 11)
fig.subplots_adjust(left=.11, right=.98, bottom=.30, top=.85)
ax.set(xlim=(-1.4, 9.7), ylim=(0, 103), ylabel='回购率')
ax.set_yticks([0, 20, 40, 60, 80, 100], ['0%', '20%', '40%', '60%', '80%', '100%'])
ax.set_xticks([0, 4, 8], ['老顾客', '新顾客', '合计'])
ax.tick_params(axis='x', length=0, pad=43)
for center, pairs in zip([0, 4, 8], [[(18, 20), (64, 80)], [(32, 80), (6, 20)], [(50, 100), (70, 100)]]):
    widths = [n*.012 for _, n in pairs]
    gap = .58
    xs = [center-gap/2-widths[0]/2, center+gap/2+widths[1]/2]
    for j, (x, w, (k, n)) in enumerate(zip(xs, widths, pairs)):
        rate = 100*k/n
        ax.bar(x, rate, width=w, facecolor=C.LIGHT if j == 0 else C.PAPER,
               edgecolor=C.INK, hatch='///' if j == 0 else None, lw=1.2)
        label(ax, f'{rate:.0f}%', (x, rate), offset=(0, 5), ha='center', va='bottom', fontsize=9)
        label(ax, f'{"甲" if j == 0 else "乙"}\n{k}/{n}', (x, 0), offset=(0, -9),
              ha='center', va='top', fontsize=9, annotation_clip=False)
ax.legend(handles=[Patch(facecolor=C.LIGHT, edgecolor=C.INK, hatch='///', label='甲'),
                   Patch(facecolor=C.PAPER, edgecolor=C.INK, label='乙')],
          loc='upper left', bbox_to_anchor=(0, 1.22), ncol=2)
fig.text(.97, .94, '宽度 = 发送人数', ha='right', color=C.INK, fontsize=9)
fig.text(.55, .035, '条下数字：回购人数 / 发送人数', ha='center', color=C.INK, fontsize=9)
assert (18+32, 64+6) == (50, 70)
save(fig, "K15-n6")
