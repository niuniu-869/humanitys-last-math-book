import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(11.2, 7.0)

theta = np.linspace(0.05, 0.95, 800)
loss = -0.7 * np.log(theta) - 0.3 * np.log(1 - theta)
ax.plot(theta, loss, color=C.BLUE, lw=2.0)

theta_hat = 0.7
min_loss = -0.7 * np.log(0.7) - 0.3 * np.log(0.3)
loss_half = -0.7 * np.log(0.5) - 0.3 * np.log(0.5)
ax.axhline(min_loss, color=C.GRAY, lw=1.1, ls="--")
label(ax, "$H(\\hat p)$", (0.92, min_loss), offset=(0, 5), color=C.INK, ha="right")
dot(ax, (theta_hat, min_loss), "0.6109", color=C.BLUE, offset=(7, -15), size=28)

dot(ax, (0.5, loss_half), "0.6931", color=C.BLUE, offset=(-48, 10), size=28)
ax.annotate("", xy=(0.5, min_loss), xytext=(0.5, loss_half),
            arrowprops=dict(arrowstyle="<->", color=C.RED, lw=1.5, shrinkA=0, shrinkB=0, mutation_scale=10))
label(ax, "$D(\\hat p\\|q_\\theta)=0.0823$", (0.5, (loss_half + min_loss) / 2),
      offset=(9, 16), color=C.INK, ha="left", va="center")

ax.set_xlim(0.05, 0.95)
ax.set_ylim(0.55, 1.0)
ax.set_xlabel("$\\theta$")
ax.set_ylabel("$-0.7\\ln\\theta-0.3\\ln(1-\\theta)$（奈特）")
ax.set_xticks([0.1, 0.3, 0.5, 0.7, 0.9])
ax.set_yticks([0.6, 0.7, 0.8, 0.9, 1.0])
save(fig, "P14-n6")
