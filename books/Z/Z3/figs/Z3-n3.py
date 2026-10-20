import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Circle


centers = {"S": (-0.55, 0.35), "P": (0.55, 0.35), "M": (0, -0.35)}
r = 0.9
coords = {(1, 1, 1): (0, 0.15), (1, 1, 0): (0, 0.78), (1, 0, 1): (-0.43, -0.18),
          (0, 1, 1): (0.43, -0.18), (1, 0, 0): (-1.03, 0.55), (0, 1, 0): (1.03, 0.55),
          (0, 0, 1): (0, -1.13), (0, 0, 0): (1.15, -1.13)}

def draw(ax, shaded, title, note, dashed=None):
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
    label(ax, "S", (-1.12, 1.03), ha="center", va="center")
    label(ax, "P", (1.12, 1.03), ha="center", va="center")
    label(ax, "M", (0, -1.28), ha="center", va="center")
    for key, xy in coords.items():
        label(ax, str(key), xy, ha="center", va="center", fontsize=7.2)
    if dashed:
        dmask = code == (dashed[0] + 2 * dashed[1] + 4 * dashed[2])
        ax.contour(X, Y, dmask.astype(float), levels=[0.5], colors=C.INK, linestyles="--", linewidths=1.8)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.45, 1.35); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, pad=6, fontsize=9.5)
    label(ax, note, (0, -1.62), ha="center", va="top", fontsize=8)

fig, axes = new_fig(16, 9.5, ncols=2)
draw(axes[0], [(1, 0, 1), (0, 0, 1), (1, 1, 0), (1, 0, 0)],
     "例 6(1)：所有 M 是 P；所有 S 是 M", "结论要求 (1,0,1)、(1,0,0) 空：已涂 ✓ 有效")
draw(axes[1], [(0, 1, 0), (1, 1, 0), (1, 0, 0)],
     "例 6(2)：所有 P 是 M；所有 S 是 M", "结论要求 (1,0,1) 空：没涂 ✗ 无效", dashed=(1, 0, 1))
save(fig, "Z3-n3")
