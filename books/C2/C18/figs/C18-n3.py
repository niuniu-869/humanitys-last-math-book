import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

t = np.linspace(0.0, 5.0, 2001)
x_c2 = np.exp(-t) * (np.cos(np.sqrt(3.0) * t) + np.sin(np.sqrt(3.0) * t) / np.sqrt(3.0))
x_c4 = (1.0 + 2.0 * t) * np.exp(-2.0 * t)
sqrt21 = np.sqrt(21.0)
x_c10 = (0.5 + 5.0 * sqrt21 / 42.0) * np.exp((-5.0 + sqrt21) * t) + (0.5 - 5.0 * sqrt21 / 42.0) * np.exp(-(5.0 + sqrt21) * t)

fig, ax = new_fig(14.5, 7.8)
ax.set_xlim(0.0, 5.0)
ax.set_ylim(-0.3, 1.05)
ax.set_xticks(np.arange(6))
ax.set_yticks([0.0, 0.5, 1.0])
ax.grid(True, color=C.LIGHT, lw=0.7, alpha=0.7, zorder=0)
ax.axhline(0.0, color=C.GRAY, lw=0.85, zorder=1)

ax.plot(t, x_c2, color=C.BLUE, lw=2.0, ls="-", zorder=3)
ax.plot(t, x_c4, color=C.RED, lw=1.7, ls="--", zorder=3)
ax.plot(t, x_c10, color=C.TEAL, lw=1.7, ls=":", zorder=3)

label(ax, "$c=2$", (2.35, -0.215), offset=(0, 0), color=C.BLUE)
label(ax, "$c=4$", (2.05, np.interp(2.05, t, x_c4)), offset=(7, 6), color=C.RED)
label(ax, "$c=10$", (3.0, np.interp(3.0, t, x_c10)), offset=(7, 5), color=C.TEAL)

ax.set_xlabel(r"$t$")
ax.set_ylabel(r"$x(t)$")
save(fig, "C18-n3")
