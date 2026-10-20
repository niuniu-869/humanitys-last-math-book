import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from scipy.stats import f

fig, ax = new_fig(15, 9)
x = np.linspace(0, 10, 1500)
critical = 3.89
p = f.sf(8, 2, 12)
assert np.isclose(f.pdf(0, 2, 12), 1)
assert round(f.isf(.05, 2, 12), 2) == critical
assert round(p, 3) == .006
ax.plot(x, f.pdf(x, 2, 12), color=C.INK, ls='-', label='$F(2,12)$')
tail = np.linspace(critical, 10, 600)
ax.fill_between(tail, 0, f.pdf(tail, 2, 12), color=C.LIGHT, hatch='///', edgecolor=C.GRAY, linewidth=.4)
ax.axvline(critical, color=C.INK, ls='--', lw=1.2)
ax.axvline(8, color=C.INK, ls='-', lw=1.2)
label(ax, '拒绝域，面积 0.05', (5.6, .035), offset=(0, 45), ha='center',
      arrowprops=dict(arrowstyle='->', color=C.GRAY, lw=.8))
label(ax, '$F=8$\n$p\\approx0.006$', (8, .72), offset=(8, 0))
ax.set(xlim=(0, 10), ylim=(0, 1.08), xlabel='$F$', ylabel='密度')
ax.set_xticks([0, 2, 3.89, 6, 8, 10], ['0', '2', '3.89', '6', '8', '10'])
ax.legend(loc='upper center')
fig.subplots_adjust(left=.12, right=.97, bottom=.15, top=.96)
save(fig, "P13-n2")
