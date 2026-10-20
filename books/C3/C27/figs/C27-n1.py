import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(15, 8)
t = np.linspace(0, 5, 501)
ax.plot(t, 0.6*np.sin(1.2*t), color=C.INK, ls="-", lw=1.5)
arrow(ax, (4.87, 0.6*np.sin(1.2*4.87)),
      (0.13, 0.6*(np.sin(6)-np.sin(1.2*4.87))), color=C.INK)
dot(ax, (0, 0), "$A$", offset=(-13, -3))
dot(ax, (5, 0.6*np.sin(6)), "$B$", offset=(6, -5))
label(ax, "$L$", (2.15, 0.6*np.sin(1.2*2.15)), offset=(0, 9))

def step(t0, angle, index, message):
    p = np.array([t0, 0.6*np.sin(1.2*t0)])
    d = np.array([1., 0.72*np.cos(1.2*t0)])
    d /= np.linalg.norm(d)
    a = np.deg2rad(angle)
    rotation = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    dr = 0.8*d
    f = 1.1*(rotation @ d)
    proj = (f @ d)*d
    foot = p + proj
    assert np.isclose(np.linalg.norm(dr), 0.8)
    assert np.isclose(np.linalg.norm(f), 1.1)
    assert np.isclose(np.rad2deg(np.arccos(f @ d/1.1)), angle)
    assert np.isclose((p+f-foot) @ d, 0)
    assert np.isclose(foot @ d - p @ d, f @ d)

    if index == 1:
        # 顺风分量：沿 Δr 方向从起点到垂足的粗线（画在 Δr 箭头下层）
        ax.plot([p[0], foot[0]], [p[1], foot[1]], color=C.GRAY, lw=5.0,
                solid_capstyle="butt", zorder=2)
        # 从 F 末端向 Δr 所在直线作垂线（细点线）
        ax.plot([p[0]+f[0], foot[0]], [p[1]+f[1], foot[1]],
                color=C.GRAY, ls=":", lw=1.1, zorder=3)
        # 垂足处的小直角符号（小方框正好落在 Δr 尖端到垂足之间）
        u = f - proj
        u /= np.linalg.norm(u)
        s = 0.08
        q1 = foot - s*d
        q2 = foot - s*d + s*u
        q3 = foot + s*u
        ax.plot([q1[0], q2[0], q3[0]], [q1[1], q2[1], q3[1]],
                color=C.INK, lw=0.9, zorder=6)

    else:
        # 逆风：垂足落在 Δr 的反向延长线上
        ax.plot([p[0], foot[0]], [p[1], foot[1]], color=C.GRAY, ls=":", lw=1)
        ax.plot([p[0]+f[0], foot[0]], [p[1]+f[1], foot[1]],
                color=C.GRAY, ls=":", lw=1)

    arrow(ax, p, dr, color=C.INK, lw=2.5)
    ax.annotate("", xy=p+f, xytext=p, arrowprops=dict(
        arrowstyle="-|>", color=C.INK, lw=1.5, ls="--",
        shrinkA=0, shrinkB=0, mutation_scale=12))
    dot(ax, p, "$P_%d$" % index, offset=(-15, -14), size=19)
    if index == 1:
        label(ax, r"$\Delta\mathbf{r}$", p+0.6*dr, offset=(0, 10), ha="center")
        label(ax, "顺风分量", foot, offset=(10, 7), fontsize=9)
    else:
        label(ax, r"$\Delta\mathbf{r}$", p+dr, offset=(8, 2))
    label(ax, r"$\mathbf{F}$", p+f, offset=(0, 7))
    label(ax, message, (t0-0.35, -1.15), fontsize=10)

step(0.8, 35, 1, r"顺风：$\mathbf{F}\cdot\Delta\mathbf{r}>0$")
step(3.6, 140, 2, r"逆风：$\mathbf{F}\cdot\Delta\mathbf{r}<0$")
ax.set_aspect("equal")
ax.set_xlim(-0.45, 5.55)
ax.set_ylim(-1.45, 1.85)
ax.axis("off")
save(fig, "C27-n1")
