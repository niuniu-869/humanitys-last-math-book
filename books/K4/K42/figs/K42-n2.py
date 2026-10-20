import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

p = np.linspace(0, 1, 601)
b = (1 - (1 - 2*p)**3) / 2
c = 3*p*(1-p)**2
d = (1 + (1 - 2*p)**3) / 2
assert np.allclose(b + d, 1)
assert np.allclose(b[[0, 300, -1]], [0, .5, 1])
assert np.allclose(c[[300, -1]], [.375, 0])
fig, ax = new_fig(13, 10)
for values, style, width in [(np.full_like(p, .5), ':', 1.4), (b, '-', 2.3),
                             (c, '--', 1.5), (d, '-.', 1.5)]:
    ax.plot(p, values, color=C.INK, ls=style, lw=width)
for x in [0, 1]:
    ax.axvline(x, color=C.GRAY, ls=':', lw=.8)
for xy in [(0, .5), (0, 1), (1, 0)]:
    ax.scatter(*xy, s=42, facecolor=C.PAPER, edgecolor=C.INK, zorder=5, clip_on=False)
dot(ax, (0, 0), size=34)
dot(ax, (1, 1), size=34)
for collection in ax.collections:
    collection.set_clip_on(False)
label(ax, '真实值 0', (0, 0), (22, 3), fontsize=9)
label(ax, '真实值 1', (1, 1), (-10, -5), ha='right', va='top', fontsize=9)
for text, xy in [('(A)', (.86, .53)), ('(B)', (.78, .81)),
                 ('(C)', (.66, .29)), ('(D)', (.18, .68))]:
    label(ax, text, xy, fontsize=11)
ax.set(xlim=(0, 1), ylim=(0, 1.05), xticks=[0, .5, 1],
       yticks=[0, .5, 1], xlabel='$p$', ylabel='概率')
ax.spines['left'].set_position(('outward', 7))
ax.spines['bottom'].set_position(('outward', 7))
fig.subplots_adjust(left=.15, right=.94, bottom=.16, top=.95)
print('K42-n2: B(0,.5,1)=', b[[0, 300, -1]], 'C(.5,1)=', c[[300, -1]])
save(fig, "K42-n2")
