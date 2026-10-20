## C.15 · 幂级数与泰勒级数（速记）

| 提示 | 内容 |
|---|---|
| 收敛域与和函数 | 函数项级数 $\sum u_n(x)$：固定 $x$ 当数项级数判，收敛的全体 $x$ 是收敛域，对应的和是和函数；$\sum x^n=\frac1{1-x}$ 只在 $\lvert x\rvert<1$ 成立 |
| 阿贝尔定理 | 幂级数在 $x_0$ 收敛 ⇒ $\lvert x\rvert<\lvert x_0\rvert$ 内绝对收敛；所以收敛域以 0（或 $x_0$）为中心，有半径 $R$，端点要单独判 |
| 收敛半径 | $R=\frac1\rho$，$\rho=\lim\left\lvert\frac{a_{n+1}}{a_n}\right\rvert$ 或 $\lim\sqrt[n]{\lvert a_n\rvert}$；缺项时对相邻非零项取比值；中心不在 0 时把 $x-x_0$ 当作整体 |
| 五个标准例子 | $\sum x^n$：$(-1,1)$；$\sum\frac{x^n}n$：$[-1,1)$；$\sum\frac{x^n}{n^2}$：$[-1,1]$；$\sum\frac{x^n}{n!}$：$\mathbb R$；$\sum n!x^n$：$\{0\}$ |
| 逐项运算 | 收敛区间内可逐项求导、逐项积分，和函数连续，半径不变；端点要重新判（求导易丢端点，积分可能得端点） |
| 系数的来历 | 能写成幂级数 ⇒ 系数 $a_k=\frac{f^{(k)}(x_0)}{k!}$，所以展开式唯一，间接展开得到的就是泰勒级数 |
| 求和函数 | 系数有分母先求导、有分子先积分，化成 $\sum q^n=\frac1{1-q}$ 再还原；积分下限取 0 并加 $S(0)$；代入一点得数项级数的和：$\sum nx^n=\frac x{(1-x)^2}$ |
| 泰勒级数的收敛 | 泰勒级数在 $x$ 处等于 $f(x)$ ⇔ $R_n(x)\to0$；导数有公共的界 $M$（充分条件）时 $\lvert R_n\rvert\le\frac{M\lvert x-x_0\rvert^{n+1}}{(n+1)!}\to0$；任意阶可导不够（$e^{-1/x^2}$） |
| 七个母式 | $\frac1{1-x}=\sum x^n$（$\lvert x\rvert<1$）；$e^x=\sum\frac{x^n}{n!}$；$\sin x=\sum\frac{(-1)^nx^{2n+1}}{(2n+1)!}$；$\cos x=\sum\frac{(-1)^nx^{2n}}{(2n)!}$（以上三式 $x\in\mathbb R$） |
| 母式（续） | $\ln(1+x)=\sum\frac{(-1)^nx^{n+1}}{n+1}$（$-1<x\le1$）；$\arctan x=\sum\frac{(-1)^nx^{2n+1}}{2n+1}$（$\lvert x\rvert\le1$）；$(1+x)^\alpha=\sum\binom\alpha nx^n$（$\lvert x\rvert<1$；$\alpha$ 为非负整数时对一切 $x$） |
| 间接展开 | 代换（$x\to-x,x^2$）、线性组合、乘 $x$ 的幂、逐项求导或积分；范围解不等式，端点重判；展开点 $x_0\ne0$ 时令 $u=x-x_0$ |
| 近似计算误差 | 交错级数：误差不超过第一个舍去项；否则尾巴与等比级数比较；代入点离中心越近越快（$\ln2$ 取 $x=\frac13$ 而不取 $1$） |
| 欧拉公式 | $e^{i\theta}=\cos\theta+i\sin\theta$；$\cos\theta=\frac{e^{i\theta}+e^{-i\theta}}2$，$\sin\theta=\frac{e^{i\theta}-e^{-i\theta}}{2i}$；乘 $e^{i\theta}$ 是绕原点逆时针转 $\theta$ |
| 复数乘方 | $z=re^{i\theta}$，$z^n=r^ne^{in\theta}$：模取 $n$ 次方，辐角乘 $n$ |
| 一致收敛 | $\sup_{x\in I}\lvert S_n-S\rvert\to0$；$\lvert u_n\rvert\le M_n$ 且 $\sum M_n$ 收敛 ⇒ 一致收敛 ⇒ 各项连续时和函数连续、可逐项积分；导数级数一致收敛才可逐项求导 |
