import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(18, 12)
z = np.unique(np.r_[np.linspace(-2, 3, 501), 1.])
ax.plot(z, np.maximum(0, 1-z), color=C.INK, ls='-', lw=2.2,
        label=r'合页损失 $\max(0,1-z)$', zorder=3)
ax.plot(z, np.logaddexp(0, -z), color=C.INK, ls='--', lw=1.6,
        label=r'逻辑损失 $\ln(1+e^{-z})$')
for x, text in [(0, '在边界上'), (1, '间隔边界')]:
    ax.axvline(x, ls=':', color=C.GRAY, lw=1)
    label(ax, text, (x, 2.65), (6, 0), fontsize=9)
samples = np.array([-1., 0., 1., 2.])
hinge = np.maximum(0, 1-samples)
logistic = np.logaddexp(0, -samples)
assert np.array_equal(hinge, [2, 1, 0, 0])
assert np.allclose(logistic, [1.3133, 0.6931, 0.3133, 0.1269], atol=0.00005)
for x, h, l in zip(samples, hinge, logistic):
    ax.scatter(x, h, s=34, color=C.INK, zorder=5, clip_on=False)
    ax.scatter(x, l, s=36, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
    label(ax, f'{h:g}', (x, h), (10, 16) if h else (10, 1), fontsize=9 if h else 8)
    label(ax, f'{l:.4f}', (x, l), (-12, -16) if x == 0 else (8, 10),
          ha='right' if x == 0 else 'left', fontsize=9)
ax.set(xlim=(-2, 3), ylim=(0, 3), xlabel=r'$z=yf$', ylabel='损失')
ax.set_aspect('equal', adjustable='box')
ax.set_xticks([-2, -1, 0, 1, 2, 3])
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.03), borderaxespad=0, fontsize=10)
fig.tight_layout()
save(fig, "M6-n3")
