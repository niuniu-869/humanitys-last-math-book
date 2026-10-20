import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from itertools import permutations

conditions = [lambda p: p[0] != "丙",
              lambda p: abs(p.index("乙") - p.index("丁")) == 1,
              lambda p: p.index("甲") < p.index("丙"),
              lambda p: p.index("乙") == p.index("甲") + 1]
def counts(order):
    candidates = list(permutations("甲乙丙丁"))
    values = [len(candidates)]
    for k in order:
        candidates = [p for p in candidates if conditions[k - 1](p)]
        values.append(len(candidates))
    return values

weak, strong = counts([1, 2, 3, 4]), counts([4, 2, 1, 3])
assert weak == [24, 18, 8, 6, 1] and strong == [24, 6, 2, 1, 1]
assert sum(weak[:-1]) == 56 and sum(strong[:-1]) == 33
fig, ax = new_fig(15, 11)
fig.subplots_adjust(bottom=.30, top=.78, left=.13, right=.96)
x = np.arange(5)
ax.plot(x, strong, ls="-", marker="s", color=C.INK, ms=6,
        label="实线：先强后弱（共检查 33 次）")
ax.plot(x, weak, ls="--", marker="o", mfc=C.PAPER, mec=C.INK,
        color=C.INK, ms=6, label="虚线：照题目顺序（共检查 56 次）")
for i, y in enumerate(weak):
    label(ax, str(y), (i, y), (0, 8), ha="center", fontsize=9)
for i, y in enumerate(strong):
    if i not in (0, 4):
        label(ax, str(y), (i, y), (0, 9) if i == 3 else (0, -15), ha="center", fontsize=9)
ax.set(xlim=(-.18, 4.18), ylim=(-2, 27), ylabel="还剩的排法数", xlabel="已用的条件数")
ax.set_xticks(x)
ax.set_yticks([0, 6, 12, 18, 24])
ax.grid(axis="y", color=C.LIGHT, ls=":", lw=.7)
ax.legend(loc="lower left", bbox_to_anchor=(0, 1.03), fontsize=9, handlelength=3)
label(ax, "虚线条件顺序：1 → 2 → 3 → 4", (2, -2), (0, -48), ha="center", fontsize=9)
label(ax, "实线条件顺序：4 → 2 → 1 → 3", (2, -2), (0, -65), ha="center", fontsize=9)
save(fig, "K13-n2")
