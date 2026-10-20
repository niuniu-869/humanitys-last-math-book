## C.1 · 函数与数列的极限（速记）

| 提示 | 内容 |
|---|---|
| 函数 | 定义域 + 对应法则，每个 $x$ 恰好对应一个 $y$；定义域、法则都相同才是同一个函数 |
| 求定义域 | 分母 $\ne0$；偶次根号下 $\ge0$；对数真数 $>0$；复合时 $x$ 在内层定义域，且内层值在外层定义域，化简前先查 |
| 有界与无界 | 有界：$\exists M\ \forall x\ \lvert f\rvert \le M$；无界：$\forall M\ \exists x\ \lvert f(x)\rvert >M$（对方报 $M$，你拿 $x$）；要看定义域：$\frac1x$ 在 $[1,+\infty)$ 有界，在 $(0,1)$ 无界 |
| 绝对值不等式 | $\lvert x-a\rvert <\delta\iff a-\delta<x<a+\delta$；$\lvert a+b\rvert \le\lvert a\rvert+\lvert b\rvert$；$\bigl\lvert\,\lvert a\rvert-\lvert b\rvert\,\bigr\rvert\le\lvert a-b\rvert$ |
| 反函数 | 严格单调则有反函数；解 $x$ 再对调字母；定义域、值域互换，图像关于 $y=x$ 对称 |
| 反三角函数 | $\arcsin:[-1,1]\to[-\frac\pi2,\frac\pi2]$；$\arccos:[-1,1]\to[0,\pi]$；$\arctan:\mathbb R\to(-\frac\pi2,\frac\pi2)$；$\arcsin x+\arccos x=\frac\pi2$；$\arcsin(\sin x)=x$ 只在 $[-\frac\pi2,\frac\pi2]$ 上成立 |
| 三角函数补全 | $\sec x=\frac1{\cos x}$，$\csc x=\frac1{\sin x}$，$\cot x=\frac{\cos x}{\sin x}$（$\tan x\ne0$ 时也等于 $\frac1{\tan x}$）；$1+\tan^2x=\sec^2x$，$1+\cot^2x=\csc^2x$；由平方关系求值后用象限定符号 |
| ε-N 定义 | $\forall\varepsilon>0\ \exists N\ \forall n>N\ \lvert a_n-a\rvert <\varepsilon$；对方给 $\varepsilon$，你回 $N$；证明时先化简再放大，$N=\lceil g(\varepsilon)\rceil$ |
| 不收敛于 $a$ | $\exists\varepsilon_0>0\ \forall N\ \exists n>N\ \lvert a_n-a\rvert \ge\varepsilon_0$；$\lvert q\rvert <1$ 时 $q^n\to0$ |
| 收敛数列的性质 | 极限唯一；有界；保号（$a>0$ 则从某项起 $a_n>\frac a2$）；子数列同极限，所以两个子数列极限不同则发散；$(-1)^n$ 是标准反例 |
| 四则运算法则 | 有限个数列的和、积成立；商要求分母极限 $\ne0$；有理式同除最高次，含根式乘共轭，$n$ 项和先求和，含 $q^n$ 同除最大底数的 $n$ 次幂 |
| 夹逼准则 | $y_n\le x_n\le z_n$，$y_n,z_n$ 同趋于 $a$，则 $x_n\to a$；$n$ 项和用最大项、最小项放缩；$c^{1/n}\to1$（$c>0$），$\sqrt[n]n\to1$ |
| 单调有界与递推数列 | 单调有界必收敛；递推数列先证有界、单调，再令 $n\to\infty$ 解 $A=f(A)$，次序不能倒（否则可能「解出」不存在的极限）；$x_{n+1}=\frac12(x_n+\frac2{x_n})\to\sqrt2$ |
| 数 $e$ | $\left(1+\frac1n\right)^n$ 单调增加且 $<3$，极限 $e\approx2.71828$；$\left(1-\frac1n\right)^n\to\frac1e$；复利结算越勤本息和越大，但有上界 |
