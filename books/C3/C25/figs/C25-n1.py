import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig3d(14, 11, elev=25, azim=-53)
q = np.arange(4) / 4
x, y = np.meshgrid(q, q)
h = (x + .25)**2 + (y + .25)**2
volume = np.sum(h) / 16
assert volume == .9375
ax.bar3d(x.ravel(), y.ravel(), np.zeros(16), .25, .25, h.ravel(),
         color=C.LIGHT, edgecolor=C.GRAY, linewidth=.55, alpha=.30, shade=False)
t = np.linspace(0, 1, 100)
for k in np.linspace(0, 1, 5):
    ax.plot(t, np.full_like(t, k), t*t+k*k, color=C.INK, ls='--', lw=1, alpha=.55)
    ax.plot(np.full_like(t, k), t, t*t+k*k, color=C.INK, ls='--', lw=1, alpha=.55)
ax.set(xlim=(0, 1), ylim=(0, 1), zlim=(0, 2.1))
ax.set_xticks([0, 1]); ax.set_yticks([0, 1]); ax.set_zticks([0, 1, 2])
ax.set_box_aspect((1, 1, 1.1))
ax.grid(False)
ax.text2D(.05, .96, r'$z=x^2+y^2$', transform=ax.transAxes)
ax.text2D(.05, .89, f'小柱体体积和：{volume:.4f}', transform=ax.transAxes)
ax.text2D(.05, .82, r'真值：$\frac{2}{3}\approx0.6667$', transform=ax.transAxes)
save(fig, "C25-n1")
