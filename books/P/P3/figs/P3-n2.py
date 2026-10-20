import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

s = np.arange(2, 13)
theory = np.array([(6 - abs(int(x) - 7)) / 36 for x in s])
sim = np.array([0.0288, 0.0558, 0.0832, 0.1115, 0.1386, 0.1660,
                0.1409, 0.1103, 0.0813, 0.0553, 0.0283])
assert np.isclose(theory[s == 7][0], 1 / 6)

fig, ax = new_fig(15, 8)
w = 0.34
ax.bar(s - w / 2, theory, width=w, facecolor=C.LIGHT, edgecolor=C.INK,
       linewidth=0.9, label="理论值")
ax.bar(s + w / 2, sim, width=w, facecolor=C.PAPER, edgecolor=C.INK,
       linewidth=0.9, label="模拟频率")
ax.set(xlim=(1.35, 12.65), ylim=(0, 0.18),
       xticks=s, yticks=np.arange(0, 0.181, 0.03),
       xlabel=r"点数和 $s$", ylabel="概率")
ax.grid(axis="y", ls=":", color=C.LIGHT, lw=0.7)
ax.set_axisbelow(True)
label(ax, r"最高：$\frac{1}{6}$", (7 - w / 2, 1 / 6), offset=(0, 7), ha="center", va="bottom", fontsize=9)
ax.legend(loc="upper left", ncol=2, handlelength=1.2, columnspacing=1.0)
save(fig, "P3-n2")
