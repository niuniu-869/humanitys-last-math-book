import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle, FancyArrowPatch

fig, ax = new_fig(14, 12)
ax.set(xlim=(-2.5, 2.5), ylim=(-1.25, 3.7), aspect="equal")
ax.axis("off")
nodes = {"z": (0, 3.2), "u": (-1.5, 1.8), "v": (1.5, 1.8),
         "x": (-1.5, 0), "y": (1.5, 0)}
edges = [("z", "u"), ("z", "v"), ("u", "x"), ("u", "y"),
         ("v", "x"), ("v", "y")]
places = [(-1.02, 2.72), (1.02, 2.72), (-1.91, .92),
          (-.65, 1.68), (.65, 1.68), (1.91, .92)]
for (a, b), pos in zip(edges, places):
    thick = b != "y"
    p, q = np.array(nodes[a]), np.array(nodes[b])
    unit = (q-p) / np.linalg.norm(q-p)
    ax.add_patch(FancyArrowPatch(p+.20*unit, q-.20*unit,
                 arrowstyle="-|>", mutation_scale=12, color=C.INK,
                 lw=2.2 if thick else 1.0, ls="-" if thick else "--"))
    label(ax, rf"$\frac{{\partial {a}}}{{\partial {b}}}$", pos,
          ha="center", va="center", fontsize=14)
for name, pos in nodes.items():
    ax.add_patch(Circle(pos, .19, facecolor=C.PAPER, edgecolor=C.INK, lw=1.2, zorder=5))
    label(ax, f"${name}$", pos, ha="center", va="center", fontsize=14)
label(ax, r"粗实线：$z_x=\frac{\partial z}{\partial u}\frac{\partial u}{\partial x}"
      r"+\frac{\partial z}{\partial v}\frac{\partial v}{\partial x}$",
      (-2.32, -.62), va="center", fontsize=11)
label(ax, r"虚线：到 $y$ 的路径，写法相同", (-2.32, -1.08), va="center")
assert sum(a in ("u", "v") and b == "x" for a, b in edges) == 2
save(fig, "C21-n1")
