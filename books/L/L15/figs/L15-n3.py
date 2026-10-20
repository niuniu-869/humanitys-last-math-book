import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def right_angle(ax, u, v, size=0.16):
    u = np.asarray(u, dtype=float); u = u / np.linalg.norm(u)
    v = np.asarray(v, dtype=float); v = v / np.linalg.norm(v)
    p1 = size * u
    p2 = size * (u + v)
    p3 = size * v
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]],
            color=C.INK, lw=0.9, zorder=5)


def setup(ax):
    ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.8, 1.8)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([-1, 0, 1]); ax.set_yticks([-1, 0, 1])
    ax.axhline(0, color=C.GRAY, lw=0.7, zorder=0)
    ax.axvline(0, color=C.GRAY, lw=0.7, zorder=0)
    ax.tick_params(labelsize=8, pad=1)


fig, axes = new_fig(28.5, 7.6, ncols=4)
fig.subplots_adjust(wspace=0.42, left=0.035, right=0.985, bottom=0.18, top=0.86)
t = np.linspace(0.0, 2.0 * np.pi, 600)
circle = np.vstack([np.cos(t), np.sin(t)])

phi = 1.618034
v1 = np.array([0.525731, 0.850651])
v2 = np.array([-0.850651, 0.525731])
u1 = np.array([0.850651, 0.525731])
u2 = np.array([-0.525731, 0.850651])
s1, s2 = 1.618034, 0.618034
out1 = np.array([1.376382, 0.850651])
out2 = np.array([-0.324920, 0.525731])

# ① 输入
ax = axes[0]; setup(ax)
ax.plot(circle[0], circle[1], color=C.INK, lw=1.15)
arrow(ax, (0, 0), v1, color=C.INK, lw=2.0)
arrow(ax, (0, 0), v2, color=C.INK, lw=1.35)
label(ax, r"$\boldsymbol{v}_1$", tuple(v1), offset=(5, 4))
label(ax, r"$\boldsymbol{v}_2$", tuple(v2), offset=(-6, 2), ha="right")
right_angle(ax, v1, v2)
dot(ax, (0, 0), size=14)
ax.set_title("① 输入", pad=8)

# ② V^T 后
ax = axes[1]; setup(ax)
ax.plot(circle[0], circle[1], color=C.INK, lw=1.15)
e1, e2 = np.array([1.0, 0.0]), np.array([0.0, 1.0])
arrow(ax, (0, 0), e1, color=C.INK, lw=2.0)
arrow(ax, (0, 0), e2, color=C.INK, lw=1.35)
label(ax, r"$V^{T}\boldsymbol{v}_1=\boldsymbol{e}_1$", tuple(e1), offset=(-18, -16), ha="right")
label(ax, r"$V^{T}\boldsymbol{v}_2=\boldsymbol{e}_2$", tuple(e2), offset=(6, 3))
right_angle(ax, e1, e2)
dot(ax, (0, 0), size=14)
ax.set_title("② 转正以后", pad=8)

# ③ Sigma 后
ax = axes[2]; setup(ax)
ax.plot(circle[0], circle[1], color=C.LIGHT, lw=1.0, ls="--")
ax.plot(s1 * np.cos(t), s2 * np.sin(t), color=C.INK, lw=1.2)
arrow(ax, (0, 0), (s1, 0), color=C.INK, lw=2.0)
arrow(ax, (0, 0), (0, s2), color=C.INK, lw=1.35)
label(ax, r"$\sigma_1\boldsymbol{e}_1$（长 1.618）", (s1, 0), offset=(-20, -16), ha="right")
label(ax, r"$\sigma_2\boldsymbol{e}_2$（长 0.618）", (0, s2), offset=(7, 4))
dot(ax, (0, 0), size=14)
ax.set_title("③ 伸缩以后", pad=8)

# ④ U 后，即 A 直接作用
ax = axes[3]; setup(ax)
ax.plot(circle[0], circle[1], color=C.LIGHT, lw=1.0, ls="--")
ax.plot(np.cos(t) + np.sin(t), np.sin(t), color=C.INK, lw=1.2)
arrow(ax, (0, 0), out1, color=C.INK, lw=2.0)
arrow(ax, (0, 0), out2, color=C.INK, lw=1.35)
label(ax, r"$\sigma_1\boldsymbol{u}_1$", tuple(out1), offset=(6, -2), ha="left")
label(ax, r"$\sigma_2\boldsymbol{u}_2$", tuple(out2), offset=(-5, 5), ha="right")
right_angle(ax, out1, out2, size=0.16)
dot(ax, (0, 0), size=14)
ax.set_title(r"④ 再转：就是 $A\boldsymbol{x}$", pad=8)

# 面板间步骤箭头与短标签
for x0, x1, txt in [(0.236, 0.272, r"$V^{T}$（转）"),
                    (0.476, 0.512, r"$\Sigma$（沿轴伸缩）"),
                    (0.716, 0.752, r"$U$（转）")]:
    axes[0].annotate("", xy=(x1, 0.54), xycoords=fig.transFigure,
                     xytext=(x0, 0.54), textcoords=fig.transFigure,
                     arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.25,
                                     shrinkA=0, shrinkB=0, mutation_scale=10))
    fig.text((x0 + x1) / 2, 0.59, txt, ha="center", va="bottom", color=C.INK, fontsize=9)

save(fig, "L15-n3")
