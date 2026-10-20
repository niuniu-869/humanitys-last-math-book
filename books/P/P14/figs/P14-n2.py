import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(10.5, 6.8)

p = np.linspace(0, 1, 800)
safe_p = np.clip(p, 1e-12, 1 - 1e-12)
H = -safe_p * np.log2(safe_p) - (1 - safe_p) * np.log2(1 - safe_p)
H[0] = H[-1] = 0
ax.plot(p, H, color=C.BLUE, lw=2.0)

ax.plot([0.5, 0.5], [0, 1], color=C.GRAY, lw=1.0, ls="--")
dot(ax, (0.5, 1.0), "1", color=C.BLUE, offset=(6, 5), size=24)
dot(ax, (0.7, -0.7 * np.log2(0.7) - 0.3 * np.log2(0.3)), "0.881", color=C.BLUE, offset=(6, 5), size=24)
ax.scatter([0.9], [-(0.9 * np.log2(0.9) + 0.1 * np.log2(0.1))], s=34, facecolors=C.PAPER,
           edgecolors=C.INK, linewidths=1.3, zorder=5)
label(ax, "0.469", (0.9, 0.468995593), offset=(-34, 5), color=C.INK)
label(ax, "最大值", (0.5, 1.0), offset=(-58, -3), color=C.INK)

ax.set_xlim(-0.02, 1.02)
ax.set_ylim(-0.03, 1.10)
ax.set_xlabel("概率 $p$")
ax.set_ylabel("二元熵 $H(p)$（比特）")
ax.set_xticks([0, 0.5, 0.7, 0.9, 1])
ax.set_yticks([0, 0.5, 1])
save(fig, "P14-n2")
