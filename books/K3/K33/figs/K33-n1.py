import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

values = [1, 2, 3, 5, 8, 9]
lo, hi, steps = 1, 6, []
while lo <= hi:
    mid = (lo + hi) // 2
    steps.append((lo, hi, mid))
    if values[mid - 1] == 8:
        break
    lo = mid + 1
assert steps == [(1, 6, 3), (4, 6, 5)]
fig, ax = new_fig(18, 8)
for row, (lo, hi, mid) in enumerate(steps):
    y = 3.5 - row * 2.2
    label(ax, f"轮 {row + 1}", (-.65, y + .4), ha="right", va="center")
    for i, value in enumerate(values, 1):
        x = (i - 1) * .9
        ax.add_patch(Rectangle((x, y), .9, .8, facecolor=C.LIGHT if i == mid else C.PAPER,
                               edgecolor=C.INK, ls="--" if i < lo else "-", lw=1))
        label(ax, str(i), (x + .45, y + .96), ha="center", fontsize=9)
        if i >= lo:
            label(ax, str(value), (x + .45, y + .4), ha="center", va="center", fontsize=12)
    left, right = (lo - 1) * .9, hi * .9
    ax.plot([left, left, right, right], [y+1.14, y+1.3, y+1.3, y+1.14], color=C.INK, lw=1)
    for i, name in [(lo, "lo"), (hi, "hi"), (mid, "mid")]:
        x = (i - .5) * .9
        arrow(ax, (x, y-.43), (0, .36), color=C.INK, lw=1)
        label(ax, f"{name}={i}", (x, y-.68), ha="center", va="center", fontsize=9)
    label(ax, "3<8，丢掉第 1–3 格" if row == 0 else "8=8，找到",
          (5.8, y+.4), va="center", fontsize=10)
label(ax, "共 2 次比较", (2.7, -.35), ha="center")
ax.set(xlim=(-1.4, 9.5), ylim=(-.7, 5.2))
ax.axis("off")
save(fig, "K33-n1")
