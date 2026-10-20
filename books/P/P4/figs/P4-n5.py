import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import erf, sqrt
from matplotlib.patches import ConnectionPatch

fig, (top, bottom) = new_fig(14, 13, nrows=2)
fig.subplots_adjust(left=0.16, right=0.97, bottom=0.1, top=0.96, hspace=0.7)
z = np.linspace(-4, 4, 801)
phi = np.exp(-z ** 2 / 2) / np.sqrt(2 * np.pi)
s = np.linspace(-1, 2, 301)
shaded = np.exp(-s ** 2 / 2) / np.sqrt(2 * np.pi)
probability = (erf(2 / sqrt(2)) - erf(-1 / sqrt(2))) / 2
assert f'{probability:.4f}' == '0.8186'
top.plot(170 + 6 * z, phi / 6, color=C.INK, ls='-')
top.fill_between(170 + 6 * s, 0, shaded / 6, color=C.LIGHT)
top.set(xlim=(146, 194), ylim=(0, 0.08), xticks=[146, 164, 170, 182, 194],
        yticks=[0, 0.03, 0.06], xlabel='身高 $x$（cm）', ylabel='密度')
label(top, f'{probability:.4f}', (173, 0.024), ha='center')
bottom.plot(z, phi, color=C.INK, ls='-')
bottom.fill_between(s, 0, shaded, color=C.LIGHT)
bottom.set(xlim=(-4, 4), ylim=(0, 0.48), xticks=[-4, -1, 0, 2, 4],
           yticks=[0, 0.2, 0.4], xlabel='$z$', ylabel='密度')
label(bottom, rf'$\Phi(2)-\Phi(-1)={probability:.4f}$', (0.45, 0.44), ha='center')
# Equal standardized horizontal scales keep all three correspondences vertical.
for value in [-1, 0, 2]:
    fraction = (value + 4) / 8
    connector = ConnectionPatch(xyA=(fraction, -0.32), coordsA=top.transAxes,
                                xyB=(fraction, 1.04), coordsB=bottom.transAxes,
                                arrowstyle='-|>', linestyle=':', color=C.INK,
                                linewidth=1, mutation_scale=10, clip_on=False)
    fig.add_artist(connector)
label(top, r'$z=\frac{x-170}{6}$', (188, -0.034), ha='center', va='center',
      annotation_clip=False)
save(fig, "P4-n5")
