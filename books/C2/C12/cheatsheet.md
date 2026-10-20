## C.12 · 反常积分（速记）

| 提示 | 内容 |
|---|---|
| 无穷区间（方法 1） | $\int_a^{+\infty}f=\lim_{b\to+\infty}\int_a^bf=F(+\infty)-F(a)$；极限不存在或为无穷则发散；极限要单独算（洛必达） |
| 两头无穷 | 在任一点 $c$ 拆开，两半都收敛才收敛；仅凭 $\lim_{R\to\infty}\int_{-R}^R$ 存在不能判收敛（$\int_{-\infty}^{+\infty}x\,\mathrm{d}x$ 发散）；两侧都收敛后，奇函数积分为 0 才成立 |
| $p$ 积分（无穷远） | $\int_1^{+\infty}\frac{\mathrm{d}x}{x^p}$：$p>1$ 收敛，值 $\frac1{p-1}$；$p\le1$ 发散；被积函数趋于 0 不够，要看快慢；$\int_2^{+\infty}\frac{\mathrm{d}x}{x\ln^px}$ 同样以 $p=1$ 为界 |
| 瑕积分（方法 2） | 瑕点 $a$：$\int_a^bf=\lim_{\varepsilon\to0^+}\int_{a+\varepsilon}^bf$；瑕点在内部必须拆开，两半都收敛才收敛；$\int_{-1}^1\frac{\mathrm{d}x}{x^2}$ 不能直接算（会得 $-2$） |
| $p$ 积分（瑕点） | $\int_0^1\frac{\mathrm{d}x}{x^p}$：$p<1$ 收敛，值 $\frac1{1-p}$；$p\ge1$ 发散；与无穷远处方向相反 |
| 换元与分部 | 先在有限区间做再取极限；换元用严格单调且有连续导数的函数，端点按极限对应；先截断再取极限；分部的边界项两端分别取极限；$x=\frac1t$ 把无穷区间与瑕积分互换 |
| 比较判别法（方法 3） | 每次只比较同一个问题端点，避开该端点后两函数连续；$0\le f\le g$：$\int g$ 收敛 $\Rightarrow\int f$ 收敛；极限形式 $\lim\frac fg=l$：$0<l<\infty$ 同敛散，$l=0$ 看 $g$ 收敛，$l=\infty$ 看 $g$ 发散（只能单向）；$f\ge0$ 不可少 |
| 怎样读 $p$ | 有幂函数主要部分时：无穷远处 $\frac c{x^p}$，瑕点 $a$ 处 $\frac c{\lvert x-a\rvert^p}$，分别按 $p>1$、$p<1$ 判断；内部瑕点两侧分别判断，每段至多一个问题端点，全部收敛才收敛；负函数取负号，变号函数可先判绝对收敛，不绝对收敛时不能直接判发散 |
| 绝对收敛 | $\int\lvert f\rvert$ 收敛 $\Rightarrow\int f$ 收敛（$0\le f+\lvert f\rvert\le2\lvert f\rvert$）；反之不成立，$\int_1^{+\infty}\frac{\sin x}x$ 条件收敛，$\int\frac{\lvert\sin x\rvert}x$ 发散 |
| $\Gamma$ 函数（方法 4） | $\Gamma(s)=\int_0^{+\infty}x^{s-1}\mathrm{e}^{-x}\mathrm{d}x$，$s>0$ 收敛；$\Gamma(s+1)=s\Gamma(s)$（分部，边界项为 0），$\Gamma(1)=1$，$\Gamma(n+1)=n!$（$n=0,1,2,\dots$） |
| $\Gamma$ 的常用值 | $\Gamma(\frac12)=\sqrt\pi$（等价于 $\int_0^{+\infty}\mathrm{e}^{-t^2}\mathrm{d}t=\frac{\sqrt\pi}2$，C.25.9）；$\Gamma(\frac32)=\frac{\sqrt\pi}2$，$\Gamma(\frac52)=\frac{3\sqrt\pi}4$ |
| 用 $\Gamma$ 算积分 | $\int_0^{+\infty}x^\alpha\mathrm{e}^{-\beta x^k}\mathrm{d}x=\frac1k\beta^{-(\alpha+1)/k}\Gamma\big(\frac{\alpha+1}k\big)$（$\beta,k>0$，$\alpha>-1$）；特例 $\int_0^{+\infty}x^m\mathrm{e}^{-\beta x}=\frac{\Gamma(m+1)}{\beta^{m+1}}$（$m>-1$），$\int_0^1(\ln\frac1x)^n\mathrm{d}x=n!$（$n$ 为非负整数）；$s$ 为正整数或正半整数时，可用递推降到 $\Gamma(1)$ 或 $\Gamma(\frac12)$；其他 $s$ 本章保留为 $\Gamma(s)$ |
| 应用 | 永续年金现值 $\int_0^{+\infty}c\,\mathrm{e}^{-rt}\mathrm{d}t=\frac cr$；指数分布 $\lambda\mathrm{e}^{-\lambda x}$ 总概率 1、平均值 $\frac1\lambda$ |
