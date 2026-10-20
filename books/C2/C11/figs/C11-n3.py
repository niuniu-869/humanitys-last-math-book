import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(14, 5.8, ncols=2); x=np.linspace(-1,1,400)
for ax in axes:
    ax.axhline(0,color=C.INK,lw=.9); ax.axvline(0,color=C.INK,lw=.9); ax.set(xlim=(-1.3,1.3), ylim=(-1.15,1.35)); ax.set_xticks([-1,0,1]); ax.set_yticks([])
ax=axes[0]; y=1-x*x; ax.plot(x,y,color=C.INK); ax.fill_between(x,0,y,color=C.LIGHT); ax.axvline(0,color=C.INK,ls='-.',lw=1.0); label(ax,'偶函数 $f(x)=1-x^2$',(0,1.32),ha='center'); label(ax,'左 = 右',(0,.48),ha='center')
ax=axes[1]; y=x**3; ax.plot(x,y,color=C.INK); xp=x[x>=0]; ax.fill_between(xp,0,xp**3,color=C.LIGHT); xn=x[x<=0]; ax.fill_between(xn,0,xn**3,color=C.PAPER,hatch='///',edgecolor=C.GRAY); label(ax,'奇函数 $g(x)=x^3$',(0,1.32),ha='center'); label(ax,'+',(0.58,.20),ha='center'); label(ax,'−',(-.58,-.28),ha='center'); label(ax,'斜线阴影 = 在 $x$ 轴下方的有符号面积，取负',(0,-1.08),ha='center',fontsize=8)
for ax in axes: ax.set_aspect('equal'); ax.axis('off')
save(fig,'C11-n3')
