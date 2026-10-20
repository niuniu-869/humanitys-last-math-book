import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

logits = np.array([16., 8., 0.])
probabilities = []
for scores in (logits, logits / np.sqrt(64)):
    e = np.exp(scores - scores.max())
    probabilities.append(e / e.sum())
expected = [["0.9997", "0.0003", "0.0000"],
            ["0.6652", "0.2447", "0.0900"]]
gradients = [p[0] * (1-p[0]) for p in probabilities]
assert [f"{g:.4f}" for g in gradients] == ["0.0003", "0.2227"]
assert [[f"{v:.4f}" for v in p] for p in probabilities] == expected

fig, axes = new_fig(17.5, 8.5, ncols=2, sharey=True)
for ax, p, title, grad in zip(axes, probabilities,
                            ["不缩放 (16, 8, 0)",
                             r"除以 $\sqrt{64}=8$：(2, 1, 0)"], gradients):
    ax.bar([1, 2, 3], p, width=.58, facecolor=C.LIGHT,
           edgecolor=C.INK, linewidth=1.1, zorder=3)
    for j, v in enumerate(p, 1):
        label(ax, f"{v:.4f}", (j, v), offset=(0, 5),
              ha="center", va="bottom", fontsize=9, annotation_clip=False)
    ax.set(xlim=(.45, 3.55), ylim=(0, 1), xticks=[1, 2, 3],
           xticklabels=["词 1", "词 2", "词 3"], yticks=np.linspace(0, 1, 6))
    ax.set_title(title, pad=27)
    ax.grid(axis="y", color=C.LIGHT, ls=":", lw=.7, zorder=0)
    ax.text(.5, -.22, rf"$p_1(1-p_1)={grad:.4f}$", transform=ax.transAxes,
            ha="center", va="top", color=C.INK, fontsize=11)
axes[0].set_ylabel("权重")
fig.subplots_adjust(left=.09, right=.98, top=.78, bottom=.24, wspace=.24)
save(fig, "M11-n3")
