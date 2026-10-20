import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

S = np.array([[2.5, 4.25], [4.25, 7.5]])
values, vectors = np.linalg.eigh(S)
angles = np.degrees(np.arctan2(vectors[1], vectors[0])) % 180
theta = np.linspace(0, 180, 721)
radians = np.deg2rad(theta)
f = 5 - 2.5 * np.cos(2 * radians) + 4.25 * np.sin(2 * radians)
w = np.column_stack([np.cos(radians), np.sin(radians)])
assert np.allclose(f, np.einsum('ni,ij,nj->n', w, S, w))
fig, ax = new_fig(14, 9)
ax.plot(theta, f, color=C.INK, ls='-')
ax.axhline(5, color=C.GRAY, ls='--', lw=1.2)
label(ax, '均值 5', (175, 5), offset=(0, 6), ha='right', fontsize=9)
for angle, value, offset in zip(angles, values, [(0, 30), (0, 12)]):
    dot(ax, (angle, value))
    label(ax, f'({angle:.1f}°, {value:.2f})', (angle, value), offset=offset,
          ha='center', fontsize=9)
ax.scatter([0, 90], [2.5, 7.5], facecolors=C.PAPER, edgecolors=C.INK,
           s=35, zorder=5, clip_on=False)
label(ax, '2.5', (0, 2.5), offset=(9, -4), fontsize=9)
label(ax, '7.5', (90, 7.5), offset=(9, 3), fontsize=9)
ax.set(xlim=(0, 180), ylim=(0, 11), xlabel=r'$\theta$', ylabel=r'$w^{\mathsf{T}} S w$')
ax.set_xticks([0, 30, 60, 90, 120, 150, 180], [f'{t}°' for t in [0, 30, 60, 90, 120, 150, 180]])
fig.tight_layout()
save(fig, "M5-n2")
