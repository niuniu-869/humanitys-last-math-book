import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

H = np.array([[22., 6.], [6., 2.]])
xstar = np.array([1.7, -0.1])

def loss(x):
    d = x - xstar
    return 0.5 * np.einsum('...i,ij,...j->...', d, H, d)

def path(eta, steps):
    x = np.array([0., 0.]); out = [x.copy()]
    for _ in range(steps):
        x = x - eta * (H @ (x - xstar))
        out.append(x.copy())
    return np.array(out)

fig, axes = new_fig(16, 7.5, ncols=2)
w = np.linspace(-0.6, 3.0, 500)
b = np.linspace(-1.4, 1.4, 500)
W, B = np.meshgrid(w, b)
Z = loss(np.stack([W, B], axis=-1))
levels = np.geomspace(0.04, 60, 14)

for ax in axes:
    ax.contour(W, B, Z, levels=levels, colors=C.LIGHT, linewidths=0.8)
    ax.set(xlim=(-0.6, 3.0), ylim=(-1.4, 1.4), aspect='equal',
           xlabel='$w$', ylabel='$b$')

# 左图：η=0.02，120 步，每 20 步一个实心点
ax = axes[0]
ax.set_title(r'$\eta=0.02$')
p = path(0.02, 120)
ax.plot(p[:, 0], p[:, 1], ls='-', color=C.INK, lw=1.3, zorder=4)
idx = np.arange(0, 121, 20)
ax.scatter(p[idx, 0], p[idx, 1], s=15, color=C.INK, edgecolors=C.PAPER,
           linewidths=0.45, zorder=5)
label(ax, '0', p[0], offset=(-4, -4), ha='right', va='top', fontsize=7)
label(ax, '20', p[20], offset=(6, 2), ha='left', va='center', fontsize=7)
label(ax, '120', p[120], offset=(6, -2), ha='left', va='center', fontsize=7)

# 右图：η=0.08，只画前 8 步，虚线连接，空心圆并标步数
ax = axes[1]
ax.set_title(r'$\eta=0.08$')
q = path(0.08, 8)
ax.plot(q[:, 0], q[:, 1], ls='--', color=C.GRAY, lw=1.2, zorder=4)
ax.scatter(q[:, 0], q[:, 1], s=26, facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.0, zorder=5)
for i, xy in enumerate(q):  # 偶数步在谷左侧，标在点正下方；奇数步在右侧，标在点正上方
    if i % 2 == 0:
        label(ax, str(i), xy, offset=(0, -6), ha='center', va='top', fontsize=7)
    else:
        label(ax, str(i), xy, offset=(0, 6), ha='center', va='bottom', fontsize=7)

for ax in axes:
    ax.scatter([xstar[0]], [xstar[1]], marker='*', s=90, color=C.INK, zorder=7)
    label(ax, '最小点', xstar, offset=(0, -9), ha='center', va='top', fontsize=9)

fig.subplots_adjust(left=0.08, right=0.98, bottom=0.17, top=0.90, wspace=0.30)
save(fig, 'M1-n2')
