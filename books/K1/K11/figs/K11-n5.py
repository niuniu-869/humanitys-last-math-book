import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, label
from matplotlib.patches import Ellipse, Polygon

# ---------------------------------------------------------------------------
# 几何：全部赋值 ⊃ B 为真的赋值 ⊃ 前提全真的赋值
# 椭圆用半轴表示，右图把灰色椭圆右移，使其约四分之一面积落在虚线圈外。
# ---------------------------------------------------------------------------
OX, OY, OA, OB = 0.0, 0.05, 4.70, 2.70      # 大椭圆（全部赋值）
DX, DY, DA, DB = 0.0, 0.05, 3.30, 1.85      # 虚线圈（B 为真的赋值）
GA, GB = 2.05, 1.15                         # 浅灰椭圆半轴
GX_OK, GY_OK = -0.05, -0.25                 # 有效时：灰圈完全在虚线圈内
GX_BAD, GY_BAD = 2.20, -0.25                # 无效时：灰圈右移，约 1/4 在外


def ellipse(cx, cy, a, b, **kw):
    return Ellipse((cx, cy), 2 * a, 2 * b, **kw)


def epoint(cx, cy, a, b, t):
    return cx + a * np.cos(t), cy + b * np.sin(t)


def e_norm(x, y, cx, cy, a, b):
    return ((x - cx) / a) ** 2 + ((y - cy) / b) ** 2


def g_crossings(cx, cy, a, b):
    """灰椭圆与虚线圈的两个交点（参数 t）。"""
    ts = np.linspace(0.0, 2 * np.pi, 7201)
    px, py = epoint(cx, cy, a, b, ts)
    vals = e_norm(px, py, DX, DY, DA, DB) - 1.0
    roots = []
    for i in range(len(ts) - 1):
        v0, v1 = vals[i], vals[i + 1]
        if v0 == 0.0:
            roots.append(ts[i])
        elif v0 * v1 < 0:
            lo, hi = ts[i], ts[i + 1]
            for _ in range(60):
                mid = (lo + hi) / 2
                mx, my = epoint(cx, cy, a, b, mid)
                if (e_norm(mx, my, DX, DY, DA, DB) - 1.0) * v0 <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
    roots.sort()
    # 去掉重合根
    out = [roots[0]]
    for r in roots[1:]:
        if abs(r - out[-1]) > 1e-6:
            out.append(r)
    return out


def cap_polygon(cx, cy, a, b):
    """灰椭圆落在虚线圈外的部分：灰弧 + 虚线圈弧围成的闭合多边形。"""
    t0, t1 = g_crossings(cx, cy, a, b)
    xm, ym = epoint(cx, cy, a, b, (t0 + t1) / 2)
    if e_norm(xm, ym, DX, DY, DA, DB) < 1.0:   # 中点在内侧，外弧是另一段
        t0, t1 = t1, t0 + 2 * np.pi
    t_arc = np.linspace(t0, t1, 241)
    gx, gy = epoint(cx, cy, a, b, t_arc)
    p0 = np.array([gx[0], gy[0]])
    p1 = np.array([gx[-1], gy[-1]])

    s0 = np.arctan2((p0[1] - DY) / DB, (p0[0] - DX) / DA)
    s1 = np.arctan2((p1[1] - DY) / DB, (p1[0] - DX) / DA)

    def d_arc(sa, sb):
        if sb < sa:
            sb += 2 * np.pi
        ss = np.linspace(sa, sb, 181)
        return DX + DA * np.cos(ss), DY + DB * np.sin(ss)

    cands = [d_arc(s0, s1), d_arc(s1, s0 + 2 * np.pi)]
    best = None
    for dxs, dys in cands:
        k = len(dxs) // 2
        if e_norm(dxs[k], dys[k], cx, cy, a, b) < 1.0:
            best = (dxs, dys)
            break
    dxs, dys = best
    dpts = np.column_stack([dxs, dys])
    # 接在灰弧 p0 → p1 后面，须从 p1 回到 p0
    if np.hypot(*(dpts[0] - p0)) < np.hypot(*(dpts[0] - p1)):
        dpts = dpts[::-1]
    verts = np.vstack([np.column_stack([gx, gy]), dpts])
    # 去掉与首点重合的末点
    if np.hypot(*(verts[0] - verts[-1])) < 1e-9:
        verts = verts[:-1]
    # 保证逆时针（仅为稳定，填充不依赖方向）
    area = 0.5 * np.sum(verts[:, 0] * np.roll(verts[:, 1], -1)
                        - np.roll(verts[:, 0], -1) * verts[:, 1])
    if area < 0:
        verts = verts[::-1]
    return verts


def nested(ax, invalid=False):
    # 大椭圆：全部赋值
    ax.add_patch(ellipse(OX, OY, OA, OB, facecolor=C.PAPER,
                         edgecolor=C.INK, lw=1.5, zorder=1))
    gx, gy = (GX_BAD, GY_BAD) if invalid else (GX_OK, GY_OK)
    # 浅灰椭圆：前提全真的赋值
    ax.add_patch(ellipse(gx, gy, GA, GB, facecolor=C.LIGHT,
                         edgecolor=C.INK, lw=1.2, zorder=2))
    if invalid:
        # 虚线圈外的那一块：深灰 + 斜线
        cap = cap_polygon(gx, gy, GA, GB)
        ax.add_patch(Polygon(cap, closed=True, facecolor=C.AMBER,
                             edgecolor=C.INK, lw=0.0, hatch='//', zorder=2.5))
    # 虚线圈：B 为真的赋值（压在灰圈上，边界连续）
    ax.add_patch(ellipse(DX, DY, DA, DB, facecolor='none',
                         edgecolor=C.INK, lw=1.4, ls='--', zorder=4))
    # 灰圈轮廓再描一遍（实线），保证和虚线圈相交处清晰
    ax.add_patch(ellipse(gx, gy, GA, GB, facecolor='none',
                         edgecolor=C.INK, lw=1.2, zorder=4.2))

    # 标签位置：全部避开椭圆边线
    label(ax, '全部赋值', (0.0, 2.32), ha='center', va='center', fontsize=8.5)
    label(ax, '$B$ 为真的赋值', (0.0, 1.32), ha='center', va='center', fontsize=8.5)
    if invalid:
        # 灰圈在虚线圈内的那一段的中心（文字左右留白相同）
        half = DA * np.sqrt(max(0.0, 1.0 - ((gy - DY) / DB) ** 2))
        lx = (gx - GA + DX + half) / 2
    else:
        lx = gx
    label(ax, '前提全真的赋值', (lx, gy - 0.03), ha='center', va='center', fontsize=8.5)

    ax.set(xlim=(-5.0, 5.0), ylim=(-3.38, 3.38)); ax.set_aspect('equal'); ax.axis('off')


fig, (ax, inset) = new_fig(16.5, 8.6, ncols=2, gridspec_kw={'width_ratios': [1, 1]})
fig.subplots_adjust(left=0.005, right=0.995, bottom=0.01, top=0.99, wspace=0.02)

nested(ax, invalid=False)
nested(inset, invalid=True)
label(ax, '有效时', (0, 2.92), ha='center', va='bottom', fontsize=10)
label(inset, '无效时', (0, 2.92), ha='center', va='bottom', fontsize=10)

# 反例行标注：文字在所有椭圆外的下方空白处，箭头指向伸出块的中间
label(inset, '这一块是反例行', (1.65, -3.09), ha='center', va='center', fontsize=8.5)
arrow(inset, (3.08, -2.95), (0.47, 2.50), color=C.INK, lw=1.2)

save(fig, 'K11-n5')
