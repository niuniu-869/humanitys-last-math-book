import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

rho=np.linspace(0,2,401); eps=.2
fig, axes = new_fig(13,5,ncols=2,sharey=True)
for ax,A,title in zip(axes,[2,-2],["$A=+2$","$A=-2$"]):
    raw=rho*A; clip=np.minimum(rho*A, A*np.clip(rho,1-eps,1+eps))
    ax.plot(rho,raw,color=C.GRAY,ls=":",lw=1.2); ax.plot(rho,clip,color=C.INK,lw=2.2)
    lo,hi=(1.2,2) if A>0 else (0,.8); ax.axvspan(lo,hi,color=C.LIGHT,alpha=.55); label(ax,"梯度为 0",((lo+hi)/2, .3 if A>0 else -.3),ha="center",fontsize=8)
    for z in [.8,1.2]: ax.axvline(z,color=C.INK,ls="--",lw=.9)
    label(ax,"$1-\\varepsilon$",(.8,ax.get_ylim()[0]),offset=(0,4),ha="center",fontsize=8); label(ax,"$1+\\varepsilon$",(1.2,ax.get_ylim()[0]),offset=(0,4),ha="center",fontsize=8)
    for x,y in ([(1.1,2.2),(1.5,2.4)] if A>0 else [(0.7,-1.6),(1.5,-3.0)]): ax.scatter([x],[y],s=34,facecolors=C.PAPER,edgecolors=C.INK,zorder=5)
    ax.set_title(title); ax.set_xlim(0,2); ax.set_xlabel("$\\rho$"); ax.grid(False)
axes[0].set_ylabel("目标值"); fig.tight_layout(); save(fig,"M15-n7")
