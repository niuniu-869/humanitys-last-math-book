import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label


students = ["甲", "乙", "丙", "丁"]
courses = ["数学", "英语", "历史"]

def draw(ax, edges, title, note):
    sx, cx = 0.0, 2.25
    sy = {s: 2.0 - i * 1.25 for i, s in enumerate(students)}
    cy = {c: 1.35 - i * 1.25 for i, c in enumerate(courses)}
    for s, c in edges:
        ax.plot([sx, cx], [sy[s], cy[c]], color=C.INK, lw=1.25, zorder=1)
    ax.scatter([sx] * 4, [sy[s] for s in students], s=52, color=C.INK, zorder=3)
    ax.scatter([cx] * 3, [cy[c] for c in courses], s=75, facecolors=C.PAPER, edgecolors=C.INK,
               marker="s", lw=1.5, zorder=3)
    for s in students:
        label(ax, s, (sx, sy[s]), offset=(-12, 0), ha="right", va="center")
    for c in courses:
        label(ax, c, (cx, cy[c]), offset=(12, 0), ha="left", va="center")
    ax.set_xlim(-0.8, 3.05); ax.set_ylim(-2.1, 2.55); ax.axis("off")
    ax.set_title(title, pad=8)
    label(ax, note, (1.1, -1.88), ha="center", va="top", fontsize=8)

fig, axes = new_fig(15, 8.5, ncols=2)
draw(axes[0], [("甲", "数学"), ("甲", "英语"), ("乙", "英语"), ("丙", "历史"), ("丁", "数学"), ("丁", "历史")],
     "(1) 每人至少选一门课", "每人都有连线：(1) 真；没有一门课连着四个人：(2) 假")
draw(axes[1], [(s, "数学") for s in students], "(2) 四人都选数学",
     "数学连着所有人：(1)(2) 都真")
save(fig, "Z3-n5")
