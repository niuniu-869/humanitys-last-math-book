import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.5, 7.2)

classes = ["类 1", "类 2", "类 3"]
values = np.array([[0.8668, 0.6652, 0.5065],
                   [0.1173, 0.2447, 0.3072],
                   [0.0159, 0.0900, 0.1863]])
temps = ["$T=0.5$", "$T=1$", "$T=2$"]
hatches = ["///", "", "."]
x = np.arange(len(classes))
width = 0.22

for i in range(3):
    bars = ax.bar(x + (i - 1) * width, values[:, i], width=width, color=C.PAPER,
                  edgecolor=C.INK, linewidth=1.0, hatch=hatches[i], label=temps[i])
    for b, v in zip(bars, values[:, i]):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.025, f"{v:.4f}", ha="center", va="bottom", fontsize=8, rotation=90)

ax.axhline(1 / 3, color=C.GRAY, lw=1.1, ls="--")
label(ax, "均匀分布 $1/3$", (2.48, 1 / 3), offset=(4, 4), color=C.INK, ha="right")

ax.set_xticks(x)
ax.set_xticklabels(classes)
ax.set_ylim(0, 1.12)
ax.set_ylabel("概率")
ax.set_yticks([0, 1 / 3, 2 / 3, 1])
ax.set_yticklabels(["0", "1/3", "2/3", "1"])
ax.legend(loc="upper right", ncol=3, fontsize=8.5, handlelength=2.0)
save(fig, "P14-n5")
