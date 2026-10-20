import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle


data = np.array([12, 15, 16, 18, 19, 21, 22, 25, 27, 31, 58])
mean, median = data.mean(), np.median(data)

fig, (ax1, ax2) = new_fig(14, 7.6, nrows=2, sharex=True,
                            gridspec_kw={"height_ratios": [3, 2], "hspace": 0.08})

bins = np.arange(10, 61, 10)
counts, edges = np.histogram(data, bins=bins)
heights = counts / (len(data) * 10)
ax1.bar(edges[:-1], heights, width=10, align="edge", color=C.LIGHT,
        edgecolor=C.INK, linewidth=1.0)
ax1.axvline(mean, color=C.INK, linestyle="--", linewidth=1.2)
ax1.axvline(median, color=C.INK, linestyle="-", linewidth=1.2)
label(ax1, "平均数 24", (mean, 0.0495), offset=(5, 2), ha="left", va="bottom")
label(ax1, "中位数 21", (median, 0.0495), offset=(-5, 2), ha="right", va="bottom")
ax1.set_ylim(0, 0.060)
ax1.set_ylabel("柱高（面积合计为 1）")
ax1.set_yticks([0, 0.02, 0.04])

# Horizontal box-and-whisker, with the isolated observation shown explicitly.
y = 0.56
ax2.plot([12, 16], [y, y], color=C.INK, lw=1.2)
ax2.plot([27, 31], [y, y], color=C.INK, lw=1.2)
ax2.plot([12, 12], [y - 0.12, y + 0.12], color=C.INK, lw=1.2)
ax2.plot([31, 31], [y - 0.12, y + 0.12], color=C.INK, lw=1.2)
ax2.add_patch(Rectangle((16, y - 0.18), 11, 0.36, facecolor=C.LIGHT,
                        edgecolor=C.INK, linewidth=1.2))
ax2.plot([21, 21], [y - 0.18, y + 0.18], color=C.INK, lw=1.5)
ax2.scatter([58], [y], s=34, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.2, zorder=5)
label(ax2, "异常点 58", (58, y), offset=(-5, 12), ha="right", va="bottom")
label(ax2, "Q1=16", (16, y), offset=(0, -12), ha="center", va="top")
label(ax2, "中位数 21", (21, y), offset=(0, 14), ha="center", va="bottom")
label(ax2, "Q3=27", (27, y), offset=(0, -12), ha="center", va="top")
ax2.set_ylim(0, 1.1)
ax2.set_yticks([])
ax2.set_xlabel("响应时间（毫秒）")
ax2.set_xlim(0, 65)

save(fig, "P10-n1")
