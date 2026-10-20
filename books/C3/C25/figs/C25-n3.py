import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(17, 9, ncols=2)
t = np.linspace(0, 1, 301)
for ax in axes:
    ax.fill_between(t, t*t, t, color=C.LIGHT)
    ax.plot(t, t, color=C.INK, ls='-')
    ax.plot(t, t*t, color=C.INK, ls='--')
    dot(ax, (0, 0), '$(0,0)$', offset=(5, -16))
    dot(ax, (1, 1), '$(1,1)$', offset=(-6, 8))
    ax.set(xlim=(-.12, 1.22), ylim=(-.12, 1.22), aspect='equal')
    ax.set_xticks([]); ax.set_yticks([])
    ax.spines[['left', 'bottom']].set_position('zero')
    label(ax, '$x$', (1.19, 0), (0, -13))
    label(ax, '$y$', (0, 1.18), (-14, 0))
ax = axes[0]
s = .60
ax.annotate('', (s, .91), (s, .10), arrowprops=dict(arrowstyle='->', linestyle='--', color=C.INK))
dot(ax, (s, s*s))
ax.scatter([s], [s], facecolor=C.PAPER, edgecolor=C.INK, s=28, zorder=5)
ax.text(.5, -.15, '进入：$y=x^2$\n离开：$y=x$\n' + r'$0\leq x\leq1$', transform=ax.transAxes, ha='center', va='top', linespacing=1.5)
ax = axes[1]
s = .40
ax.annotate('', (.94, s), (.12, s), arrowprops=dict(arrowstyle='->', linestyle='--', color=C.INK))
dot(ax, (s, s))
ax.scatter([np.sqrt(s)], [s], facecolor=C.PAPER, edgecolor=C.INK, s=28, zorder=5)
ax.text(.5, -.15, '进入：$x=y$\n' + r'离开：$x=\sqrt{y}$' + '\n' + r'$0\leq y\leq1$', transform=ax.transAxes, ha='center', va='top', linespacing=1.5)
fig.subplots_adjust(bottom=.30, wspace=.3)
save(fig, "C25-n3")
