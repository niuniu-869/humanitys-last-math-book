import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path
from itertools import permutations

valid = [p for p in permutations("甲乙丙丁戊") if p[2] == "戊"
         and abs(p.index("甲") - p.index("乙")) == 1
         and abs(p.index("丙") - p.index("丁")) == 1
         and p.index("甲") < p.index("丙")
         and p.index("乙") < p.index("甲") and p.index("丙") < p.index("丁")]
assert valid == [tuple("乙甲戊丙丁")]
fig, ax = new_fig(15, 7)
ax.set(xlim=(-.3, 5.3), ylim=(-.85, 2.8))
ax.axis("off")
for i, person in enumerate(valid[0]):
    ax.add_patch(Rectangle((i, 0), 1, .85, facecolor=C.LIGHT if i == 2 else C.PAPER,
                           edgecolor=C.INK, lw=1.2))
    ax.text(i + .5, .43, person, ha="center", va="center", fontsize=17, color=C.INK)
    label(ax, str(i + 1), (i + .5, -.28), ha="center", va="center")

def brace(left, right):
    middle = (left + right) / 2
    vertices = [(left, 1.04), (left, 1.22), (middle-.15, 1.1), (middle, 1.32),
                (middle+.15, 1.1), (right, 1.22), (right, 1.04)]
    ax.add_patch(PathPatch(Path(vertices, [Path.MOVETO] + [Path.CURVE4]*6),
                           fill=False, edgecolor=C.INK, lw=1.1))
brace(.05, 1.95)
brace(3.05, 4.95)
label(ax, "甲乙（相邻）", (1, 1.57), ha="center")
label(ax, "丙丁（相邻）", (4, 1.57), ha="center")
label(ax, "甲在丙的左边 ⇒ 甲乙在左", (2.5, 2.32), ha="center")
label(ax, "乙在甲的左边", (1, -.73), ha="center", fontsize=9)
label(ax, "丙在丁的左边", (4, -.73), ha="center", fontsize=9)
save(fig, "K13-n3")
