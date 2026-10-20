import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

n = np.arange(51)
exact = np.array([1-np.prod(1-np.arange(k)/365) for k in n])
lower = -np.expm1(-n*(n-1)/730)
assert np.all(lower <= exact + 1e-14)
assert np.allclose(exact[[10, 23, 30, 40]], [.1169, .5073, .7063, .8912], atol=5e-5)
assert exact[22] < .5 < exact[23] and 23*22//2 == 253
fig, ax = new_fig(17, 11)
ax.plot(n, exact, color=C.INK, ls='-', lw=1.7, label='精确值')
ax.plot(n, lower, color=C.RED, ls='--', lw=1.4, label='指数下界')
ax.axhline(.5, color=C.GRAY, ls=':', lw=1)
ax.axvline(23, color=C.GRAY, ls=':', lw=1)
for k, offset in [(10, (8, -13)), (23, (-15, 17)), (30, (-16, 18)), (40, (-12, 17))]:
    dot(ax, (k, exact[k]), size=25 if k == 23 else 15)
    label(ax, (rf'$n=23$，{exact[k]:.3f}' if k == 23 else f'{exact[k]:.3f}'),
          (k, exact[k]), offset, ha='right' if k == 23 else 'center')
ax.set(xlim=(0, 50), ylim=(0, 1), xlabel=r'$n$', ylabel='生日重复的概率')
ax.set_xticks([0, 10, 20, 23, 30, 40, 50])
ax.set_yticks([0, .25, .5, .75, 1])
ax.legend(loc='upper left')
fig.tight_layout()
save(fig, "K37-n3")
