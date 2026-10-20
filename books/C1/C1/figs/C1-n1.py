import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 8.5)
x1 = np.linspace(0, 3000, 120)
x2 = np.linspace(3000, 12000, 220)
x3 = np.linspace(12000, 15000, 100)
y1 = 0.03 * x1
y2 = 90 + 0.1 * (x2 - 3000)
y3 = 990 + 0.2 * (x3 - 12000)
assert np.isclose(y1[-1], 90) and np.isclose(y2[-1], 990) and np.isclose(y3[-1], 1590)
for x, y in [(x1, y1), (x2, y2), (x3, y3)]:
    ax.plot(x, y, color=C.INK, lw=2.0)
for x, y, text, off, ha in [(3000, 90, "$(3000,90)$", (0, 14), "center"),
                              (12000, 990, "$(12000,990)$", (-9, 9), "right")]:
    ax.plot([x, x], [0, y], color=C.GRAY, ls="--", lw=1.1)
    dot(ax, (x, y), size=30)
    # 折点标注离开两段折线；第一处居中放在折点上方，避开“斜率 0.03”
    label(ax, text, (x, y), offset=off, ha=ha, va="bottom", fontsize=9)
# 前两段斜率标在线上方；第三段斜率标在线段下方
label(ax, "斜率 0.03", (1100, 33), offset=(0, 12), ha="center", va="bottom", fontsize=9)
label(ax, "斜率 0.1", (7500, 540), offset=(0, 12), ha="center", va="bottom", fontsize=9)
label(ax, "斜率 0.2", (14100, 1120), ha="center", va="center", fontsize=9)
label(ax, "只画到 $x=15000$，第三档到 25000 为止", (7500, 1755),
      ha="center", va="top", fontsize=8.5)
ax.set_xlim(0, 15000); ax.set_ylim(0, 1800)
ax.set_xlabel("$x$（元）"); ax.set_ylabel("$T$（元）")
ax.set_xticks([0, 3000, 6000, 9000, 12000, 15000])
ax.set_yticks([0, 300, 600, 900, 1200, 1500, 1800])
ax.grid(False)
fig.tight_layout()
save(fig, "C1-n1")
