import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import FancyArrowPatch, Circle

fig, ax = new_fig(12.5, 8.5)
fig.subplots_adjust(left=0.04, right=0.96, bottom=0.04, top=0.94)
ax.set_aspect("equal", adjustable="box")
ax.set_xlim(-2.25, 2.25)
ax.set_ylim(-2.25, 2.25)
ax.axis("off")

nodes = {"1": np.array([-1.15, 0.92]), "2": np.array([1.15, 0.92]), "3": np.array([0.0, -1.05])}
r = 0.34
for k, p in nodes.items():
    ax.add_patch(Circle(tuple(p), r, facecolor=C.PAPER, edgecolor=C.INK, lw=1.5, zorder=3))
    label(ax, k, p, offset=(0, -1), color=C.INK, ha="center", va="center", fontsize=12)

# straight arrow helper with endpoints trimmed around node circles
def link(a, b, text, offset=(0, 0), rad=0.0):
    pa, pb = nodes[a], nodes[b]
    v = pb - pa
    u = v / np.linalg.norm(v)
    start = pa + r * u
    end = pb - r * u
    patch = FancyArrowPatch(tuple(start), tuple(end), arrowstyle="-|>", mutation_scale=14,
                            connectionstyle=f"arc3,rad={rad}", color=C.INK, lw=1.55,
                            shrinkA=0, shrinkB=0, zorder=2)
    ax.add_patch(patch)
    mid = (start + end) / 2
    label(ax, text, mid, offset=offset, color=C.INK, ha="center", va="center")

link("1", "2", r"$\frac{1}{2}$", offset=(0, 12))
link("1", "3", r"$\frac{1}{2}$", offset=(-18, 0), rad=0.18)
link("2", "3", "1", offset=(18, 0), rad=-0.18)
link("3", "1", "1", offset=(18, 1), rad=0.18)

save(fig, "L11-n3")
