import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

fig, ax = new_fig(17.5, 8.5)
ax.set_xlim(1.0, 12.2); ax.set_ylim(1.3, 6.7)
ax.set_aspect("equal"); ax.axis("off")

W, H = 2.0, 0.75
boxes = {
    "偏导连续": (2.4, 4.4),
    "可微":     (6.6, 4.4),
    "连续":     (10.7, 6.1),
    "偏导存在": (10.7, 2.7),
}
for text, (cx, cy) in boxes.items():
    ax.add_patch(Rectangle((cx - W/2, cy - H/2), W, H, facecolor=C.PAPER,
                           edgecolor=C.INK, linewidth=1.2, zorder=2))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=10.5, zorder=6)

def solid_arrow(start, end):
    ax.annotate("", xy=end, xytext=start, zorder=3,
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.5,
                                shrinkA=0, shrinkB=0, mutation_scale=12))

def dashed_arrow(start, end, rad):
    ax.annotate("", xy=end, xytext=start, zorder=3,
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.15,
                                ls="--", shrinkA=0, shrinkB=0,
                                mutation_scale=11,
                                connectionstyle=f"arc3,rad={rad}"))

# 三条成立的蕴含（实线）
solid_arrow((3.4, 4.4), (5.6, 4.4))       # 偏导连续 → 可微
solid_arrow((7.6, 4.55), (9.7, 5.90))     # 可微 → 连续
solid_arrow((7.6, 4.25), (9.7, 2.90))     # 可微 → 偏导存在

# 四条不成立的方向（虚线弯箭头 + 中点叉号）
# 1) 偏导存在 → 连续（右弯），反例 ③ h
dashed_arrow((10.8, 3.075), (10.8, 5.725), 0.3)
label(ax, "×", (11.1975, 4.4), offset=(0, 0), ha="center", va="center",
      fontsize=14)
label(ax, "③ $h$", (11.38, 4.4), offset=(0, 0), ha="left", va="center",
      fontsize=9)

# 2) 连续 → 偏导存在（左弯），反例 锥面 sqrt(x^2+y^2)
dashed_arrow((10.6, 5.725), (10.6, 3.075), 0.3)
label(ax, "×", (10.2025, 4.4), offset=(0, 0), ha="center", va="center",
      fontsize=14)
label(ax, r"锥面 $\sqrt{x^2+y^2}$", (9.98, 4.4), offset=(0, 0), ha="right",
      va="center", fontsize=8.5)

# 3) 连续且偏导存在 → 可微（下弯），反例 ④ g
dashed_arrow((9.7, 2.55), (6.6, 4.03), -0.3)
label(ax, "×", (7.928, 2.825), offset=(0, 0), ha="center", va="center",
      fontsize=14)
label(ax, "④ $g$", (7.9, 2.32), offset=(0, 0), ha="center", va="center",
      fontsize=9)
label(ax, "连续且偏导存在", (7.9, 1.95), offset=(0, 0), ha="center",
      va="center", fontsize=8.5)

# 4) 可微 → 偏导连续（上弯），反例 (x^2+y^2) sin(1/(x^2+y^2))
dashed_arrow((7.0, 4.775), (3.0, 4.775), 0.3)
label(ax, "×", (5.0, 5.375), offset=(0, 0), ha="center", va="center",
      fontsize=14)
label(ax, r"$(x^2+y^2)\sin\frac{1}{x^2+y^2}$", (5.0, 5.95), offset=(0, 0),
      ha="center", va="center", fontsize=9)

fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
save(fig, "C20-n5")
