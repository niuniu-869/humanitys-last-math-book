import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
x = np.linspace(-8, 8, 1201)
for var, style in [(1, '-'), (4, ':'), (5, '--')]:
    density = np.exp(-x*x/(2*var))/np.sqrt(2*np.pi*var)
    ax.plot(x, density, color=C.INK, ls=style)
label(ax, '$N(0,1)$', (0, 1/np.sqrt(2*np.pi)), (8, 4))
label(ax, '$N(0,4)$', (-2.5, 0.12), (-10, 10), ha='right')
arrow(ax, (-2.7, 0.13), (0.55, np.exp(-2.15**2/8)/np.sqrt(8*np.pi)-0.13), color=C.INK, lw=0.7)
label(ax, '$N(0,5)$', (3.6, 0.09), (3, 8))
arrow(ax, (3.7, 0.09), (-0.45, np.exp(-3.25**2/10)/np.sqrt(10*np.pi)-0.09), color=C.INK, lw=0.7)
ax.set(xlim=(-8, 8), ylim=(0, 0.45), xlabel='$x$', ylabel='密度')
ax.set_yticks([])
ax.set_xticks([-8, -4, 0, 4, 8])
save(fig, 'P6-n5')
