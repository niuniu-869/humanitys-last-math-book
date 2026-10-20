import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x5 = np.arange(1, 6.); y5 = np.array([2, 3, 5, 6, 9.]); X = np.c_[x5, np.ones(5)]
H = 2/5 * X.T @ X; xstar = np.array([1.7, -0.1])
def loss(t):
    d = t - xstar; return 0.5*np.einsum('...i,ij,...j->...', d, H, d)
def g_i(t, i): return 2*(X[i] @ t - y5[i]) * X[i]
def g_full(t): return 2/5 * X.T @ (X @ t - y5)
fig, ax = new_fig(12, 8)
w = np.linspace(-0.6, 3.0, 400); b = np.linspace(-1.4, 1.4, 400); W, B = np.meshgrid(w, b)
ax.contour(W, B, loss(np.stack([W, B], -1)), levels=np.geomspace(.04, 60, 14), colors=C.LIGHT, linewidths=.7)
rng = np.random.default_rng(3)
full = [np.zeros(2)]; mini = [np.zeros(2)]
for _ in range(40):
    full.append(full[-1] - .02*g_full(full[-1]))
    idx = rng.integers(0, 5, size=2)
    mini.append(mini[-1] - .02*np.mean([g_i(mini[-1], i) for i in idx], axis=0))
full = np.array(full); mini = np.array(mini)
ax.plot(full[:,0], full[:,1], color=C.INK, lw=1.3); ax.scatter(full[::2,0], full[::2,1], s=20, color=C.INK, zorder=5)
ax.plot(mini[:,0], mini[:,1], color=C.GRAY, ls='--', lw=1.3); ax.scatter(mini[:,0], mini[:,1], s=20, facecolors=C.PAPER, edgecolors=C.GRAY, zorder=6)
label(ax, '实线加实心点：全梯度', (-0.5, -0.95), offset=(0, 0)); label(ax, '虚线加空心点：小批量 $B=2$', (-0.5, -1.2), offset=(0, 0), color=C.GRAY)
ax.scatter([xstar[0]], [xstar[1]], marker='*', s=90, color=C.INK, zorder=7); label(ax, '最小点', xstar, offset=(8, -16))
ax.set(xlim=(-0.6, 3.0), ylim=(-1.4, 1.4), xlabel='$w$', ylabel='$b$', aspect='equal')
save(fig, 'M1-n4')
