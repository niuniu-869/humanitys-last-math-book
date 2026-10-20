import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

x = np.linspace(-1.5, 1.5, 800)
p2 = 1 + x + x**2 / 2
actual = np.abs(np.exp(x) - p2)
bound = np.exp(np.abs(x)) * np.abs(x)**3 / 6
assert abs(actual[np.argmin(np.abs(x - 1))] - (np.e - 2.5)) < 0.002
assert abs(np.e / 6 - 0.4530) < 0.001
assert abs(abs(np.exp(-1) - 0.5) - 0.1321) < 0.001

fig, ax = new_fig(14, 7)
ax.plot(x, actual, color=C.INK, ls='-', lw=2.0)
ax.plot(x, bound, color=C.GRAY, ls='--', lw=1.7)
ax.set(xlabel='$x$', ylabel='$y$', xlim=(-1.5, 1.5), ylim=(0, 2.1))

# 「实际误差」放在实线正下方、右侧的空白处，不用引线
label(ax, '实际误差', (1.30, 0.17), ha='center', va='center')
label(ax, '上界', (1.10, np.exp(1.10) * 1.10**3 / 6), offset=(5, 5))
save(fig, 'C7-n5')
