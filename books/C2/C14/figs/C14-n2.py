import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, axes = new_fig(17, 8, ncols=2)
fig.subplots_adjust(wspace=.30, bottom=.19, top=.82)
x = np.linspace(.8, 6.4, 600)
for i, ax in enumerate(axes):
    ax.set(xlim=(.7, 6.45), ylim=(0, 1.32), xticks=range(1, 7),
           yticks=[0, .5, 1], xlabel='$x$')
    ax.plot(x, 1/x, color=C.INK, ls='-', lw=1.7, zorder=4)
    for n in range(1 if i == 0 else 2, 6 if i == 0 else 7):
        left = n if i == 0 else n-1
        ax.add_patch(Rectangle((left, 0), 1, 1/n,
                              facecolor=C.LIGHT if i == 0 else 'none',
                              edgecolor=C.INK, lw=1, ls='-' if i == 0 else '--'))
    label(ax, r'$f(x)=1/x$', (4.5, .7), ha='center')
    title = (r'左排：$\int_n^{n+1}f\leq u_n$' if i == 0 else
             r'右排（虚线）：$u_n\leq\int_{n-1}^{n}f$')
    ax.set_title(title, pad=18)
    arrow(ax, (4.35, .62), (-.85, -.28), color=C.INK, lw=.8)
label(axes[0], r'$u_n=f(n)$', (1.6, .82), (35, 30), ha='left',
      arrowprops=dict(arrowstyle='->', color=C.INK, lw=.8))
save(fig, 'C14-n2')
