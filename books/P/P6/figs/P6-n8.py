import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 10, ncols=2)
fig.subplots_adjust(left=0.07, right=0.97, bottom=0.42, top=0.93, wspace=0.38)
left, right = axes
left.fill([0, 1, 1, 0], [0, 0, 1, 1], color=C.LIGHT)
left.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], color=C.INK)
right.fill([0, 0, 1], [0, 1, 1], color=C.LIGHT)
right.plot([0, 0, 1, 0], [0, 1, 1, 0], color=C.INK)
for x0 in [0.3, 0.8]:
    left.plot([x0, x0], [0, 1], color=C.INK, ls='--')
    right.plot([x0, x0], [0, 1], color=C.INK, ls='--', lw=1)
    right.plot([x0, x0], [x0, 1], color=C.INK, lw=3)
label(left, '$f=4xy$', (0.43, 0.75))
label(right, '$f=8xy$', (0.06, 0.8))
right.plot(0.8, 0.5, 'o', mfc=C.PAPER, mec=C.INK, ms=6, zorder=5)
label(right, '$f=0$', (0.8, 0.5), (-9, -4), ha='right')
label(right, r'$f_Xf_Y>0$', (0.8, 0.5), (-9, -21), ha='right')
for ax in axes:
    ax.set(xlim=(0, 1.06), ylim=(0, 1.08), aspect='equal', xlabel='$x$', ylabel='$y$')
    ax.set_xticks([0, 0.3, 0.8, 1], ['0', '0.3', '0.8', '1'])
    ax.set_yticks([0, 1])
# Horizontal density and vertical y preserve the orientation of each slice.
for x0, pos in [(0.3, [0.16, 0.17, 0.09, 0.15]), (0.8, [0.35, 0.17, 0.09, 0.15])]:
    inset = fig.add_axes(pos)
    y = np.linspace(0, 1, 101)
    inset.plot(4*x0*y, y, color=C.INK)
    inset.set(xlim=(0, 3.4), ylim=(0, 1.05), xlabel='$f$', ylabel='$y$')
    inset.set_xticks([0, 4*x0], ['0', f'{4*x0:g}'])
    inset.set_yticks([1])
    label(inset, f'$x={x0}$', (0, 1), (0, 8), fontsize=9)
label(left, '放大后相同', (0.3, 0.015), xycoords='figure fraction', ha='center', fontsize=9)
label(right, '切口范围不同', (0.5, -0.42), ha='center', annotation_clip=False)
assert 0.8 > 0.5
assert (4*0.8*(1-0.8**2))*(4*0.5**3) > 0
save(fig, 'P6-n8')
