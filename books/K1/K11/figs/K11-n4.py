import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, C, new_fig, save, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(9, 8)
x0, y0, s = 0.85, 0.55, 2.0
for i, p in enumerate((1, 0)):
    for j, q in enumerate((1, 0)):
        x, y = x0 + j*s, y0 + (1-i)*s
        ax.add_patch(Rectangle((x, y), s, s, facecolor=C.LIGHT,
                               edgecolor=C.INK, lw=1.4))
        clause = {(1, 1): r'$\neg p\vee\neg q$', (1, 0): r'$\neg p\vee q$',
                  (0, 1): r'$p\vee\neg q$', (0, 0): r'$p\vee q$'}[(p, q)]
        # Small X in the upper part of the cell, clear of the formula below.
        cx, cy = x + s/2, y + 1.42
        ax.plot([cx - 0.55, cx + 0.55], [cy - 0.45, cy + 0.45],
                color=C.INK, lw=1.4, solid_capstyle='round')
        ax.plot([cx - 0.55, cx + 0.55], [cy + 0.45, cy - 0.45],
                color=C.INK, lw=1.4, solid_capstyle='round')
        label(ax, clause, (cx, y + 0.44), ha='center', va='center', fontsize=11)

label(ax, '$q$', (x0 + s, y0 + 2*s + 0.34), ha='center', va='bottom')
label(ax, '$1$', (x0 + s/2, y0 + 2*s + 0.10), ha='center', va='bottom')
label(ax, '$0$', (x0 + 1.5*s, y0 + 2*s + 0.10), ha='center', va='bottom')
label(ax, '$p$', (x0 - 0.28, y0 + s), ha='right', va='center')
label(ax, '$1$', (x0 - 0.12, y0 + 1.5*s), ha='right', va='center')
label(ax, '$0$', (x0 - 0.12, y0 + 0.5*s), ha='right', va='center')
ax.set(xlim=(0.10, 5.15), ylim=(0.20, 5.15)); ax.set_aspect('equal'); ax.axis('off')
save(fig, 'K11-n4')
