import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

from matplotlib.patches import Rectangle

fig, ax = new_fig(16, 9)
f = lambda x: 1 + 0.6*np.sin(1.3*x)
edges = np.linspace(0, 4, 9)
# Include every stationary point, so upper/lower sums are not sampling estimates.
critical = (np.pi/2 + np.arange(2)*np.pi)/1.3
lower, upper = [], []
for a, b in zip(edges[:-1], edges[1:]):
    candidates = np.r_[a, b, critical[(critical > a) & (critical < b)]]
    m, M = np.min(f(candidates)), np.max(f(candidates))
    lower.append(m)
    upper.append(M)
    ax.add_patch(Rectangle((a, 0), b-a, m, facecolor=C.LIGHT,
                           edgecolor=C.INK, lw=0.8, ls='-'))
    ax.add_patch(Rectangle((a, m), b-a, M-m, facecolor=C.PAPER,
                           edgecolor=C.INK, hatch='///', lw=0.8, ls='--'))
    assert np.all(f(np.linspace(a, b, 501)) >= m-1e-12)
    assert np.all(f(np.linspace(a, b, 501)) <= M+1e-12)
x = np.linspace(0, 4, 801)
ax.plot(x, f(x), color=C.INK, lw=2.1, ls='-')
ax.set(xlim=(0, 4.2), ylim=(0, 2.1), xlabel='$x$', ylabel='$y$')
ax.set_xticks([0, 0.5, 1, 2, 3, 4])
ax.set_yticks([0, 0.5, 1.5, 2])
label(ax, '$m_i$', (0, lower[0]), offset=(-12, 0), ha='right', va='center')
label(ax, '$M_i$', (0, upper[0]), offset=(-12, 0), ha='right', va='center')
ax.annotate('', xy=(0.5, -0.23), xytext=(0, -0.23), annotation_clip=False,
            arrowprops=dict(arrowstyle='<->', color=C.INK, lw=0.9))
label(ax, r'$\Delta x_i$', (0.25, -0.23), offset=(0, -7), ha='center', va='top', annotation_clip=False)
label(ax, r'$(M_i-m_i)\Delta x_i$', (0.23, 1.22), offset=(44, 65),
      arrowprops=dict(arrowstyle='-', color=C.INK, lw=0.8))
label(ax, r'$y=1+0.6\sin(1.3x)$', (2.4, 1.7))
integral = 4 + 0.6/1.3*(1-np.cos(5.2))
assert np.dot(lower, np.diff(edges)) < integral < np.dot(upper, np.diff(edges))
assert np.isclose(max(upper), 1.6) and np.isclose(min(lower), 0.4)
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.25, top=0.95)
save(fig, "C9-n6")
