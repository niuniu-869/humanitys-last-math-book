import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(12, 7.5)
m = np.arange(1, 7)
h = (2 * m - 1) / 36
ax.bar(m, h, width=0.72, color=C.LIGHT, edgecolor=C.INK, linewidth=1.1)
for x, y, k in zip(m, h, m):
    label(ax, rf"$\frac{{{2*k-1}}}{{36}}$", (x, y), offset=(0, 5), ha="center", va="bottom")
support = 161 / 36
ax.plot([support], [-0.012], marker="^", markersize=12, color=C.INK, clip_on=False)
label(ax, r"$E(M)=161/36\approx4.47$", (support, -0.012), offset=(0, -22), ha="center", va="top")
ax.axvline(3.5, color=C.GRAY, ls="--", lw=1.2)
label(ax, "中点 3.5", (3.38, 0.265), offset=(0, 0), ha="right", va="bottom")
ax.set_xlim(0.35, 6.65); ax.set_ylim(-0.08, 0.34)
ax.set_xticks(m); ax.set_xlabel(""); ax.set_ylabel("$P(M=m)$")
label(ax, "$m$", (6.55, 0), offset=(0, -18), ha="right", va="top")
ax.spines["bottom"].set_position(("data", 0)); ax.grid(False)
save(fig, "P7-n1")
