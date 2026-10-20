import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(23, 9, ncols=3)
cases = [
    (.5, r'$r<1$：$T(n)=2T(n/2)+n^2$', r'$\Theta(n^2)$', '根'),
    (1, r'$r=1$：$T(n)=2T(n/2)+n$', r'$\Theta(n\log n)$', '各层相等'),
    (2, r'$r>1$：$T(n)=4T(n/2)+n$', r'$\Theta(n^2)$', '叶子'),
]
assert [2/2**2, 2/2, 4/2] == [case[0] for case in cases]
for ax, (ratio, title, conclusion, emphasis) in zip(axes, cases):
    lengths = ratio**np.arange(5, dtype=float)
    widths = lengths / max(lengths)
    assert np.allclose(lengths[1:] / lengths[:-1], ratio)
    for i, width in enumerate(widths):
        dominant = ratio == 1 or (ratio < 1 and i == 0) or (ratio > 1 and i == 4)
        ax.barh(i, width, height=.48, facecolor=C.LIGHT, edgecolor=C.INK,
                lw=1.8 if dominant else .8, ls='--' if dominant else '-')
        value = (['1', r'$1/2$', r'$1/4$', r'$1/8$', r'$1/16$'][i]
                 if ratio < 1 else str(int(lengths[i])))
        label(ax, value, (width+.035, i), va='center', fontsize=9)
    ax.set_title(title, fontsize=9, pad=13)
    ax.set_yticks(range(5), [f'$i={i}$' for i in range(5)], fontsize=9)
    ax.set(xlim=(0, 1.53), ylim=(4.65, -.65))
    ax.set_xticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis='y', length=0)
    at = 0 if ratio < 1 else (2 if ratio == 1 else 4)
    label(ax, emphasis, (1.25, at), va='center', fontsize=9)
    label(ax, conclusion, (.6, 5.2), ha='center', fontsize=12, annotation_clip=False)
fig.subplots_adjust(left=.06, right=.98, top=.80, bottom=.19, wspace=.43)
save(fig, "K31-n4")
