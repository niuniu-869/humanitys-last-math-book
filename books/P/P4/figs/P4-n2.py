import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, (top, bottom) = new_fig(14, 12, nrows=2, sharex=True)
fig.subplots_adjust(left=0.23, right=0.97, bottom=0.11, top=0.97, hspace=0.22)
x = np.linspace(0, 3, 601)
s = np.linspace(1, 2, 201)
top.fill_between(s, 0, s ** 2 / 9, color=C.LIGHT)
top.plot(x, x ** 2 / 9, color=C.INK, ls='-')
top.set(ylim=(0, 1.1), ylabel='$f(x)$', yticks=[0, 0.5, 1])
label(top, r'面积 $=P(1<X\leq 2)=\frac{7}{27}$', (0.1, 0.83))
bottom.plot(x, x ** 3 / 27, color=C.INK, ls='-')
bottom.plot([-0.2, 0], [0, 0], color=C.INK, ls='-', clip_on=False)
bottom.plot([3, 3.2], [1, 1], color=C.INK, ls='-')
for a in [1, 2]:
    value = a ** 3 / 27
    bottom.plot([a, a], [0, value], color=C.INK, ls=':', lw=1)
    bottom.plot([0, a], [value, value], color=C.GRAY, ls=':', lw=0.8)
    dot(bottom, (a, value), size=20)
bottom.annotate('', xy=(0.48, 8 / 27), xytext=(0.48, 1 / 27),
                arrowprops=dict(arrowstyle='<->', color=C.INK, lw=1))
label(bottom, r'差 $=\frac{7}{27}$', (0.58, 0.16), va='center')
bottom.set(xlim=(-0.2, 3.2), ylim=(0, 1.1), xlabel='$x$', ylabel='$F(x)$',
           xticks=[0, 1, 2, 3], yticks=[1 / 27, 8 / 27, 1])
bottom.set_yticklabels([r'$F(1)=\frac{1}{27}$', r'$F(2)=\frac{8}{27}$', '$1$'])
save(fig, "P4-n2")
