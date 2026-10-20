import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11, 6)
rng = np.random.default_rng(20261017)
arrivals = []
t = 0.0
while True:
    t += rng.exponential(1 / 3)
    if t > 2: break
    arrivals.append(t)
print("arrival_times=" + ", ".join(f"{t:.6f}" for t in arrivals))
times = [0.0] + arrivals + [2.0]
levels = np.arange(len(arrivals) + 1)
for i in range(len(levels)):
    ax.plot([times[i], times[i + 1]], [levels[i], levels[i]], color=C.INK, ls="-", lw=1.5)
    if i < len(arrivals):
        ax.plot([times[i + 1], times[i + 1]], [levels[i], levels[i + 1]], color=C.INK, ls="-", lw=1.5)
        ax.plot(times[i + 1], levels[i], marker="o", markersize=5, markerfacecolor=C.PAPER, markeredgecolor=C.INK, zorder=4)
        ax.plot(times[i + 1], levels[i + 1], marker="o", markersize=5, markerfacecolor=C.INK, markeredgecolor=C.INK, zorder=4)
for i in range(min(3, len(arrivals))):
    mid = (times[i] + times[i + 1]) / 2
    ax.annotate("", xy=(times[i + 1], -0.18), xytext=(times[i], -0.18),
                arrowprops=dict(arrowstyle="<->", color=C.INK, lw=1.0))
    label(ax, f"T_{i + 1}", (mid, -0.34), ha="center", va="top", fontsize=9)
ax.set_xlim(0, 2); ax.set_ylim(-0.55, max(3, len(arrivals) + 0.5))
ax.set_xlabel("时间（小时）"); ax.set_ylabel("N(t)")
save(fig, "P9-n6")
