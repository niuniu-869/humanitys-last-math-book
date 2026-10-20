import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(14, 9)
ax.set_xlim(-0.8, 13.8); ax.set_ylim(-7.5, 5.0); ax.axis('off')
inp = np.array([[1,3,2,1],[4,2,0,5],[6,1,3,3],[2,0,1,4]])
maxpos = {(1,0),(1,3),(2,0),(3,3)}
def grid(x0, y0, data, fill_positions=None, texts=None, thick=False):
    for r in range(4):
        for c in range(4):
            fc = C.LIGHT if fill_positions and (r,c) in fill_positions else C.PAPER
            lw = 0.8
            ax.add_patch(Rectangle((x0+c, y0-r-1), 1, 1, facecolor=fc, edgecolor=C.INK, lw=lw))
            value = texts.get((r,c), data[r,c]) if texts is not None else data[r,c]
            label(ax, str(value), (x0+c+0.5, y0-r-0.5), offset=(-3,-5), fontsize=10)
grid(0, 4, inp, maxpos, thick=True)
for br in (0,2):
    for bc in (0,2):
        ax.add_patch(Rectangle((bc, 4-br-2), 2, 2, fill=False, edgecolor=C.INK, lw=2.0, zorder=7))
label(ax, '输入', (1.5,4.45), offset=(-12,0), fontsize=10)
arrow(ax, (4.6,2.1), (2.0,0), text='最大池化', lw=1.8, offset=(-15,10))
out = np.array([[4,5],[6,4]])
for r in range(2):
    for c in range(2):
        ax.add_patch(Rectangle((8+c, 3-r-1), 1, 1, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0)); label(ax, str(out[r,c]), (8.5+c,2.5-r), offset=(-3,-5), fontsize=10)
label(ax, '输出', (9,4.45), offset=(-12,0), fontsize=10)
texts = {(1,0):1,(1,3):2,(2,0):3,(3,3):4}
grid(0, -1.4, np.zeros((4,4),dtype=int), texts=texts)
label(ax, '反向误差', (1.5,-6.5), offset=(-23,0), fontsize=10)
save(fig, "M8-n6")
