import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

words = ['猫', '狗', '吃', '喝', '鱼', '骨头', '牛奶', '水']
A = np.array([[0,0,1,1,0,0,0,0], [0,0,2,1,0,0,0,0],
              [1,2,0,0,2,1,0,0], [1,1,0,0,0,0,1,1],
              [0,0,2,0,0,0,0,0], [0,0,1,0,0,0,0,0],
              [0,0,0,1,0,0,0,0], [0,0,0,1,0,0,0,0]])
assert np.array_equal(A, A.T)
fig, ax = new_fig(16, 12)
for i in range(8):
    for j in range(8):
        ax.add_patch(Rectangle((j, i), 1, 1, facecolor=[C.PAPER,C.LIGHT,C.AMBER][A[i,j]], edgecolor=C.GRAY, lw=.5))
        ax.text(j+.5, i+.5, str(A[i,j]), ha='center', va='center')
    ax.text(-.2, i+.5, words[i], ha='right', va='center')
    ax.text(i+.5, -.25, words[i], ha='center', va='bottom')
for i in [0,1,4,6]:
    ax.add_patch(Rectangle((0,i), 8, 1, fill=False, edgecolor=C.INK, lw=1.8, ls='-' if i<2 else '--'))
cos = np.dot(A[0], A[1])/np.linalg.norm(A[0])/np.linalg.norm(A[1])
label(ax, rf'$\cos={cos:.4f}$', (8.3,1), va='center')
ax.plot([8.15,8.35,8.35,8.15],[4.5,4.5,6.5,6.5],color=C.INK,ls='--',lw=1)
label(ax, r'$\cos=0$', (8.55,5.5), va='center')
ax.set(xlim=(-1,10.6), ylim=(8.2,-.8), aspect='equal')
ax.axis('off')
save(fig, "M9-n1")
