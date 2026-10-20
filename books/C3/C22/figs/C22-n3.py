import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 14)
theta = np.linspace(0, 2*np.pi, 721)
for level in [4, 8, 12]:
    ax.plot(np.sqrt(level)*np.cos(theta), np.sqrt(level)/2*np.sin(theta),
            color=C.INK, lw=1.3, ls="-")
    a = 0.0
    anchor = (np.sqrt(level)*np.cos(a), np.sqrt(level)/2*np.sin(a))
    label(ax, f"$f={level}$", anchor, offset=(7, 6), ha="left", fontsize=9)

points = np.array([[2., 1.], [0., np.sqrt(3)], [-2., 0.],
                   [-1.5, np.sqrt((8-2.25)/4)]])
gradients = points * np.array([2., 8.])
assert np.allclose(points[:, 0]**2 + 4*points[:, 1]**2, [8, 12, 4, 8])
assert np.allclose(gradients[:3], [[4, 8], [0, 8*np.sqrt(3)], [-4, 0]])
for point, gradient in zip(points, gradients):
    arrow(ax, point, 0.25*gradient, color=C.INK, lw=2.0)
    dot(ax, point, size=23)

p = points[0]
tangent = np.array([2., -1.]) / np.sqrt(5)
normal = gradients[0] / np.linalg.norm(gradients[0])
ends = p + np.array([[-0.75], [0.75]])*tangent
assert np.allclose(ends[:, 0] + 2*ends[:, 1], 4)
assert np.isclose(tangent @ gradients[0], 0)
ax.plot(ends[:, 0], ends[:, 1], color=C.INK, lw=1.2, ls="--")
corner = np.array([p + 0.19*tangent, p + 0.19*(tangent+normal), p + 0.19*normal])
ax.plot(corner[:, 0], corner[:, 1], color=C.INK, lw=0.9, ls="-")
label(ax, "$(2,1)$", (1.5, 0.91), ha="center", fontsize=9)
label(ax, r"箭头 $=0.25\nabla f$", (1.0, 4.9), fontsize=10)

# The specified 0.25 scaling puts the highest tip at y=3*sqrt(3).
# Extend y only, retaining equal units and all exact vector lengths.
ax.set(xlim=(-4.5, 4.5), ylim=(-2.5, 5.6), aspect="equal")
ax.set_xticks([-4, -2, 0, 2, 4])
ax.set_yticks([-2, 0, 2, 4])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", rotation=0, loc="top")
tips = points + 0.25*gradients
assert np.all((tips[:, 0] > -4.5) & (tips[:, 0] < 4.5))
assert np.all((tips[:, 1] > -2.5) & (tips[:, 1] < 5.6))
fig.subplots_adjust(left=0.10, right=0.98, bottom=0.10, top=0.98)
save(fig, "C22-n3")
