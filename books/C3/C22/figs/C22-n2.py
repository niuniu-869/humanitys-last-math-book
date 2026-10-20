import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 9)
theta = np.linspace(0, 2*np.pi, 1001)
value = np.cos(theta)**2 * np.sin(theta)
ax.axhline(0, color=C.INK, ls="--", lw=1.3,
           label=r"可微时的公式 $f_x\cos\theta+f_y\sin\theta$（这里 $f_x=f_y=0$）")
ax.plot(theta, value, color=C.INK, ls="-", lw=2,
        label="真正的方向导数")
p = (np.pi/4, np.sqrt(2)/4)
dot(ax, p)
label(ax, r"$\frac{\sqrt{2}}{4}\approx0.354$", p, offset=(18, 20), ha="left")
ax.set(xlim=(0, 2*np.pi), ylim=(-0.6, 0.6))
ax.set_xticks(np.arange(5)*np.pi/2,
              ["$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"])
ax.set_yticks([-0.6, -0.3, 0, 0.3, 0.6])
ax.set_xlabel(r"$\theta$", loc="right")
ax.set_ylabel("方向导数")
ax.legend(loc="lower left", bbox_to_anchor=(-0.1, 1.025), fontsize=9,
          borderaxespad=0, handlelength=2.6)
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.18, top=0.75)
assert np.isclose(np.cos(p[0])**2 * np.sin(p[0]), p[1])
assert np.isclose(2/(3*np.sqrt(3)), 0.3849001794597505)
save(fig, "C22-n2")
