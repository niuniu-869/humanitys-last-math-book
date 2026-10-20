import sys; sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[4] / "tools"))
from figstyle import plt, np, C, new_fig, new_fig3d, save, arrow, dot, label

rhos = [-.8, 0, .5, .95]
rng = np.random.default_rng(20261017)
z = rng.standard_normal((2000, 2))
fig, axes = new_fig(16, 4, ncols=4, squeeze=False)
t = np.linspace(0, 2*np.pi, 400)
for j, rho in enumerate(rhos):
    ax = axes[0, j]
    S = np.array([[1, rho], [rho, 1.]])
    pts = z @ np.linalg.cholesky(S).T
    ax.scatter(pts[:,0], pts[:,1], s=2.2, color=C.GRAY, alpha=.42, linewidths=0)
    ev, V = np.linalg.eigh(S)
    E = V @ np.diag(np.sqrt(ev * 4)) @ np.vstack((np.cos(t), np.sin(t)))
    ax.plot(E[0], E[1], color=C.INK, ls="-", lw=1.3)
    ax.axhline(0, color=C.LIGHT, lw=.65); ax.axvline(0, color=C.LIGHT, lw=.65)
    ax.set_xlim(-3.5, 3.5); ax.set_ylim(-3.5, 3.5); ax.set_aspect("equal")
    ax.set_xticks([-3, 0, 3]); ax.set_yticks([-3, 0, 3])
    ax.set_xlabel(rf"$\rho={rho}$", labelpad=5)
save(fig, "P7-n3")
