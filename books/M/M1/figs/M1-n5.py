import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

H = np.array([[22., 6.], [6., 2.]]); xstar = np.array([1.7, -0.1])
def grad(t): return H @ (t - xstar)
def loss(t):
    d = t - xstar; return 0.5*np.einsum('...i,ij,...j->...', d, H, d)
fig, ax = new_fig(12, 8)
w = np.linspace(-0.6, 3.2, 400); b = np.linspace(-1.4, 1.4, 400); W, B = np.meshgrid(w, b)
ax.contour(W, B, loss(np.stack([W, B], -1)), levels=np.geomspace(.04, 60, 14), colors=C.LIGHT, linewidths=.7)
t = np.zeros(2); gd = [t.copy()]
for _ in range(60): t = t - .02*grad(t); gd.append(t.copy())
t = np.zeros(2); v = np.zeros(2); mo = [t.copy()]
for _ in range(60): v = .9*v + grad(t); t = t - .02*v; mo.append(t.copy())
gd = np.array(gd); mo = np.array(mo)
ax.plot(gd[:,0], gd[:,1], color=C.INK, lw=1.3); ax.scatter(gd[::5,0], gd[::5,1], s=22, color=C.INK, zorder=5)
ax.plot(mo[:,0], mo[:,1], color=C.GRAY, ls='--', lw=1.3); ax.scatter(mo[::3,0], mo[::3,1], s=22, facecolors=C.PAPER, edgecolors=C.GRAY, zorder=6)
label(ax, '实线加实心点：普通梯度下降，每 5 步一点', (-0.5, -0.95), offset=(0, 0)); label(ax, '虚线加空心点：动量 $\\beta=0.9$，每 3 步一点', (-0.5, -1.2), offset=(0, 0), color=C.GRAY)
ax.scatter([xstar[0]], [xstar[1]], marker='*', s=90, color=C.INK, zorder=7); label(ax, '最小点', xstar, offset=(10, -18))
ax.set(xlim=(-0.6, 3.2), ylim=(-1.4, 1.4), xlabel='$w$', ylabel='$b$', aspect='equal')
save(fig, 'M1-n5')
