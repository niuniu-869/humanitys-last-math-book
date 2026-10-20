import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

win = [False]
for n in range(1, 22):
    win.append(any(not win[n-k] for k in range(1, min(3, n)+1)))
assert [n for n in range(22) if not win[n]] == list(range(0, 22, 4))
fig, ax = new_fig(20, 7)
arrow(ax, (-.6, 0), (22.3, 0), color=C.INK, lw=.8)
for n in range(22):
    ax.scatter(n, 0, marker='o' if win[n] else 's', s=30, facecolor=C.PAPER if win[n] else C.INK, edgecolor=C.INK, zorder=5)
    label(ax, str(n), (n, 0), offset=(0, -17), ha='center', fontsize=8)
    label(ax, '赢' if win[n] else '输', (n, 0), offset=(0, -34), ha='center', fontsize=8)
for start, end, rad in [(5, 4, .65), (6, 4, .85), (7, 4, 1.0), (21, 20, .7)]:
    assert 1 <= start-end <= 3 and not win[end]
    ax.annotate('', xy=(end, .08), xytext=(start, .08), arrowprops=dict(arrowstyle='-|>', connectionstyle=f'arc3,rad={rad}', color=C.INK, lw=.9, shrinkA=5, shrinkB=5))
for text, xy in [('5→4：取 1', (2, 1.3)), ('6→4：取 2', (6, 1.3)), ('7→4：取 3', (10, 1.3)), ('取 1', (20.5, .45))]:
    label(ax, text, xy, ha='center', fontsize=9)
label(ax, '先手', (21, 1.1), ha='center')
label(ax, '先取 1 颗，留下 20', (21.5, 1.65), ha='right')
ax.set(xlim=(-.7, 21.8), ylim=(-.85, 2), aspect='auto')
ax.set_axis_off()
fig.text(.5, .04, '必输局面：$n$ 是 4 的倍数', ha='center')
fig.subplots_adjust(bottom=.15, top=.98, left=.03, right=.98)
print('K41-n3: losing=', [n for n in range(22) if not win[n]])
save(fig, 'K41-n3')
