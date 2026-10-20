import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label


theta = 0.5
q = np.array([2.0, 1.0])
k = np.array([1.0, 1.0])
ALPHA = np.arctan2(q[0] * k[1] - q[1] * k[0],
                   q[0] * k[0] + q[1] * k[1])   # q 与 k 的夹角，约 0.32175 rad
DELTA = 1.0                                        # (n-m)theta，两幅图都是 1 rad


def rot(v, a):
    return np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]]) @ v


def angle_between(a, b):
    """从 a 逆时针转到 b 的角，落在 [0, 2π)。"""
    return (np.arctan2(b[1], b[0]) - np.arctan2(a[1], a[0])) % (2 * np.pi)


def vec_arrow(ax, v, ls="-"):
    """从原点画向量；实线=转之前，虚线=转之后（与图注一致）。"""
    ax.annotate("", xy=tuple(v), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=C.INK, lw=1.55,
                                ls=ls, shrinkA=0, shrinkB=0, mutation_scale=11),
                zorder=4)


def arc(ax, a0, a1, r, ls):
    t = np.linspace(a0, a1, 200)
    ax.plot(r * np.cos(t), r * np.sin(t), color=C.GRAY, ls=ls, lw=1.0, zorder=2)


def panel(ax, title, rq, rk, post_lab, rq_lab, rk_lab):
    ax.set_aspect("equal")
    ax.set_xlim(-2.5, 2.5); ax.set_ylim(-2.5, 2.5)
    ax.axhline(0, color=C.LIGHT, lw=0.7, zorder=0)
    ax.axvline(0, color=C.LIGHT, lw=0.7, zorder=0)
    ax.set_xticks([-2, 0, 2]); ax.set_yticks([-2, 0, 2])
    ax.set_title(title)

    # 图注约定：实线是转之前，虚线是转之后；两类箭头都直接标名称。
    vec_arrow(ax, q, "-"); vec_arrow(ax, k, "-")
    vec_arrow(ax, rq, "--"); vec_arrow(ax, rk, "--")

    label(ax, "$q$", (2.10, 0.88), ha="left", va="center", fontsize=10)
    label(ax, "$k$", (1.08, 1.02), ha="left", va="center", fontsize=10)
    label(ax, "$R(m\\theta)q$", rq_lab[0], ha=rq_lab[1], va=rq_lab[2], fontsize=8.8)
    label(ax, "$R(n\\theta)k$", rk_lab[0], ha=rk_lab[1], va=rk_lab[2], fontsize=8.8)

    # 转之前的小弧，标注 α 放在两条箭头之间的角平分线上，不压箭头。
    aq, ak = np.arctan2(q[1], q[0]), np.arctan2(k[1], k[0])
    arc(ax, aq, ak, 0.55, "-")
    mid0 = (aq + ak) / 2
    label(ax, "$\\alpha$", (0.85 * np.cos(mid0), 0.85 * np.sin(mid0)),
          ha="center", va="center", fontsize=9)

    # 转之后的大弧。m<n 时两条向量转过的角度不同，夹角增加 (n-m)theta。
    bq, bk = np.arctan2(rq[1], rq[0]), np.arctan2(rk[1], rk[0])
    if bk <= bq:
        bk += 2 * np.pi
    arc(ax, bq, bk, 0.95, "--")
    # 标注放在弧线外、两箭头之间，同时避开水平零轴。
    label(ax, "$\\alpha+1$", post_lab, ha="center", va="center", fontsize=9)

    # 线型说明放在各子图左上角的空白处。
    label(ax, "实线：转之前　虚线：转之后", (-2.42, 2.40),
          ha="left", va="top", fontsize=7.2)

    # 夹角数值说明放在左下空白处，避开所有箭头和弧线。
    label(ax, "转之前夹角 $\\alpha$\n转之后夹角 $\\alpha+(n-m)\\theta=\\alpha+1$",
          (-2.42, -1.45), ha="left", va="top", fontsize=7.4, linespacing=1.35)

    label(ax, "点积都是 0.7794", (0, -2.30), ha="center", va="center", fontsize=9.2)


fig, axes = new_fig(16.8, 7.6, ncols=2)
fig.subplots_adjust(left=0.055, right=0.985, bottom=0.075, top=0.92, wspace=0.18)

rq1, rk1 = rot(q, theta), rot(k, 3 * theta)
rq2, rk2 = rot(q, 4 * theta), rot(k, 6 * theta)
assert abs(np.dot(rq1, rk1) - 0.7794) < 5e-4
assert abs(np.dot(rq2, rk2) - 0.7794) < 5e-4
assert abs(angle_between(rq1, rk1) - (ALPHA + DELTA)) < 1e-9
assert abs(angle_between(rq2, rk2) - (ALPHA + DELTA)) < 1e-9

panel(axes[0], "$m=1,\\ n=3$", rq1, rk1, (0.02, 1.18),
      ((1.18, 1.92), "right", "bottom"), ((-1.02, 1.10), "center", "center"))
panel(axes[1], "$m=4,\\ n=6$", rq2, rk2, (-1.30, -0.18),
      ((-1.74, 1.55), "center", "bottom"), ((-1.13, -1.02), "center", "top"))

save(fig, "M12-n4")
