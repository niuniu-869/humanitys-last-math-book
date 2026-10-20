import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

fig, ax = new_fig(16, 10)
fig.subplots_adjust(left=0.09, right=0.98, bottom=0.13, top=0.96)
phi = (1 + np.sqrt(5))/2
psi = (1 - np.sqrt(5))/2
n = np.arange(11)
fib = [0, 1]
for _ in range(9):
    fib.append(fib[-1] + fib[-2])
fib = np.array(fib)
assert fib.tolist() == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
approx = phi**n / np.sqrt(5)
assert np.allclose(approx - fib, psi**n / np.sqrt(5))
assert np.all(np.abs(approx - fib) < 0.5)
assert np.all(np.diff(np.abs(approx - fib)) < 0)
ax.bar(n, fib, width=0.56, facecolor=C.LIGHT, edgecolor=C.INK, lw=0.9, label=r"$F_n$")
t = np.linspace(0, 10, 600)
ax.plot(t, phi**t / np.sqrt(5), color=C.INK, lw=1.8, ls="-", label=r"$\varphi^n/\sqrt{5}$")
ax.scatter(n, approx, s=29, facecolors=C.PAPER, edgecolors=C.INK, marker="o", zorder=4)
for i, value in enumerate(fib):
    label(ax, str(value), (i, max(value, approx[i])), (-5, 7), ha="right", va="bottom", fontsize=9)
ax.set(xlim=(-0.65, 10.65), ylim=(0, 60), xlabel="$n$", xticks=n, yticks=np.arange(0, 61, 10))
ax.legend(loc="upper left", handlelength=2.5)
label(ax, r"差 $=\varphi^n/\sqrt{5}-F_n=\psi^n/\sqrt{5}$", (9.35, 58), ha="right", va="top", fontsize=9)
label(ax, r"$|\cdot|<\frac{1}{2}$", (9.35, 52.8), ha="right", va="top", fontsize=9)
save(fig, "K21-n3")
