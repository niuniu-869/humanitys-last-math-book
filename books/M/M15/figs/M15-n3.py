import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

before = np.array([.6652,.2447,.09]); after = np.array([.4517,.2530,.2953])
assert np.isclose(before.sum(),1,atol=2e-4) and np.isclose(after.sum(),1,atol=2e-4)
fig, axes = new_fig(13, 5, ncols=2, sharey=True)
for ax, vals, title in zip(axes, [before,after], ["更新前","更新后"]):
    ax.bar([0,1,2], vals, width=.58, color=[C.LIGHT,C.LIGHT,C.GRAY if title=="更新后" else C.LIGHT], edgecolor=C.INK, linewidth=.9, hatch=[None,None,"///"] if title=="更新后" else [None,None,"///"])
    for i,y in enumerate(vals): label(ax, f"{y:.4f}", (i,y+.025), ha="center", fontsize=8)
    ax.set_title(title); ax.set_xticks([0,1,2],["词 1","词 2","词 3"]); ax.set_ylim(0,.82); ax.set_ylabel("概率")
axes[0].annotate("", xy=(1.08,.56), xytext=(.92,.56), xycoords="axes fraction", arrowprops=dict(arrowstyle="-|>",lw=1.5,color=C.INK))
label(fig.axes[0], "$R=1$，$\\hat g=\\bf e_3-\\pi$", (1.02,.72), transform=fig.axes[0].transAxes, ha="center", fontsize=9)
fig.tight_layout(); save(fig, "M15-n3")
