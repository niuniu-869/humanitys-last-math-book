import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(9, 8)
xlim = (0.5, 4.0); ylim = (-0.5, 3.0)
x = np.linspace(xlim[0], xlim[1], 900)
ax.plot(x, 1 / x, color=C.INK, lw=2.0, ls="-")
ax.plot(x, -x / 4 + 1, color=C.INK, lw=1.1, ls="-")
ax.plot(x, 4 * x - 7.5, color=C.GRAY, lw=1.1, ls="--")
T = (2.0, 0.5)
dot(ax, T, color=C.INK, size=30)
label(ax, r"$(2,\frac{1}{2})$", T, offset=(-51, -24))
label(ax, "法线", (2.7, 2.3), offset=(6, 0))
label(ax, "切线", (3.2, 0.0), offset=(0, -15))

# A small right-angle marker using unit tangent and normal directions.
u = np.array([1.0, -0.25]); u /= np.linalg.norm(u)
v = np.array([1.0, 4.0]); v /= np.linalg.norm(v)
s = 0.16
assert np.isclose(u @ v, 0)
assert np.isclose(4 * T[0] - 7.5, T[1])
a = np.array(T) + s * u
b = a + s * v
c = np.array(T) + s * v
ax.plot([a[0], b[0], c[0]], [a[1], b[1], c[1]], color=C.INK, lw=1.0, ls="-")

ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal", adjustable="box")
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
ax.set_xticks([0.5, 1, 2, 3, 4]); ax.set_yticks([-0.5, 0, 0.5, 1, 2, 3])
save(fig, "C4-n2")
