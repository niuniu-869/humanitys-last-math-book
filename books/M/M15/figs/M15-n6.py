import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

sig=lambda x:1/(1+np.exp(-x)); assert np.isclose(sig(10),.99995,atol=1e-5)
fig, ax = new_fig(10,6); b=np.logspace(np.log10(.05),np.log10(20),400); ax.semilogx(b,sig(1/b),color=C.INK,lw=2)
for x,y,t in [(.1,.99995,"$\\beta=0.1$：0.99995"),(.5,.8808,"$\\beta=0.5$：0.8808"),(2,.6225,"$\\beta=2$：0.6225")]: dot(ax,(x,y)); label(ax,t,(x,y),offset=(8,8) if x==2 else (5,-14),fontsize=8)
ax.axhline(.5,color=C.INK,ls="--",lw=1); label(ax,"$\\pi_{\\rm ref}$（$\\beta\\to\\infty$）",(.06,.5),offset=(0,-14),ha="left",fontsize=8); label(ax,"$\\beta\\to0$：只选奖励最大的",(18,.96),ha="right",fontsize=8)
ax.set(xlim=(.05,20),ylim=(.4,1.02),xlabel="$\\beta$",ylabel="$\\pi^*(A)$"); fig.tight_layout(); save(fig,"M15-n6")
