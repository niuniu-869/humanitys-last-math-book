import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(14, 9)
t = np.linspace(-1, 3, 401)
g = 2 + 1.2*t - 0.3*t**2
tt = np.array([-1, 2.2])
ax.axvspan(0, 3, color=C.LIGHT, zorder=0)
ax.axvline(0, color=C.GRAY, lw=0.7, ls=":")
ax.plot(t, g, color=C.INK, lw=2.2, ls="-")
ax.plot(tt, 2 + 1.2*tt, color=C.INK, lw=1.5, ls="--")
dot(ax, (0, 2), "$P_0$", offset=(-23, 5))
label(ax, "截线", (2.75, 3.03125), offset=(0, -21), ha="center")
label(ax, r"斜率 $=\partial f/\partial\boldsymbol{l}$", (2.2, 4.64),
      offset=(0, 9), ha="center")
label(ax, r"只取 $t\to0^+$", (1.5, 0.45), ha="center")
ax.set(xlim=(-1.15, 3.35), ylim=(0, 5.5))
ax.set_xticks([-1, 0, 1, 2, 3])
ax.set_xlabel(r"沿 $\boldsymbol{l}$ 的有向位移 $t$")
ax.set_ylabel("$z$", rotation=0, loc="top")
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.19, top=0.96)
assert np.isclose(2 + 1.2*0 - 0.3*0**2, 2)
assert np.isclose(np.diff(2 + 1.2*tt)[0] / np.diff(tt)[0], 1.2)
save(fig, "C22-n1")
