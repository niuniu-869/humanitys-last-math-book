import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = new_fig(18, 15)
ax.set(xlim=(0, 12), ylim=(0, 10.5))
ax.axis("off")
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)

def box(x, y, text, w=5.1, h=1.0, lw=1.1, fill=C.PAPER, ls="-"):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.03,rounding_size=0.10", facecolor=fill,
        edgecolor=C.INK, linewidth=lw, linestyle=ls))
    label(ax, text, (x, y), ha="center", va="center", fontsize=10)

def link(a, b, ls="-"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>",
        mutation_scale=12, lw=1.3, ls=ls, color=C.INK))

box(6, 9.6, "子句：" + r"$(\neg a\vee b)\quad(\neg b\vee c)$" + "\n"
    + r"$(\neg a\vee\neg c\vee d)\quad(\neg b\vee\neg d)\quad(a\vee b)$",
    w=10.5, h=1.15)
link((4.1, 8.99), (3.0, 7.61))
link((7.9, 8.99), (9.0, 7.61), "--")
label(ax, "决定 $a=$ 真", (2.65, 8.6), ha="center", fontsize=10)
label(ax, "回溯后决定 $a=$ 假", (9.65, 8.6), ha="center", fontsize=10)

left = ["传播 $b=$ 真\n" + r"由 $\neg a\vee b$",
        "传播 $c=$ 真\n" + r"由 $\neg b\vee c$",
        "传播 $d=$ 真\n" + r"由 $\neg a\vee\neg c\vee d$",
        "冲突：" + r"$\neg b\vee\neg d$" + " 被删空 ×"]
right = ["传播 $b=$ 真\n" + r"由 $a\vee b$",
         "传播 $c=$ 真\n" + r"由 $\neg b\vee c$",
         "传播 $d=$ 假\n" + r"由 $\neg b\vee\neg d$",
         "全部子句为真 √\n$(a,b,c,d)=$（假, 真, 真, 假）"]
ys = [7.05, 5.05, 3.05, 1.05]
for x, rows, ls in [(3, left, "-"), (9, right, "--")]:
    for i, (y, text) in enumerate(zip(ys, rows)):
        box(x, y, text, h=1.05 if i < 3 else 1.25,
            lw=2.2 if i == 3 and x == 3 else 1.1,
            fill=C.LIGHT if i == 3 and x == 9 else C.PAPER, ls=ls)
        if i < 3:
            link((x, y-.56), (x, ys[i+1]+(.66 if i == 2 else .56)), ls)

# The successful assignment must satisfy every original clause.
a, b, c, d = False, True, True, False
assert all((not a or b, not b or c, not a or not c or d,
            not b or not d, a or b))
save(fig, "K16-n1")
