import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(18, 11)
fig.subplots_adjust(left=0.03, right=0.98, bottom=0.05, top=0.98)
ax.set(xlim=(-0.35, 5.9), ylim=(-2.45, 2.45))
ax.axis("off")
positions = {"root": (0, 0), "a": (2, 1.1), "b": (2, -1.1),
             "c": (4, 1.85), "d": (4, 0.5), "e": (4, -0.5), "f": (4, -1.85)}
edges = [("root", "a", 0.6, "-", 2.5), ("root", "b", 0.4, "--", 2.5),
         ("a", "c", 0.5, "-", 2.5), ("a", "d", 0.5, "-", 0.9),
         ("b", "e", 0.9, "--", 2.5), ("b", "f", 0.1, "-", 0.9)]
for parent, child, probability, style, width in edges:
    start, end = np.array(positions[parent]), np.array(positions[child])
    ax.plot([start[0], end[0]], [start[1], end[1]], color=C.INK, ls=style, lw=width)
    midpoint = (start+end)/2
    label(ax, f"{probability:.1f}", midpoint, offset=(0, 11 if end[1] > start[1] else -15), ha="center")
for node, xy in positions.items():
    if node == "e":
        dot(ax, xy, size=40)
    else:
        ax.scatter(*xy, s=40, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
    if node in ("a", "b"):
        label(ax, f"${node}$", xy, offset=(0, 12), ha="center")
    elif node != "root":
        label(ax, f"${node}$", xy, offset=(-2, 11), ha="center")
leaf_data = [("c", "ac", 0.6*0.5, "贪心"), ("d", "ad", 0.6*0.5, ""),
             ("e", "be", 0.4*0.9, "最大"), ("f", "bf", 0.4*0.1, "")]
for node, word, value, note in leaf_data:
    x, y = positions[node]
    label(ax, f"${word}$  {note + ' ' if note else ''}{value:.2f}", (x+0.25, y), va="center")
assert np.isclose(sum(item[2] for item in leaf_data), 1)
assert max(leaf_data, key=lambda item: item[2])[1] == "be"
label(ax, "粗实线：贪心路径    粗虚线：整句最优路径", (2.75, -2.35), ha="center", fontsize=9)
save(fig, "M14-n4")
