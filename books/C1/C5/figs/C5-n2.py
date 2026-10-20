import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, axs = new_fig(18, 15, nrows=2, ncols=2)
fig.subplots_adjust(left=0.10, right=0.97, bottom=0.10, top=0.90, hspace=0.95, wspace=0.52)
cases = [(-0.5, 0.5, 0.1, np.exp, lambda x: 1+x,
          r'$y=e^x$', '近似 1.1 < 真值 1.1052', 0.02),
         (3.5, 4.5, 4.1, np.sqrt, lambda x: 2+(x-4)/4,
          r'$y=\sqrt{x}$', '近似 2.025 > 真值 2.0248', 0.0005)]
for col, (lo, hi, p, f, tangent, title, note, half) in enumerate(cases):
    ax, zoom = axs[:, col]
    y, ty = f(p), tangent(p)
    xx = np.linspace(lo, hi, 500)
    for a, xs in ((ax, xx), (zoom, np.linspace(p-half/3, p+half/3, 200))):
        a.plot(xs, f(xs), color=C.INK, ls='-', label='曲线')
        a.plot(xs, tangent(xs), color=C.RED, ls='--', label='切线')
        a.axvline(p, color=C.GRAY, ls=':', lw=0.8)
        dot(a, (p, y), size=18 if a is ax else 30)
        a.scatter([p], [ty], s=24 if a is ax else 36,
                  facecolors=C.PAPER, edgecolors=C.INK, zorder=5)
        a.set(xlabel='$x$', ylabel='$y$')
    ax.set_xlim(lo, hi)
    ax.set_ylim((0.5, 1.75) if col == 0 else (1.6, 2.6))
    ax.set_aspect('equal')
    ax.set_title(title, pad=10)
    ax.set_xticks([lo, p, hi])
    if col == 1:
        ax.set_yticks([1.75, 2, 2.25, 2.5])
    ax.legend(loc='upper left', fontsize=8)
    mid = (y+ty)/2
    zoom.set(xlim=(p-half/3, p+half/3), ylim=(mid-half, mid+half))
    zoom.set_xticks([p])
    zoom.set_yticks([y, ty], [f'{y:.6f}', f'{ty:g}'])
    zoom.tick_params(labelsize=8)
    zoom.set_title('局部放大（纵轴已放大）', fontsize=9, pad=12)
    label(zoom, '真值', (p, y), (-14, -14 if y < ty else 10), ha='right', fontsize=9)
    label(zoom, '近似', (p, ty), (14, 10 if ty > y else -14), fontsize=9)
    label(zoom, note, (0.5, -0.37), xycoords='axes fraction',
          ha='center', fontsize=9, annotation_clip=False)
assert np.exp(0.1) > 1.1 and np.sqrt(4.1) < 2.025
save(fig, "C5-n2")
