import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 13)
theta = np.linspace(0, 2*np.pi, 500)
cov = np.array([[36, 18], [18, 36]])
values, vectors = np.linalg.eigh(cov)
circle = np.array([np.cos(theta), np.sin(theta)])
for radius in [.75, 1.5, 2.25]:
    ellipse = 170 + radius * (vectors @ np.diag(np.sqrt(values)) @ circle)
    ax.plot(*ellipse, color=C.AMBER, ls='-', lw=.8)
xx = np.linspace(155, 185, 300)
ax.plot(xx, xx, color=C.INK, ls=':', lw=1.3, label='$y=x$')
ax.plot(xx, 170+.5*(xx-170), color=C.INK, ls='-', label='$y=170+0.5(x-170)$')
ax.plot(170+.5*(xx-170), xx, color=C.INK, ls='--', label='$x=170+0.5(y-170)$')
ax.plot([182, 182], [155, 182], color=C.GRAY, ls='-', lw=.7)
dot(ax, (182, 176), size=34)
ax.scatter([182], [182], facecolor=C.PAPER, edgecolor=C.INK, s=34, zorder=5)
label(ax, '$(182,176)$', (182, 176), offset=(-165, 12), ha='right',
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=.7))
label(ax, '$(182,182)$', (182, 182), offset=(-130, 12), ha='center',
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=.7))
ax.set(xlim=(155, 185), ylim=(155, 185), xlabel='父亲身高', ylabel='儿子身高', aspect='equal')
ax.set_xticks([155, 160, 170, 180, 185])
ax.set_yticks([155, 160, 170, 180, 185])
ax.legend(loc='upper center', bbox_to_anchor=(.5, 1.26), fontsize=9)
fig.subplots_adjust(left=.14, right=.97, bottom=.12, top=.78)
save(fig, "P13-n7")
