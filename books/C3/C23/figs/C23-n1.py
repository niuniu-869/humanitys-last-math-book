import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from _h3 import *
V = View(-60, 14)
fig, ax = setup(12, 9.5)
k = 0.55
pt = lambda a: np.array([2*np.cos(a), 2*np.sin(a), k*a])
t0 = np.radians(-5)
t = np.linspace(t0-2.6, t0+3.6, 500)
P, Q1, Q2 = pt(t0), pt(t0+1.5), pt(t0+0.75)
T = np.array([-2*np.sin(t0), 2*np.cos(t0), k]); Tn = T/np.linalg.norm(T)
e1 = np.array([0, 0, 1.0]); e1 = e1 - (e1@Tn)*Tn; e1 /= np.linalg.norm(e1); e2 = np.cross(Tn, e1)
assert abs(e1@Tn) < 1e-9 and abs(e2@Tn) < 1e-9
# 法平面（浅灰阴影）
poly(ax, V, [P-1.7*e1-1.3*e2, P+1.7*e1-1.3*e2, P+1.7*e1+1.3*e2, P-1.7*e1+1.3*e2], z=1)
# 螺旋线：被法平面挡住的一侧用点线（t<t0 在平面后方近似处理为全程实线，只在平面内部分用点线）
line(ax, V, np.stack(pt(t), axis=0).T, lw=1.8, zorder=3)
for Q in (Q1, Q2):
    line(ax, V, [P, Q], lw=1.3, ls="--", zorder=4)
    dot3(ax, V, Q, 26)
arrow3(ax, V, P, 2.2*Tn)
dot3(ax, V, P, 40)
text3(ax, V, P, "$P$", off=(-14, -6), fontsize=13)
text3(ax, V, Q1, "$Q_1$", off=(5, 5), fontsize=13)
text3(ax, V, Q2, "$Q_2$", off=(6, -12), fontsize=13)
text3(ax, V, P+2.2*Tn, r"$\boldsymbol{T}$", off=(6, 2), fontsize=14)
text3(ax, V, P-1.7*e1-1.3*e2, "法平面", off=(-4, -12), fontsize=11)
save(fig, "C23-n1")
