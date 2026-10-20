import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(21, 15, nrows=2, ncols=2)
fig.subplots_adjust(left=0.09, right=0.91, bottom=0.15, top=0.88, hspace=0.42, wspace=0.42)
distributions = [np.array([0.92, 0.03, 0.02, 0.01, 0.01, 0.01]),
                 np.array([0.25, 0.25, 0.20, 0.15, 0.10, 0.05])]
for row, p in enumerate(distributions):
    cumulative = np.cumsum(p)
    assert np.isclose(cumulative[-1], 1)
    count = int(np.searchsorted(cumulative, 0.9)) + 1
    assert count == [1, 5][row]
    for col in range(2):
        ax = axes[row, col]
        keep = 3 if col == 0 else count
        for i, value in enumerate(p, 1):
            ax.bar(i, value, width=0.6, facecolor=C.LIGHT if i <= keep else C.PAPER,
                   edgecolor=C.INK, ls="-" if i <= keep else "--", lw=1.1)
        ax.set(xlim=(0.4, 6.6), ylim=(0, 1), xticks=range(1, 7),
               xlabel="词序号", ylabel=f"$P_{row+1}$ 概率")
        ax.text(0.97, 1.07, f"保留 {keep} 个", transform=ax.transAxes, ha="right", fontsize=9)
        if col == 1:
            right = ax.twinx()
            right.set(ylim=(0, 1), yticks=[0, 0.5, 1], ylabel="累积概率")
            right.spines["right"].set_visible(True)
            right.step(np.r_[0.4, np.arange(1, 7), 6.6], np.r_[0, cumulative, 1],
                       where="post", color=C.INK, ls=":", lw=1.5, clip_on=False)
            right.axhline(0.9, color=C.INK, ls="--", lw=0.8)
            label(right, "$p=0.9$", (5.65, 0.9), offset=(0, -12), ha="center", fontsize=8)
axes[0, 0].set_title(r"top-$k$，$k=3$", pad=29)
axes[0, 1].set_title(r"top-$p$，$p=0.9$", pad=29)
assert np.allclose(np.cumsum(distributions[1]), [0.25, 0.50, 0.70, 0.85, 0.95, 1])
fig.text(0.5, 0.035, "实线填充条：保留    虚线空心条：去掉    点线：累积概率", ha="center", fontsize=9)
save(fig, "M14-n3")
