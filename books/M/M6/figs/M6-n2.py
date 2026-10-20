import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 12)
xx = np.linspace(0, 5.5, 500)
ax.fill_between(xx, np.maximum(0, 2-xx), np.minimum(5, 6-xx), color=C.LIGHT)
for b, ls, lw in [(2, '--', 1.4), (4, '-', 2.2), (6, '--', 1.4)]:
    ax.plot(xx, b-xx, color=C.INK, ls=ls, lw=lw)
points = np.array([[3., 3.], [4., 3.], [1., 1.]])
w = np.array([0.5, 0.5])
assert np.allclose(points @ w - 2, [1, 1.5, -1])
assert np.allclose(0.25*points[0]-0.25*points[2], w)
for i, p in enumerate(points):
    if i in [0, 2]:
        ax.scatter(*p, s=190, facecolors='none', edgecolors=C.INK, lw=1.1, zorder=4)
    ax.scatter(*p, s=42, facecolors=C.INK if i < 2 else C.PAPER,
               edgecolors=C.INK, zorder=5)
label(ax, r'$\boldsymbol{x}_1$ 支持向量'+'\n'+r'$\alpha=\frac{1}{4}$', (3.1, 4.05),
      ha='left', fontsize=9)
label(ax, r'$\boldsymbol{x}_2$ 带外'+'\n'+r'$\alpha=0$', (4, 3), (12, 4), fontsize=9)
label(ax, r'$\boldsymbol{x}_3$ 支持向量'+'\n'+r'$\alpha=\frac{1}{4}$', (1.45, 1.1),
      fontsize=9)
arrow(ax, (1.15, 2.85), w, color=C.INK, text=r'$\boldsymbol{w}$', offset=(5, 4))
start, end = np.array([1.75, 0.25]), np.array([3.75, 2.25])
assert np.isclose(np.linalg.norm(end-start), 2*np.sqrt(2))
ax.annotate('', xy=end, xytext=start,
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1))
label(ax, r'宽度 $2\sqrt{2}$', (2.3, 0.25))
label(ax, r'$x_1+x_2=6$', (3.7, 2.3), (12, -1), fontsize=9)
label(ax, r'$x_1+x_2=4$', (3.25, 0.75), (12, 3), fontsize=9)
label(ax, r'$x_1+x_2=2$', (0.12, 0.5), fontsize=9)
ax.set(xlim=(0, 5.5), ylim=(0, 5), xlabel=r'$x_1$', ylabel=r'$x_2$')
ax.set_aspect('equal', adjustable='box')
fig.tight_layout()
save(fig, "M6-n2")
