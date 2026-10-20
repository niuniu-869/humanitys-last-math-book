import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch

fig, ax = new_fig(16, 16)
t = np.linspace(0, 2*np.pi, 801)
ax.plot(np.sqrt(2)*np.cos(t), np.sqrt(2)*np.sin(t), color=C.INK, lw=2.2, ls='-')
for value, style, width in [(1, '--', 1.3), (-1, '--', 1.3), (.5, ':', 1)]:
    for sign in [-1, 1]:
        x = sign*np.linspace(abs(value)/2.2, 2.2, 501)
        ax.plot(x, value/x, color=C.INK, lw=width, ls=style)
for x, y, offset, align in [(1, 1, (-12, -26), 'right'), (-1, -1, (12, 8), 'left'),
                           (1, -1, (-12, 8), 'right'), (-1, 1, (12, -26), 'left')]:
    assert x*x+y*y == 2
    dot(ax, (x, y), size=30)
    text = f'$({x},{y})$\n' + ('最大 1' if x*y == 1 else '最小 −1')
    if x*y == 1:
        label(ax, text, (1.5*x, 1.02*y), ha='center', va='center', fontsize=9)
    else:
        label(ax, text, (x, y), offset, ha=align, fontsize=9)
direction = np.array([1, 1]) / np.sqrt(2)
for length, style, width in [(.7, '--', 1.3), (.5, '-', 1.7)]:
    endpoint = np.array([1, 1]) + length*direction
    assert np.isclose(np.linalg.norm(endpoint - 1), length)
    ax.add_patch(FancyArrowPatch((1, 1), endpoint, arrowstyle='-|>',
                                mutation_scale=12, shrinkA=0, shrinkB=0,
                                color=C.INK, lw=width, ls=style, zorder=4))
label(ax, r'$\nabla f$', (1.37, 1.30), (9, -8), fontsize=11)
label(ax, r'$\nabla g$', (1.50, 1.50), (-13, 7), ha='right', fontsize=11)
label(ax, '$xy=1$', (.61, 1.95), (8, 0), fontsize=11)
label(ax, '$xy=-1$', (-.65, 1.95), (-9, 0), ha='right', fontsize=11)
label(ax, '$xy=0.5$', (1.61, .12), fontsize=10)
label(ax, '$x^2+y^2=2$', (-1.98, -.85), fontsize=10)
ax.set(xlim=(-2.2, 2.2), ylim=(-2.2, 2.2), aspect='equal',
       xticks=[-2, -1, 1, 2], yticks=[-2, -1, 1, 2])
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
label(ax, '$x$', (2.07, .10))
label(ax, '$y$', (.10, 2.07))
fig.subplots_adjust(left=.07, right=.97, bottom=.07, top=.97)
roots = np.sqrt([1 + np.sqrt(3)/2, 1 - np.sqrt(3)/2])
assert np.allclose(roots**2 + (.5/roots)**2, 2)
assert np.allclose(roots*(.5/roots), .5)
print('K42-n3: positive intersections=', list(zip(roots, .5/roots)))
save(fig, "K42-n3")
