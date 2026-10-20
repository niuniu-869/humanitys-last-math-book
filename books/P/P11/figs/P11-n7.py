import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from scipy.stats import chi2, t, norm

fig, (ax1, ax2) = new_fig(15, 6, ncols=2)
x1 = np.linspace(0, 18, 600)
y1 = chi2.pdf(x1, 5)
qlo, qhi = chi2.ppf(0.025, 5), chi2.ppf(0.975, 5)
ax1.plot(x1, y1, color=C.BLUE, ls='-', lw=1.6)
mask = (x1 >= qlo) & (x1 <= qhi)
ax1.fill_between(x1, 0, y1, where=mask, color=C.LIGHT, alpha=0.9)
for q in (qlo, qhi): ax1.axvline(q, color=C.GRAY, ls='--', lw=1.0)
label(ax1, r'$1-\alpha$', (6.5, 0.04), ha='center', va='center')
# 左尾太窄放不下字：标注放在峰的左上方空白处，折线引线先向左、再竖直落进左尾
ax1.annotate(r'$\frac{\alpha}{2}$', xy=(0.42, 0.012), xytext=(1.6, 0.212),
             ha='left', va='center', color=C.INK,
             arrowprops=dict(arrowstyle='->', color=C.INK, lw=0.7, shrinkA=2, shrinkB=0,
                             connectionstyle='angle,angleA=180,angleB=90,rad=0'))
label(ax1, r'$\frac{\alpha}{2}$', (15.2, 0.04), ha='center')
ax1.set(xlim=(0,18), ylim=(0,0.24), xlabel=r'$\chi^2$', ylabel='密度')
ax1.set_title(r'$\chi^2(5)$：分位数不对称')
x2 = np.linspace(-5, 5, 600)
ax2.plot(x2, t.pdf(x2, 5), color=C.BLUE, ls='-', lw=1.6)
ax2.plot(x2, norm.pdf(x2), color=C.GRAY, ls='--', lw=1.2)
# 竖点线止于 0.40（略高于正态峰值），给右上角标注让出空间
for q in (-2.571, 2.571): ax2.plot([q, q], [0, 0.40], color=C.INK, ls=':', lw=1.0)
label(ax2, '$t$ 比正态胖：\n$t_{0.025}(5)=2.571>1.960$', (4.9, 0.43), ha='right', va='bottom')
ax2.set(xlim=(-5,5), ylim=(0,0.56), xlabel='统计量', ylabel='密度')
ax2.set_title(r'$t(5)$ 与标准正态')
save(fig, "P11-n7")
