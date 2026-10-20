import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

sig = lambda x: 1/(1+np.exp(-x))
assert np.isclose(sig(1),.7311,atol=1e-4) and np.isclose(np.log(.7/.3),.8473,atol=1e-4)
fig, ax = new_fig(10,6); x=np.linspace(-6,6,400); ax.plot(x,sig(x),color=C.INK,lw=2)
ax.axhline(.5,color=C.INK,ls="--",lw=1); ax.axvline(0,color=C.INK,ls="--",lw=1); dot(ax,(0,.5),size=28)
dot(ax,(1,sig(1)),size=28); label(ax,"$\\sigma(1)=0.7311$",(1,sig(1)),offset=(8,5),fontsize=9); ax.plot([1,1],[0,sig(1)],ls=":",color=C.GRAY,lw=1); ax.plot([-6,1],[sig(1),sig(1)],ls=":",color=C.GRAY,lw=1)
dot(ax,(.8473,.7),size=30,color=C.PAPER); ax.scatter([.8473],[.7],s=30,facecolors=C.PAPER,edgecolors=C.INK,zorder=5); label(ax,"胜率 0.7 ⇒ $\\Delta=0.8473$",(.8473,.7),offset=(8,-15),fontsize=9)
ax.set(xlim=(-6,6),ylim=(0,1),xlabel="$\\Delta=r_i-r_j$",ylabel="胜率 $\\sigma(\\Delta)$"); fig.tight_layout(); save(fig,"M15-n5")
