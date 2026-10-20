import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

removed = {(0, 0), (5, 5)}
black = sum((r+c) % 2 == 0 for r in range(6) for c in range(6) if (r, c) not in removed)
white = 36-len(removed)-black
assert (black, white) == (16, 18)
fig, ax = new_fig(14, 12)
for r in range(6):
    for c in range(6):
        gone = (r, c) in removed
        ax.add_patch(Rectangle((c, 5-r), 1, 1, facecolor=C.LIGHT if (r+c) % 2 == 0 and not gone else C.PAPER, edgecolor=C.GRAY, lw=.8, ls='--' if gone else '-'))
        if gone:
            label(ax, '×', (c+.5, 5.5-r), ha='center', va='center', fontsize=24)
for r, c in removed:
    ax.add_patch(Rectangle((c, 5-r), 1, 1, fill=False, edgecolor=C.PAPER, lw=2))
    ax.add_patch(Rectangle((c, 5-r), 1, 1, fill=False, edgecolor=C.GRAY, lw=1, ls='--'))
for x, y, w, h in [(1, 4, 2, 1), (4, 1, 1, 2)]:
    ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor=C.INK, lw=2.5))
label(ax, '骨牌', (1.5, 4.5), ha='center', va='center')
label(ax, '骨牌', (4.5, 2.5), ha='center', va='center')
for i in range(6):
    label(ax, str(i), (i+.5, 6.18), ha='center', va='bottom', fontsize=9)
    label(ax, str(i), (-.18, 5.5-i), ha='right', va='center', fontsize=9)
ax.set(xlim=(-.5, 6.2), ylim=(-.1, 6.65), aspect='equal')
ax.set_axis_off()
fig.subplots_adjust(bottom=.19, top=.98)
fig.text(.5, .11, '阴影 = 黑格；× = 去掉的格', ha='center')
fig.text(.5, .045, f'剩 {black} 个黑格、{white} 个白格；17 块骨牌需要黑、白各 17 格', ha='center', fontsize=9)
print(f'K41-n2: black={black}, white={white}')
save(fig, 'K41-n2')
