"""Recompute all 15 numbered lesson examples from their original data.

NumPy least squares and direct sums supply the results; SciPy supplies tail
probabilities and quantiles. Tolerances follow the printed decimal precision.
The original simulation checks remain in sim_lesson.py.
"""
import sys

import numpy as np
from scipy import stats

failures = 0
G = [[8, 10, 9, 11, 12], [13, 12, 15, 14, 16], [10, 12, 11, 13, 14]]


def close(actual, expected, atol=1e-10):
    np.testing.assert_allclose(actual, expected, rtol=0, atol=atol)


def one_way(groups):
    arrays = [np.asarray(g, dtype=float) for g in groups]
    values = np.concatenate(arrays)
    n, k = len(values), len(arrays)
    means = np.array([g.mean() for g in arrays])
    sizes = np.array([len(g) for g in arrays])
    overall = values.mean()
    between = np.sum(sizes * (means-overall)**2)
    within = sum(np.sum((g-m)**2) for g, m in zip(arrays, means))
    total = np.sum((values-overall)**2)
    return dict(means=means, mean=overall, B=between, W=within, T=total,
                df=[k-1, n-k, n-1], MS=[between/(k-1), within/(n-k)],
                F=(between/(k-1))/(within/(n-k)))


def regress(columns, y):
    y = np.asarray(y, dtype=float)
    X = np.column_stack([np.ones(len(y)), *columns])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    fitted = X @ b
    residual = y-fitted
    total = np.sum((y-y.mean())**2)
    error = residual @ residual
    return dict(X=X, b=b, fitted=fitted, residual=residual, E=error, T=total,
                R=total-error, R2=1-error/total, var=error/(len(y)-X.shape[1]))


def main_fit():
    return regress([np.arange(1, 6)], [2, 3, 5, 4, 6])


def ex01():
    a = one_way(G)
    close(a["means"], [10, 14, 12])
    close([a["mean"], a["B"], a["W"], a["T"]], [12, 40, 30, 70])
    close(a["df"], [2, 12, 14])
    close([np.var(g, ddof=1) for g in G], [2.5]*3)
    close(a["MS"][1], 2.5)


def ex02():
    a = one_way([[4, 6], [7, 9, 7, 9], [10, 12]])
    close(a["means"], [5, 8, 11])
    close([a["mean"], a["B"], a["W"], a["T"]], [8, 36, 8, 44])
    close(a["df"], [2, 5, 7])


def ex03():
    a = one_way(G)
    close(a["MS"], [20, 2.5])
    close(a["F"], 8)
    close(stats.f.isf(.05, 2, 12), 3.89, .005)
    p = stats.f.sf(a["F"], 2, 12)
    close(p, .006, .0005)
    assert p < .05
    se = np.sqrt(a["MS"][1]*(1/5+1/5))
    pair_t = np.abs(a["means"][[1, 2]]-a["means"][0])/se
    close([se, *pair_t], [1, 4, 2])
    pair_p = 2*stats.t.sf(pair_t, 12)
    close(pair_p[0], .0018, .00005)
    close(pair_p[1], .069, .0005)
    # The book multiplies its rounded p=.0018 by 3 to display .0054.
    close(pair_p[0]*3, .0054, .00015)
    close(pair_p[1]*3, .21, .005)
    assert pair_p[0]*3 < .05 < pair_p[1]*3


def ex04():
    a = one_way(G[:2])
    close([a["mean"], a["B"], a["W"], a["F"]], [12, 40, 20, 16])
    close(a["MS"], [40, 2.5])
    t = stats.ttest_ind(G[0], G[1], equal_var=True).statistic
    close(t, -4)
    close(a["F"], t*t)


def ex05():
    a = np.array([[9, 11, 10], [12, 11, 13], [12, 14, 16]], float)
    mean, rows, cols = a.mean(), a.mean(1), a.mean(0)
    close(rows, [10, 12, 14])
    close(cols, [11, 12, 13])
    close(mean, 12)
    ssr = a.shape[1]*np.sum((rows-mean)**2)
    ssc = a.shape[0]*np.sum((cols-mean)**2)
    residual = a-rows[:, None]-cols[None, :]+mean
    sse = np.sum(residual**2)
    total = np.sum((a-mean)**2)
    mse = sse/((a.shape[0]-1)*(a.shape[1]-1))
    fs = np.array([ssr/2, ssc/2])/mse
    close([ssr, ssc, sse, total, mse, *fs], [24, 6, 6, 36, 1.5, 8, 2])
    close(stats.f.isf(.05, 2, 4), 6.94, .005)
    assert fs[0] > 6.94 > fs[1]
    single = one_way(a)
    close([single["W"], single["df"][1], single["MS"][1], single["F"]], [12, 6, 2, 6])


def ex06():
    a = np.array([[[10, 12, 11], [14, 16, 15]], [[18, 17, 19], [12, 13, 11]]], float)
    nr, nc, m = a.shape
    cell, grand = a.mean(2), a.mean()
    rows, cols = a.mean((1, 2)), a.mean((0, 2))
    close(cell, [[11, 15], [18, 12]])
    close(rows, [13, 15])
    close(grand, 14)
    ssr = nc*m*np.sum((rows-grand)**2)
    ssc = nr*m*np.sum((cols-grand)**2)
    ssi = m*np.sum((cell-rows[:, None]-cols[None, :]+grand)**2)
    sse = np.sum((a-cell[:, :, None])**2)
    mse = sse/(nr*nc*(m-1))
    close([ssr, ssc, ssi, sse, mse], [12, 3, 75, 8, 1])
    fs = np.array([ssr, ssc, ssi])/mse
    close(fs, [12, 3, 75])
    close(stats.f.isf(.05, 1, 8), 5.32, .005)
    assert list(fs > 5.32) == [True, False, True]
    assert (cell[1, 0]-cell[0, 0])*(cell[1, 1]-cell[0, 1]) < 0


def ex07():
    x, y = np.arange(1, 6), np.array([2, 3, 5, 4, 6])
    a = main_fit()
    xc, yc = x-x.mean(), y-y.mean()
    close([x.mean(), y.mean(), xc@xc, xc@yc], [3, 4, 10, 9])
    close(a["b"], [1.3, .9])
    close(a["fitted"], [2.2, 3.1, 4, 4.9, 5.8])
    close(a["residual"], [-.2, -.1, 1, -.9, .2])
    close(a["residual"].sum(), 0)
    close(a["E"], 1.9)
    close(a["var"], .633, .0005)
    close([a["T"], a["R"], a["R2"]], [10, 8.1, .81])
    close(np.corrcoef(x, y)[0, 1], .9)
    close(a["R"]/a["var"], 12.79, .005)


def ex08():
    cov, varx, ex, ey = .15, .24, .6, 2
    slope, intercept = cov/varx, ey-cov/varx*ex
    close([intercept, slope], [13/8, 5/8])
    # Binary X: E[XY]=P(X=1) E[Y|X=1].
    exy = cov+ex*ey
    conditional1 = exy/ex
    conditional0 = (ey-exy)/(1-ex)
    close([conditional0, conditional1], [13/8, 9/4])
    close([intercept, intercept+slope], [conditional0, conditional1])


def ex09():
    a = main_fit()
    se = np.sqrt(a["var"]/10)
    t = a["b"][1]/se
    critical = stats.t.isf(.025, 3)
    close(np.sqrt(a["var"]), .796, .0005)
    close(se, .2517, .00005)
    close(t, 3.576, .0005)
    close(critical, 3.182, .0005)
    close(2*stats.t.sf(abs(t), 3), .037, .0005)
    close(a["b"][1]+np.array([-1, 1])*critical*se, [.10, 1.70], .005)
    assert abs(t) > critical


def ex10():
    x = np.repeat([0., 1.], 5)
    y = np.array(G[:2]).reshape(-1)
    a = regress([x], y)
    xc, yc = x-x.mean(), y-y.mean()
    close([x.mean(), xc@xc, xc@yc], [.5, 2.5, 10])
    close(a["b"], [10, 4])
    close(a["fitted"], [10]*5+[14]*5)
    close([a["E"], a["var"]], [20, 2.5])
    se = np.sqrt(a["var"]/(xc@xc))
    t = a["b"][1]/se
    close([se, t, t*t], [1, 4, 16])
    close(t*t, one_way(G[:2])["F"])


def ex11():
    x = np.arange(1, 6)
    y = x*x
    a = regress([x], y)
    close([x.mean(), y.mean(), np.sum((x-x.mean())**2), (x-x.mean())@(y-y.mean())], [3, 11, 10, 60])
    close(a["b"], [-7, 6])
    close(a["T"], 374)
    close(a["R2"], .963, .0005)
    close(a["residual"], [2, -1, -2, -1, 2])
    assert list(np.sign(a["residual"])) == [1, -1, -1, -1, 1]
    assert not np.allclose(a["residual"], 0)


def ex12():
    a = main_fit()
    x0 = np.array([3, 4, 6])
    h = 1/5+(x0-3)**2/10
    center = a["b"][0]+a["b"][1]*x0
    multiplier = stats.t.isf(.025, 3)*np.sqrt(a["var"])
    mean_width = multiplier*np.sqrt(h)
    pred_width = multiplier*np.sqrt(1+h)
    close(h, [.2, .3, 1.1])
    close(center, [4, 4.9, 6.7])
    close(mean_width, [1.13, 1.39, 2.66], .005)
    close(pred_width, [2.77, 2.89, 3.67], .005)
    close(np.column_stack([center-mean_width, center+mean_width]), [[2.87, 5.13], [3.51, 6.29], [4.04, 9.36]], .005)
    close(np.column_stack([center-pred_width, center+pred_width]), [[1.23, 6.77], [2.01, 7.79], [3.03, 10.37]], .005)
    assert np.all(pred_width > mean_width)
    assert np.argmin(mean_width) == np.argmin(pred_width) == 0
    assert x0[-1] > 5


def ex13():
    n = np.array([1, 2, 4, 8, 16], float)
    loss = np.array([3.90, 3.42, 3.01, 2.63, 2.31])
    u, v = np.log(n), np.log(loss)
    close(loss[:-1]-loss[1:], [.48, .41, .38, .32])
    close(loss[1:]/loss[:-1], [.877, .880, .874, .878], .0005)
    close(u, [0, .693, 1.386, 2.079, 2.773], .0005)
    close(v, [1.361, 1.230, 1.102, .967, .837], .0005)
    a = regress([u], v)
    close(a["b"], [1.361, -.189], .0005)
    close(np.exp(a["b"][0]), 3.90, .005)
    close(a["R2"], .9999, .00005)
    close(2**a["b"][1], .877, .0005)
    close(1-2**a["b"][1], .12, .005)
    close(np.exp(a["b"][0]+a["b"][1]*np.log(32)), 2.03, .005)
    assert 32 > n.max()


def ex14():
    x1 = np.array([-1, -1, 0, 0, 1, 1])
    x2 = np.array([-1, 1, -1, 1, -1, 1])
    y = np.array([3, 5, 4, 7, 8, 9])
    a = regress([x1, x2], y)
    X = a["X"]
    close(X.T@X, np.diag([6, 4, 6]))
    close(X.T@y, [36, 9, 6])
    close(a["b"], [6, 9/4, 1])
    close(a["fitted"], [2.75, 4.75, 5, 7, 7.25, 9.25])
    close(a["residual"], [.25, .25, -1, 0, .75, -.25])
    close([a["E"], a["T"], a["R2"]], [1.75, 28, .9375])
    close(a["var"], .583, .0005)
    close(regress([x1], y)["b"][1], a["b"][1])
    close(regress([x2], y)["b"][1], a["b"][2])


def ex15():
    x1 = np.arange(1, 7)
    x2 = np.array([2, 1, 4, 3, 6, 5])
    y = np.array([3, 2, 6, 4, 8, 6])
    a = regress([x1, x2], y)
    X = a["X"]
    close(np.corrcoef(x1, x2)[0, 1], .83, .005)
    single_slope = regress([x1], y)["b"][1]
    close(single_slope, 31/35)
    close(single_slope, .886, .0005)
    close(X.T@X, [[6, 21, 21], [21, 91, 88], [21, 88, 91]])
    close(X.T@y, [29, 117, 122])
    close(a["b"], np.array([43, -13, 67])/48)
    close(a["b"], [.896, -.271, 1.396], .0005)
    assert single_slope > 0 > a["b"][1]


if __name__ == "__main__":
    for number in range(1, 16):
        try:
            globals()[f"ex{number:02d}"]()
        except Exception as exc:
            failures += 1
            print(f"FAIL 例{number} {type(exc).__name__}: {exc}")
        else:
            print(f"PASS 例{number}")
    sys.exit(bool(failures))
