import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle

options = [("北京", "上海", "成都", "广州"), ("广州", "北京", "上海", "成都"),
           ("上海", "广州", "北京", "成都"), ("广州", "北京", "成都", "上海"),
           ("上海", "北京", "成都", "广州")]
conditions = [lambda p: p[0] not in ("北京", "成都"), lambda p: p[2] in ("成都", "上海"),
              lambda p: p[1] != "北京" or p[3] == "广州", lambda p: p[3] != "上海"]
rows = []
for p in options:
    row, stopped = [], False
    for condition in conditions:
        row.append("—" if stopped else "✓" if condition(p) else "✗")
        stopped = stopped or row[-1] == "✗"
    rows.append(row)
assert rows == [list("✗———"), list("✓✓✗—"), list("✓✗——"), list("✓✓✗—"), list("✓✓✓✓")]
assert [sum(row[j] != "—" for row in rows) for j in range(4)] == [5, 4, 3, 1]
fig, ax = new_fig(13, 10)
ax.set(xlim=(-.8, 4.2), ylim=(-.9, 5.7))
ax.axis("off")
for j, k in enumerate([2, 3, 1, 4]):
    label(ax, f"条件 {k}", (j + .5, 5.3), ha="center", va="center")
for i, row in enumerate(rows):
    y = 4 - i
    label(ax, f"({chr(65+i)})", (-.4, y+.5), ha="center", va="center")
    for j, mark in enumerate(row):
        ax.add_patch(Rectangle((j, y), 1, 1, facecolor=C.LIGHT if mark == "✗" else C.PAPER,
                               edgecolor=C.GRAY if mark == "—" else C.INK,
                               hatch="///" if mark == "—" else None, lw=.9))
        label(ax, r"$\times$" if mark == "✗" else mark, (j+.5, y+.5),
              ha="center", va="center", fontsize=18)
label(ax, "检验次数：5 + 4 + 3 + 1 = 13", (2, -.6), ha="center")
save(fig, "K13-n4")
