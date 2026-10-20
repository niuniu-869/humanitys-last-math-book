import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, axes = new_fig(14, 5.8, ncols=2)
target = {4: 0.46875, 10: 0.385}
for ax, n in zip(axes, [4, 10]):
    x = np.linspace(0, 1, 400)
    ax.plot(x, x*x, color=C.INK, lw=1.7)
    dx = 1/n
    for i in range(1, n+1):
        ax.add_patch(Rectangle(((i-1)*dx, 0), dx, (i*dx)**2,
                               facecolor=C.LIGHT, edgecolor=C.INK, lw=.8))
    S = sum(i*i for i in range(1, n+1))/n**3
    assert abs(S - target[n]) < 1e-12
    label(ax, fr'$n={n}$，$S_{{{n}}}={S:.5g}$', (0.5, 1.10), ha='center')
    # 放在左上角柱子上方的空白处，白底盖住，不压矩形竖线和曲线
    label(ax, r'极限 $\frac{1}{3}\approx0.3333$', (.03, .98),
          ha='left', va='top', fontsize=8,
          bbox={'facecolor': C.PAPER, 'edgecolor': 'none', 'pad': 2})
    ax.set(xlim=(-.03, 1.05), ylim=(-.04, 1.14),
           xticks=[0, 1], yticks=[0, 1])
    ax.set_aspect('equal')
    ax.axis('off')
save(fig, 'C11-n7')
