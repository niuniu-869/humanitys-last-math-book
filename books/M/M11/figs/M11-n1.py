import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Patch
from matplotlib.colors import LinearSegmentedColormap

plain = np.array([[0.4011, 0.1978, 0.4011],
                  [0.2840, 0.1400, 0.5760],
                  [0.3057, 0.0743, 0.6200]])
masked = np.array([[1, 0, 0], [0.6698, 0.3302, 0],
                   [0.3057, 0.0743, 0.6200]])
assert np.allclose(plain.sum(axis=1), 1)
assert np.allclose(masked.sum(axis=1), 1)
assert np.all(masked[np.triu_indices(3, 1)] == 0)
scores = np.array([[1., 0., 1.], [2., 1., 3.], [3., 1., 4.]]) / np.sqrt(2)
for target, causal in [(plain, False), (masked, True)]:
    logits = scores.copy()
    if causal:
        logits[np.triu_indices(3, 1)] = -np.inf
    e = np.exp(logits - logits.max(axis=1, keepdims=True))
    assert np.array_equal(np.round(e / e.sum(axis=1, keepdims=True), 4), target)

fig, axes = new_fig(17.5, 8.3, ncols=2)
cmap = LinearSegmentedColormap.from_list("weights", [C.PAPER, C.RED])
for ax, values, title in zip(axes, [plain, masked],
                            ["例 3：不加掩码", "例 5：因果掩码"]):
    im = ax.imshow(values, vmin=0, vmax=1, cmap=cmap)
    for i in range(3):
        for j in range(3):
            hidden = ax is axes[1] and j > i
            ax.add_patch(Rectangle((j-.5, i-.5), 1, 1,
                                  fill=False, edgecolor=C.GRAY, lw=.65,
                                  hatch="///" if hidden else None))
            v = values[i, j]
            text = str(int(v)) if v in (0, 1) else f"{v:.4f}"
            ax.text(j, i, text, ha="center", va="center", fontsize=10,
                    color=C.PAPER if v >= .55 else C.INK,
                    bbox=dict(facecolor=C.PAPER, edgecolor="none", pad=1)
                    if hidden else None)
    ax.set(xticks=range(3), yticks=range(3), xticklabels=[1, 2, 3],
           yticklabels=[1, 2, 3], xlabel="被看的词 $j$", ylabel="发问的词 $i$")
    ax.set_title(title, pad=10)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
fig.subplots_adjust(left=.09, right=.87, top=.84, bottom=.22, wspace=.44)
cax = fig.add_axes([.91, .26, .018, .52])
fig.colorbar(im, cax=cax, ticks=[0, .5, 1])
axes[1].legend(handles=[Patch(facecolor=C.PAPER, edgecolor=C.GRAY,
                             hatch="///", label="被遮住")],
               loc="upper center", bbox_to_anchor=(.5, -.25), fontsize=9)
save(fig, "M11-n1")
