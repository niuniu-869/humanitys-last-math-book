import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

def sim(std,n=256,D=10,B=1000,seed=0):
    rng=np.random.default_rng(seed);a=rng.normal(size=(B,n));out=[]
    for l in range(D):
        z=a@(rng.normal(size=(n,n))*std);out.append(z.std());a=np.maximum(z,0)
    return out

fig, ax = new_fig(13, 8)
x = np.arange(1, 11)
specs = [
    (np.sqrt(2/256), '-', 'o', True, C.BLUE, r"$\omega=\sqrt{2/256}$ (He)"),
    (np.sqrt(1/256), '--', 'o', False, C.RED, r"$\omega=\sqrt{1/256}$"),
    (0.1, '-.', 's', True, C.TEAL, r"$\omega=0.1$"),
    (0.01, ':', '^', False, C.AMBER, r"$\omega=0.01$"),
]
for std, ls, marker, filled, color, lab in specs:
    y = sim(std)
    ax.plot(x, y, ls=ls, marker=marker, color=color, label=lab,
            markerfacecolor=color if filled else C.PAPER,
            markeredgecolor=color, markersize=5.5, linewidth=1.7)
ax.set_yscale('log')
ax.set_ylim(1e-10, 1e1)
ax.set_xlim(0.7, 10.3)
ax.set_xticks(x)
ax.set_xlabel('层号')
ax.set_ylabel('加权和的标准差')
ax.grid(True, axis='y', which='major', color=C.LIGHT, lw=0.6)
ax.legend(loc='lower left', fontsize=7.5)
save(fig, "M8-n2")
