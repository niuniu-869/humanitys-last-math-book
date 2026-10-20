import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig = plt.figure(figsize=(19/2.54, 13/2.54))
t = np.linspace(-1.35, 1.35, 161)
X, Y = np.meshgrid(t, t)
surfaces = [X**2+Y**2, X**2-Y**2, -X**2-Y**2]
titles = [r'$z=x^2+y^2$', r'$z=x^2-y^2$', r'$z=-x^2-y^2$']
for i, (Z, title) in enumerate(zip(surfaces, titles)):
    ax = fig.add_subplot(2, 3, i+1, projection='3d')
    ax.plot_wireframe(X, Y, Z, rstride=16, cstride=16, color=C.INK,
                      lw=.65, alpha=.5)
    ax.scatter([0], [0], [0], color=C.INK, s=28, alpha=.55, depthshade=False)
    ax.set_title(title, pad=0)
    ax.set_axis_off()
    ax.view_init(elev=27, azim=-58)
    ax.set_box_aspect((1, 1, .8))
    ax = fig.add_subplot(2, 3, i+4)
    levels = [.3, .8, 1.5] if i == 0 else ([-1.5, -.6, .6, 1.5] if i == 1 else [-1.5, -.8, -.3])
    cs = ax.contour(X, Y, Z, levels=levels, colors=C.INK, linestyles='-', linewidths=1)
    ax.clabel(cs, fmt='%g', fontsize=9)
    ax.axhline(0, color=C.GRAY, lw=.8, ls=':')
    ax.axvline(0, color=C.GRAY, lw=.8, ls=':')
    dot(ax, (0, 0), size=17)
    ax.set(xlim=(-1.45, 1.45), ylim=(-1.45, 1.45), xlabel='$x$', ylabel='$y$')
    ax.set_aspect('equal')
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    if i == 1:
        ax.text(.5, -.28, r'沿 $x$ 轴向外：$f$ 增大'+'\n'+r'沿 $y$ 轴向外：$f$ 减小',
                transform=ax.transAxes, ha='center', va='top', fontsize=9)
fig.subplots_adjust(left=.07, right=.98, bottom=.19, top=.95, wspace=.4, hspace=.12)
save(fig, "C24-n1")
