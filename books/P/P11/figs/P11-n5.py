import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

rng = np.random.default_rng(2)
means = rng.normal(170, 6, size=(20, 36)).mean(axis=1)
lo, hi = means - 1.96, means + 1.96
covered = (lo <= 170) & (hi >= 170)
fig, ax = new_fig(12, 8)
for idx, (a, b, ok) in enumerate(zip(lo, hi, covered), 1):
    y = 21 - idx
    if ok:
        ax.plot([a, b], [y, y], color=C.BLUE, ls='-', lw=1.1)
        ax.plot([a, a], [y-0.12, y+0.12], color=C.INK, lw=0.9)
        ax.plot([b, b], [y-0.12, y+0.12], color=C.INK, lw=0.9)
    else:
        ax.plot([a, b], [y, y], color=C.INK, ls='--', lw=2.0)
        label(ax, '未盖住', (170.15, y), offset=(0, 0), ha='left')
    ax.plot(means[idx-1], y, marker='o', ms=3.5, color=C.INK)
    label(ax, str(idx), (166.15, y), offset=(0, -4))
ax.axvline(170, color=C.GRAY, ls='--', lw=1.1)
label(ax, r'$\mu=170$', (170, 20.4), offset=(5, 0))
ax.set(xlim=(166, 174), ylim=(0.3, 20.7), xlabel=r'$\mu$ 的 95% 区间', yticks=[])
save(fig, "P11-n5")
