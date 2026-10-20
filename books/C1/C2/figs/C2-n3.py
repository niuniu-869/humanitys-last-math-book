import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 9)
# Uniform phase sampling resolves each oscillation equally well.
phase = np.linspace(1/0.3, 1/0.012, 12000)
ax.plot(1/phase, np.sin(phase), color=C.INK, ls='-', lw=0.95)
for y in [-1, 1]:
    ax.axhline(y, color=C.GRAY, ls=':', lw=0.8)
n = np.arange(1, 10)
xn, yn = 1/(n*np.pi), 1/(2*n*np.pi+np.pi/2)
assert np.allclose(np.sin(1/xn), 0) and np.allclose(np.sin(1/yn), 1)
xn = xn[xn <= 0.3]
ax.scatter(xn, np.zeros_like(xn), s=25, color=C.INK, zorder=5)
ax.scatter(yn, np.ones_like(yn), s=6, facecolors=C.PAPER, edgecolors=C.INK, linewidths=0.7, zorder=5)
ax.set(xlim=(0, 0.3), ylim=(-1.3, 1.3), xlabel='$x$', ylabel='$y$')
ax.set_xticks([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3])
ax.set_yticks([-1, 0, 1])
label(ax, r'实心点：$x_n$，值 0     空心点：$y_n$，值 1', (0.5, 1.08), xycoords='axes fraction', ha='center', annotation_clip=False)
fig.subplots_adjust(left=0.1, right=0.97, bottom=0.18, top=0.86)
save(fig, "C2-n3")
