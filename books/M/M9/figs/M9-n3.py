import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle, Circle

fig, ax = new_fig(28, 8.5)
nodes = [(0,1.5,'中心词编号\n$c$'), (2,2.2,'查表 $V_{\\mathrm{in}}$\n$(V\\times d)$\n取第 $c$ 行'),
         (4.7,1.2,'$\\boldsymbol{v}_c$\n$(d)$'),(6.4,2.2,'乘 $U_{\\mathrm{out}}$\n$(V\\times d)$'),
         (9.1,1.2,'$\\boldsymbol{z}$\n$(V)$'),(10.8,1.8,'softmax'),(13.1,1.2,'$\\boldsymbol{p}$\n$(V)$')]
for x,w,t in nodes:
    ax.add_patch(Rectangle((x,2),w,1.3,facecolor=C.PAPER,edgecolor=C.INK,lw=1))
    ax.text(x+w/2,2.65,t,ha='center',va='center',fontsize=9)
for (x,w,_),(nx,_,_) in zip(nodes,nodes[1:]):
    arrow(ax,(x+w,2.65),(nx-x-w,0),color=C.INK,lw=1)
ax.add_patch(Circle((15.7,2.65),.65,facecolor=C.LIGHT,edgecolor=C.INK))
ax.text(15.7,2.65,'交叉熵\n$\\ell$',ha='center',va='center',fontsize=9)
arrow(ax,(14.3,2.65),(.75,0),color=C.INK,lw=1)
ax.text(15.7,4.2,'真实词的独热\n$\\boldsymbol{y}$  $(V)$',ha='center',va='center',fontsize=9)
arrow(ax,(15.7,3.7),(0,-.4),color=C.INK,lw=1)
# Separate return paths keep derivatives out of the forward boxes.
ax.plot([13.7,13.7],[2,1.35],ls='--',color=C.INK,lw=1)
ax.annotate('',xy=(9.7,1.35),xytext=(13.7,1.35),arrowprops=dict(arrowstyle='->',ls='--',color=C.INK))
ax.annotate('',xy=(9.7,2),xytext=(9.7,1.35),arrowprops=dict(arrowstyle='->',ls='--',color=C.INK))
label(ax,r'$\boldsymbol{p}-\boldsymbol{y}$',(11.7,1.35),(0,-18),ha='center')
ax.plot([9.7,9.7],[1.35,.35],ls='--',color=C.INK,lw=1)
ax.annotate('',xy=(5.3,.35),xytext=(9.7,.35),arrowprops=dict(arrowstyle='->',ls='--',color=C.INK))
ax.annotate('',xy=(5.3,2),xytext=(5.3,.35),arrowprops=dict(arrowstyle='->',ls='--',color=C.INK))
label(ax,r'$U_{\mathrm{out}}^{\mathsf{T}}(\boldsymbol{p}-\boldsymbol{y})$',(7.5,.35),(0,-20),ha='center')
ax.set(xlim=(-.2,16.6),ylim=(-.4,4.7)); ax.axis('off')
save(fig, "M9-n3")
