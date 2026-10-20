import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from matplotlib.patches import Rectangle
from itertools import product

valid = [p for p in product(range(3), repeat=7) if [p.count(k) for k in range(3)] == [3, 2, 2]
         and p[2] == p[3] and p[4] != 0 and p[6] == 2 and p[2] != 0]
assert valid == [(0, 0, 1, 1, 2, 0, 2)]
fig, ax = new_fig(17, 9)
ax.set(xlim=(-.3, 10.8), ylim=(-2.7, 2.3))
ax.axis("off")
for left, people, title in [(0, "甲乙己", "一组（3 人）"), (4.1, "丙丁", "二组（2 人）"),
                             (8.2, "庚戊", "三组（2 人）")]:
    label(ax, title, (left+len(people)/2, 1.55), ha="center")
    for j, person in enumerate(people):
        ax.add_patch(Rectangle((left+j, .2), 1, .95,
                               facecolor=C.LIGHT if person == "庚" else C.PAPER,
                               edgecolor=C.INK, lw=1.1))
        ax.text(left+j+.5, .68, person, ha="center", va="center", fontsize=17, color=C.INK)
label(ax, "③ 剩下的三人", (1.5, -.5), ha="center", fontsize=9)
arrow(ax, (1.5, -.25), (0, .35), color=C.INK, lw=1)
label(ax, "① 丙丁同组，丙不在一组\n三组已有庚，再放会超员", (5.1, -.65), ha="center", va="top", fontsize=9)
arrow(ax, (5.1, -.25), (0, .35), color=C.INK, lw=1)
label(ax, "① 庚在三组", (9.2, 2.08), ha="center", fontsize=9)
label(ax, "② 戊不在一组\n二组已满，只剩三组", (9.2, -.65), ha="center", va="top", fontsize=9)
arrow(ax, (9.7, -.25), (0, .35), color=C.INK, lw=1)
label(ax, "浅灰：直接给出（庚）    白：推出    圈内数字：步骤", (5.25, -2.3), ha="center", fontsize=9)
save(fig, "K13-n5")
