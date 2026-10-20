import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(-4, 4, 1601)
normal = np.exp(-x*x/2) / np.sqrt(2*np.pi)
fig, axes = new_fig(20, 6.2, ncols=4, sharex=True, sharey=True)
for ax, t in zip(axes, [0, 3, 10, 30]):
    ax.plot(x, normal, color=C.RED, ls=':', lw=1.5, label=r'$N(0,1)$')
    if t == 0:
        for mu in [-2, 2]:
            arrow(ax, (mu, 0), (0, .43), color=C.INK)
        label(ax, r'$x_0=\pm2$', (0, .49), ha='center')
    else:
        a = .9**t
        mu, sd = 2*np.sqrt(a), np.sqrt(1-a)
        density = sum(np.exp(-.5*((x-m)/sd)**2)/(2*sd*np.sqrt(2*np.pi)) for m in [-mu, mu])
        ax.plot(x, density, color=C.INK, ls='-', lw=1.7)
        label(ax, rf'$\bar\alpha_{{{t}}}={a:.4f}$', (0, .49), ha='center')
    ax.set(xlim=(-4, 4), ylim=(0, .56), xticks=[-4, 0, 4], yticks=[], xlabel='$x$', title=f'$t={t}$')
axes[0].set_ylabel('密度')
axes[0].legend(loc='upper center', bbox_to_anchor=(.5, -.25), fontsize=9)
fig.subplots_adjust(left=.065, right=.985, bottom=.27, top=.85, wspace=.22)
save(fig, "M17-n1")
