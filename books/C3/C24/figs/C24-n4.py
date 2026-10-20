import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 10)
x = np.arange(1.,5.)
y = np.array([2.,3.,5.,6.])
a,b = np.linalg.lstsq(np.column_stack([x,np.ones(4)]),y,rcond=None)[0]
pred = a*x+b
err = pred-y
assert np.allclose([a,b],[1.4,.5])
assert np.allclose(err,[-.1,.3,-.3,.1]) and np.isclose(err@err,.2)
t = np.array([.4,4.5])
ax.plot(t,a*t+b,color=C.INK,ls='-',lw=1.5,label=r'$y=1.4x+0.5$')
for i,(xx,yy,pp,e) in enumerate(zip(x,y,pred,err)):
    ax.plot([xx,xx],[yy,pp],color=C.INK,ls='--',dashes=(1,1),lw=1.2,dash_capstyle='butt')
    dot(ax,(xx,yy),size=16)
    label(ax,f'${e:+.1f}$',(xx,(yy+pp)/2), (12,-7) if e>0 else (-12,10),
          va='center',ha='left' if e>0 else 'right')
ax.legend(loc='upper left')
ax.text(.04,.86,r'$e=\widehat y-y$',transform=ax.transAxes)
ax.set(xlim=(.4,4.65),ylim=(.7,7.25),xlabel='$x$',ylabel='$y$')
ax.set_xticks(x); ax.set_yticks(range(1,8))
fig.subplots_adjust(left=.12,right=.97,bottom=.14,top=.97)
save(fig, "C24-n4")
