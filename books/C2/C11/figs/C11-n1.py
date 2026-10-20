import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Arc, Rectangle

fig, axes = new_fig(16, 5.2, ncols=3)
specs = [
    (r"$x=a\sin t$", r"$x$", r"$\sqrt{a^2-x^2}$", r"$a$", {'v','h'}, (.08, .10)),
    (r"$x=a\tan t$", r"$x$", r"$a$", r"$\sqrt{a^2+x^2}$", {'v','b'}, (.125, .375)),
    (r"$x=a\sec t$", r"$\sqrt{x^2-a^2}$", r"$a$", r"$x$", {'b','h'}, (.08, .10)),
]
for ax, (title, lv, lb, lh, known, hpos) in zip(axes, specs):
    p2, p3 = (1.65, 0), (0, 1.15)
    # 三边：代换式已知的边画粗实线，勾股定理得到的第三边画虚线
    ax.plot([p3[0], p2[0]], [p3[1], p2[1]], color=C.INK,
            ls='-' if 'h' in known else '--', lw=2.2 if 'h' in known else 1.4)
    ax.plot([0, p2[0]], [0, 0], color=C.INK,
            ls='-' if 'b' in known else '--', lw=2.2 if 'b' in known else 1.4)
    ax.plot([0, p3[0]], [0, p3[1]], color=C.INK,
            ls='-' if 'v' in known else '--', lw=2.2 if 'v' in known else 1.4)
    # 直角方框放在直角顶点的三角形内侧
    ax.add_patch(Rectangle((0, 0), .10, .10, facecolor=C.PAPER, edgecolor=C.INK, lw=1))
    # 角 t 在右下方的锐角顶点
    theta = np.degrees(np.arctan2(p3[1]-p2[1], p3[0]-p2[0]))
    ax.add_patch(Arc(p2, .72, .72, angle=0, theta1=theta, theta2=180, color=C.INK, lw=1.1))
    mid = np.deg2rad((theta + 180) / 2)
    label(ax, '$t$', (p2[0] + .50*np.cos(mid), .50*np.sin(mid)),
          ha='center', va='center', fontsize=9)
    label(ax, lb, (p2[0]/2, -.18), ha='center', va='top')
    label(ax, lv, (-.14, p3[1]/2), ha='right', va='center')
    label(ax, lh, ((p3[0]+p2[0])/2+hpos[0], (p3[1]+p2[1])/2+hpos[1]), ha='center', va='bottom')
    label(ax, title, (1.0, 1.55), ha='center', va='bottom')
    ax.set(xlim=(-.55,2.05), ylim=(-.42,1.8), aspect='equal'); ax.axis('off')
fig.text(0.5, 0.015, r'$a>0$，图中 $x>0$（正边长）', ha='center', va='bottom')
save(fig, 'C11-n1')
