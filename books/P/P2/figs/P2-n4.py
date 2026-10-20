import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import comb
from fractions import Fraction

k = np.arange(11)
exact = [Fraction(comb(10, int(j)) * 7**int(j) * 3**int(10-j), 10**10) for j in k]
p = np.array([float(v) for v in exact])
assert sum(exact) == 1 and int(p.argmax()) == 7
assert f'{float(sum(exact[8:])):.4f}' == '0.3828'
assert [f'{v:.4f}' for v in p] == ['0.0000', '0.0001', '0.0014', '0.0090',
    '0.0368', '0.1029', '0.2001', '0.2668', '0.2335', '0.1211', '0.0282']

fig, ax = new_fig(19, 10)
for j, height in zip(k, p):
    face = C.INK if j == 7 else C.LIGHT if j >= 8 else C.PAPER
    ax.bar(j, height, width=.72, facecolor=face, edgecolor=C.INK, lw=1, zorder=3)
    label(ax, f'{height:.4f}', (j, height), offset=(0, 5),
          ha='center', va='bottom', fontsize=9)
ax.plot([7.65, 7.65, 10.35, 10.35], [.266, .276, .276, .266],
        color=C.INK, lw=1.1, ls='-')
label(ax, '合计 0.3828', (9, .281), ha='center', va='bottom')
label(ax, r'阴影 = $k\geq8$', (2.1, .25), ha='center')
label(ax, r'黑柱：$k=7$，最高', (2.1, .218), ha='center')
ax.set(xlim=(-.6, 10.6), ylim=(0, .3), xticks=k,
       xlabel='$k$', ylabel=r'恰好命中 $k$ 次的概率', title=r'$n=10,\quad p=0.7$')
ax.set_yticks(np.arange(0, .301, .05))
ax.grid(axis='y', color=C.LIGHT, lw=.6, ls=':', zorder=0)
fig.subplots_adjust(left=.13, right=.98, bottom=.16, top=.89)
save(fig, 'P2-n4')
