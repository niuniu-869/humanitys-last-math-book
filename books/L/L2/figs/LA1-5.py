import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import C, arrow, dot, label, new_fig, new_fig3d, np, plt, save

fig, ax = new_fig(11.5, 7.5)

t = np.linspace(-3.0, 1.0, 400)
f1 = 10 * t**2 + 10 * t + 5        # a=(1,2), b=(3,1)：不共线（正文的例子）
f2 = 5 * t**2 + 20 * t + 20        # a=(2,4), b=(1,2)：共线，5(t+2)^2

ax.axhline(0, color=C.GRAY, lw=1.0, zorder=1)
ax.plot(t, f1, color=C.BLUE, lw=2.2, zorder=3)
ax.plot(t, f2, color=C.RED, lw=2.2, ls='--', zorder=3)

# 共线时抛物线切在 t 轴上
dot(ax, (-2.0, 0.0), color=C.RED, size=26)
label(ax, "虚线，共线的一对：$t=-2$ 处 $f=0$", (-2.0, 0.0), offset=(0, -20), color=C.RED, ha="center")

# 不共线时整条曲线在 t 轴上方
dot(ax, (-0.5, 2.5), color=C.BLUE, size=26)
ax.annotate("实线，正文的 $\\boldsymbol{a}=(1,2)^{\\mathsf{T}},\\boldsymbol{b}=(3,1)^{\\mathsf{T}}$：\n$f(t)=10t^2+10t+5$ 恒正，最小 $2.5$", xy=(-0.5, 2.5), xytext=(-1.95, 33),
            color=C.BLUE, ha="left", arrowprops=dict(arrowstyle="-", color=C.GRAY, lw=0.8), zorder=6)

ax.set_xlim(-3.05, 1.05)
ax.set_ylim(-8.0, 44.0)
ax.set_xticks([-3, -2, -1, 0, 1])
ax.set_yticks([0, 20, 40])
ax.set_xlabel("$t$")
ax.set_ylabel("$f(t)=\\Vert\\boldsymbol{a}+t\\boldsymbol{b}\\Vert^2$")
save(fig, "LA1-5")
