import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(14, 8)
s = np.linspace(0.005, 0.995, 900)
a, b = 0.0968, 0.0324
elbo = s * np.log(a / s) + (1 - s) * np.log(b / (1 - s))
logp = np.log(a + b)
post = a / (a + b)
def E(q): return q * np.log(a / q) + (1 - q) * np.log(b / (1 - q))
assert np.isclose(E(0.5), -2.1893, atol=5e-4)
assert np.isclose(E(0.2), -2.7105, atol=5e-4)
assert np.isclose(logp, -2.0465, atol=5e-4)
ax.plot(s, elbo, color=C.INK, lw=2)
ax.axhline(logp, ls='--', color=C.RED, lw=1.5)
ax.axvline(post, ls=':', color=C.GRAY, lw=1.1)
dot(ax, (post, logp), color=C.INK, size=30)
label(ax, '$\\log p(x)$', (0.83, logp), offset=(4, 5), color=C.RED)
label(ax, '$q=$ 后验，间隔 0', (post, logp), offset=(8, -30), ha='left')
for q, off, ha_ in [(0.5, (-6, -30), 'right'), (0.2, (-8, 0), 'right')]:
    ev = E(q)
    ax.add_patch(FancyArrowPatch((q, ev), (q, logp), arrowstyle='<->', mutation_scale=11,
                                 color=C.TEAL, lw=1.3))
    label(ax, f'KL {logp-ev:.4f}', (q, (ev + logp) / 2), offset=off,
          ha=ha_, color=C.TEAL)
ax.scatter([0.5, 0.2], [E(0.5), E(0.2)], s=24, color=C.INK, zorder=5)
ax.set(xlim=(0, 1), ylim=(-4.5, -1.8), xlabel='$s=q(z{=}1)$', ylabel='对数值')
save(fig, 'M16-n3')
