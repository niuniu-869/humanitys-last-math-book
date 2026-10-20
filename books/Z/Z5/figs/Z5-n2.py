import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(15, 8.5); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0.0, 6.4)
ax.add_patch(Rectangle((0.4, 2.2), 2.0, 2.4, fill=False, ec=C.INK, lw=1.5))
label(ax, "5 人选 3", (1.4, 4.8), ha="center")
for i, t in enumerate("甲乙丙丁戊"): label(ax, t, (1.4, 4.2 - i*0.45), ha="center")
ax.add_patch(FancyBboxPatch((3.05, 3.1), 2.7, 0.9, boxstyle="round,pad=0.08", fill=False, ec=C.INK, lw=1.5))
label(ax, "小组 {甲，乙，丙}", (4.4, 3.55), ha="center")
ax.plot([5.8, 6.15], [3.55, 3.55], color=C.INK); ax.plot([6.15, 6.15], [1.9, 5.9], color=C.INK)
for i, t in enumerate(["(甲,乙,丙)", "(甲,丙,乙)", "(乙,甲,丙)", "(乙,丙,甲)", "(丙,甲,乙)", "(丙,乙,甲)"]):
    label(ax, t, (6.35, 5.6 - i*0.72), ha="left")
label(ax, "同一个小组对应的 6 种职务安排", (6.35, 6.15), ha="left", fontsize=8)
ax.text(0.4, 1.74, r"排列 $\mathrm{A}_5^3=60$ ＝ 小组数 $\mathrm{C}_5^3$ × 每组的排法 $3!$", ha="left", va="center")
ax.text(0.4, 0.98, r"$\mathrm{C}_5^3\times3!=60$，其中 $3!=6$", ha="left", va="center")
ax.text(0.4, 0.22, r"所以 $\mathrm{C}_5^3=60\div6=10$", ha="left", va="center")
save(fig, "Z5-n2")
