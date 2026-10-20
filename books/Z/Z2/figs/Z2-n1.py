import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch


fig, ax = new_fig(16, 8.5)
ax.set_xlim(-0.8, 8.9)
ax.set_ylim(-1.25, 2.25)
ax.axis("off")

xs = np.arange(5, dtype=float)*1.9
top = [r"$\neg e$", r"$a$", r"$b$", r"$\neg c$", r"$\neg d$"]
bot = [r"$e$", r"$\neg a$", r"$\neg b$", r"$c$", r"$d$"]
yt, yb = 1.45, 0.15

def node(x, y, txt, fill=C.PAPER, lw=1.5, ls="-"):
    patch = FancyBboxPatch((x - 0.31, y - 0.18), 0.62, 0.36,
                           boxstyle="round,pad=0.04,rounding_size=0.07",
                           facecolor=fill, edgecolor=C.INK, linewidth=lw, linestyle=ls, zorder=3)
    ax.add_patch(patch)
    label(ax, txt, (x, y), ha="center", va="center", offset=(0, 0), fontsize=11)

for i, txt in enumerate(top):
    node(xs[i], yt, txt)
for i, txt in enumerate(bot):
    node(xs[i], yb, txt, fill=C.LIGHT if i == 4 else C.PAPER)

def conn(i, y, j, style="-", lw=1.8):
    x0 = xs[i] + (0.33 if j > i else -0.33)
    x1 = xs[j] - (0.33 if j > i else -0.33)
    ax.annotate("", xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=lw, linestyle=style,
                                mutation_scale=11, shrinkA=0, shrinkB=0), zorder=2)

# Original rules
conn(1, yt, 2, "-", 2.4)
conn(2, yt, 3, "-", 2.4)
conn(4, yb, 3, "-", 2.4)
conn(1, yb, 0, "-", 2.4)
# Contrapositives
conn(2, yb, 1, "--", 2.0)
conn(3, yb, 2, "--", 2.0)
conn(3, yt, 4, "--", 2.0)
conn(0, yt, 1, "--", 2.0)

# Route from d: d -> c -> ¬b -> ¬a -> e
conn(4, yb, 3, "-", 3.8)
conn(3, yb, 2, "--", 3.8)
conn(2, yb, 1, "--", 3.8)
conn(1, yb, 0, "-", 3.8)

label(ax, "出发点 $d$", (xs[4], yb), offset=(12, -22), fontsize=9)
label(ax, r"从 $a$ 出发：$b,\ \neg c,\ \neg d$，走不到 $e$", (xs[1], yt),
      offset=(-35, 25), fontsize=8.5, ha="center")
label(ax, "实线：原规则", (6.2, -0.82), fontsize=8.5)
label(ax, "虚线：逆否箭头", (6.2, -1.02), fontsize=8.5)
label(ax, "粗线：从 $d$ 出发的路线", (6.2, -1.22), fontsize=8.5)
save(fig, "Z2-n1")
