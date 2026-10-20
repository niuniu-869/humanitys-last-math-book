import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(17, 9, ncols=2)
u, v, du, dv = .55, .45, .50, .40
# A smooth nonlinear map with positive Jacobian throughout this rectangle.
def transform(u, v):
    return np.array([u+.35*v*v, v+.25*u*u])
p = transform(u, v)
eu = np.array([du, .5*u*du])
ev = np.array([.7*v*dv, dv])
assert 1-.35*(u+du)*(v+dv) > 0
assert np.isclose(np.linalg.det(np.column_stack([eu, ev])), (1-.35*u*v)*du*dv)
ax = axes[0]
ax.fill([u, u+du, u+du, u], [v, v, v+dv, v+dv], facecolor=C.LIGHT, edgecolor=C.INK)
dot(ax, (u, v), size=20)
label(ax, '$(u,v)$', (u, v), (-8, -10), ha='right')
label(ax, r'$\Delta u$', (u+du/2, v), (0, -17), ha='center')
label(ax, r'$\Delta v$', (u, v+dv/2), (-12, 0), ha='right')
ax = axes[1]
t = np.linspace(0, 1, 101)
uv = [(u+du*t, np.full_like(t, v)), (np.full_like(t, u+du), v+dv*t),
      (u+du*(1-t), np.full_like(t, v+dv)), (np.full_like(t, u), v+dv*(1-t))]
boundary = np.concatenate([transform(uu, vv) for uu, vv in uv], axis=1)
ax.fill(*boundary, color=C.LIGHT)
ax.plot(*boundary, color=C.INK, ls='-', lw=1.5)
par = np.array([p, p+eu, p+eu+ev, p+ev, p])
ax.plot(*par.T, color=C.INK, ls='--', lw=1.2)
for vec in (eu, ev):
    ax.annotate('', p+vec, p, arrowprops=dict(arrowstyle='->', linestyle='--', color=C.INK, lw=1.3))
dot(ax, p, size=20)
label(ax, r'$(x_u\Delta u,\,y_u\Delta u)$', p+.55*eu, (15, -24), ha='center', fontsize=9)
label(ax, r'$(x_v\Delta v,\,y_v\Delta v)$', p+.5*ev, (-18, 20), ha='center', fontsize=9)
for ax, names in zip(axes, [('u', 'v'), ('x', 'y')]):
    arrow(ax, (0, 0), (1.65, 0), color=C.GRAY, lw=.9)
    arrow(ax, (0, 0), (0, 1.45), color=C.GRAY, lw=.9)
    label(ax, '$'+names[0]+'$', (1.65, 0), (0, -14))
    label(ax, '$'+names[1]+'$', (0, 1.45), (-15, 0))
    ax.set(xlim=(-.14, 1.85), ylim=(-.18, 1.65), aspect='equal')
    ax.set_axis_off()
fig.text(.52, .83, r'$\longrightarrow$', ha='center', fontsize=20)
fig.text(.52, .12, r'面积 $\approx |x_u y_v-x_v y_u|\,\Delta u\,\Delta v$', ha='center')
fig.subplots_adjust(wspace=.22, bottom=.20)
save(fig, "C25-n7")
