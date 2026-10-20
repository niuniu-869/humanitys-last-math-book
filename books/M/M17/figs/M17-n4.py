import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

mu_likelihood, var_likelihood = 2.0744, .1/.9
mu_prior, var_prior = 1.8, 1-.9**2
var_post = 1/(1/var_likelihood + 1/var_prior)
mu_post = var_post*(mu_likelihood/var_likelihood + mu_prior/var_prior)
assert round(mu_post, 4) == 1.9731 and round(var_post, 4) == .0701
x = np.linspace(1, 2.8, 1601)
fig, ax = new_fig(15, 9)
curves = [(mu_likelihood, var_likelihood, ':', r'由 $x_3$：均值 2.0744'),
          (mu_prior, var_prior, '--', r'由 $x_0$：均值 1.8'),
          (mu_post, var_post, '-', '后验：均值 1.9731')]
for mu, var, ls, text in curves:
    density = np.exp(-(x-mu)**2/(2*var))/np.sqrt(2*np.pi*var)
    ax.plot(x, density, color=C.INK, ls=ls, lw=1.7, label=text)
    peak = 1/np.sqrt(2*np.pi*var)
    ax.plot([mu, mu], [peak+.025, peak+.12], color=C.INK, ls=ls, lw=1.2)
ax.set(xlim=(1, 2.8), ylim=(0, 1.68), xlabel='$x_2$', ylabel='密度', yticks=[], xticks=[1, 1.4, 1.8, 2.2, 2.6, 2.8])
ax.legend(loc='lower center', bbox_to_anchor=(.5, 1.02), ncol=1, fontsize=9, handlelength=3)
fig.subplots_adjust(left=.08, right=.97, bottom=.15, top=.73)
save(fig, "M17-n4")
