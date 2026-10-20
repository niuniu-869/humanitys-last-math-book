import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

d = 512
n = np.linspace(0, 1024, 1025)
assert 50**2*d == 1280000
assert 50*d**2 == 13107200
assert d**2*d == d*d**2
fig, ax = new_fig(15, 10)
ax.plot(n, n**2*d, color=C.INK, ls='-', label=r'自注意力 $n^2d$')
ax.plot(n, n*d**2, color=C.INK, ls='--', label=r'循环层 $nd^2$')
ax.axvline(d, color=C.GRAY, ls=':', lw=1.2)
dot(ax, (d, d**3))
label(ax, r'$n=d$', (d, d**3), offset=(12, -22))
for value, text, xytext in [
    (50**2*d, r'$1.28\times10^6$', (650, 0.25e8)),
    (50*d**2, r'$1.31\times10^7$', (90, 1.15e8)),
]:
    ax.scatter(50, value, s=35, facecolor=C.PAPER, edgecolor=C.INK, zorder=5)
    ax.annotate(text, xy=(50, value), xytext=xytext, fontsize=10,
                color=C.INK, arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.8))
ax.set(xlim=(0, 1024), ylim=(-0.15e8, 5.65e8), xlabel=r'序列长度 $n$', ylabel='运算量')
ax.set_xticks([0, 50, 256, 512, 768, 1024])
ax.tick_params(axis='x', labelsize=8)
ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0), useMathText=True)
ax.legend(loc='upper left')
label(ax, r'$d=512$', (970, 0.35e8), ha='right')
fig.tight_layout()
save(fig, "M18-n3")
