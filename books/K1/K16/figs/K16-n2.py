import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch

fig, ax = new_fig(18, 12)
fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
ax.set(xlim=(-.6, 12.7), ylim=(.3, 9.2), aspect="equal")
ax.axis("off")
pos = {"p": (0, 4.2), "a": (0, 3), "s": (0, 8.5), "d": (0, 1.2),
       "R1": (2, 3.6), "c": (3.8, 3.6), "R2": (6, 7.1), "f": (8, 7.1),
       "R3": (6, 2.3), "m": (8, 2.3), "R4": (10, 3.6), "g": (12, 3.6),
       "e": (6, 6), "R5": (6, 4.9), "r": (8, 4.9)}
heavy = {"p", "a", "s", "d", "c", "m", "g", "R1", "R3", "R4"}
patches = {}
for name, (x, y) in pos.items():
    style = dict(facecolor=C.LIGHT if name in heavy else C.PAPER,
                 edgecolor=C.INK, lw=2 if name in heavy else 1.1,
                 ls="--" if name in {"e", "R5", "r"} else "-", zorder=3)
    patch = (Rectangle((x-.42, y-.36), .84, .72, **style) if name.startswith("R")
             else Circle((x, y), .31, **style))
    ax.add_patch(patch)
    patches[name] = patch
    label(ax, name if name.startswith("R") else f"${name}$", (x, y),
          ha="center", va="center", fontsize=10)

edges = [("p", "R1"), ("a", "R1"), ("R1", "c"),
         ("c", "R2"), ("s", "R2"), ("R2", "f"),
         ("c", "R3"), ("d", "R3"), ("R3", "m"),
         ("m", "R4"), ("s", "R4"), ("R4", "g"),
         ("e", "R5"), ("c", "R5"), ("R5", "r")]
for source, target in edges:
    bold = source in heavy and target in heavy
    if (source, target) == ("s", "R4"):
        # Route above all other nodes, then descend into R4.
        ax.plot([.31, 10, 10], [8.5, 8.5, 4.15], color=C.INK, lw=2.2, ls="-")
        arrow(ax, (10, 4.15), (0, -.19), color=C.INK, lw=2.2)
        continue
    if (source, target) == ("c", "R2"):
        ax.plot([3.8, 4.5, 4.5, 5.35], [3.91, 4.6, 7.1, 7.1],
                color=C.INK, lw=1.1, ls="-")
        arrow(ax, (5.35, 7.1), (.23, 0), color=C.INK, lw=1.1)
        continue
    ax.add_patch(FancyArrowPatch(pos[source], pos[target],
        patchA=patches[source], patchB=patches[target], shrinkA=2, shrinkB=2,
        arrowstyle="-|>", mutation_scale=11, color=C.INK,
        lw=2.2 if bold else 1.1, ls="--" if source in {"e", "R5"} else "-",
        zorder=2))
label(ax, "不是事实", (6.5, 6), va="center", fontsize=9)
label(ax, "粗线：查询 $g$ 的依赖", (9.3, .65), ha="center", fontsize=9)
assert len([name for name in pos if not name.startswith("R")]) == 10
assert ("R2", "g") not in edges and "f" not in heavy
save(fig, "K16-n2")
