import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

n = np.array([1000, 2000, 4000, 8000])
times = np.array([.8, 3.1, 12.6, 49.5])
x, y = np.log2(n/1000), np.log2(times)
assert np.allclose(np.round(y, 3), [-.322, 1.632, 3.655, 5.629])
b, a = np.polyfit(x, y, 1)
assert round(b, 4) == 1.9877 and round(a, 4) == -.3328
xp = np.log2(16000/1000)
yp, predicted = a+b*xp, 2**(a+b*xp)
fig, ax = new_fig(15, 11)
for start, end, ls in [(0, 3, '-'), (3, xp, '--')]:
    xx = np.array([start, end])
    ax.plot(xx, a+b*xx, color=C.INK, ls=ls, lw=1.5)
ax.scatter(x, y, color=C.INK, s=32, zorder=5)
ax.scatter(xp, yp, facecolor=C.PAPER, edgecolor=C.INK, s=48, zorder=5)
label(ax, f'$n=16000$，约 {predicted:.0f} 毫秒', (xp, yp), offset=(-12, 4), ha='right', va='bottom', fontsize=9)
label(ax, rf'斜率 $b\approx{b:.3f}$', (1.25, a+b*1.25), offset=(-5, 30), ha='center')
ax.set(xlim=(-.3, 4.3), ylim=(-1, 8), xticks=np.arange(5), yticks=np.arange(0, 9, 2), xlabel=r'$x=\log_2(n/1000)$', ylabel=r'$y=\log_2 T$')
ax.xaxis.set_label_coords(.5, -.10)
for xx in range(5):
    ax.text(xx, -.22, str(int(1000*2**xx)), transform=ax.get_xaxis_transform(), ha='center', fontsize=9)
ax.text(-.04, -.22, '$n$', transform=ax.transAxes, ha='right')
fig.subplots_adjust(left=.13, right=.96, bottom=.25, top=.96)
print(f'K41-n6: b={b:.9f}, a={a:.9f}, y(4)={yp:.9f}, T(16000)={predicted:.6f}')
save(fig, 'K41-n6')
