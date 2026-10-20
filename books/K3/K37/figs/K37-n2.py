import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

chains = [[8], [5, 1, 9], [2], [3]]
assert [len(c) for c in chains] == [1, 3, 1, 1]
assert sum(map(len, chains)) == 6
assert all(k % 4 == slot for slot, chain in enumerate(chains) for k in chain)
fig, ax = new_fig(18, 10)
for slot, chain in enumerate(chains):
    y = -slot * 1.2
    ax.add_patch(Rectangle((-.32, y-.28), .64, .56,
                          facecolor=C.LIGHT, edgecolor=C.INK))
    label(ax, str(slot), (0, y), ha='center', va='center')
    for j, key in enumerate(chain):
        x = 1.6 + j * 1.4
        start = .32 if j == 0 else x-1.4+.32
        arrow(ax, (start, y), (x-.32-start, 0), color=C.INK, lw=1.2)
        ax.add_patch(Rectangle((x-.32, y-.28), .64, .56,
                              facecolor=C.PAPER, edgecolor=C.INK))
        label(ax, str(key), (x, y), ha='center', va='center')
label(ax, r'$h(k)=k\;\mathrm{mod}\;4$', (-2.0, -1.8), ha='center')
label(ax, '槽', (0, .65), ha='center')
label(ax, '找 9：比较 3 次', (3, -.64), ha='center')
label(ax, '找 2：比较 1 次', (3.0, -2.4), va='center')
label(ax, r'$n=6,\quad m=4,\quad \alpha=n/m=1.5$', (1.1, -4.42), ha='center')
ax.set(xlim=(-3.1, 5.2), ylim=(-4.75, 1.0))
ax.axis('off')
fig.tight_layout()
save(fig, "K37-n2")
