import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle

centers = {"S": (-0.55, 0.35), "P": (0.55, 0.35), "M": (0, -0.35)}
r = 0.9
coords = {(1, 1, 1): (0, 0.15), (1, 1, 0): (0, 0.78), (1, 0, 1): (-0.43, -0.18),
          (0, 1, 1): (0.43, -0.18), (1, 0, 0): (-1.03, 0.55), (0, 1, 0): (1.03, 0.55),
          (0, 0, 1): (0, -1.13)}

def draw(ax, shaded, title, note, cross, label_111=(0, 0.15)):
    x = np.linspace(-1.6, 1.6, 460); y = np.linspace(-1.55, 1.45, 400)
    X, Y = np.meshgrid(x, y)
    S = (X + 0.55) ** 2 + (Y - 0.35) ** 2 <= r ** 2
    P = (X - 0.55) ** 2 + (Y - 0.35) ** 2 <= r ** 2
    M = X ** 2 + (Y + 0.35) ** 2 <= r ** 2
    code = S.astype(int) + 2 * P.astype(int) + 4 * M.astype(int)
    mask = np.isin(code, [s + 2 * p + 4 * m for s, p, m in shaded])
    ax.contourf(X, Y, mask.astype(float), levels=[0.5, 1.5], colors=[C.LIGHT], alpha=0.95)
    for cx, cy in centers.values():
        ax.add_patch(Circle((cx, cy), r, fill=False, ec=C.INK, lw=1.35))
    for t, xy in [("S", (-1.12, 1.03)), ("P", (1.12, 1.03)), ("M", (0, -1.28))]:
        label(ax, t, xy, ha="center", va="center")
    for key, xy in coords.items():
        if key == (1, 1, 1):
            xy = label_111
        if key == (1, 0, 1) and cross != "inside":
            xy = (-0.55, -0.18)  # 右图 × 压在边界上，编号左移让开
        label(ax, str(key), xy, ha="center", va="center", fontsize=7.2)
    if cross == "inside":
        ax.plot(0, 0.15, marker="x", ms=15, mew=2.5, color=C.INK, zorder=5)
    else:
        xy = (-0.16, -0.20)
        ax.plot(*xy, marker="x", ms=15, mew=2.5, color=C.INK, zorder=5)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.35); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, pad=6, fontsize=9.5)
    label(ax, note, (0, -1.62), ha="center", va="top", fontsize=8)

fig, axes = new_fig(16, 9.5, ncols=2)
draw(axes[0], [(1, 0, 1), (0, 0, 1)], "例 7(1)：所有 M 是 P；有的 M 是 S",
     "× 落在 S、P 共有的部分：有的 S 是 P 成立", "inside", label_111=(0, 0.40))
draw(axes[1], [(0, 1, 0), (1, 1, 0)], "例 7(2)：所有 P 是 M；有的 S 是 M",
     "× 压在 P 的边界上：不知道在不在 P 里，推不出", "boundary")
save(fig, "Z3-n4")
