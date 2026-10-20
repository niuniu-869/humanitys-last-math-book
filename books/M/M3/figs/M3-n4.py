import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

H = np.array([[0.65, -0.1], [-0.1, 1.0]])
r = 1.5
centers = [np.array([2., 1.]), np.array([2.4, 0.5])]
# Circle KKT condition: H(c-w) = mu*w, with ||w|| = r.
lo, hi = 0., 10.
for _ in range(100):
    mu = (lo+hi)/2
    w = np.linalg.solve(H+mu*np.eye(2), H@centers[0])
    if np.linalg.norm(w) > r:
        lo = mu
    else:
        hi = mu
circle_contact = np.linalg.solve(H+hi*np.eye(2), H@centers[0])
diamond_contact = np.array([r, 0.])
assert np.isclose(np.linalg.norm(circle_contact), r)
assert np.all(np.abs(circle_contact) > 0.01)
normal = H@(centers[1]-diamond_contact)
assert normal[0] > abs(normal[1])  # Strictly inside the vertex normal cone.
eig, basis = np.linalg.eigh(H)
theta = np.linspace(0, 2*np.pi, 1201)
unit = np.array([np.cos(theta), np.sin(theta)])
fig, axes = new_fig(18, 9.6, ncols=2)
for i, (ax, c, contact) in enumerate(zip(axes, centers, [circle_contact, diamond_contact])):
    if i == 0:
        boundary = r*unit
    else:
        boundary = np.array([[r, 0, -r, 0, r], [0, r, 0, -r, 0]])
    ax.fill(*boundary, color=C.LIGHT, alpha=0.55, zorder=0)
    ax.plot(*boundary, color=C.INK, ls='--', lw=1.3)
    level = (contact-c)@H@(contact-c)
    for factor in (0.35, 1., 1.9):
        ellipse = c[:, None] + basis@(np.sqrt(level*factor/eig)[:, None]*unit)
        ax.plot(*ellipse, color=C.RED, ls='-', lw=1.1)
    ax.scatter(*c, marker='+', color=C.INK, s=46, zorder=5)
    label(ax, '无惩罚的解', c, offset=(-5, 50), ha='right', fontsize=8,
          arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6))
    dot(ax, contact, size=32)
    if i == 0:
        label(ax, '接触点', contact, offset=(-44, -25), fontsize=8,
              arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6))
    else:
        label(ax, '$w_2=0$', contact, offset=(9, -28), fontsize=9,
              arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=0.6))
    ax.set(xlim=(-3, 3), ylim=(-3, 3), xlabel='$w_1$', ylabel='$w_2$')
    ax.set_aspect('equal'); ax.set_xticks([-3, 0, 3]); ax.set_yticks([-3, 0, 3])
    ax.set_title('圆盘约束' if i == 0 else '菱形约束')
fig.tight_layout(w_pad=2)
save(fig, "M3-n4")
