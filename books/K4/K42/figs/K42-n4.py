import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Ellipse

fig, ax = new_fig(19, 13)
def box(x, y, w, h, text, ellipse=False, fontsize=11):
    patch = (Ellipse((x, y), w, h, facecolor=C.PAPER, edgecolor=C.INK, ls='--', lw=1)
             if ellipse else Rectangle((x-w/2, y-h/2), w, h,
                                       facecolor=C.PAPER, edgecolor=C.INK, lw=1))
    ax.add_patch(patch)
    label(ax, text, (x, y), ha='center', va='center', fontsize=fontsize)

box(6, .6, 10.5, .8, r'已知：$A$ 实对称正定，$\mathbf{v}\ne\mathbf{0}$ 是特征向量')
xs = [1.9, 5.8, 10.2]
reasons = [r'$A$ 正定的定义'+'\n'+r'$(\mathbf{v}\ne\mathbf{0})$',
           r'$\mathbf{v}\ne\mathbf{0}$',
           r'$A\mathbf{v}=\lambda\mathbf{v}$'+'\n'+r'两边左乘 $\mathbf{v}^{\mathsf{T}}$']
claims = [r'$\mathbf{v}^{\mathsf{T}}A\mathbf{v}>0$',
          r'$\Vert\mathbf{v}\Vert^2>0$',
          r'$\mathbf{v}^{\mathsf{T}}A\mathbf{v}=\lambda\Vert\mathbf{v}\Vert^2$']
for x, reason, claim, width, target in zip(xs, reasons, claims, [3.1, 3.1, 4.1], [4.7, 6, 7.3]):
    box(x, 2.3, width, 1.1, reason, ellipse=True, fontsize=10)
    box(x, 4, width, .8, claim)
    arrow(ax, (x, 1), (0, .75), color=C.INK, lw=1)
    arrow(ax, (x, 2.85), (0, .75), color=C.INK, lw=1)
    arrow(ax, (x, 4.4), (target-x, 1.15), color=C.INK, lw=1)
box(6, 6.15, 4.4, 1.2,
    r'$\lambda=\dfrac{\mathbf{v}^{\mathsf{T}}A\mathbf{v}}{\Vert\mathbf{v}\Vert^2}$', fontsize=14)
arrow(ax, (6, 6.75), (0, .65), color=C.INK, lw=1)
box(6, 7.8, 3.3, .8, r'结论：$\lambda>0$', fontsize=12)
ax.set(xlim=(-.1, 12.5), ylim=(-.05, 8.5))
ax.set_axis_off()
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
save(fig, "K42-n4")
