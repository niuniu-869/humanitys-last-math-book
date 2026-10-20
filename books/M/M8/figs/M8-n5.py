import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(13, 7)
ax.set_xlim(-2.2, 11.5); ax.set_ylim(-5.0, 2.2); ax.axis('off')
for i in range(10):
    ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0)); label(ax, str(i), (i+0.5,0.5), offset=(-3,-5), fontsize=9)
label(ax, '输入的列号', (0,1.0), offset=(0,8), fontsize=8)
for row, start in enumerate((0,2,4,6)):
    y = -0.9 - row*0.85
    ax.plot([start, start+3], [y,y], color=C.INK, lw=1.3); ax.plot([start,start], [y-0.22,y+0.22], color=C.INK, lw=1.3); ax.plot([start+3,start+3], [y-0.22,y+0.22], color=C.INK, lw=1.3)
    label(ax, rf'$y_{row}$', (start+3.3,y), offset=(0,-4), fontsize=9)
    label(ax, f'起点 {start}', (start-0.2,y), offset=(-38,-4), fontsize=8)
ax.add_patch(Rectangle((9, -0.08), 1, 1.16, fill=False, edgecolor=C.GRAY, lw=1.3, linestyle=':')); label(ax, '第 9 列未被使用', (9.5,0.5), offset=(-45,-28), fontsize=8)
label(ax, r'$\lfloor(10-3)/2\rfloor+1=4$', (0,-4.4), fontsize=11)
save(fig, "M8-n5")
