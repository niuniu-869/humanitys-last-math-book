import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

t=np.arange(1,41); m=1-.9**t; mh=m/(1-.9**t); v=1-.999**t; vh=v/(1-.999**t)
fig,axes=new_fig(13,5.5,ncols=2)
axes[0].plot(t,m,color=C.INK); axes[0].plot(t,mh,color=C.GRAY,ls='--'); axes[0].set(xlabel='$t$',ylabel='值',xlim=(1,40),ylim=(0,1.08)); label(axes[0],'$m_t$',(14,m[14]),offset=(5,5)); label(axes[0],r'$\hat m_t$',(26,1),offset=(5,-12),color=C.GRAY)
axes[1].plot(t,v,color=C.INK); axes[1].plot(t,vh,color=C.GRAY,ls='--'); axes[1].set(xlabel='$t$',ylabel='值',xlim=(1,40),ylim=(0,1.08)); label(axes[1],'$s_t$',(24,v[24]),offset=(5,5)); label(axes[1],r'$\hat s_t$',(26,1),offset=(5,-12),color=C.GRAY)
fig.subplots_adjust(wspace=.35); save(fig,'M1-n6')
