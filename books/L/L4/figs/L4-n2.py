import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig = plt.figure(figsize=(16/2.54, 8.2/2.54))
ax = fig.add_subplot(1,2,1, projection='3d')
bx = fig.add_subplot(1,2,2, projection='3d')
for a in (ax,bx):
    a.view_init(elev=24, azim=-58)
    for axis in (a.xaxis,a.yaxis,a.zaxis):
        axis.pane.set_facecolor((1,1,1,0)); axis.pane.set_edgecolor(C.LIGHT)
        axis._axinfo['grid']['color']=(0.85,0.85,0.85,0.55)
    a.set_box_aspect((1,1,1))
ax.set_title('输入空间')
ax.set_xlim(-1,5); ax.set_ylim(-1,3); ax.set_zlim(-2,2)
ax.set_xlabel('$x_1$'); ax.set_ylabel('$x_2$'); ax.set_zlabel('$x_3$', labelpad=-1)
s=np.linspace(-1,2.5,200); pts=np.column_stack((3-2*s,s,-1+0*s))
ax.plot(pts[:,0],pts[:,1],pts[:,2], ls='--', color=C.BLUE, lw=1.8)
for sv in (0,1,2):
    p=(3-2*sv,sv,-1); ax.scatter(*p, color=C.INK, s=24, depthshade=False)
    ax.text(p[0]+.35,p[1],p[2]+.25, f'$s={sv}$', color=C.INK, fontsize=8)
ax.quiver(0,0,0,-2,1,0,color=C.RED,arrow_length_ratio=.18,lw=1.5)
ax.text(-1.4,.7,0, '方向 $(-2,1,0)$', color=C.INK, fontsize=8)

bx.set_title('输出空间')
bx.set_xlim(-1,4); bx.set_ylim(-1,4); bx.set_zlim(-1,7)
bx.set_xlabel('$b_1$'); bx.set_ylabel('$b_2$'); bx.set_zlabel('$b_3$', labelpad=-1)
u=np.linspace(-1,4,25); v=np.linspace(-1,4,25); U,V=np.meshgrid(u,v); W=U+V
bx.plot_surface(U,V,W,color=C.LIGHT,alpha=.45,shade=False,edgecolor='none')
bx.plot_wireframe(U,V,W,color=C.GRAY,alpha=.25,rstride=6,cstride=6,linewidth=.5)
bx.scatter(2,3,5,color=C.INK,s=32,depthshade=False)
bx.text(1.0,2.0,3.0, '像：$b_3=b_1+b_2$', color=C.INK, fontsize=8)
bx.text(2.3,3,5.4, '$(2,3,5)$', color=C.INK, fontsize=8)
bx.scatter(1,1,1,facecolors='white',edgecolors=C.INK,s=40,depthshade=False,linewidths=1.2)
bx.plot([1,1],[1,1],[1,2],ls=':',color=C.INK,lw=1.8)
bx.text(1.5,1,0.2, '$(1,1,1)$：不在像里', color=C.INK, fontsize=8)
fig.text(.5,.80,'⑤',ha='center',va='center',fontsize=18,color=C.INK,
         bbox=dict(boxstyle='rarrow,pad=.12',fc=C.PAPER,ec=C.INK,lw=1))
fig.subplots_adjust(left=0.0,right=0.93,bottom=0.05,top=0.92,wspace=0.12)
save(fig, "L4-n2")
