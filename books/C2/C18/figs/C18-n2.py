import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

def momentum(h, t_end=4.0):
    a, c = 4.0, 2.0
    n = int(round(t_end / h))
    t = np.arange(n + 1) * h
    x = np.empty(n + 1)
    x_prev, x[0] = 1.0, 1.0
    beta, eta = 1.0 - c * h, h * h
    for k in range(n):
        x_next = x[k] - eta * a * x[k] + beta * (x[k] - x_prev)
        x_prev, x[k + 1] = x[k], x_next
    return t, x

t = np.linspace(0.0, 4.0, 1601)
x_exact = np.exp(-t) * (np.cos(np.sqrt(3.0) * t) + np.sin(np.sqrt(3.0) * t) / np.sqrt(3.0))
t1, x1 = momentum(0.1)
t2, x2 = momentum(0.05)

fig, ax = new_fig(14.5, 7.8)
ax.set_xlim(0.0, 4.0)
ax.set_ylim(-0.3, 1.05)
ax.set_xticks(np.arange(5))
ax.set_yticks([0.0, 0.5, 1.0])
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.7, zorder=0)
ax.axhline(0.0, color=C.GRAY, lw=0.85, zorder=1)

ax.plot(t, x_exact, color=C.BLUE, lw=2.0, ls="-", zorder=3, label="方程的解")
ax.scatter(t1, x1, s=25, marker="o", facecolors=C.PAPER, edgecolors=C.RED, linewidths=1.1, zorder=4, label="迭代点，$h=0.1$")
ax.scatter(t2[::2], x2[::2], s=17, marker="o", color=C.INK, zorder=4, label="迭代点，$h=0.05$")


ax.legend(loc="upper right", frameon=True, framealpha=1.0, edgecolor=C.GRAY)
ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$x(t)$")
save(fig, "C18-n2")
