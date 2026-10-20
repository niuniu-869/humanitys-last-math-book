import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
fail = [20, 35, 60, 90]
for i, t in enumerate(fail, 1):
    y = 11 - i
    ax.plot([0, t], [y, y], color=C.BLUE, ls='-', lw=1.4)
    ax.plot(t, y, marker='x', color=C.INK, ms=6, mew=1.2)
for i in range(5, 11):
    y = 11 - i
    ax.plot([0, 100], [y, y], color=C.BLUE, ls='-', lw=1.4)
    arrow(ax, (100, y), (5, 0), color=C.INK, lw=1.1)
ax.axvline(100, color=C.GRAY, ls='--', lw=1.1)
label(ax, '停止测试', (100, 10.2), offset=(5, 0))
for i in range(1, 11):
    label(ax, str(i), (0, 11-i), offset=(-14, -4))
label(ax, '总工作时间 = 20+35+60+90 + 6×100 = 805 小时', (3, 0.2), offset=(0, -4))
ax.set(xlim=(-3, 112), ylim=(-0.8, 10.8), xlabel='时间 t（小时）', yticks=[], xticks=[20, 35, 60, 90, 100])
save(fig, "P11-n3")
