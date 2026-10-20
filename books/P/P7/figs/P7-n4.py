import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(12, 5.8, ncols=2, squeeze=False)
x = np.linspace(-1, 1, 200)
ax = axes[0,0]; ax.plot(x, x*x, color=C.INK, lw=1.5); ax.scatter(x, x*x, s=7, color=C.INK)
ax.axhline(0, color=C.LIGHT, lw=.7); ax.axvline(0, color=C.LIGHT, lw=.7)
ax.set_xlim(-1.3,1.3); ax.set_ylim(-1.3,1.3); ax.set_aspect("equal"); ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
ax = axes[0,1]; t = np.linspace(0,2*np.pi,400); ax.plot(np.cos(t), np.sin(t), color=C.INK, lw=1.5)
rng = np.random.default_rng(20261018); q = rng.uniform(-1,1,(6000,2)); q = q[np.sum(q*q,axis=1)<=1][:1500]
ax.scatter(q[:,0], q[:,1], s=3, color=C.GRAY, alpha=.5, linewidths=0)
for sx in (-1,1):
    for sy in (-1,1):
        ax.fill_between([.9,1.3] if sx>0 else [-1.3,-.9], sy*.9, sy*1.3, color=C.LIGHT, alpha=.8, hatch="//", edgecolor=C.GRAY, linewidth=.7)
ax.axhline(0, color=C.LIGHT, lw=.7); ax.axvline(0, color=C.LIGHT, lw=.7)
label(ax, "斜线方块内没有点", (0, 1.17), offset=(0, 0), ha="center", va="center")
ax.set_xlim(-1.3,1.3); ax.set_ylim(-1.3,1.3); ax.set_aspect("equal"); ax.set_xlabel("$X$"); ax.set_ylabel("$Y$")
save(fig, "P7-n4")
