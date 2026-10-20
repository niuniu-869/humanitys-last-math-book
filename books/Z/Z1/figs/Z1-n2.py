import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle, Polygon


fig, ax = new_fig(14, 8.2)
ax.set_xlim(-0.4, 8.5)
ax.set_ylim(-1.05, 7.0)
ax.set_aspect("equal")
ax.axis("off")

ax.add_patch(Rectangle((0, 0), 8.1, 6.25, fill=False, edgecolor=C.INK, linewidth=1.5))
label(ax, "全班四名学生", (0.25, 6.12), fontsize=10)

left = Circle((3.25, 3.25), 2.05, fill=False, edgecolor=C.INK, linewidth=1.8)
right = Circle((5.15, 3.25), 2.05, fill=False, edgecolor=C.INK, linewidth=1.8, linestyle="--")
ax.add_patch(left)
ax.add_patch(right)
label(ax, "选数学", (2.05, 5.47), fontsize=10)
label(ax, "选英语", (5.90, 5.47), fontsize=10)

# Violation region, shown with a dashed boundary and a light fill.
# Exact boundary of left disk minus right disk, meeting at x=4.2.
theta = np.arccos(1.9 / (2 * 2.05))
t_left = np.linspace(theta, 2*np.pi-theta, 240)
t_right = np.linspace(np.pi+theta, np.pi-theta, 240)
violation = np.vstack((np.column_stack((3.25+2.05*np.cos(t_left), 3.25+2.05*np.sin(t_left))),
                       np.column_stack((5.15+2.05*np.cos(t_right), 3.25+2.05*np.sin(t_right)))))
ax.add_patch(Polygon(violation, closed=True, facecolor=C.LIGHT, edgecolor=C.GRAY,
                     linewidth=2.0, linestyle="--", alpha=0.55, zorder=3))
label(ax, r"违约行：$p=1,\ q=0$", (2.25, 0.58), fontsize=9.5, ha="center")
arrow(ax, (2.25, 1.05), (-0.25, 0.80), color=C.INK, lw=1)

# Four students: circle, open circle, filled square, open square.
dot(ax, (4.12, 3.38), "甲", color=C.INK, offset=(7, -9), size=28)
ax.scatter(5.65, 3.82, s=46, facecolors=C.PAPER, edgecolors=C.INK, linewidths=1.5, zorder=5)
label(ax, "乙", (5.65, 3.82), offset=(8, -9), fontsize=10)
ax.scatter(6.72, 1.48, s=42, marker="s", color=C.INK, zorder=5)
label(ax, "丙", (6.72, 1.48), offset=(8, -9), fontsize=10)
ax.scatter(2.42, 3.78, s=48, marker="s", facecolors=C.PAPER, edgecolors=C.INK,
           linewidths=1.5, zorder=5)
label(ax, "丁", (2.42, 3.78), offset=(-18, -9), fontsize=10)

label(ax, "甲 (1,1)    乙 (0,1)    丙 (0,0)    丁 (1,0)", (4.05, -0.75),
      fontsize=9.5, ha="center")

save(fig, "Z1-n2")
