import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axes = new_fig(16, 5.5, ncols=3, sharey=True)
for ax, n in zip(axes, (10, 100, 1000)):
    dt = 1 / n
    rng = np.random.default_rng(20261017)
    steps = rng.choice([-1.0, 1.0], size=n) * np.sqrt(dt)
    x = np.linspace(0, 1, n + 1)
    path = np.r_[0, np.cumsum(steps)]
    print(f"n={n}, endpoint={path[-1]:.6f}")
    t = np.linspace(0, 1, 501)
    ax.plot(x, path, color=C.INK, ls="-", lw=1.2)
    ax.plot(t, np.sqrt(t), color=C.GRAY, ls="--", lw=0.9)
    ax.plot(t, -np.sqrt(t), color=C.GRAY, ls="--", lw=0.9)
    ax.set_title(f"{n} 步")
    ax.set_xlim(0, 1); ax.set_ylim(-3, 3)
    ax.set_xlabel("时间")
axes[0].set_ylabel("位置")
save(fig, "P9-n5")
