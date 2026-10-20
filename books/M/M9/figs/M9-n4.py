import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

U = np.array([[1.,1.],[1.,0.],[1.,-1.]])
v = np.array([1.,1.])
p = np.exp(U@v - np.max(U@v)); p /= p.sum()
mean = p@U
step = U[0]-mean
updated = v+step
assert np.allclose(updated,[1,1.4248],atol=.00005)
fig, ax = new_fig(12, 13)
ax.axhline(0,color=C.GRAY,lw=.7,ls=':'); ax.axvline(0,color=C.GRAY,lw=.7,ls=':')
for point,w,off in zip(U,['鱼','骨头','牛奶'],[(-27,5),(10,7),(10,-4)]):
    dot(ax,point,w,offset=off)
ax.scatter(*v,s=110,facecolors='none',edgecolors=C.INK,zorder=6)
label(ax,r'$\boldsymbol{v}_c$',v,(13,3))
ax.scatter(*mean,s=42,marker='s',color=C.INK,zorder=5)
label(ax,r'$\bar{\boldsymbol{u}}$（预期）',mean,(12,-12))
ax.scatter(*updated,s=70,facecolors=C.PAPER,edgecolors=C.INK,zorder=5)
label(ax,'更新后',updated,(12,2))
arrow(ax,v,step,color=C.INK,lw=1.7)
ax.annotate('',xy=U[0],xytext=mean,arrowprops=dict(arrowstyle='-|>',ls='--',color=C.INK,lw=1.5,shrinkA=5,shrinkB=5))
label(ax,r'$\boldsymbol{u}_o-\bar{\boldsymbol{u}}$'+'\n（下降方向）',(.96,.78),(-18,-4),ha='right',fontsize=9)
ax.set(xlim=(-.5,2),ylim=(-1.5,2),aspect='equal')
ax.set_xticks([-.5,0,1,2]); ax.set_yticks([-1,0,1,2])
save(fig, "M9-n4")
