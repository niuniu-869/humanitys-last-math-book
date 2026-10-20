import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 8)
theta, dt, r, dr = .38, .40, 2., .40
angles = np.linspace(theta, theta+dt, 150)
polar = lambda radius, angle: np.array([radius*np.cos(angle), radius*np.sin(angle)])
inner, outer = polar(r, angles), polar(r+dr, angles)
ax.fill(np.r_[inner[0], outer[0, ::-1]], np.r_[inner[1], outer[1, ::-1]], color=C.LIGHT)
for radius, ls in [(r, '-'), (r+dr, '--')]:
    arc = polar(radius, angles)
    ax.plot(*arc, color=C.INK, ls=ls)
for angle in (theta, theta+dt):
    end = polar(2.72, angle)
    ax.plot([0, end[0]], [0, end[1]], color=C.INK)
ax.plot([0, 1.0], [0, 0], color=C.GRAY, lw=.8)
dot(ax, (0, 0), '$O$', offset=(-14, -8))
arc = polar(.55, np.linspace(0, theta, 50))
ax.plot(*arc, color=C.GRAY, lw=.9)
label(ax, r'$\theta$', polar(.7, theta/2), (0, -3))
arc = polar(.93, angles)
ax.plot(*arc, color=C.GRAY, lw=.9)
label(ax, r'$\Delta\theta$', polar(1.12, theta+dt/2), (-8, 0))
label(ax, '$r$', polar(1.45, theta), (0, -17))
label(ax, r'$\Delta r$', polar(r+dr/2, theta), (0, -17))
label(ax, r'$r\Delta\theta$', polar(1.65, theta+dt/2), (-2, 4), ha='center')
label(ax, r'$\theta+\Delta\theta$', polar(2.7, theta+dt), (-15, 9))
length = r*dt
left, bottom = 3.3, .8
ax.plot([left, left+length, left+length, left, left],
        [bottom, bottom, bottom+dr, bottom+dr, bottom], ls='--', color=C.INK)
label(ax, r'$r\Delta\theta$', (left+length/2, bottom), (0, -19), ha='center')
label(ax, r'$\Delta r$', (left+length, bottom+dr/2), (9, 0), va='center')
ax.set(xlim=(-.2, 4.65), ylim=(-.25, 2.3), aspect='equal')
ax.set_axis_off()
save(fig, "C25-n5")
