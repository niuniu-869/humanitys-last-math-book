import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


def draw_arc(ax, p1, p2, text, radius=0.38, clockwise=False):
    a1 = np.arctan2(p1[1], p1[0])
    a2 = np.arctan2(p2[1], p2[0])
    if clockwise:
        while a2 >= a1:
            a2 -= 2 * np.pi
    else:
        while a2 <= a1:
            a2 += 2 * np.pi
    angles = np.linspace(a1, a2, 80)
    ax.plot(radius * np.cos(angles), radius * np.sin(angles), color=C.GRAY, lw=1.0, zorder=5)
    t = angles[-1]
    end = np.array([radius * np.cos(t), radius * np.sin(t)])
    tangent = np.array([-np.sin(t), np.cos(t)]) * (1 if not clockwise else -1)
    ax.annotate("", xy=tuple(end), xytext=tuple(end - 0.12 * tangent),
                arrowprops=dict(arrowstyle="-|>", color=C.GRAY, lw=1.0, mutation_scale=9,
                                shrinkA=0, shrinkB=0), zorder=6)
    mid = angles[len(angles) // 2]
    if text:
        label(ax, text, (0.80 * radius * np.cos(mid), 0.80 * radius * np.sin(mid)),
          offset=(0, 0), color=C.INK, ha="center", va="center")


def setup(ax):
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(-1.5, 3.5)
    ax.set_ylim(-1.5, 3.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axhline(0, color=C.LIGHT, lw=0.7, zorder=0)
    ax.axvline(0, color=C.LIGHT, lw=0.7, zorder=0)


fig, axs = new_fig(19.0, 12.5, nrows=2, ncols=3)
axs = np.asarray(axs)
for ax in list(axs.flat)[:5]:
    setup(ax)
axs[1, 2].axis("off")
fig.subplots_adjust(left=0.03, right=0.97, top=0.98, bottom=0.12, hspace=0.62, wspace=0.12)

square = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]], dtype=float)
# (ax, title, image, e1, e2, clockwise, pos of 第1列, pos of 第2列)
items = [
    (axs[0, 0], "① 对称伸缩：行列式 3\n面积 3，逆时针", np.array([[0, 0], [2, 1], [3, 3], [1, 2], [0, 0]], float),
     np.array([2.0, 1.0]), np.array([1.0, 2.0]), False, (2.55, 0.55), (0.35, 2.45)),
    (axs[0, 1], "② 剪切：行列式 1\n面积 1，逆时针", np.array([[0, 0], [1, 0], [2, 1], [1, 1], [0, 0]], float),
     np.array([1.0, 0.0]), np.array([1.0, 1.0]), False, (1.0, -0.5), (0.45, 1.55)),
    (axs[0, 2], "③ 转 90°：行列式 1\n面积 1，逆时针", np.array([[0, 0], [0, 1], [-1, 1], [-1, 0], [0, 0]], float),
     np.array([0.0, 1.0]), np.array([-1.0, 0.0]), False, (0.2, 1.5), (-1.0, -0.5)),
    (axs[1, 0], "④ 投影：行列式 0\n压成线段，面积 0", None,
     np.array([0.5, 0.5]), np.array([0.5, 0.5]), False, None, None),
    (axs[1, 1], "反射：行列式 −1\n面积 1，顺时针（翻面）", np.array([[0, 0], [1, 0], [1, -1], [0, -1], [0, 0]], float),
     np.array([1.0, 0.0]), np.array([0.0, -1.0]), True, (1.75, 0.3), (-0.75, -1.1)),
]

for ax, title, image, e1, e2, clockwise, p1, p2 in items:
    ax.plot(square[:, 0], square[:, 1], color=C.GRAY, lw=1.15, ls="--", zorder=2)
    if image is not None:
        ax.fill(image[:, 0], image[:, 1], color=C.LIGHT, alpha=0.76, zorder=1)
        ax.plot(image[:, 0], image[:, 1], color=C.INK, lw=1.55, zorder=3)
    else:
        ax.plot([0, 1], [0, 1], color=C.INK, lw=3.0, zorder=3)
        label(ax, "像：这条线段", (1.95, 1.25), offset=(0, 0), color=C.INK, ha="center", va="center")

    if np.allclose(e1, e2):
        arrow(ax, np.array([0.0, 0.0]), e1, color=C.INK, lw=1.8, offset=(7, 7))
        label(ax, "两列重合于 (0.5, 0.5)", (1.55, -0.45), offset=(0, 0), color=C.INK, ha="center", va="center")
    else:
        arrow(ax, np.array([0.0, 0.0]), e1, color=C.INK, lw=1.65, offset=(5, 6))
        arrow(ax, np.array([0.0, 0.0]), e2, color=C.GRAY, lw=1.65, offset=(5, 6))
        label(ax, "第1列", tuple(p1), offset=(0, 0), color=C.INK, ha="center", va="center")
        label(ax, "第2列", tuple(p2), offset=(0, 0), color=C.GRAY, ha="center", va="center")
        draw_arc(ax, e1, e2, "", radius=0.42, clockwise=clockwise)
    ax.set_title(title, y=-0.27, pad=0, color=C.INK)

save(fig, "L6-n3")
