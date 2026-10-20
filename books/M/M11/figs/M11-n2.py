import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

# One common scale for rows and columns; these illustrate shapes, not data.
n, d, dk, dv = 1.5, 1.1, .5, .85
assert n > d > dv > dk
shapes = {"X": (n, d), "Q": (n, dk), "K": (n, dk),
          "KT": (dk, n), "V": (n, dv), "S": (n, n),
          "A": (n, n), "out": (n, dv)}
assert shapes["Q"][1] == shapes["K"][1] == shapes["KT"][0]
assert shapes["A"][1] == shapes["V"][0]

fig, ax = new_fig(23, 10)
ax.set(xlim=(-.1, 19.0), ylim=(-.7, 7.0), aspect="equal")
ax.axis("off")

def matrix(x, y, name, shape, dims, weight=False, shaded=False):
    h, w = shape
    ax.add_patch(Rectangle((x-w/2, y-h/2), w, h,
                          facecolor=C.LIGHT if shaded else C.PAPER,
                          edgecolor=C.INK, lw=1.1,
                          ls="--" if weight else "-", zorder=3))
    ax.text(x, y, name, ha="center", va="center",
            fontsize=10 if weight else 12, zorder=4)
    label(ax, dims, (x, y-h/2), offset=(0, -8),
          ha="center", va="top", fontsize=10)

matrix(1, 3.1, "$X$", shapes["X"], r"$n\times d$")
for y, suffix, width, dim in [(5.4, "Q", dk, "d_k"),
                              (3.1, "K", dk, "d_k"),
                              (.8, "V", dv, "d_v")]:
    arrow(ax, (1+d/2, 3.1), (2.0, y-3.1), color=C.INK, lw=1)
    label(ax, "乘", (3.05, y+(.28 if suffix != "V" else -.28)),
          ha="center", fontsize=9)
    matrix(4, y, f"$W_{suffix}$", (d, width),
           rf"$d\times {dim}$", weight=True)
    arrow(ax, (4+width/2+.12, y), (1.75-width, 0), color=C.INK, lw=1)
    matrix(6, y, f"${suffix}$", shapes[suffix], rf"$n\times {dim}$")

arrow(ax, (6+dk/2+.1, 3.1), (.75, 0), color=C.INK, lw=1)
label(ax, "转置", (6.9, 3.1), offset=(0, 10), ha="center", fontsize=9)
matrix(8, 3.1, r"$K^{\mathsf{T}}$", shapes["KT"], r"$d_k\times n$")
arrow(ax, (6+dk/2+.12, 5.4), (1.23, 0), color=C.INK, lw=1)
arrow(ax, (8, 3.1+dk/2+.1), (0, 1.53), color=C.INK, lw=1)
ax.text(8, 5.4, r"$\times$", ha="center", va="center", fontsize=16)
arrow(ax, (8.32, 5.4), (1.41, 0), color=C.INK, lw=1)
label(ax, r"除以 $\sqrt{d_k}$", (9.025, 5.4), offset=(0, 12), ha="center", fontsize=9)
matrix(10.6, 5.4, "$S$", shapes["S"], r"$n\times n$", shaded=True)
arrow(ax, (11.45, 5.4), (1.5, 0), color=C.INK, lw=1)
label(ax, "逐行 softmax", (12.2, 5.4), offset=(0, 12), ha="center", fontsize=9)
matrix(13.8, 5.4, "$A$", shapes["A"], r"$n\times n$", shaded=True)
arrow(ax, (14.65, 5.4), (.77, 0), color=C.INK, lw=1)
ax.text(15.8, 5.4, r"$\times$", ha="center", va="center", fontsize=16)
ax.plot([6+dv/2+.1, 15.8, 15.8], [.8, .8, 4.4],
        color=C.INK, lw=1, ls="-")
arrow(ax, (15.8, 4.4), (0, .55), color=C.INK, lw=1)
arrow(ax, (16.15, 5.4), (.72, 0), color=C.INK, lw=1)
matrix(17.4, 5.4, "$AV$", shapes["out"], r"$n\times d_v$")
label(ax, "输出", (17.4, 6.4), ha="center", fontsize=10)
fig.tight_layout(pad=.5)
save(fig, "M11-n2")
