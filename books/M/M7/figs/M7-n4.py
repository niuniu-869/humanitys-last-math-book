import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

u = 1.; s = 1/(1+np.exp(-u)); ds = s*(1-s); gu = s+u*ds
assert np.allclose([s, ds, gu], [.7311,.1966,.9277], atol=5e-5)
fig, ax = new_fig(16, 8)
ax.set(xlim=(-1.8,10), ylim=(-3.6,2.7)); ax.axis('off')
def txt(text, xy, size=10):
    label(ax,text,xy,ha='center',va='center',fontsize=size)
def node(text,xy,width=1.1):
    x,y=xy
    ax.add_patch(Rectangle((x-width/2,y-.32),width,.64,facecolor=C.PAPER,edgecolor=C.INK))
    txt(text,xy)
def edge(a,b,back=False):
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='-|>',color=C.INK,lw=1.2,linestyle='--' if back else '-',shrinkA=0,shrinkB=0))
node('$u$',(0,0))
node(r'$s=\sigma(u)$',(4,-1.7),2.1)
node(r'$L=u\cdot s$',(8,0),2.0)
txt('$u=1$',(0,.65))
txt(rf'$s={s:.4f}$',(4,-1.05))
txt(rf'$L={u*s:.4f}$',(8,.65))
txt(r'$\bar L=1$',(8,-.75))
txt(r'$\bar s=u=1$',(4,-2.38))
txt(rf'$\bar u={s:.4f}+{u*ds:.4f}={gu:.4f}$',(1.6,-3.15),10)
# Direct branch occupies the upper lane.
edge((.55,.15),(7,.15))
edge((7,-.12),(.55,-.12),True)
txt('直接路',(4,.6),9)
txt(r'$0.7311$',(4,-.48),9)
# The sigmoid branch has separate outward and return lanes.
edge((.25,-.32),(2.95,-1.55))
edge((5.05,-1.55),(7.4,-.32))
edge((7.7,-.32),(5.05,-1.85),True)
edge((2.95,-1.85),(-.05,-.32),True)
txt(r'$\bar s\,\sigma^\prime(u)=0.1966$',(.6,-2.2),9)
txt(r'$\bar s=1$',(6.8,-2.15),9)
edge((1.6,2.1),(2.8,2.1)); txt('前向',(3.5,2.1),9)
edge((6.6,2.1),(5.4,2.1),True); txt('反向',(7.3,2.1),9)
save(fig, "M7-n4")
