import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14.0, 9.5)
x = np.linspace(0, 3, 700)
y = np.sqrt(x)
x0, y0, eps = 1.0, 1.0, 0.5
f_lo, f_hi = np.sqrt(0.5), np.sqrt(1.5)
delta = min(y0 - f_lo, f_hi - y0)

ax.fill_between([0.5, 1.5], -0.035, 0.035, color=C.LIGHT, zorder=0)
ax.plot(x, y, color=C.INK, lw=1.8, ls="-", zorder=3)
dot(ax, (x0, y0), size=30)
for xx, yy in [(0.5, f_lo), (1.5, f_hi)]:
    ax.plot([xx, xx], [0, yy], color=C.GRAY, lw=1.0, ls=":")
    ax.plot([0, xx], [yy, yy], color=C.GRAY, lw=1.0, ls=":")
ax.plot([0, 0], [y0 - delta, y0 + delta], color=C.INK, lw=3.0, ls="-")
ax.plot([0.5, 1.5], [0, 0], color=C.INK, lw=3.0, ls="-")

label(ax, r"$f(x)=\sqrt{x}$", (2.0, 1.68), offset=(0, 0))
label(ax, r"$(1,1)$", (1, 1), offset=(8, -16))
ax.plot([0.16, 0.23, 0.23, 0.16], [y0, y0, y0+delta, y0+delta], color=C.INK, lw=0.9)
label(ax, r"$\delta$", (0.23, y0 + delta/2), offset=(6, 0), va="center")
label(ax, r"$\delta=\sqrt{1.5}-1\approx0.225$", (0.05, 1.61), offset=(0, 0))

ax.set_xlim(-0.03, 3.05); ax.set_ylim(-0.05, 1.9)
ax.spines["left"].set_position(("data", 0))
ax.spines["bottom"].set_position(("data", 0))
ax.set_xticks([0, 0.5, 1, 1.5, 2, 3])
ax.set_xticklabels(["0", "$x_0-\\varepsilon$\n$0.5$", "$x_0$\n$1$", "$x_0+\\varepsilon$\n$1.5$", "2", "3"])
ax.set_yticks([0, f_lo, 1, f_hi, 1.5])
ax.set_yticklabels(["0", r"$f(x_0-\varepsilon)$", r"$y_0=1$", r"$f(x_0+\varepsilon)$", "1.5"])
ax.set_xlabel("$x$"); ax.set_ylabel("$y$")
assert np.isclose(delta, np.sqrt(1.5)-1)
assert (y0-delta)**2 > x0-eps and np.isclose((y0+delta)**2, x0+eps)
fig.subplots_adjust(left=0.23, bottom=0.20, right=0.97, top=0.97)
save(fig, "C3-n3")
