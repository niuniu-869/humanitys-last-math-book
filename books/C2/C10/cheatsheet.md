## C.10 · 微积分基本定理（速记）

| 提示 | 内容 |
|---|---|
| 变上限积分 | $\Phi(x)=\int_a^xf(t)\,\mathrm dt$，$f$ 连续 ⟹ $\Phi'(x)=f(x)$；积分变量用 $t$，不与上限 $x$ 混 |
| 证明骨架 | 可加性得 $\Phi(x+h)-\Phi(x)=\int_x^{x+h}f$ → 中值定理 $=f(\xi_h)h$ → $\xi_h\to x$、$f$ 连续 |
| 上下限是函数 | $\frac{\mathrm d}{\mathrm dx}\int_{v(x)}^{u(x)}f(t)\,\mathrm dt=f(u)u'-f(v)v'$；上下限颠倒先变号 |
| 被积函数含 $x$ | 能拆成「只含 $x$ 的因子」乘「只含 $t$ 的函数」时，先提出前者再用乘积法则（$\int_0^x(x^2-t^2)f(t)\,\mathrm dt\to2x\int_0^xf$）；不能这样拆时（如 $\mathrm e^{xt}$）不可直接套公式 |
| 条件 | $f$ 可积时 $\Phi$ 连续；$f$ 在某点连续，则该点 $\Phi'=f$（连续是充分条件，不连续的点要单独检查）；跳跃点需分别检查左右导数（$f$ 跳跃时 $\Phi$ 连续但可有尖点） |
| 原函数 | $F'=f$；两个原函数差常数（导数恒为 0，要在区间上）；$\int f\,\mathrm dx=F+C$ |
| 不定积分 vs 定积分 | 不定积分是一族函数，定积分是一个数；$(\int f)'=f$，$\int F'=F+C$ |
| 基本积分表 | $\int x^\alpha\mathrm dx=\frac{x^{\alpha+1}}{\alpha+1}+C$（$\alpha\ne-1$），$\int\frac1x\mathrm dx=\ln\lvert x\rvert+C$（区间不跨 0），$\int\mathrm e^x\mathrm dx=\mathrm e^x+C$，$\int a^x\mathrm dx=\frac{a^x}{\ln a}+C$（$a>0,a\ne1$），$\int\sin x\,\mathrm dx=-\cos x+C$，$\int\cos x\,\mathrm dx=\sin x+C$，$\int\sec^2x\,\mathrm dx=\tan x+C$，$\int\csc^2x\,\mathrm dx=-\cot x+C$，$\int\frac{\mathrm dx}{\sqrt{1-x^2}}=\arcsin x+C$（$\lvert x\rvert<1$），$\int\frac{\mathrm dx}{1+x^2}=\arctan x+C$ |
| 化成表中形状 | 根号、分母写成指数；乘积先展开；$\tan^2=\sec^2-1$，$1=\sin^2+\cos^2$ 拆分子 |
| 原函数存在 | $f$ 连续 ⟹ 有原函数 $\int_a^xf$；存在不等于有初等表达式（$\mathrm e^{-x^2}$） |
| 牛顿–莱布尼茨 | $f$ 连续，$F'=f$：$\int_a^bf=F(b)-F(a)=[F]_a^b$；常数抵消，所以不加 $C$ |
| 公式的前提 | 常用前提是区间上连续（更一般：可积且有原函数）；$\int_{-1}^1\frac{\mathrm dx}{x^2}$ 不能用（无界不可积，算出的 $-2$ 是错的）；分段、$\max$、绝对值先拆区间 |
| 密度与分布函数 | $X$ 只取 $[0,1]$ 内的值时，$F(x)=\int_0^xf(t)\,\mathrm dt$（$0\le x\le1$），区间外分别为 0、1；在密度连续的内部点有 $F'=f$；$P(a\le X\le b)=F(b)-F(a)$（$0\le a\le b\le1$） |
| 变限积分的分析 | 求极限：$\frac00$ 或 $\frac\infty\infty$ 用洛必达，积分按公式求导（上限为 $u(x)$ 时乘 $u'$）；单调与极值：$\Phi'=f$ 的符号决定增减，变号点是极值点，极值用牛顿–莱布尼茨算 |
| 求导证性质 | 要证 $G\equiv0$：证 $G'\equiv0$ 加一点的值（奇函数的 $\int_0^xf$ 是偶函数） |
