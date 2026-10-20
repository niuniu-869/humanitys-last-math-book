import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import erf

fig, (ax_top, ax_bot) = new_fig(16, 11, nrows=2)
z = np.linspace(-4, 4, 801)
sig = 1/(1+np.exp(-z)); dsig = sig*(1-sig)
tanh = np.tanh(z); dtanh = 1-tanh**2
relu = np.maximum(0, z); drelu = (z > 0).astype(float)
phi = 0.5*(1+np.vectorize(erf)(z/np.sqrt(2)))
varphi = np.exp(-z*z/2)/np.sqrt(2*np.pi)
gelu = z*phi; dgelu = phi + z*varphi
assert np.allclose(gelu[[200,600]], [-.0455,1.9545], atol=5e-5)
assert np.allclose(dgelu[[200,600]], [-.0852,1.0852], atol=5e-5)
curves = [(sig, '-', 'sigmoid'), (tanh, '--', 'tanh'), (relu, ':', 'ReLU'), (gelu, '-.', 'GELU')]
for y, ls, name in curves:
    ax_top.plot(z, y, ls=ls, lw=1.7, color=C.INK if name == 'sigmoid' else C.GRAY, label=name)
ax_top.set_xlim(-4, 4); ax_top.set_ylim(-1.2, 4.2); ax_top.set_ylabel(r'$\varphi(z)$')
ax_top.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
ax_top.axhline(0, color=C.LIGHT, lw=0.7)
for y, ls, name in [(dsig, '-', 'sigmoid'), (dtanh, '--', 'tanh'), (drelu, ':', 'ReLU'), (dgelu, '-.', 'GELU')]:
    if name == 'ReLU':
        ax_bot.plot(z[z<0], y[z<0], ls=ls, lw=1.7, color=C.GRAY, label=name)
        ax_bot.plot(z[z>0], y[z>0], ls=ls, lw=1.7, color=C.GRAY)
    else:
        ax_bot.plot(z, y, ls=ls, lw=1.7, color=C.INK if name == 'sigmoid' else C.GRAY, label=name)
ax_bot.set_xlim(-4, 4); ax_bot.set_ylim(-0.16, 1.18); ax_bot.set_xlabel(r'$z$'); ax_bot.set_ylabel(r'$\varphi\prime(z)$')
ax_bot.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
ax_bot.axhline(0, color=C.LIGHT, lw=0.7)
ax_bot.scatter([0], [0], s=38, facecolor=C.PAPER, edgecolor=C.INK, zorder=5)
label(ax_bot, 'sigmoid: 0.25', (-2.5, 0.45), ha='center', fontsize=8)
label(ax_bot, 'tanh: 1', (0, 1), offset=(-50, 9), fontsize=8)
label(ax_bot, 'ReLU: 0（约定）', (-3.7, 0.11), fontsize=8)
fig.tight_layout(h_pad=1.2)
save(fig, "M7-n2")
