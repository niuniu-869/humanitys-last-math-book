import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axs = new_fig(21, 8, ncols=3)
cases = [
    (1, np.sin, lambda x: x, r'$\sin x$', '$x$', r'实心点：$x=0.1$，$\sin 0.1=0.09983$', [0, 0.5, 1]),
    (1.2, lambda x: 1-np.cos(x), lambda x: x*x/2, r'$1-\cos x$', '$x^2/2$', r'实心点：$x=0.1$，$1-\cos 0.1=0.004996$', [0, 0.6, 1.2]),
    (0.8, lambda x: np.tan(x)-np.sin(x), lambda x: x**3/2, r'$\tan x-\sin x$', '$x^3/2$', r'实心点：$x=0.1$，$\tan 0.1-\sin 0.1=0.000501$', [0, 0.4, 0.8]),
]
for ax, (end, f, main, name, leading, value, ticks) in zip(axs, cases):
    x = np.linspace(0, end, 1000)
    ax.plot(x, f(x), color=C.INK, ls='-', label=name)
    ax.plot(x, main(x), color=C.INK, ls='--', label=leading)
    dot(ax, (0.1, f(0.1)), size=22)
    ax.set(xlim=(0, end), ylim=(0, max(f(end), main(end))*1.06), xlabel='$x$', ylabel='$y$')
    ax.set_xticks(ticks)
    ax.legend(loc='upper left', fontsize=9, handlelength=2.6)
    label(ax, value, (0.5, -0.34), xycoords='axes fraction', ha='center', annotation_clip=False, fontsize=8.5)
fig.subplots_adjust(left=0.07, right=0.98, wspace=0.4, bottom=0.3, top=0.97)
save(fig, "C2-n5")
