import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

t = np.arange(1001)
beta = np.linspace(1e-4, .02, 1000)
abar = np.r_[1., np.cumprod(1-beta)]
signal, noise = np.sqrt(abar), np.sqrt(1-abar)
assert np.allclose(signal**2+noise**2, 1)
tc = np.interp(.5, abar[::-1], t[::-1])
fig, ax = new_fig(15, 9)
ax.plot(t, signal, color=C.INK, ls='-', label='信号系数')
ax.plot(t, noise, color=C.INK, ls='--', label='噪声系数')
ax.vlines(tc, 0, np.sqrt(.5), color=C.GRAY, ls=':', lw=1.2)
dot(ax, (tc, np.sqrt(.5)), size=27)
label(ax, r'SNR $=1$', (tc, np.sqrt(.5)), offset=(14, -5), va='top')
for value, offset in [(signal[500], (12, 7)), (noise[500], (12, -18))]:
    ax.scatter([500], [value], s=32, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
    label(ax, f'{value:.4f}', (500, value), offset=offset)
label(ax, r'$\sqrt{\bar\alpha_T}\approx0.006$', (985, .075), ha='right')
ax.set(xlim=(0, 1000), ylim=(0, 1), xlabel='$t$', ylabel='系数', xticks=[0, 250, 500, 750, 1000], yticks=[0, .5, 1])
ax.legend(loc='center right', bbox_to_anchor=(.99, .53))
fig.subplots_adjust(left=.10, right=.97, bottom=.16, top=.94)
save(fig, "M17-n3")
