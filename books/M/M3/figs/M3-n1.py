import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

# Exact coefficients of the interpolant, before decimal rounding.
p = np.poly1d([5/24, -29/12, 235/24, -175/12, 9])
train = np.array([[1, 2], [2, 3], [3, 5], [4, 6], [5, 9]])
valid = np.array([[1.5, 2.4], [2.5, 4.3], [4.5, 7.4], [6, 10.6]])
assert np.allclose(p(train[:, 0]), train[:, 1])
assert np.isclose(p(6), 22)
fig, ax = new_fig(14, 10)
x = np.linspace(0, 7, 1401)
ax.plot(x, 1.7*x-0.1, color=C.INK, ls='-', label='直线')
ax.plot(x, p(x), color=C.RED, ls='--', label='四次多项式')
ax.scatter(*train.T, color=C.INK, s=32, zorder=5, label='训练')
ax.scatter(*valid.T, facecolor=C.PAPER, edgecolor=C.INK, s=38,
           zorder=5, label='验证')
exit_x = min(r.real for r in (p-12).r if abs(r.imag) < 1e-8 and r.real > 5)
label(ax, r'$x=6$ 处为 22', (exit_x, 11.98), offset=(-12, -12),
      ha='right', va='top', fontsize=9,
      arrowprops=dict(arrowstyle='->', color=C.INK, connectionstyle='arc3,rad=-0.15'))
ax.set(xlim=(0, 7), ylim=(0, 12), xlabel='$x$', ylabel='$y$')
ax.set_xticks(range(8)); ax.set_yticks(range(0, 13, 2))
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.02), ncol=4,
          fontsize=9, handlelength=2.2, columnspacing=1.1)
fig.tight_layout()
save(fig, "M3-n1")
