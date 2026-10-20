import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(8.5, 7)
uA, uB = .3, 1.; vA, vB = np.sqrt(uA), 1.

# 浅灰：曲线下方，u 从 u_A 到 u_B
u = np.linspace(uA, uB, 400)
ax.fill_between(u, 0, np.sqrt(u), color=C.LIGHT, zorder=1)

# 斜线：曲线左边，v 从 v_A 到 v_B；右边界就是 u=v^2（不是 A、B 的连线）
vv = np.linspace(vA, vB, 400)
ax.fill_betweenx(vv, 0, vv**2, facecolor='none', hatch='//',
                 edgecolor=C.GRAY, lw=0, zorder=2)
ax.plot(u, np.sqrt(u), color=C.INK, lw=1.8, zorder=4)

# 两个矩形的边
ax.plot([uA, uA], [0, vA], color=C.INK, ls='--', lw=1)
ax.plot([uB, uB], [0, vB], color=C.INK, ls='--', lw=1)
ax.plot([0, uA], [vA, vA], color=C.INK, ls='--', lw=1)
ax.plot([0, uB], [vB, vB], color=C.INK, ls='--', lw=1)

ax.scatter([uA], [vA], s=38, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
ax.scatter([uB], [vB], s=34, color=C.INK, zorder=5)
label(ax, '$A$', (uA, vA), offset=(-15, 6))
label(ax, '$B$', (uB, vB), offset=(6, 3))

# 两块面积互不重叠，合起来等于大矩形减小矩形
area_check = (2/3*(uB**1.5 - uA**1.5) + (vB**3 - vA**3)/3) - (uB*vB - uA*vA)
assert abs(area_check) < 1e-12

label(ax, r'$\int v\,\mathrm{d}u$', (.64, .30), ha='center')
label(ax, r'$\int u\,\mathrm{d}v$', (.15, .78), ha='center',
      bbox={'facecolor': C.PAPER, 'edgecolor': 'none', 'pad': 1.5})
label(ax, '$u_Av_A$', (.035, .46), ha='left', va='bottom', fontsize=8)
label(ax, '$u_Bv_B$', (.84, 1.035), ha='left', va='bottom', fontsize=9)
ax.set(xlim=(-.05, 1.12), ylim=(-.06, 1.12),
       xticks=[0, .2, .4, .6, .8, 1], yticks=[0, .2, .4, .6, .8, 1],
       xlabel='$u$', ylabel='$v$')
ax.set_aspect('equal')
fig.text(0.5, -0.10, '浅灰 + 斜线 = 大矩形 $u_Bv_B$ 减小矩形 $u_Av_A$',
         ha='center', va='top', fontsize=8)
save(fig, 'C11-n5')
