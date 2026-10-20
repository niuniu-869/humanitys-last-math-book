import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.19, top=0.96)
t = np.linspace(0, 2, 801)
tail = np.linspace(0.5, 2, 601)
ax.fill_between(tail, 0, 3 * np.exp(-3 * tail), color=C.LIGHT)
ax.plot(t, 3 * np.exp(-3 * t), color=C.INK, ls='-')
ax.plot([0.5, 0.5], [0, 3 * np.exp(-1.5)], color=C.INK, ls=':', lw=1)
dot(ax, (0, 3), size=20)
label(ax, '$3$', (0, 3), (9, 2), va='center')
label(ax, r'$P(T>0.5)=e^{-1.5}\approx0.2231$', (0.65, 1.2))
arrow(ax, (1.05, 1.02), (0, -0.9), color=C.INK, lw=0.8)
ax.set(xlim=(0, 2), ylim=(0, 3.3), xticks=[0, 0.5, 1, 1.5, 2],
       yticks=[0, 1, 2], xlabel='$t$（小时）', ylabel='$f(t)$')
save(fig, "P4-n3")
