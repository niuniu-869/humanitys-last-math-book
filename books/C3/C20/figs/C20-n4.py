import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(13, 8)
s = np.linspace(0, 0.5, 300)
z_surface = 5 - 2*s + s**2
z_plane = 5 - 2*s
ax.plot(s, z_surface, color=C.INK, lw=2.2)
ax.plot(s, z_plane, color=C.INK, ls="--", lw=1.8)
dot(ax, (0, 5), "(0,5)", offset=(5, 5), size=28)

# 两个端点用不同点形：实心方块（曲面）、空心圆（切平面）
ax.scatter([0.5], [z_surface[-1]], s=34, marker="s", color=C.INK, zorder=5)
ax.scatter([0.5], [z_plane[-1]], s=40, facecolors="none", edgecolors=C.INK,
           linewidths=1.2, zorder=5)
ax.plot([0.5, 0.5], [z_plane[-1], z_surface[-1]], color=C.INK, ls=":", lw=1.4)

# 右侧花括号标出 0.25 的高度差，o(ρ) 写在括号旁
ax.text(0.555, 4.125, "}", fontsize=30, ha="center", va="center", color=C.INK)
label(ax, r"$o(\rho)$", (0.575, 4.125), offset=(0, 0), ha="left", va="center",
      fontsize=9.5)
label(ax, r"$\Delta z$", (0.5, z_surface[-1]), offset=(0, 9),
      ha="center", va="bottom", fontsize=9.5)
label(ax, r"$\mathrm{d}z$", (0.5, z_plane[-1]), offset=(7, 0),
      ha="left", va="center", fontsize=9.5)

# ρ=0.5 放到横轴下方；不再画与 dz 点重叠的水平灰箭头
ax.set_xlabel("沿位移方向的距离 $s$", labelpad=24)
ax.annotate(r"$\rho=0.5$", xy=(0.5, 0), xycoords=("data", "axes fraction"),
            xytext=(0, -30), textcoords="offset points", ha="center", va="top",
            fontsize=9, annotation_clip=False)

ax.set(xlim=(-0.03, 0.64), ylim=(3.88, 5.15))
ax.set_xticks([0, 0.5]); ax.set_xticklabels(["0", "0.5"])
ax.set_yticks([4, 4.25, 4.5, 4.75, 5])
fig.tight_layout(pad=1.0)
save(fig, "C20-n4")
