import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 6.5)
X, Y = np.meshgrid(np.linspace(0.2, 5.8, 15), np.linspace(-0.1, 1.7, 10))
S = Y * (1 - Y)
L = 0.16
dx = L / np.sqrt(1 + S**2); dy = S * dx
field = []
for x0, y0, a, b in zip(X.ravel(), Y.ravel(), dx.ravel(), dy.ravel()):
    field.extend(ax.plot([x0 - a, x0 + a], [y0 - b, y0 + b], color=C.AMBER, lw=0.7, ls="-"))
x = np.linspace(0, 6, 300)
for y0, off in [(1.6, (8, 4)), (0.3, (8, 5)), (0.05, (8, -14))]:
    y = 1 / (1 + (1 / y0 - 1) * np.exp(-x))
    ax.plot(x, y, color=C.INK, lw=1.8)
    dot(ax, (0, y0), size=26)
label(ax, "$y_0=1.6$", (0, 1.6), offset=(8, 4))
label(ax, "$y_0=0.3$", (0.9, 1 / (1 + (1 / 0.3 - 1) * np.exp(-0.9))), offset=(-30, 10))
label(ax, "$y_0=0.05$", (2.0, 1 / (1 + 19 * np.exp(-2.0))), offset=(8, -16))
ax.plot([0, 6], [1, 1], color=C.INK, lw=1.6, ls="--")
label(ax, r"常数解 $y\equiv1$（虚线）", (3.9, 1), offset=(0, 16))
label(ax, "短线：斜率场；实线：解曲线", (3.0, 1.66), fontsize=8.5)
ax.set_xlim(0, 6); ax.set_ylim(-0.2, 1.8)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
# Leave clear space around labels without changing the field slopes.
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
boxes = [text.get_window_extent(renderer).expanded(1.08, 1.25) for text in ax.texts]
for line in field:
    path = line.get_path().transformed(line.get_transform())
    if any(path.intersects_bbox(box, filled=False) for box in boxes):
        line.remove()
assert np.isclose(1 / (1 + (1 / 0.3 - 1) * np.exp(-6)), 0.9942495043793638)
save(fig, "C17-n1")
