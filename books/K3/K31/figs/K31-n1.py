import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label
from math import factorial

n = np.arange(1, 21)
facts = [factorial(int(k)) for k in n]
assert facts[-1] == 2432902008176640000
assert 2**4 == 4**2 == 16 and 2**10 == 1024 > 10**3 == 1000
fig, ax = new_fig(17, 14)
curves = [
    (n * np.log2(n), r'$n\log_2 n$', '-', .9),
    (n**2, r'$n^2$', '-', 2.0),
    (n**3, r'$n^3$', '--', 1.5),
    (2**n, r'$2^n$', ':', 1.6),
    (np.array(facts, dtype=float), r'$n!$', '-.', 1.5),
]
for values, name, style, width in curves:
    # Zero is omitted rather than moved to a false positive height on the log axis.
    ax.plot(n, np.ma.masked_less_equal(values, 0), color=C.INK,
            ls=style, lw=width, marker='o', ms=2.5)
    label(ax, name, (20, values[-1]), (8, 0), va='center', fontsize=10)
ax.set_yscale('log')
ax.set(xlim=(.7, 23.4), ylim=(1, 1e19), xlabel='$n$')
ax.set_xticks([1, 4, 10, 15, 20])
ax.set_yticks([10.0**k for k in range(20)])
ax.set_yticklabels([rf'$10^{{{k}}}$' for k in range(20)], fontsize=8)
ax.grid(axis='y', color=C.LIGHT, ls=':', lw=.6)
ax.axvline(10, color=C.GRAY, ls=':', lw=.8)
label(ax, r'$n=10$：$2^n=1024>n^3=1000$', (10, 1e15),
      (10, 0), fontsize=9, va='center')
label(ax, r'$n=4$：$2^n=n^2=16$', (4, 16), (0, 85),
      fontsize=9, ha='center',
      arrowprops=dict(arrowstyle='-', color=C.GRAY, lw=.7))
fig.subplots_adjust(left=.12, right=.98, bottom=.09, top=.98)
save(fig, "K31-n1")
