import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 14)
ax.set(xlim=(-0.5, 4.5), ylim=(-2.5, 2.5), aspect="equal")
theta = np.linspace(0, 2*np.pi, 721)
for level in [1, 4, 10, 20]:
    ax.plot(np.sqrt(level)*np.cos(theta), np.sqrt(level)/2*np.sin(theta),
            color=C.GRAY, lw=0.65, ls="-", zorder=0)

paths = {}
for eta, linestyle, marker in [(0.1, "-", "o"), (0.2, ":", "s"), (0.3, "--", "^")]:
    points = [np.array([4., 1.])]
    for _ in range(6):
        x, y = points[-1]
        points.append(points[-1] - eta*np.array([2*x, 8*y]))
    points = np.array(points)
    k = np.arange(7)
    assert np.allclose(points[:, 0], 4*(1-2*eta)**k)
    assert np.allclose(points[:, 1], (1-8*eta)**k)
    paths[eta] = points
    visible = points[np.abs(points[:, 1]) <= 2.5]
    name = {0.1: "实线", 0.2: "点线", 0.3: "虚线"}[eta]
    ax.plot(visible[:, 0], visible[:, 1], color=C.INK, ls=linestyle, lw=1.7,
            marker=marker, ms=5, mfc=C.INK if eta == 0.1 else C.PAPER,
            mec=C.INK, mew=1, label=rf"$\eta={eta}$ {name}", zorder=3)

assert np.sum(np.abs(paths[0.3][:, 1]) <= 2.5) == 3
# η=0.3 的下一步 (0.256,-2.744) 已在图外：从最后一个可见点朝它画一段虚线，
# 只画到图框下边缘，不加任何标记，也不画图外的点。
last, nxt = paths[0.3][2], paths[0.3][3]
assert np.allclose(last, (0.64, 1.96)) and np.allclose(nxt, (0.256, -2.744))
y_edge = ax.get_ylim()[0]
t = (y_edge - last[1]) / (nxt[1] - last[1])
edge = last + t*(nxt - last)
assert -0.5 < edge[0] < 4.5
ax.plot([last[0], edge[0]], [last[1], edge[1]], color=C.INK, ls="--", lw=1.7,
        marker="none", zorder=2, clip_on=True)
label(ax, "继续发散", (0.33, -1.86), offset=(7, 0), ha="left", va="center")
label(ax, "$(4,1)$", (4, 1), offset=(0, 11), ha="center")
ax.set_xticks([0, 1, 2, 3, 4])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel("$x$", loc="right")
ax.set_ylabel("$y$", rotation=0, loc="top")
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=3,
          fontsize=8.5, handlelength=2.2, columnspacing=1.0, handletextpad=0.5)
fig.subplots_adjust(left=0.13, right=0.97, bottom=0.1, top=0.87)
save(fig, "C22-n4")
