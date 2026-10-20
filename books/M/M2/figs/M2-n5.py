import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

p = np.array([0.6652, 0.2447, 0.0900])
grad = p - np.array([1.0, 0.0, 0.0])
cats = ['类 1（正确）', '类 2', '类 3']
pos = np.arange(3, dtype=float)
w = 0.34

fig, ax = new_fig(12, 7.5)
bars_p = ax.bar(pos - w / 2, p, width=w, color=C.LIGHT, edgecolor=C.GRAY, linewidth=0.8, label=r'$\boldsymbol{p}$')
bars_g = ax.bar(pos + w / 2, grad, width=w, color=C.PAPER, edgecolor=C.INK, linewidth=1.0, label=r'$\boldsymbol{p}-\boldsymbol{y}$')
ax.axhline(0, color=C.INK, lw=0.9)
for xi, yi in zip(pos - w / 2, p):
    label(ax, f'{yi:.4f}', (xi, yi), offset=(0, 5), ha='center', fontsize=8.3)
for xi, yi in zip(pos + w / 2, grad):
    label(ax, f'{yi:.4f}', (xi, yi), offset=(0, -15 if yi < 0 else 5), ha='center', fontsize=8.3)
label(ax, '和 = 0', (2 + w / 2, 0.30), offset=(0, 0), ha='center', fontsize=8.5)
ax.set_xticks(pos, cats)
ax.set(xlim=(-0.65, 2.65), ylim=(-0.45, 0.82), ylabel='数值')
ax.legend(loc='upper right', fontsize=9)
save(fig, 'M2-n5')
