import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(18, 9)
fig.subplots_adjust(left=0.08, right=0.68, bottom=0.16, top=0.88)
x = np.linspace(3.5, 5.5, 600)
yc, yt = np.sqrt(5), 2.25
assert np.isclose(yt-yc, 0.01393202250021)
ax.plot(x, np.sqrt(x), color=C.INK, ls='-', label=r'$y=\sqrt{x}$')
ax.plot(x, 2+(x-4)/4, color=C.RED, ls='--', label='切线')
for a in (4, 5):
    ax.axvline(a, color=C.GRAY, ls='--', lw=0.7)
ax.plot([4, 5], [2, 2], color=C.GRAY, ls=':')
# A wide solid stroke and narrow dashed stroke share the true x=5 location.
ax.plot([5, 5], [2, yc], color=C.TEAL, lw=4, ls='-')
ax.plot([5, 5], [2, yt], color=C.INK, lw=1.4, ls='--')
dot(ax, (4, 2), r'$P_0=(4,2)$', offset=(-58, 10))
dot(ax, (5, yc), size=14)
ax.scatter([5], [yt], s=22, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, r'$\Delta x=\mathrm{d}x=1$', (4.5, 2), (0, -21), ha='center')
# 两条细引线分别指向曲线上的增量段与切线上的增量段。
label(ax, r'$\Delta y\approx0.236$', (5, 2.16), (8, -16), ha='left', va='center', fontsize=8.5,
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6, shrinkA=1, shrinkB=1))
label(ax, r'$\mathrm{d}y=0.25$', (5, yt), (10, -8), ha='left', va='center', fontsize=9,
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6, shrinkA=1, shrinkB=1))
ax.set(xlim=(3.5, 5.5), ylim=(1.7, 2.5), xlabel='$x$', ylabel='$y$')
ax.set_aspect('equal')
ax.set_xticks([3.5, 4, 5, 5.5])
ax.set_yticks([1.8, 2, 2.5])
ax.legend(loc='upper left', bbox_to_anchor=(0, 1.32), ncol=2)

zoom = fig.add_axes([0.77, 0.27, 0.19, 0.42])
xx = np.linspace(4.998, 5.002, 200)
zoom.plot(xx, np.sqrt(xx), color=C.INK, ls='-')
zoom.plot(xx, 2+(xx-4)/4, color=C.RED, ls='--')
zoom.plot([5, 5], [yc, yt], color=C.INK, lw=2)
dot(zoom, (5, yc), size=24)
zoom.scatter([5], [yt], s=32, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
zoom.set(xlim=(4.998, 5.002), ylim=(2.230, 2.256), xlabel='$x$', ylabel='$y$')
zoom.set_xticks([5]); zoom.set_yticks([yc, yt], ['2.2361', '2.25'])
zoom.tick_params(labelsize=8)
zoom.set_title('局部放大', pad=12)
label(zoom, r'差 $\approx0.014$'+'\n'+r'比 $\Delta x$ 小得多', (0.5, -0.36),
      xycoords='axes fraction', ha='center', va='top', fontsize=9, annotation_clip=False)
save(fig, "C5-n1")
