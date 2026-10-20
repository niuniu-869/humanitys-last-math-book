import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, (left, right) = new_fig(19, 9, ncols=2)
left.fill_between([0, 2], 0, 2, color=C.LIGHT)
left.fill_between([-2, 0], -2, 0, color=C.LIGHT)
left.axhline(0, color=C.INK, lw=2.0)
left.axvline(0, color=C.INK, lw=2.0)
points = np.array([[1, 1], [-1, -1], [1, -1], [-1, 1]])
phi2 = np.sqrt(2)*points[:, 0]*points[:, 1]
assert np.allclose(phi2, [np.sqrt(2), np.sqrt(2), -np.sqrt(2), -np.sqrt(2)])
for i, p in enumerate(points):
    face = C.INK if i < 2 else C.PAPER
    left.scatter(*p, s=48, facecolors=face, edgecolors=C.INK, zorder=5)
    label(left, f'$({p[0]},{p[1]})$', p, (0, -20), ha='center', fontsize=9)
    # Vertical displacement only separates samples sharing one exact coordinate.
    y = 0.24 if i % 2 == 0 else -0.24
    right.scatter(phi2[i], y, s=48, facecolors=face, edgecolors=C.INK, zorder=5)
    label(right, f'$({p[0]},{p[1]})$', (phi2[i], y),
          (0, 11 if y > 0 else -20), ha='center', fontsize=9)
label(left, r'$f=x_1x_2>0$', (1, 1.65), ha='center', fontsize=9)
label(left, r'$f=x_1x_2>0$', (-1, -1.75), ha='center', fontsize=9)
left.set(xlim=(-2, 2), ylim=(-2, 2), xlabel=r'$x_1$', ylabel=r'$x_2$', title='原平面')
left.set_xticks([-2, -1, 0, 1, 2])
left.set_yticks([-2, -1, 0, 1, 2])
right.spines['bottom'].set_position(('data', 0))
right.spines['left'].set_visible(False)
right.plot([0, 0], [-0.85, 0.85], color=C.INK, lw=2.2)
right.set(xlim=(-2, 2), ylim=(-2, 2), title='第二个新坐标')
right.set_xticks([-np.sqrt(2), 0, np.sqrt(2)], [r'$-\sqrt{2}$', '$0$', r'$+\sqrt{2}$'])
right.tick_params(axis='x', pad=44)
right.set_yticks([])
label(right, r'$\varphi_2=\sqrt{2}x_1x_2$', (0, -1.4), ha='center')
label(right, r'新坐标下用一个平面 $\varphi_2=0$' + '\n' + '（图中画成一条竖线）分开',
      (0, 1.15), ha='center', fontsize=9)
for ax in (left, right):
    ax.set_aspect('equal', adjustable='box')
fig.tight_layout(w_pad=2.5)
save(fig, "M6-n4")
