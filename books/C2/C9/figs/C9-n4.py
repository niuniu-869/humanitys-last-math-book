import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 12)
x = np.array([0, 0.2, 0.5, 1])
y = np.array([0, 0.6, 0.8, 1])
areas = np.diff(x)*(y[:-1]+y[1:])/2
assert np.allclose(areas, [0.06, 0.21, 0.45])
assert np.isclose(areas.sum(), 0.72)
for i in range(3):
    ax.fill([x[i], x[i+1], x[i+1], x[i]], [0, 0, y[i+1], y[i]],
            facecolor=C.LIGHT, edgecolor=C.INK, lw=0.8)
ax.plot(x, y, color=C.INK, lw=2.1, ls='-')
ax.scatter(x, y, s=30, facecolors=C.INK, edgecolors=C.INK, zorder=5, clip_on=False)
ax.plot([0, 1], [0, 1], color=C.INK, lw=1.1, ls=':')
label(ax, '0.06', (0.12, 0.26), offset=(-22, 47), ha='center',
      arrowprops=dict(arrowstyle='-', color=C.INK, lw=0.8))
label(ax, '0.21', (0.35, 0.49), ha='center')
label(ax, '0.45', (0.73, 0.82), ha='center')
label(ax, '理想随机基准，面积 0.5', (0.75, 0.14), ha='center', va='center')
ax.annotate('', xy=(0.56, 0.56), xytext=(0.65, 0.18),
            arrowprops=dict(arrowstyle='-', color=C.INK, lw=0.7,
                            shrinkA=0, shrinkB=3))
label(ax, 'AUC ≈ 0.72', (0.06, 0.92))
ax.set(xlim=(0, 1), ylim=(0, 1), xlabel='$x$  假阳性率', ylabel='$y$  真阳性率')
ax.set_aspect('equal')
ax.set_xticks([0, 0.2, 0.5, 1])
ax.set_yticks([0, 0.6, 0.8, 1])
fig.subplots_adjust(left=0.17, right=0.96, bottom=0.15, top=0.96)
save(fig, "C9-n4")
