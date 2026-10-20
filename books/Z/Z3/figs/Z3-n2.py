import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyBboxPatch


fig, ax = new_fig(16, 10)
ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.1, 3.1); ax.axis("off")
pts = {"A": (-2.2, 1.7), "E": (2.2, 1.7), "I": (-2.2, -1.7), "O": (2.2, -1.7)}
txt = {"A": "A\n所有 S 是 P", "E": "E\n所有 S 不是 P", "I": "I\n有的 S 是 P", "O": "O\n有的 S 不是 P"}
for k, (x, y) in pts.items():
    ax.add_patch(FancyBboxPatch((x - 0.92, y - 0.46), 1.84, 0.92,
                                boxstyle="round,pad=0.06,rounding_size=0.12",
                                fc=C.PAPER, ec=C.INK, lw=1.4))
    label(ax, txt[k], (x, y), ha="center", va="center", linespacing=1.3)

def seg(a, b, ls="-", lw=1.6, z=1):
    if {a, b} == {"A", "O"}:
        p, q = (-1.35, 1.35), (1.35, -1.35)
    elif {a, b} == {"E", "I"}:
        p, q = (1.35, 1.35), (-1.35, -1.35)
    elif {a, b} == {"A", "E"}:
        p, q = (-1.28, 1.7), (1.28, 1.7)
    else:
        p, q = (-1.28, -1.7), (1.28, -1.7)
    if a in ("E", "O") and b in ("I", "A"):
        p, q = q, p
    ax.plot([p[0], q[0]], [p[1], q[1]], ls=ls, lw=lw, color=C.INK, zorder=z)

seg("A", "O", lw=2.1); seg("E", "I", lw=2.1)
seg("A", "E"); seg("I", "O", ls="--")
arrow(ax, (-2.2, 1.22), (0, -1.9), color=C.INK, lw=1.5)
arrow(ax, (2.2, 1.22), (0, -1.9), color=C.INK, lw=1.5)
label(ax, "矛盾：一真一假", (0, 0), offset=(0, 7), ha="center", va="bottom")
label(ax, "反对：不能同真，可以同假", (0, 2.35), ha="center", va="bottom")
label(ax, "下反对：不能同假，可以同真", (0, -2.35), ha="center", va="top")
label(ax, "从属", (-2.2, 0), offset=(-18, 0), ha="right", va="center", rotation=90)
label(ax, "从属", (2.2, 0), offset=(18, 0), ha="left", va="center", rotation=90)
label(ax, "A 真则 I 真；E 真则 O 真", (0, -2.75), ha="center", va="top", fontsize=8)
label(ax, "反对、下反对、从属都要求 S 非空", (0, -3.0), ha="center", va="top", fontsize=8)
save(fig, "Z3-n2")
