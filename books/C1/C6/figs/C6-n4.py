import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(7.8, 7.2)
t = np.linspace(0, 1, 400)
x = t**2
y = t**3
ax.plot(x, y, color=C.INK, ls='-')
ax.plot([0, 1], [0, 1], color=C.GRAY, ls='--')
xi_t = 2 / 3
xi_x = xi_t**2
xi_y = xi_t**3
ax.scatter([0, 1], [0, 1], s=28, color=C.INK, zorder=5)
ax.scatter([xi_x], [xi_y], s=34, facecolors=C.INK, edgecolors=C.INK, zorder=5)
ax.plot([0.17, 0.73], [xi_y - (xi_x - 0.17), xi_y + (0.73 - xi_x)], color=C.GRAY, ls=':', lw=1.2)
ax.set(xlim=(-0.1, 1.2), ylim=(-0.1, 1.2), xlabel='$x=g(t)=t^2$\n虚线：弦，斜率 1\n点线：$t=\\frac{2}{3}$ 处的切线\n与弦平行', ylabel='$y=f(t)=t^3$', aspect='equal')
fig.tight_layout()
save(fig, 'C6-n4')
