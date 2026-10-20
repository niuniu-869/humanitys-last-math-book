import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(11, 7, nrows=2, sharex=True)
data = [([-0.5,0,.5],[.2,.5,.3],"不加基线",.1225), ([-.25,.25],[.4,.6],"基线 $b=0.5$",.06)]
for ax,(x,p,title,var) in zip(axes,data):
    ax.bar(x,p,width=.13,color=C.LIGHT,edgecolor=C.INK); ax.axvline(.05,color=C.INK,ls="--",lw=1)
    for a,b in zip(x,p): label(ax,f"{b:g}",(a,b+.035),ha="center",fontsize=9)
    label(ax,"均值 0.05",(.05,.88),ha="left",fontsize=8); label(ax,f"方差 {var:g}",(.97,.9),transform=ax.transAxes,ha="right",fontsize=8)
    ax.set_title(title); ax.set_ylim(0,.72); ax.set_ylabel("概率")
axes[-1].set_xlabel("$\\hat g_A$ 的取值"); axes[-1].set_xticks([-.5,-.25,0,.25,.5]); fig.tight_layout(); save(fig,"M15-n4")
