import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


fig, axes = new_fig(14, 8.5, nrows=3, sharex=True, sharey=True)
fig.subplots_adjust(left=0.11, right=0.79, top=0.97, bottom=0.11, hspace=0.18)

p = np.linspace(0, 100, 1001)
curves = [
    (np.sin(p), "频率 1", "-"),
    (np.sin(p / 10), "频率 1/10", "--"),
    (np.sin(p / 100), "频率 1/100", ":"),
]
for ax, (y, title, ls) in zip(axes, curves):
    ax.plot(p, y, color=C.INK, ls=ls, lw=1.6,
            dash_capstyle="butt", solid_capstyle="round")
    ax.set_ylim(-1.12, 1.12)
    ax.set_yticks([-1, 0, 1])
    ax.set_xlim(0, 100)
    ax.grid(axis="y", color=C.LIGHT, lw=0.6)
    ax.set_axisbelow(True)
    # 放到坐标框外右侧的空白处：曲线、坐标轴和刻度都不会穿过标签。
    label(ax, title, (1.025, 0.96), xycoords="axes fraction",
          ha="left", va="top", fontsize=8.8)

axes[-1].set_xlabel("位置 p")
axes[1].set_ylabel("值")
save(fig, "M12-n3")
