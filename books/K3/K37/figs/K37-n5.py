import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from fractions import Fraction

accept = [Fraction(1), Fraction(3, 5), Fraction(2, 5)]
heights = [a/3 for a in accept]
total = sum(heights)
assert total == Fraction(2, 3)
assert [h/total for h in heights] == [Fraction(1, 2), Fraction(3, 10), Fraction(1, 5)]
fig, ax = new_fig(19, 11)
x = np.arange(1, 4)
ax.bar(x, [1/3]*3, width=.54, color=C.PAPER, edgecolor=C.INK, lw=1.2)
ax.bar(x, list(map(float, heights)), width=.54, color=C.LIGHT, edgecolor=C.INK, lw=1.2)
for k, h, a in zip(x, heights, accept):
    label(ax, f'{float(h):.3f}', (k+.30, float(h)), (4, -3), va='center')
    label(ax, rf'$a_{k}={float(a):g}$', (k, .365), ha='center', va='center', annotation_clip=False)
    label(ax, '接受', (k, float(h)/2), ha='center', va='center')
    if a < 1:
        label(ax, '拒绝', (k, (float(h)+1/3)/2), ha='center', va='center')
ax.set(xlim=(.35, 3.95), ylim=(0, 1/3), ylabel='一次尝试的概率')
ax.set_xticks(x, [r'$x=1$', r'$x=2$', r'$x=3$'])
ax.set_yticks([0, 1/15, 2/15, 1/5, 4/15, 1/3],
              ['0', r'$1/15$', r'$2/15$', r'$1/5$', r'$4/15$', r'$1/3$'])
ax.text(.02, 1.18, r'接受概率 $a_x$', transform=ax.transAxes)
fig.subplots_adjust(left=.12, right=.96, top=.77, bottom=.23)
fig.text(.5, .105, r'灰色总高 $=2/3$（一次被接受的概率）', ha='center')
fig.text(.5, .035, r'灰色高度之比 $(1/3):(1/5):(2/15)=0.5:0.3:0.2$', ha='center')
save(fig, "K37-n5")
