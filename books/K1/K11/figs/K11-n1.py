import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig3d(14, 10, elev=24, azim=-58)

# Coordinates are exactly the binary assignments (p, q, r).
vertices = {(p, q, r): np.array([p, q, r], dtype=float)
            for p in (0, 1) for q in (0, 1) for r in (0, 1)}
edges = []
for v in vertices:
    for k in range(3):
        w = list(v)
        w[k] = 1 - w[k]
        w = tuple(w)
        if v[k] == 0:
            edges.append((v, w))

# Dashed edges are the three hidden back edges in this viewing direction.
hidden = {((0, 0, 1), (0, 1, 1)), ((0, 0, 1), (1, 0, 1)),
          ((0, 1, 1), (1, 1, 1))}
for u, v in edges:
    key = (u, v) if (u, v) in hidden else (v, u)
    ax.plot([vertices[u][0], vertices[v][0]],
            [vertices[u][1], vertices[v][1]],
            [vertices[u][2], vertices[v][2]],
            color=C.INK, ls='--' if key in hidden else '-', lw=1.3,
            zorder=1)

true_vertices = {(0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)}
for v, xyz in vertices.items():
    face = C.INK if v in true_vertices else C.PAPER
    ax.scatter([xyz[0]], [xyz[1]], [xyz[2]], s=45, facecolors=face,
               edgecolors=C.INK, linewidths=1.0, depthshade=False, zorder=5)
    bits = ''.join(map(str, v))
    row = v[0] * 4 + v[1] * 2 + v[2]
    ax.text(xyz[0] + 0.04, xyz[1] + 0.04, xyz[2] + 0.04,
            rf'${bits}\,({row})$', color=C.INK, fontsize=8, zorder=6)

ax.text2D(0.02, 0.97, r'实心：$h=1$，对应 $m_3,m_5,m_6,m_7$',
          transform=ax.transAxes, va='top', ha='left', fontsize=9, color=C.INK)
ax.text2D(0.02, 0.92, r'空心：$h=0$，对应 $M_0,M_1,M_2,M_4$',
          transform=ax.transAxes, va='top', ha='left', fontsize=9, color=C.INK)
ax.set(xlim=(-0.25, 1.35), ylim=(-0.25, 1.35), zlim=(-0.25, 1.35))
ax.set_xlabel('$p$', labelpad=2); ax.set_ylabel('$q$', labelpad=2); ax.set_zlabel('$r$', labelpad=2)
ax.set_xticks([0, 1]); ax.set_yticks([0, 1]); ax.set_zticks([0, 1])
save(fig, 'K11-n1')
