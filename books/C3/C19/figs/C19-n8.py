import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from _geometry import line, axes, ring

fig, panels = new_fig(19, 17, nrows=2, ncols=3)
fig.subplots_adjust(left=.03, right=.97, top=.98, bottom=.11, wspace=.18, hspace=.28)
titles = [
    '椭球面\n'+r'$\frac{x^2}{4}+\frac{y^2}{4}+z^2=1$',
    '单叶双曲面\n'+r'$x^2+y^2-z^2=1$',
    '双叶双曲面\n'+r'$x^2+y^2-z^2=-1$',
    '椭圆锥面\n'+r'$z^2=x^2+y^2$',
    '椭圆抛物面\n'+r'$z=x^2+y^2$',
    '马鞍面\n'+r'$z=x^2-y^2$']

def revolution(ax, heights, radius):
    for z in heights:
        line(ax, ring(radius(z), z), color=C.GRAY, lw=.6)
    zs = np.linspace(min(heights), max(heights), 161)
    for angle in np.linspace(0, 2*np.pi, 13)[:-1]:
        rs = radius(zs)
        line(ax, np.column_stack((rs*np.cos(angle), rs*np.sin(angle), zs)), color=C.GRAY, lw=.6)

for i, ax in enumerate(panels.flat):
    ax.set_aspect('equal'); ax.axis('off')
    if i == 0:
        radius = lambda z: 2*np.sqrt(np.maximum(0, 1-z*z))
        revolution(ax, np.linspace(-1, 1, 11), radius)
        line(ax, ring(radius(.5), .5), lw=2)
    elif i == 1:
        radius = lambda z: np.sqrt(1+z*z)
        revolution(ax, np.linspace(-1.5, 1.5, 11), radius)
        for z in [0, 1]: line(ax, ring(radius(z), z), lw=2)
    elif i == 2:
        radius = lambda z: np.sqrt(np.maximum(0, z*z-1))
        for sign in [-1, 1]:
            revolution(ax, sign*np.linspace(1, 2, 7), radius)
            line(ax, ring(radius(sign*1.5), sign*1.5), lw=2)
        label(ax, '$-1<z<1$ 无点', (0, 0), (8, 1), fontsize=8)
    elif i == 3:
        for sign in [-1, 1]: revolution(ax, sign*np.linspace(0, 2, 8), np.abs)
        line(ax, ring(1, 1), lw=2)
    elif i == 4:
        revolution(ax, np.linspace(0, 2, 11), np.sqrt)
        line(ax, ring(np.sqrt(1.5), 1.5), lw=2)
    else:
        t = np.linspace(-1.2, 1.2, 101)
        for k in np.linspace(-1.2, 1.2, 13):
            line(ax, np.column_stack((t, 0*t+k, t*t-k*k)), color=C.GRAY, lw=.6)
            line(ax, np.column_stack((0*t+k, t, k*k-t*t)), color=C.GRAY, lw=.6)
        line(ax, np.column_stack((t, t*0, t*t)), lw=2)
        line(ax, np.column_stack((t*0, t, -t*t)), lw=2, ls='--')
        label(ax, '$y=0$', (-.83, 1.05), (-14, 2), fontsize=8)
        label(ax, '$x=0$', (1.2, -1.5), (2, -8), fontsize=8)
    axes(ax, [2.5, 2.5, 2.7])
    ax.set_xlim(-3.2, 3.65); ax.set_ylim(-3.2, 3.2)
    ax.text(.5, -.07, titles[i], transform=ax.transAxes, ha='center', va='top', fontsize=10, color=C.INK)

assert np.isclose((2*np.sqrt(1-.5**2))**2/4+.5**2, 1)
assert np.isclose(np.sqrt(1.5**2-1)**2-1.5**2, -1)
save(fig, 'C19-n8')
