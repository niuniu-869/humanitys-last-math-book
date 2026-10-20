import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

counts = [sum((p == 1, p == 3, p != 2, p != 3)) for p in range(4)]
assert counts == [2, 3, 1, 2]
fig, ax = new_fig(15, 8)
bars = ax.bar(np.arange(4), counts, width=0.58, color=C.LIGHT,
              edgecolor=C.INK, linewidth=1.1)
bars[2].set_facecolor(C.PAPER)
bars[2].set_hatch("///")
ax.axhline(1, color=C.INK, ls="--", lw=1.4)
label(ax, "题目所给：\n恰 1 句真话", (3.55, 1.12), va="bottom", fontsize=10)
for x, y in enumerate(counts):
    label(ax, str(y), (x, y), (0, 6), ha="center", va="bottom")
ax.set_xticks(range(4), ["甲干的", "乙干的", "丙干的", "丁干的"])
ax.set_yticks(range(4))
ax.set_ylabel("真话数")
ax.set_xlim(-0.6, 5.1)
ax.set_ylim(0, 3.55)
save(fig, "K12-n1")
