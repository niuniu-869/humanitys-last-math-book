import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(18, 9, ncols=2)
f = lambda x, y: x**3+y**3-3*x*y
ax = axes[0]
t = np.linspace(.4, 1.6, 601)
X, Y = np.meshgrid(t, t)
levels = [-.96, -.85, -.7, -.56]
cs = ax.contour(X, Y, f(X,Y), levels=levels, colors=C.INK, linewidths=1, linestyles='-')
assert all(np.allclose(seg[0], seg[-1]) for group in cs.allsegs for seg in group)
ax.clabel(cs, fmt='%g', fontsize=9)
dot(ax, (1,1))
label(ax, r'$f=-1$', (1,1), (0,-12), ha='center', fontsize=8)
ax.set(xlim=(.4,1.6), ylim=(.4,1.6), title=r'$(1,1)$ 附近', xlabel='$x$', ylabel='$y$')
ax.set_xticks([.4,1,1.6]); ax.set_yticks([.4,1,1.6])
ax = axes[1]
t = np.linspace(-.8,.8,601)
X,Y = np.meshgrid(t,t)
cs = ax.contour(X,Y,f(X,Y),levels=[-1,-.4,.4,1],colors=C.INK,linewidths=.85,linestyles='-')
ax.clabel(cs,fmt='%g',fontsize=9,manual=[(-.7,-.3),(-.6,-.1),(-.1,.6),(-.3,.7)])
ax.contour(X,Y,f(X,Y),levels=[0],colors=C.INK,linewidths=2,linestyles='-')
ax.plot(t,t,color=C.GRAY,ls='--',lw=1.1)
ax.plot(t,-t,color=C.GRAY,ls='--',lw=1.1)
dot(ax,(0,0),size=20)
label(ax, r'$f=0$', (.46, .16), offset=(0,7))
ax.set(xlim=(-.8,.8),ylim=(-.8,.8),title=r'$(0,0)$ 附近',xlabel='$x$',ylabel='$y$')
ax.set_xticks([-.8,0,.8]); ax.set_yticks([-.8,0,.8])
ax.text(.5,-.23,r'$y=x:\ f<0$；$y=-x:\ f>0$'+'\n'+r'（原点除外）',transform=ax.transAxes,ha='center',va='top',fontsize=9)
for ax in axes:
    ax.set_aspect('equal')
assert f(1,1) == -1 and f(0,0) == 0
fig.subplots_adjust(left=.08,right=.98,bottom=.25,top=.9,wspace=.32)
save(fig, "C24-n2")
