import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

S = np.array([[.8,.1,.3],[.2,.7,0],[.1,.2,.9]])
tau = .5
P = np.exp((S-S.max(axis=1,keepdims=True))/tau)
P /= P.sum(axis=1,keepdims=True)
loss = -np.log(P.diagonal())
assert np.allclose(P.sum(axis=1),1)
fig, ax = new_fig(16, 11)
for i in range(3):
    ax.text(-.15,i+.5,f'图片 {i+1}',ha='right',va='center')
    ax.text(i+.5,-.17,f'文字 {i+1}',ha='center',va='bottom')
    for j in range(3):
        ax.add_patch(Rectangle((j,i),1,1,facecolor=C.LIGHT if i==j else C.PAPER,edgecolor=C.INK,lw=2 if i==j else .6,zorder=3 if i==j else 1))
        ax.text(j+.5,i+.30,f'{S[i,j]:.1f}',ha='center',va='center',zorder=4)
        ax.text(j+.5,i+.72,f'{P[i,j]:.4f}',ha='center',va='center',zorder=4)
    ax.text(3.2,i+.5,rf'$\ell_{i+1}={loss[i]:.3f}$',va='center')
ax.text(1.5,-.75,r'上：$S_{ij}$　下：行 softmax 概率（$\tau=0.5$）',ha='center',fontsize=9)
ax.text(1.5,3.55,rf'三行平均 $\approx {loss.mean():.4f}$；$\ln 3={np.log(3):.4f}$',ha='center')
ax.set(xlim=(-.9,4.4),ylim=(3.9,-1),aspect='equal'); ax.axis('off')
save(fig, "M9-n7")
