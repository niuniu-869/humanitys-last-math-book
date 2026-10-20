import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(14, 6, ncols=2, squeeze=False, gridspec_kw={"wspace": .38})
t = np.linspace(0, 2*np.pi, 400)
z0 = np.array([1., -1.]); L = np.array([[np.sqrt(2), 0], [1/np.sqrt(2), np.sqrt(3/2)]])
x0 = L @ z0
ax = axes[0,0]
for r in (1,2): ax.plot(r*np.cos(t), r*np.sin(t), color=C.INK, ls="--", lw=1.2)
ax.scatter([z0[0]],[z0[1]], s=65, facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
label(ax, r"$\boldsymbol{z}=(1,-1)$", z0, offset=(7, 7)); ax.axhline(0,color=C.LIGHT,lw=.7); ax.axvline(0,color=C.LIGHT,lw=.7)
ax.set_xlim(-3.5,3.5); ax.set_ylim(-3.5,3.5); ax.set_aspect("equal"); ax.set_xlabel("$z_1$"); ax.set_ylabel("$z_2$")
ax = axes[0,1]; S = np.array([[2.,1.],[1.,2.]])
for r in (1,2):
    E = np.linalg.eigh(S)[1] @ np.diag(np.sqrt(np.linalg.eigh(S)[0])*r) @ np.vstack((np.cos(t),np.sin(t)))
    ax.plot(E[0],E[1],color=C.INK,ls="-",lw=1.3)
u = np.array([1,1])/np.sqrt(2); v=np.array([-1,1])/np.sqrt(2)
for d in (u,v): ax.plot([-3.5*d[0],3.5*d[0]],[-3.5*d[1],3.5*d[1]],color=C.GRAY,ls=":",lw=.9)
ax.scatter([x0[0]],[x0[1]],s=65,color=C.INK,zorder=5); label(ax,r"$\boldsymbol{x}=L\boldsymbol{z}$",x0,offset=(7,7))
label(ax,r"$\sqrt{3}$",(1.22,1.22),offset=(3,3)); label(ax,"1",(-1.17,.75),offset=(0,0),ha="center",va="center")
label(ax,r"$2\sqrt{3}$",(2.55,2.80),offset=(0,0),ha="center",va="bottom")
label(ax,"2",(-1.75,1.45),offset=(0,0),ha="center",va="center")
ax.axhline(0,color=C.LIGHT,lw=.7); ax.axvline(0,color=C.LIGHT,lw=.7); ax.set_xlim(-3.5,3.5); ax.set_ylim(-3.5,3.5); ax.set_aspect("equal"); ax.set_xlabel("$x_1$"); ax.set_ylabel("$x_2$")
fig.text(.5,.95,"乘 $L$",ha="center",va="center",fontsize=11)
save(fig, "P7-n6")
