import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

def leaf_count(k):
    return 1 if k < 2 else leaf_count(k-1) + leaf_count(k-2)

def make_tree(k, x0, x1, depth=0, side=None):
    x = (x0 + x1) / 2
    node = {"k": k, "x": x, "y": -depth, "children": [], "side": side}
    if k >= 2:
        split = x0 + (x1-x0)*leaf_count(k-1)/leaf_count(k)
        node["children"] = [make_tree(k - 1, x0, split, depth+1, "L"),
                             make_tree(k - 2, split, x1, depth+1, "R")]
    return node

def collect(n, out):
    out.append(n)
    for c in n["children"]:
        collect(c, out)

root = make_tree(5, 0, 8)
nodes = []
collect(root, nodes)
assert len(nodes) == 15
counts = {k: sum(n["k"] == k for n in nodes) for k in range(6)}
assert counts == {0: 3, 1: 5, 2: 3, 3: 2, 4: 1, 5: 1}

fig, ax = new_fig(18, 11)
for n in nodes:
    for c in n["children"]:
        ax.plot([n["x"], c["x"]], [n["y"], c["y"]], color=C.INK, lw=1.0, zorder=1)
for n in nodes:
    fill = C.LIGHT if n["k"] == 2 else C.PAPER
    ax.add_patch(Circle((n["x"], n["y"]), .39, facecolor=fill,
                        edgecolor=C.INK, linewidth=1.1, zorder=3))
    label(ax, f"Fib({n['k']})", (n["x"], n["y"]), ha="center", va="center", fontsize=8)
fib3_nodes = [n for n in nodes if n["k"] == 3]
for n in fib3_nodes:
    sub = []
    collect(n, sub)
    xs = [q["x"] for q in sub]
    ys = [q["y"] for q in sub]
    ax.add_patch(Rectangle((min(xs)-.50, min(ys)-.50), max(xs)-min(xs)+1.0,
                           max(ys)-min(ys)+1.0, fill=False, edgecolor=C.INK,
                           lw=1.1, ls="--", zorder=2))
label(ax, "相同的子树", (6.5, -3.75), ha="center", va="center", fontsize=9)
label(ax, "相同的子树", (1.0, -1.25), ha="center", va="center", fontsize=9)
ax.set(xlim=(-.25, 8.3), ylim=(-4.7, .7), aspect="equal")
ax.axis("off")
save(fig, "K34-n1")
