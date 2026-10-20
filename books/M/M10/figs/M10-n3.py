import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, save, arrow, dot, label

k = np.arange(0, 51)
y09, y11, y099 = 0.9**k, 1.1**k, 0.99**k
assert abs(y09[20] - 0.1216) < 5e-4 and abs(y11[20] - 6.727) < 2e-3
assert abs(y099[20] - 0.818) < 5e-4
assert abs(y09[50] - 0.0052) < 5e-4 and abs(y11[50] - 117) < 1 and abs(y099[50] - 0.605) < 5e-3
fig, ax = new_fig(14.5, 8.5)
ax.semilogy(k, y09, color=C.INK, ls='-', label='$0.9^k$')
ax.semilogy(k, y11, color=C.GRAY, ls='--', label='$1.1^k$')
ax.semilogy(k, y099, color=C.RED, ls=':',
            label='$0.99^k$（固定遗忘门 0.99 时，\n沿细胞状态直接路径的倍率）')
ax.axhline(1, color=C.TEAL, ls='-.', lw=1.0)
label(ax, '不变', (20.0, 1.12), ha='left', va='bottom', fontsize=9)
for yy, text, dx in [(y09[-1], '0.0052', 1.0), (y11[-1], '117', 1.0), (y099[-1], '0.605', 1.0)]:
    dot(ax, (50, yy), size=22)
    label(ax, text, (50, yy), offset=(dx*7, 0), ha='left', va='center', fontsize=9)
ax.set(xlim=(0, 56), ylim=(1e-3, 1e3), xlabel='往回隔的步数 $k$', ylabel='梯度倍率（对数坐标）')
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.grid(axis='y', color=C.LIGHT, lw=.7, ls=':')
ax.legend(loc='upper left', fontsize=8, handlelength=2.0,
          labelspacing=.35, borderaxespad=.35)
save(fig, 'M10-n3')
