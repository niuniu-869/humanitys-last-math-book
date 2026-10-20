## C.7 · 洛必达法则与泰勒公式（速记）

| 提示 | 内容 |
|---|---|
| 洛必达（$\frac00$） | $x\to a$ 时 $f,g\to0$，$g'\ne0$，且 $\lim\frac{f'}{g'}$ 存在（或 $\pm\infty$），则 $\lim\frac fg=\lim\frac{f'}{g'}$；由柯西中值定理：高度之比 = 某点斜率之比 |
| 洛必达（$\frac\infty\infty$） | 分子分母都趋于无穷，条件同上；对数 $\ll$ 幂 $\ll$ 指数：$\frac{\ln x}{x^\alpha}\to0$，$\frac{x^n}{e^x}\to0$ |
| 使用前先查 | 每一步都要确认仍是未定式；分母趋于非零有限数且分子有极限时直接用商的极限法则，不再求导（$\frac{1-\cos x}{x+x^2}$ 不能用第二次）；还要查去心邻域可导和 $g'\ne0$；求导后先化简 |
| 单向的法则 | 在条件满足时，$\lim\frac{f'}{g'}$ 存在就能推出 $\lim\frac fg$ 相等；反之不成立（$\frac{x^2\sin(1/x)}{\sin x}$、$\frac{x+\sin x}{x}$）；振荡或兜圈子就换办法 |
| 化归 | $0\cdot\infty$：$f\cdot g$ 可写成 $\frac{f}{1/g}$ 或 $\frac{g}{1/f}$，选求导后容易化简的一种；$\infty-\infty$：通分；$1^\infty,0^0,\infty^0$：先确认底数 $u>0$，再 $u^v=e^{v\ln u}$ |
| 与等价替换配合 | 乘除因子可以先换简单，再用洛必达；例 $\frac1x-\frac1{e^x-1}\to\frac12$ |
| 泰勒多项式 | $P_n=\sum_{k=0}^n\frac{f^{(k)}(x_0)}{k!}(x-x_0)^k$，泰勒公式 $f=P_n+o((x-x_0)^n)$（$n\ge1$，$x_0$ 处 $n$ 阶可导）；$n=1$ 是线性近似 |
| 展开的唯一性 | $n$ 次多项式加 $o((x-x_0)^n)$ 的写法只有一种；展开式中 $x^n$ 项的系数 $=\frac{f^{(n)}(0)}{n!}$（展开点 0，函数在该点 $n$ 阶可导），可由展开式读出高阶导数 |
| 五个展开（$x\to0$） | $e^x=1+x+\frac{x^2}{2!}+\cdots+\frac{x^n}{n!}+o(x^n)$；$\sin x=x-\frac{x^3}6+\frac{x^5}{120}-\cdots+o(x^{2m+2})$；$\cos x=1-\frac{x^2}2+\frac{x^4}{24}-\cdots+o(x^{2m+1})$；$\ln(1+x)=x-\frac{x^2}2+\frac{x^3}3-\cdots+o(x^n)$；$(1+x)^\alpha=1+\alpha x+\frac{\alpha(\alpha-1)}{2}x^2+\cdots+o(x^n)$ |
| 间接展开 | 代换 $u(x)\to0$；相乘时每个因子展开到「目标阶 − 另一因子的最低次数」；$\tan x=x+\frac{x^3}3+\cdots$ 用 $\tan x\cos x=\sin x$ 待定系数 |
| 泰勒求极限 | 展开到分母的阶：低次项全为零则读 $cx^m$ 的 $c$；还有非零低次项则约出主项再判断；全为零则极限为 0，定阶要继续找主项；$\tan x-\sin x=\frac{x^3}2+o(x^3)$，加减抵消时不能只换第一项 |
| 拉格朗日余项 | $R_n=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x-x_0)^{n+1}$，$\xi$ 在 $x_0$ 与 $x$ 之间；$n=0$ 是拉格朗日中值定理；证明：对 $R$ 和 $(x-x_0)^{n+1}$ 连用 $n+1$ 次柯西中值定理 |
| 误差估计 | 误差是 $R_n$，误差上界是 $\lvert R_n\rvert\le\frac{M}{(n+1)!}\lvert x-x_0\rvert^{n+1}$，$M$ 是 $\lvert f^{(n+1)}\rvert$ 在两点之间的上界；按精度从小到大试 $n$；余项的符号可比较大小 |
