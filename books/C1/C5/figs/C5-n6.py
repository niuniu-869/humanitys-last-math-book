import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 13)
fig.subplots_adjust(left=0.09, right=0.97, bottom=0.09, top=0.97)
h = 1.5; r = h/2
assert r == 0.75 and r/h == 2/4
ax.fill([-r, 0, r], [h, 0, h], color=C.LIGHT, zorder=0)
ax.plot([-2, 0, 2, -2], [4, 0, 4, 4], color=C.INK, ls='-')
ax.plot([-r, r], [h, h], color=C.INK, ls='--')
arrow(ax, (-2.8, 0), (5.6, 0), color=C.GRAY, lw=0.7, text='$x$')
arrow(ax, (0, -0.3), (0, 5.1), color=C.GRAY, lw=0.7, text='$y$')
dot(ax, (0, 0), '$O$', offset=(8, -14), size=16)

def dimension(start, end):
    ax.annotate('', xy=end, xytext=start,
                arrowprops=dict(arrowstyle='<->', color=C.INK, lw=0.9, shrinkA=0, shrinkB=0))

dimension((-2.45, 0), (-2.45, 4))
for y in (0, 4):
    ax.plot([-2.6, -2], [y, y], color=C.GRAY, ls=':', lw=0.7)
label(ax, '深 $4$', (-2.45, 2.8), (-7, 0), ha='right')
dimension((0, 4.4), (2, 4.4))
ax.plot([2, 2], [4, 4.55], color=C.GRAY, ls=':', lw=0.7)
label(ax, '半径 $2$', (1, 4.4), (0, 9), ha='center')
dimension((1.25, 0), (1.25, h))
ax.plot([r, 1.45], [h, h], color=C.GRAY, ls=':', lw=0.7)
label(ax, '水深 $h$', (1.25, h/2), (9, 0))
dimension((0, h+0.32), (r, h+0.32))
ax.plot([r, r], [h, h+0.45], color=C.GRAY, ls=':', lw=0.7)
label(ax, '水面\n半径 $r$', (r/2, h+0.32), (0, 12), ha='center')
label(ax, r'$r=\frac{h}{2}$', (-0.25, 0.65), (-10, 0), ha='right')
ax.set(xlim=(-3.1, 3.1), ylim=(-0.5, 5.1))
ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
save(fig, "C5-n6")
