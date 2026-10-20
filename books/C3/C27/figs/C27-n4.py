import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10, 6.5)
a = 2.
theta = np.linspace(0, np.pi, 501)
x, y = a/2*(1+np.cos(theta)), a/2*np.sin(theta)
assert np.allclose(x*x+y*y, a*x)
ax.fill(x, y, color=C.LIGHT, lw=0)
ax.plot(x, y, color=C.INK, ls="-", lw=1.7)
for t in (0.7, 2.1):
    start = np.array([1+np.cos(t), np.sin(t)])
    end = np.array([1+np.cos(t+0.18), np.sin(t+0.18)])
    arrow(ax, start, end-start, color=C.INK)
ax.plot([0, a], [0, 0], color=C.INK, ls="--", lw=1.5)
ax.annotate("", xy=(1.3, 0), xytext=(0.8, 0), arrowprops=dict(
    arrowstyle="-|>", color=C.INK, lw=1.5, ls="--",
    shrinkA=0, shrinkB=0, mutation_scale=12))
dot(ax, (0, 0), "$O$", offset=(-12, -15))
dot(ax, (a, 0), "$A(2,0)$", offset=(3, -15))
label(ax, "$L$", (1.5, np.sqrt(3)/2), offset=(8, 10))
label(ax, "$D$", (1, 0.43), ha="center", fontsize=13)
label(ax, "补线", (1, 0), offset=(0, -19), ha="center")
ax.set_aspect("equal")
ax.set_xlim(-0.3, 2.55)
ax.set_ylim(-0.45, 1.3)
ax.axis("off")
save(fig, "C27-n4")
