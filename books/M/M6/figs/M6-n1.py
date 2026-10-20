import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(17, 12)
points = np.array([[3., 3.], [4., 3.], [1., 1.]])
targets = np.array([1, 1, -1])
xx = np.linspace(0, 5.5, 500)
lines = [(np.array([1., 1.]), 4, '-', 2.2,
          r'$x_1+x_2=4$：间隔 $\sqrt{2}$'),
         (np.array([1., 0.]), 2, '--', 1.5,
          r'$x_1=2$：间隔 $1$'),
         (np.array([0., 1.]), 2, ':', 1.5,
          r'$x_2=2$：间隔 $1$'),
         (np.array([1., 3.]), 6, '-.', 1.5,
          r'$x_1+3x_2=6$：间隔 $0.63$')]
for normal, intercept, style, width, text in lines:
    assert np.all(targets * (points @ normal - intercept) > 0)
    if normal[1] == 0:
        ax.axvline(intercept, color=C.INK, ls=style, lw=width, label=text)
    else:
        ax.plot(xx, (intercept-normal[0]*xx)/normal[1],
                color=C.INK, ls=style, lw=width, label=text)
assert np.isclose(np.min(np.abs(points @ lines[3][0]-6))/np.sqrt(10), 2/np.sqrt(10))
for i in [0, 2]:
    p = points[i]
    foot = p - (p.sum()-4)/2 * np.ones(2)
    assert np.allclose(foot, [2, 2])
    assert np.isclose(np.linalg.norm(p-foot), np.sqrt(2))
    ax.plot([p[0], foot[0]], [p[1], foot[1]], color=C.GRAY, lw=1, ls='-')
label(ax, r'$\sqrt{2}$', (2.55, 2.55), (8, -12))
label(ax, r'$\sqrt{2}$', (1.35, 0.55))
for i, p in enumerate(points):
    ax.scatter(*p, s=48, facecolors=C.INK if i < 2 else C.PAPER,
               edgecolors=C.INK, zorder=5)
    label(ax, rf'$\boldsymbol{{x}}_{i+1}$', p, (8, 8) if i < 2 else (-15, -14))
ax.set(xlim=(0, 5.5), ylim=(0, 5), xlabel=r'$x_1$', ylabel=r'$x_2$')
ax.set_aspect('equal', adjustable='box')
ax.legend(loc='lower left', bbox_to_anchor=(0, 1.02), ncol=2, fontsize=9,
          borderaxespad=0, handlelength=3)
fig.tight_layout()
save(fig, "M6-n1")
