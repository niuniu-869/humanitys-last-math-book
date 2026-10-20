import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch


fig, ax = new_fig(14, 8)
ax.set_xlim(-0.8, 6.8)
ax.set_ylim(-1.3, 2.3)
ax.axis("off")

xs = np.arange(4, dtype=float)*1.8
top = ["$k$", "$z$", "$t$", "$j$"]
bot = ["$\\neg k$", "$\\neg z$", "$\\neg t$", "$\\neg j$"]
yt, yb = 1.35, 0.05

def node(x, y, txt, fill=C.PAPER):
    patch = FancyBboxPatch((x - 0.31, y - 0.18), 0.62, 0.36,
                           boxstyle="round,pad=0.04,rounding_size=0.07",
                           facecolor=fill, edgecolor=C.INK, linewidth=1.5, zorder=3)
    ax.add_patch(patch)
    label(ax, txt, (x, y), ha="center", va="center", offset=(0, 0), fontsize=11)

for i, txt in enumerate(top):
    node(xs[i], yt, txt)
for i, txt in enumerate(bot):
    node(xs[i], yb, txt, fill=C.LIGHT if i == 2 else C.PAPER)

def conn(i, y, j, style="-", lw=2.0):
    x0 = xs[i] + (0.33 if j > i else -0.33)
    x1 = xs[j] - (0.33 if j > i else -0.33)
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=lw, linestyle=style,
                                mutation_scale=11, shrinkA=0, shrinkB=0), zorder=2)

# Original rules
conn(1, yt, 0, "-", 2.3)
conn(1, yt, 2, "-", 2.3)
conn(2, yb, 3, "-", 2.3)
# Contrapositives
conn(0, yb, 1, "--", 2.0)
conn(2, yb, 1, "--", 2.0)
conn(3, yt, 2, "--", 2.0)
# Route from ¬t
conn(2, yb, 3, "-", 3.8)
conn(2, yb, 1, "--", 3.8)

label(ax, "已知", (xs[2], yb), offset=(12, -22), fontsize=9)
label(ax, "到此为止：$\\neg z$ 没有箭头通向 $\\neg k$", (xs[1], yb),
      offset=(0, -27), fontsize=8.5, ha="center")
label(ax, "实线：原规则", (3.6, -0.77), fontsize=8.5)
label(ax, "虚线：逆否箭头", (3.6, -0.97), fontsize=8.5)
label(ax, "粗线：从已知出发的路线", (2.5, -1.17), fontsize=8.5)
save(fig, "Z2-n3")
