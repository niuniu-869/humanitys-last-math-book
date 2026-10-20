import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig3d(22, 11, elev=24, azim=35)
ax.set_position([.01,.17,.43,.71])
E = np.eye(3)
for i in range(3):
    ax.plot(*np.stack([np.zeros(3), E[i]]).T, color=C.INK, lw=1, alpha=.55)
    ax.scatter(*E[i], color=C.INK, s=28, alpha=.55)
    j = (i+1)%3
    assert np.isclose(np.linalg.norm(E[i]-E[j]), np.sqrt(2))
    ax.plot(*np.stack([E[i], E[j]]).T, color=C.INK, ls='--', alpha=.55)
    pos = E[i]*1.25
    ax.text(*pos, ['$e$猫','$e$狗','$e$鱼'][i], ha='center', fontsize=10)
ax.set(xlim=(0,1.25), ylim=(0,1.25), zlim=(0,1.25))
ax.set_box_aspect((1,1,1))
ax.set_axis_off()
ax.set_title('独热向量（$V=3$ 的示意）', pad=6)
fig.text(.225,.13, r'三条虚线边长均为 $\sqrt{2}$', ha='center')
bx = fig.add_axes([.55,.23,.42,.65])
points = {'猫':(1,.2), '狗':(.9,.4), '吃':(-.5,.8), '喝':(-.6,.6),
          '鱼':(.1,-.9), '骨头':(.2,-1), '牛奶':(-.3,-.8), '水':(-.2,-.9)}
offsets = {'猫':(7,-8),'狗':(5,8),'吃':(5,8),'喝':(-23,-10),
           '鱼':(9,7),'骨头':(7,-13),'牛奶':(-31,8),'水':(-20,-15)}
for w, p in points.items():
    bx.scatter(*p,s=28,edgecolors=C.INK,facecolors=C.INK if w in ['猫','狗','吃','鱼'] else C.PAPER,zorder=5)
    label(bx,w,p,offsets[w],fontsize=9)
for w in ['猫','狗','鱼']:
    arrow(bx,(0,0),points[w],color=C.INK,lw=.9)
bx.axhline(0,color=C.GRAY,lw=.6,ls=':')
bx.axvline(0,color=C.GRAY,lw=.6,ls=':')
bx.set(xlim=(-1,1.4),ylim=(-1.3,1.05),aspect='equal',title='嵌入向量（$d=2$）')
bx.set_xticks([-1,0,1]); bx.set_yticks([-1,0,1])
cos = lambda a,b: np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b)
fig.text(.76,.12, rf'cos(猫, 狗)$\approx {cos(points["猫"],points["狗"]):.3f}$',ha='center')
fig.text(.76,.06, rf'cos(猫, 鱼)$\approx {cos(points["猫"],points["鱼"]):.3f}$',ha='center')
save(fig, "M9-n2")
