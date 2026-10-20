import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 12)
x = 0.9
P = np.array([np.cos(x), np.sin(x)])
T = np.array([1, np.tan(x)])
assert np.sin(x)/2 < x/2 < np.tan(x)/2
t = np.linspace(0, 2*np.pi, 1000)
s = np.linspace(0, x, 300)
# 扇形 OAP 整体填浅灰：O -> 弧 AP -> O，含弦 PA 外侧的弓形。
ax.fill(np.r_[0, np.cos(s), 0], np.r_[0, np.sin(s), 0], color=C.LIGHT, zorder=0)
ax.plot(np.cos(t), np.sin(t), color=C.INK, ls='-', lw=1.2)
ax.plot([0, 1, 1, 0], [0, 0, T[1], 0], color=C.INK, ls='-', lw=1.4)
# 三角形 OAP 的三条边 OA、AP、PO 都画实线，不另填色；T、P、O 共线，PO 边由上面的 OT 实线给出。
ax.plot([1, P[0]], [0, P[1]], color=C.INK, ls='-', lw=1.1)
ax.plot([P[0], P[0]], [0, P[1]], color=C.INK, ls=':', lw=1)
ax.plot(0.23*np.cos(s), 0.23*np.sin(s), color=C.INK, ls='-', lw=0.8)
for point, text, off in [((0, 0), '$O$', (-13, -14)), ((1, 0), '$A$', (7, -13)), (P, '$P$', (-20, 20)), (T, '$T$', (7, 3))]:
    dot(ax, point, text=text, offset=off, size=22)
label(ax, '$x$', (0.29, 0.11))
label(ax, '1', (0.5, -0.13), ha='center')
label(ax, r'$\sin x$', (P[0]-0.08, 0.32), ha='right')
label(ax, r'$\tan x$', (1.08, 0.58))
ax.set(xlim=(-1.15, 1.46), ylim=(-1.12, 1.46), xlabel='$x$', ylabel='$y$', aspect='equal')
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])
label(ax, r'三角形 $OAP$ < 扇形 $OAP$ < 三角形 $OAT$', (0.5, -0.21), xycoords='axes fraction', ha='center', annotation_clip=False, fontsize=9)
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.22, top=0.98)
save(fig, "C2-n4")
