import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

x = np.array([1.,2.])
W1 = np.array([[.5,-.5],[.25,.5]])
w2 = np.array([1.,-1.])
z1 = W1@x; h = 1/(1+np.exp(-z1))
z2 = w2@h; yh = 1/(1+np.exp(-z2)); loss = -np.log(yh)
d2 = yh-1; gh = w2*d2; d1 = gh*h*(1-h)
gW1 = np.outer(d1,x); gw2 = d2*h
assert np.allclose(gW1,[[-.1407,-.2814],[.1036,.2073]],atol=5e-5)
assert np.allclose(gw2,[-.2260,-.4653],atol=5e-5)
fig, ax = new_fig(21, 9.5)
ax.set(xlim=(-1.4,16.4),ylim=(-3.8,2.25)); ax.axis('off')
def txt(text,xy,size=9):
    label(ax,text,xy,ha='center',va='center',fontsize=size)
def edge(a,b,back=False):
    ax.annotate('',xy=b,xytext=a,arrowprops=dict(arrowstyle='-|>',color=C.INK,lw=1.15,linestyle='--' if back else '-',shrinkA=0,shrinkB=0))
positions = np.arange(6)*3.
names = [r'$\boldsymbol{x}$',r'$\boldsymbol{z}_1$',r'$\boldsymbol{h}$',r'$z_2$',r'$\hat y$',r'$L$']
vals = ['$ (1,2) $',rf'$({z1[0]:.2f},{z1[1]:.2f})$',rf'$({h[0]:.4f},{h[1]:.4f})$',rf'$ {z2:.4f}$',rf'$ {yh:.4f}$',rf'$ {loss:.4f}$']
for pos,name,val in zip(positions,names,vals):
    ax.add_patch(Rectangle((pos-.4,-.28),.8,.56,facecolor=C.PAPER,edgecolor=C.INK))
    txt(name,(pos,0),11); txt(val,(pos,.85),9)
for i in range(5):
    edge((positions[i]+.4,.13),(positions[i+1]-.4,.13))
    edge((positions[i+1]-.4,-.13),(positions[i]+.4,-.13),True)
for mid,op in zip([1.5,4.5,7.5,10.5,13.5],[r'$W_1$',r'$\sigma$',r'$\boldsymbol{w}_2^{\mathsf{T}},\,b_2$',r'$\sigma$',r'$-\ln$']):
    txt(op,(mid,.4),9)
for mid,rule in [(1.5,r'$W_1^{\mathsf{T}}\boldsymbol{\delta}_1$'),(4.5,r'$\times\sigma^\prime$'),(7.5,r'$W_2^{\mathsf{T}}\delta_2$'),(10.5,r'$\times\sigma^\prime$'),(13.5,r'$\times(-1/\hat y)$')]:
    txt(rule,(mid,-.48),9)
for pos,name,value in [(3,r'\boldsymbol{\delta}_1',d1),(6,r'\bar{\boldsymbol{h}}',gh)]:
    txt(rf'$ {name}$',(pos,-1.05),10)
    txt(rf'$({value[0]:.4f},{value[1]:.4f})$',(pos,-1.48),9)
txt(r'$\delta_2=\hat y-y$',(9,-1.05),10)
txt(rf'$ {d2:.4f}$',(9,-1.48),9)
txt(r'$\bar{\hat y}=-1/\hat y$',(12,-1.05),9)
txt(r'$\bar L=1$',(15,-1.05),10)
txt(r'$\partial W_1=\boldsymbol{\delta}_1\boldsymbol{x}^{\mathsf{T}}$',(3,-2.35),10)
# Mathtext has no matrix environment: draw the computed entries and brackets.
cx, cy = 3., -3.12
for i in range(2):
    for j in range(2):
        txt(f'$ {gW1[i,j]:.4f}$',(cx-.7+1.4*j,cy+.23-.46*i),10)
for side in [-1,1]:
    xx=cx+side*1.5
    ax.plot([xx-side*.12,xx,xx,xx-side*.12],[cy+.52,cy+.52,cy-.52,cy-.52],color=C.INK,lw=1)
txt(r'$\partial\boldsymbol{w}_2=\delta_2\boldsymbol{h}$',(9,-2.35),10)
txt(rf'$({gw2[0]:.4f},{gw2[1]:.4f})$',(9,-2.92),10)
edge((3.9,1.85),(5.1,1.85)); txt('前向值',(6.0,1.85),9)
edge((10.2,1.85),(9.,1.85),True); txt('反向梯度',(11.3,1.85),9)
save(fig, "M7-n5")
