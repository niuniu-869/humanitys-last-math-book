import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(13, 7)
ax.set_xlim(-0.9, 7.2); ax.set_ylim(-1.2, 4.6); ax.axis('off')
vals = [1,3,2,5,4,6]
ax.add_patch(Rectangle((0, -0.08), 3, 1.16, facecolor=C.LIGHT, edgecolor=C.GRAY, lw=1.1))
for i, v in enumerate(vals):
    ax.add_patch(Rectangle((i, 0), 1, 1, facecolor='none', edgecolor=C.INK, lw=1.0)); label(ax, str(v), (i+0.5,0.5), offset=(-3,-5), fontsize=10)
    label(ax, rf'$x_{i}$', (i+0.5,0), offset=(-7,-16), fontsize=8)
for j, v in enumerate([-1,-2,-2,-1]):
    ax.add_patch(Rectangle((j+1, 3), 1, 1, facecolor=C.PAPER, edgecolor=C.INK, lw=1.0)); label(ax, str(v), (j+1.5,3.5), offset=(-5,-5), fontsize=10); label(ax, rf'$y_{j}$', (j+1.5,4), offset=(-7,4), fontsize=8)
# y0 的三条连线，标权重
for r, kv in enumerate((1, 0, -1)):
    x_end = r + 0.5
    ax.plot([x_end, 1.5], [1.05, 3], color=C.INK, lw=1.6)
    px, py = x_end + 0.3*(1.5-x_end), 1.05 + 0.3*(3-1.05)
    label(ax, rf'$K_{r}={kv}$', (px, py), offset=(-14 if r==0 else (0 if r==1 else 8), 0), fontsize=8, ha='center')
# y1 的连线：同一组权重
for r in range(3):
    ax.plot([r+1.5, 2.5], [1.05, 3], color=C.GRAY, lw=1.0, ls='--')
label(ax, r'$y_1$ 用同一组 $K_0,K_1,K_2$（虚线）', (4.4, 2.1), fontsize=8)
label(ax, '$y_0$ 的窗口（阴影）', (0, -0.4), offset=(0,-34), fontsize=8)
label(ax, r'$\boldsymbol{x}$', (-0.6,0.5), fontsize=9); label(ax, r'$\boldsymbol{y}$', (5.3,3.5), fontsize=9)
save(fig, "M8-n4")
