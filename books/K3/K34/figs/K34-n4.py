import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

assert 4 <= 7 <= 8 < 10 <= 10.5 < 12
fig, ax = new_fig(18, 9)
y_o, y_g = 1.7, 0.0
ax.hlines([y_o, y_g], 0, 12, color=C.GRAY, lw=.8)
for t in range(13):
    ax.plot([t, t], [-.98, -.88], color=C.GRAY, lw=.8)
    label(ax, str(t), (t, -1.04), ha="center", va="top", fontsize=8)
ax.plot([0,12],[-.93,-.93],color=C.GRAY,lw=.8)
label(ax, "时间", (12.25,-.93), va="center", fontsize=9)
label(ax, "最优方案 O", (-.25, y_o), ha="right", va="center", fontsize=10)
label(ax, "换成 g1 后", (-.25, y_g), ha="right", va="center", fontsize=10)
def seg(a, b, y, ls="-", lw=3.2):
    ax.plot([a, b], [y, y], color=C.INK, ls=ls, lw=lw, solid_capstyle="butt", zorder=3)
    ax.plot([a, a], [y-.11, y+.11], color=C.INK, lw=1.0, zorder=3)
    ax.plot([b, b], [y-.11, y+.11], color=C.INK, lw=1.0, zorder=3)
seg(2, 7, y_o); seg(8, 10, y_o); seg(10.5, 12, y_o)
seg(1, 4, y_g); seg(8, 10, y_g); seg(10.5, 12, y_g)
seg(2, 7, y_g+.45, ls="--", lw=1.6)
label(ax, "o1", (4.5, y_o), offset=(0, 9), ha="center", fontsize=9)
label(ax, "o2", (9, y_o), offset=(0, 9), ha="center", fontsize=9)
label(ax, "o3", (11.25, y_o), offset=(0, 9), ha="center", fontsize=9)
label(ax, "g1", (2.5, y_g), offset=(0, -14), ha="center", fontsize=9)
label(ax, "o1 被换掉", (5.5, y_g+.45), offset=(0, 9), ha="center", fontsize=9)
label(ax, "o2", (9, y_g), offset=(0, 9), ha="center", fontsize=9)
label(ax, "o3", (11.25, y_g), offset=(0, 9), ha="center", fontsize=9)
for x in (4, 7, 8):
    ax.plot([x, x], [-.85, 2.35], color=C.INK, ls=":", lw=1.0, zorder=1)
label(ax, "g1 结束更早", (5.5, 2.55), ha="center", va="center", fontsize=9)
label(ax, "后面的会议开始时间不早于 7\n所以也不早于 4", (9.8, 3.2),
      ha="center", va="center", fontsize=9)
ax.set(xlim=(-2.5, 13.0), ylim=(-1.55, 3.8))
ax.set_xticks([]); ax.set_yticks([])
ax.spines[:].set_visible(False)
save(fig, "K34-n4")
