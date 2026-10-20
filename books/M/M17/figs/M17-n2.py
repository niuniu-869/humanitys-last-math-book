import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

beta = .1
a, b = np.sqrt((1-beta)*beta), np.sqrt(beta)
c = np.hypot(a, b)
assert np.isclose(c*c, 1-(1-beta)**2)
fig, ax = new_fig(15, 8.5)
ax.fill([0, a, a], [0, 0, b], color=C.LIGHT)
ax.plot([0, a, a], [0, 0, b], color=C.INK, ls='-')
ax.plot([0, a], [0, b], color=C.INK, ls='--')
s = .025
ax.plot([a-s, a-s, a], [0, s, s], color=C.INK, ls='-', lw=1)
label(ax, r'$\sqrt{\alpha_2\beta_1}=0.3$', (a/2, -.025), ha='center', va='top')
label(ax, rf'$\sqrt{{\beta_2}}={b:.4f}$', (a+.025, b/2), va='center')
label(ax, rf'$\sqrt{{1-\alpha_1\alpha_2}}={c:.4f}$', (a/2-.025, b/2+.035),
      ha='center', rotation=np.degrees(np.arctan2(b, a)), rotation_mode='anchor')
label(ax, r'方差：$0.09+0.10=0.19$', (.23, -.10), ha='center', va='center')
ax.set(xlim=(-.12, .66), ylim=(-.13, .39), aspect='equal')
ax.axis('off')
fig.subplots_adjust(left=.03, right=.97, bottom=.03, top=.97)
save(fig, "M17-n2")
