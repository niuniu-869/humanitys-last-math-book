import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 10)
a, b, c, d = 1, 3, 1, 2.5
ax.fill([a, b, b, a], [c, c, d, d], color=C.LIGHT)
# Coincident boundaries retain their exact coordinates; white dash gaps reveal
# the wider underlying boundary without displacing any quadrant.
for x, y, style, width in [(b, d, '-', 2.8), (a, d, '--', 1.8),
                          (b, c, ':', 1.8), (a, c, '-.', 1.2)]:
    ax.plot([-1.3, x, x], [y, y, -1.2], color=C.PAPER, lw=width+0.7)
    ax.plot([-1.3, x, x], [y, y, -1.2], color=C.INK, ls=style, lw=width)
ax.plot([a, b, b, a, a], [c, c, d, d, c], color=C.INK, lw=0.65)
for p in [(a, c), (a, d), (b, c), (b, d)]:
    dot(ax, p)
label(ax, '$F(b,d)$', (b, d), (9, 8))
label(ax, '$F(a,d)$', (a, d), (-8, 11), ha='right')
label(ax, '$F(b,c)$', (b, c), (9, 6))
label(ax, '$F(a,c)$', (a, c), (-9, 8), ha='right')
label(ax, '被减了两次\n加回一次', (-0.75, -0.65), ha='center', va='center', fontsize=9)
for side in ['left', 'bottom']:
    ax.spines[side].set_position('zero')
ax.set(xlim=(-1.3, 4.15), ylim=(-1.2, 3.2), aspect='equal')
ax.set_xticks([a, b], ['', ''])
ax.set_yticks([c, d], ['', ''])
for x, name in [(a, '$a$'), (b, '$b$')]:
    label(ax, name, (x, 0), (8, -16))
for y, name in [(c, '$c$'), (d, '$d$')]:
    label(ax, name, (0, y), (-9, 7), ha='right')
label(ax, '$x$', (4.0, 0), (0, 6))
label(ax, '$y$', (0, 3.05), (6, 0))
save(fig, 'P6-n1')
