## C.9 · 定积分的概念与性质（速记）

| 提示 | 内容 |
|---|---|
| 四步 | 分割、近似、求和、取极限；$[0,b]$ 上 $x^2$ 的右端点和 $S_n=\frac{b^3}6(1+\frac1n)(2+\frac1n)\to\frac{b^3}3$ |
| 平方和 | $\sum_{i=1}^ni^2=\frac{n(n+1)(2n+1)}6$（归纳法），$\sum i=\frac{n(n+1)}2$ |
| 黎曼和与定义 | $S=\sum f(\xi_i)\Delta x_i$，$\lambda=\max\Delta x_i\to0$ 时极限与分割、取点无关，则 $\int_a^bf\,\mathrm dx=\lim S$；条件是 $\lambda\to0$，不是 $n\to\infty$；只算出等分右端点和的极限不能断定可积（狄利克雷函数的右端点和恒为 1） |
| 几何意义 | 带符号的面积：轴上方为正、轴下方为负；$\int_0^3(x-1)\,\mathrm dx=\frac32$，半圆 $\int_{-2}^2\sqrt{4-x^2}\,\mathrm dx=2\pi$ |
| 梯形近似 | 采样点之间连线，面积是「宽 × 两边高的平均」；ROC 曲线下面积 AUC 就这样估 |
| 可积的条件 | 连续 ⟹ 可积；有界且只有有限个间断点 ⟹ 可积；单调 ⟹ 可积；可积 ⟹ 有界（无界不可积）；前三条只是充分条件；证明靠大和与小和之差趋于 0 |
| 两个反例 | 狄利克雷函数有界但不可积（全取有理点得和 1，全取无理点得和 0）；$\sin\frac1x$（补 $f(0)=0$）只有一个间断点，可积 |
| 约定与线性 | $\int_a^a=0$，$\int_b^a=-\int_a^b$；$\int(\alpha f+\beta g)=\alpha\int f+\beta\int g$；$\int_a^bk\,\mathrm dx=k(b-a)$ |
| 区间可加 | $\int_a^b=\int_a^c+\int_c^b$，$c$ 在区间外也成立；带绝对值、取整、分段的函数在分界点拆开 |
| 易混 | 通常不能把乘积的积分拆成两个积分的乘积；如 $f=g=x$ 在 $[0,1]$ 上，两者是 $\frac13$ 与 $\frac14$ |
| 比较与估值 | $a<b$ 时 $f\le g\Rightarrow\int f\le\int g$；$m(b-a)\le\int_a^bf\le M(b-a)$；$\lvert\int f\rvert\le\int\lvert f\rvert$；$\int f\ge0$ 推不出 $f\ge0$；$a>b$ 时先换成 $-\int_b^a$，不等号反向 |
| 积分极限的夹逼 | 先估值再夹逼；被积函数在某点附近不变小时（如 $x^n$ 在 1 附近），切出那一小段另估（先看 $\varepsilon$ 再选 $\delta$、再选 $N$）；逐点趋于 0 不能直接搬进积分号 |
| 平均值 | $\bar f=\frac1{b-a}\int_a^bf\,\mathrm dx$ 是 $\frac1n\sum f(x_i)$ 的极限；$x^2$ 在 $[0,3]$ 上 $\bar f=3$（不是两端平均 4.5），$\xi=\sqrt3$ |
| 积分中值定理 | $f$ 连续 ⟹ $\exists\xi\in[a,b]$，$\int_a^bf=f(\xi)(b-a)$；证明：最值定理 → 估值 → 介值定理；连续时 $\xi$ 可取在 $(a,b)$ 内；没有连续条件时不保证存在中值点，阶梯函数就是反例 |
| 带积分条件的存在性 | 先用中值定理把积分换成函数值，再接罗尔定理（系数抵掉区间长度） |
