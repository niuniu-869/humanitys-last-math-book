import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, Ellipse


fig, ax = new_fig(13, 8)
ax.set_xlim(-1.4, 5.8)
ax.set_ylim(-2.0, 2.4)
ax.axis("off")

def node(x, y, txt, lw=1.5, ls="-", fill=C.PAPER, size=(0.72, 0.44)):
    w, h = size
    patch = FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                           boxstyle="round,pad=0.04,rounding_size=0.08",
                           facecolor=fill, edgecolor=C.INK, linewidth=lw, linestyle=ls, zorder=3)
    ax.add_patch(patch)
    label(ax, txt, (x, y), ha="center", va="center", offset=(0, 0), fontsize=12)

node(0, 1.05, "$p$")
node(0, -0.25, "$q$")
node(3.6, 0.4, "$r$", lw=2.6)
node(1.15, -1.35, "$x$", ls="--", fill=C.PAPER)

ell = Ellipse((0, 0.4), width=2.2, height=2.6, facecolor="none", edgecolor=C.INK, linewidth=1.6, zorder=1)
ax.add_patch(ell)
label(ax, "$p\\vee q$：至少站着一个", (0.05, 1.88), offset=(0, 0), ha="center", fontsize=9.5)

def conn(start, end, style="-", lw=2.0):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=lw, linestyle=style,
                                mutation_scale=11, shrinkA=10, shrinkB=13), zorder=2)

conn((0.4, 1.05), (3.15, 0.48))
conn((0.4, -0.25), (3.15, 0.34))
conn((1.55, -1.35), (3.1, 0.27), "--", 1.8)
ax.text(2.25, -0.56, "×", fontsize=18, ha="center", va="center", color=C.INK, zorder=5)
label(ax, "第三种情况", (1.15, -1.35), offset=(0, -23), fontsize=9)
label(ax, "没分全：$r$ 推不出", (3.6, -0.3), offset=(0, 0), fontsize=9.5, ha="center")
save(fig, "Z2-n2")
