import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

vals = np.array([[0,0,0],[0,0,1],[0,.9,1],[.81,.9,1],[.81,.9,1]])
assert np.allclose(vals[-1], vals[-2])
fig, axes = new_fig(17, 4.6, ncols=5, sharey=True)
for k, (ax, row) in enumerate(zip(axes, vals)):
    ax.bar([0,1,2], row, width=.58, color=C.LIGHT, edgecolor=C.INK, linewidth=.9)
    for i, y in enumerate(row): label(ax, f"{y:g}", (i,y+.045), ha="center", va="bottom", fontsize=8)
    ax.set_title(f"第 {k} 遍"); ax.set_xticks([0,1,2], ["格 1","格 2","格 3"]); ax.set_ylim(0,1.08); ax.grid(False)
    if k == 0: ax.set_ylabel("价值")
    if k == 4: label(ax, "与第 3 遍相同，收敛", (1,-.25), ha="center", fontsize=8)
fig.tight_layout(); save(fig, "M15-n2")
