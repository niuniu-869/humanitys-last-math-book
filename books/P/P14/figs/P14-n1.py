import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.5, 7.2)

p = np.linspace(0.008, 1.0, 800)
info = -np.log2(p)
ax.plot(p, info, color=C.BLUE, lw=2.0)

for prob, val, text in ((1 / 2, 1.0, "1"), (1 / 4, 2.0, "2"), (1 / 8, 3.0, "3"), (1 / 36, np.log2(36), "5.17")):
    ax.plot([prob, prob], [0, val], color=C.GRAY, lw=1.0, ls=":", zorder=1)
    dot(ax, (prob, val), text, color=C.BLUE, offset=(8, 7), size=25)

prob = 1 / 6
val = np.log2(6)
ax.plot([prob, prob], [0, val], color=C.GRAY, lw=1.0, ls="--", zorder=1)
ax.scatter([prob], [val], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.3, zorder=5)
label(ax, "2.585", (prob, val), offset=(26, 6), color=C.INK)
label(ax, "概率越小，信息量越大", (0.31, 4.95), color=C.INK, ha="center")

ax.set_xlim(0, 1.03)
ax.set_ylim(0, 6.15)
ax.set_xlabel("概率 $p$")
ax.set_ylabel("信息量 $I(p)=-\\log_2 p$（比特）")
ax.set_xticks([1 / 36, 1 / 8, 1 / 4, 1 / 2, 1])
ax.set_xticklabels(["1/36", "1/8", "1/4", "1/2", "1"])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
save(fig, "P14-n1")
