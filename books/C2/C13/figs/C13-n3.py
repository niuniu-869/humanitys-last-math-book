import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc

fig, ax = new_fig(8.8, 8.0)
th = np.linspace(0, 2*np.pi, 900)
r = 1 + np.cos(th)
ax.plot(r*np.cos(th), r*np.sin(th), color=C.INK, ls=":", lw=1.15)
up = np.linspace(0, np.pi, 500)
ru = 1 + np.cos(up)
ax.plot(ru*np.cos(up), ru*np.sin(up), color=C.INK, lw=1.8)
ax.fill(np.r_[0, ru*np.cos(up)], np.r_[0, ru*np.sin(up)], color=C.LIGHT, zorder=0)
t0, t1 = 1.0, 1.25
rt0, rt1 = 1+np.cos(t0), 1+np.cos(t1)
curve_t = np.linspace(t0, t1, 100); rc = 1+np.cos(curve_t)
ax.fill(np.r_[0, rt0*np.cos(t0), rc*np.cos(curve_t), rt1*np.cos(t1)],
        np.r_[0, rt0*np.sin(t0), rc*np.sin(curve_t), rt1*np.sin(t1)], color=C.GRAY, alpha=0.55, zorder=2)
for t, rt in ((t0, rt0), (t1, rt1)):
    ax.plot([0, rt*np.cos(t)], [0, rt*np.sin(t)], color=C.INK, lw=1.5)
label(ax, r"$\theta$", (0.22, 0.44), offset=(-4, 0))
label(ax, r"$\theta+\mathrm{d}\theta$", (0.52, 0.98), offset=(4, 3))
label(ax, r"$r$", (0.48, 0.72), offset=(5, 0))
ax.add_patch(Arc((0, 0), 0.48, 0.48, theta1=np.degrees(t0), theta2=np.degrees(t1), color=C.INK, lw=1.0))
label(ax, r"$\mathrm{d}\theta$", (0.28, 0.18), offset=(2, 0))
label(ax, r"细扇形面积 $\approx\frac{1}{2}r^2\,\mathrm{d}\theta$", (-0.25, 1.90), ha="right")
ax.axhline(0, color=C.GRAY, lw=0.6); ax.axvline(0, color=C.GRAY, lw=0.6)
ax.set(xlim=(-2.45, 2.25), ylim=(-1.3, 2.15), aspect="equal")
ax.set_xticks([]); ax.set_yticks([])
save(fig, "C13-n3")
