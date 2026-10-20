import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import norm

fig, ax = new_fig(12, 7.5)
z = 1.96
x = np.linspace(-4, 4, 800)
y = norm.pdf(x)
ax.plot(x, y, color=C.BLUE, ls='-', lw=1.6)
mid = (x >= -z) & (x <= z)
ax.fill_between(x, 0, y, where=mid, color=C.LIGHT, alpha=0.9)
for q in (-z, z):
    ax.axvline(q, color=C.GRAY, ls='--', lw=1.0)
ax.axvline(0, color=C.INK, ls='-', lw=0.8)
label(ax, '面积 $1-\\alpha$', (0, 0.29), offset=(0, 0), ha='center')
label(ax, r'$\frac{\alpha}{2}$', (-3.0, 0.08), offset=(0, 0), ha='center')
label(ax, r'$\frac{\alpha}{2}$', (3.0, 0.08), offset=(0, 0), ha='center')
ax.set(xlim=(-4, 4), ylim=(0, 0.43), xlabel='标准化统计量', ylabel='密度')
ax.set_xticks([-z, 0, z], [r'$-z_{\alpha/2}=-1.96$', '0', r'$z_{\alpha/2}=1.96$'])
save(fig, "P11-n6")
