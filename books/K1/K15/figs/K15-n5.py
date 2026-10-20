import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(18, 8)
ax.set(xlim=(-230, 1190), ylim=(-1.25, 2.4)); ax.axis('off')
for y, total, repeat, title in [(1.5, 1000, 310, '推出前'), (0, 600, 228, '推出后')]:
    rest = total-repeat
    ax.barh(y, repeat, height=.6, color=C.LIGHT, edgecolor=C.INK, hatch='///', lw=1.2)
    ax.barh(y, rest, left=repeat, height=.6, color=C.PAPER, edgecolor=C.INK, lw=1.2)
    label(ax, f'复购 {repeat}', (repeat/2, y), ha='center', va='center', fontsize=9)
    label(ax, f'其余 {rest}', (repeat+rest/2, y), ha='center', va='center', fontsize=9)
    label(ax, f'{title}\n{repeat/total:.0%}', (-80, y), ha='center', va='center')
    label(ax, f'{total} 人', (total+25, y), va='center', fontsize=9)
assert 310/1000 == .31 and 228/600 == .38
ax.plot([0, 1000], [-.65, -.65], color=C.INK, lw=1)
for x in range(0, 1001, 200):
    ax.plot([x, x], [-.65, -.72], color=C.INK, lw=1)
    label(ax, str(x), (x, -.77), ha='center', va='top', fontsize=8)
label(ax, '人数；阴影 = 复购的顾客', (500, -1.2), ha='center', fontsize=9)
save(fig, "K15-n5")
