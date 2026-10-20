import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
import math

n, p, q = 100, 0.7, 0.3
ks = np.arange(58, 85)
pmf = np.array([math.comb(n, int(k)) * p**k * q**(n-k) for k in ks])
tail = sum(math.comb(n, k) * p**k * q**(n-k) for k in range(75, n + 1))
assert abs(tail - 0.1631) < 0.0001
fig, ax = new_fig(13.5, 7.5)
colors = [C.LIGHT if k >= 75 else C.PAPER for k in ks]
ax.bar(ks, pmf, width=1, color=colors, edgecolor=C.INK, linewidth=0.8, align='center', zorder=2)
x = np.linspace(58, 84, 600)
normal = np.exp(-(x - 70)**2 / (2 * 21)) / np.sqrt(2 * np.pi * 21)
ax.plot(x, normal, color=C.INK, ls='-', lw=1.8, zorder=3)
ax.axvline(74.5, color=C.INK, ls='-', lw=1.4, zorder=4)
ax.axvline(75, color=C.GRAY, ls='--', lw=1.4, zorder=4)
ax.set(xlim=(57.4, 84.6), ylim=(0, max(normal.max(), pmf.max()) * 1.38), xlabel='$k$', ylabel='概率 / 密度')
ymax = ax.get_ylim()[1]
ax.annotate('截点 74.5（修正）：从这里开始算', xy=(74.5, 0.075), xytext=(60.5, 0.105),
            ha='left', va='center', arrowprops=dict(arrowstyle='->', color=C.INK, lw=1.2))
ax.annotate('截点 75（不修正）：丢掉了这半根柱子', xy=(75, 0.052), xytext=(77.5, 0.092),
            ha='left', va='center', arrowprops=dict(arrowstyle='->', color=C.GRAY, lw=1.2, ls='--'))
ax.text(79.5, 0.06, '阴影面积 $P(X\\geq 75)=0.1631$', ha='left', va='center')
save(fig, 'P8-n4')
