import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11, 11)
a = 1.
t = np.linspace(0, 2*np.pi, 500)
for radius, ls in [(a, '--'), (np.sqrt(2)*a, ':')]:
    ax.plot(radius*np.cos(t), radius*np.sin(t), color=C.INK, ls=ls)
ax.plot([-a, a, a, -a, -a], [-a, -a, a, a, -a], color=C.INK, ls='-')
dot(ax, (0, 0), '$O$', offset=(-14, -13))
arrow(ax, (0, 0), (a, 0), color=C.INK, lw=1)
arrow(ax, (0, 0), (-a, a), color=C.INK, lw=1)
label(ax, '$a$', (.50, 0), (0, -16))
label(ax, r'$\sqrt{2}a$', (-.57, .57), (-22, -10))
ax.set(xlim=(-1.55, 1.55), ylim=(-1.55, 1.55), aspect='equal')
ax.set_axis_off()
save(fig, "C25-n6")
