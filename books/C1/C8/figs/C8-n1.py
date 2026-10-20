import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

f = lambda x: x**3 - 3*x
fp = lambda x: 3*x**2 - 3
assert np.isclose(f(-1), 2) and np.isclose(f(1), -2)
assert np.isclose(fp(0), -3) and np.isclose(fp(1.7), 5.67)

fig, ax = new_fig(12, 7.5)
x = np.linspace(-2.3, 2.3, 900)
ax.plot(x, f(x), color=C.INK, ls='-', lw=1.8)

for x0 in (-1.7, 0, 1.7):
    y0, m = f(x0), fp(x0)
    half = 0.5
    ax.plot([x0-half, x0+half], [y0-m*half, y0+m*half], color=C.GRAY, ls=':', lw=1.1)
for x0, y0 in [(-1, 2), (1, -2)]:
    ax.plot([x0-.42, x0+.42], [y0, y0], color=C.GRAY, ls='--', lw=1.2)
    ax.scatter([x0], [y0], s=34, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)

for x0 in (-1, 1):
    ax.axvline(x0, color=C.GRAY, ls=':', lw=.8, zorder=0)
# 「减」放在中段正上方的空白处（避开 y 轴和刻度 3）
for xx, yy, t in [(-1.625, 3.15, '增'), (0.5, 2.6, '减'), (1.625, 3.15, '增')]:
    label(ax, t, (xx, yy), ha='center', va='center', fontsize=11)
ax.set(xlim=(-2.3, 2.3), ylim=(-3.5, 3.5), xlabel='$x$', ylabel='$y$')
ax.spines['bottom'].set_position(('data', -3.0))
ax.spines['left'].set_position(('data', 0))
ax.tick_params(axis='both', direction='out', length=3)
save(fig, 'C8-n1')
