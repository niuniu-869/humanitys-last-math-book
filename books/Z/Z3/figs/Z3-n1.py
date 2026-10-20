import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle


def region_fill(ax, kind):
    x = np.linspace(-1.5, 1.5, 420)
    y = np.linspace(-1.15, 1.15, 320)
    X, Y = np.meshgrid(x, y)
    S = (X + 0.45) ** 2 + Y ** 2 <= 0.8 ** 2
    P = (X - 0.45) ** 2 + Y ** 2 <= 0.8 ** 2
    if kind == "A":
        mask = S & ~P
    elif kind == "E":
        mask = S & P
    elif kind == "I":
        mask = np.zeros_like(S, dtype=bool)
    else:
        mask = np.zeros_like(S, dtype=bool)
    if mask.any():
        ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5], colors=[C.LIGHT], alpha=0.95)
    for cx, name in [(-0.45, "S"), (0.45, "P")]:
        ax.add_patch(Circle((cx, 0), 0.8, fill=False, ec=C.INK, lw=1.5))
        label(ax, name, (cx, 0.8), offset=(0, 3), ha="center", va="bottom")
    coords = {"①": (-0.72, 0.0), "②": (0, 0.0), "③": (0.72, 0.0), "④": (0, -0.98)}
    for t, xy in coords.items():
        label(ax, t, xy, ha="center", va="center", fontsize=8)
    if kind == "I":
        ax.plot(0, 0, marker="x", ms=14, mew=2.3, color=C.INK, zorder=5)
    if kind == "O":
        ax.plot(-1.0, 0, marker="x", ms=14, mew=2.3, color=C.INK, zorder=5)
    ax.set_xlim(-1.45, 1.45); ax.set_ylim(-1.12, 1.12)
    ax.set_aspect("equal"); ax.axis("off")


fig, axes = new_fig(16, 11, nrows=2, ncols=2)
items = [("A：所有 S 是 P", "A"), ("E：所有 S 不是 P", "E"),
         ("I：有的 S 是 P", "I"), ("O：有的 S 不是 P", "O")]
for ax, (title, kind) in zip(axes.flat, items):
    region_fill(ax, kind)
    ax.set_title(title, pad=7)
    label(ax, "阴影：这一块没有对象；×：这一块至少有一个对象", (0, -1.32),
          ha="center", va="top", fontsize=8)
save(fig, "Z3-n1")
