## C.12 · 反常积分（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| C12-01 | A | 方法 1 |
| C12-02 | A | 方法 1、2（选择） |
| C12-03 | A | 方法 2（选择） |
| C12-04 | A | 方法 4 |
| C12-05 | B | 方法 1、3（选择） |
| C12-06 | B | 方法 1 |
| C12-07 | B | 方法 2、3 |
| C12-08 | B | 方法 3、4 |
| C12-09 | B | 方法 3（证明） |
| C12-10 | B | 方法 2、3 |
| C12-11 | C | 方法 1、2、3 |
| C12-12 | C | 方法 1、2、3、4 |
| C12-13 | B | 混合（答案里标） |
| C12-14 | B | 混合（答案里标） |
| C12-15 | B | 混合（答案里标） |

### A 基础

**C12-01**〔A｜方法 1 · 考查：先截断，再取极限〕求 $\displaystyle\int_2^{+\infty}\frac{\mathrm{d}x}{(x+1)^2}$，并写出积到有限上限 $b$ 时的表达式。

**C12-02**〔A｜方法 1、2 · 考查：两种 $p$ 积分的分界方向〕（选择）记 $I_p=\displaystyle\int_0^1x^{-p}\,\mathrm{d}x$，$J_p=\displaystyle\int_1^{+\infty}x^{-p}\,\mathrm{d}x$，其中 $p\in\mathbb R$。下列说法正确的是（　）。

(A) $p<1$ 时，两者都收敛。

(B) $p>1$ 时，两者都发散。

(C) $p=1$ 时，两者都收敛。

(D) 不存在使两者同时收敛的实数 $p$。

**C12-03**〔A｜方法 2 · 考查：内部瑕点不能跨过去代端点〕（选择）关于 $\displaystyle\int_0^3\frac{\mathrm{d}x}{x-1}$，下列说法正确的是（　）。

(A) 原函数为 $\ln|x-1|$，所以积分等于 $\ln2$。

(B) $x=1$ 右侧的积分趋于 $+\infty$，所以整个积分的值为 $+\infty$。

(C) 左侧积分趋于 $-\infty$，右侧积分趋于 $+\infty$，所以反常积分发散。

(D) 只要把被积函数在 $x=1$ 处定义为 0，就能按普通定积分计算。

**C12-04**〔A｜方法 4 · 考查：半整数处的递推〕求 $\Gamma(\frac92)$。

### B 进阶

**C12-05**〔B｜方法 1、3 · 考查：零比值极限不保证同敛散〕（选择）在 $[\mathrm e,+\infty)$ 上，设 $f(x)=\dfrac1{x\ln x}$、$g(x)=\dfrac1{\sqrt x}$，记 $L=\displaystyle\lim_{x\to+\infty}\frac{f(x)}{g(x)}$。下列说法正确的是（　）。

(A) $L=0$，且 $\int_{\mathrm e}^{+\infty}f(x)\,\mathrm{d}x$ 收敛。

(B) $L=1$，且 $\int_{\mathrm e}^{+\infty}f(x)\,\mathrm{d}x$ 发散。

(C) $L=0$，且 $\int_{\mathrm e}^{+\infty}f(x)\,\mathrm{d}x$ 发散。

(D) $L=+\infty$，且 $\int_{\mathrm e}^{+\infty}f(x)\,\mathrm{d}x$ 发散。

选出答案后，说明为什么不能仅凭 $L=0$ 和 $\int_{\mathrm e}^{+\infty}g$ 发散来判断 $\int_{\mathrm e}^{+\infty}f$。

**C12-06**〔B｜方法 1 · 考查：差的积分与两个积分之差〕某项持续运行的服务，从第 $1$ 个月末开始比较两种方案。运行到第 $t$ 个月末附近，原方案的连续支出速率为 $1/\sqrt t$ 万元/月，新方案为 $1/\sqrt{t+1}$ 万元/月，其中 $t\ge1$。本题不计利息，两种方案都一直运行下去。建立反常积分，求新方案累计节省的支出；能否先分别计算两种方案的无限期总支出，再相减？说明理由。

**C12-07**〔B｜方法 2、3 · 考查：同一函数在两端需要不同的比较〕判断 $\displaystyle\int_0^{+\infty}\frac{1-\cos x}{x^2}\,\mathrm{d}x$ 的敛散性，无须求值。分别给出 $x=0$ 附近和无穷远处的依据。

**C12-08**〔B｜方法 3、4 · 考查：先保证可拆项，再反求系数〕求实数 $c$，使 $\displaystyle\int_0^{+\infty}(x^2-c)\mathrm e^{-x^2}\,\mathrm{d}x=0$，并说明拆成两项积分为什么合法。

**C12-09**〔B｜方法 3 · 考查：把变号函数拆成两个非负函数〕设 $f$ 在 $[1,+\infty)$ 上连续，且 $\displaystyle\int_1^{+\infty}|f(x)|\,\mathrm{d}x$ 收敛。定义 $f_+(x)=\dfrac{|f(x)|+f(x)}2$、$f_-(x)=\dfrac{|f(x)|-f(x)}2$。证明：$\int_1^{+\infty}f_+$ 与 $\int_1^{+\infty}f_-$ 都收敛，进而 $\int_1^{+\infty}f$ 收敛，并且

$$\left|\int_1^{+\infty}f(x)\,\mathrm{d}x\right|\le\int_1^{+\infty}|f(x)|\,\mathrm{d}x.$$

**C12-10**〔B｜方法 2、3 · 考查：内部问题点与两个端点一起筛选参数〕求实数 $a$ 的全部取值，使

$$\int_0^{+\infty}\frac{\mathrm{d}x}{\sqrt x\,|x-1|^a(1+x)}$$

收敛。$x=1$ 处的函数值不影响判断；若能连续补定义，可补定义后处理。

### C 提高

**C12-11**〔C｜方法 1、2、3 · 考查：先判收敛，再用分部把对数转走〕设 $a\in\mathbb R$。

1. 求 $\displaystyle I(a)=\int_0^{+\infty}\frac{\ln(1+x)}{x^a}\,\mathrm{d}x$ 收敛的全部参数范围，单独说明边界值为何不能取。
2. 求 $I(\frac32)$，并验证分部积分中两个端点的边界项都趋于 0。

拆法：先做 C12-05、C12-10。

**C12-12**〔C｜方法 1、2、3、4 · 考查：对数换元后，参数为零时要重新判断〕设 $a,b\in\mathbb R$，定义

$$K(a,b)=\int_0^1\frac{x^{a-1}}{(1+\ln\frac1x)^b}\,\mathrm{d}x.$$

1. 求积分收敛的全部参数条件。
2. 求 $K(0,2)$ 与 $K(1,-2)$。

拆法：先做 C12-05、C12-08。

### 章末混合练习

**C12-13**〔B〕分别求 $\displaystyle\int_0^{+\infty}(x-1)\mathrm e^{-x}\,\mathrm{d}x$ 与 $\displaystyle\int_0^{+\infty}|x-1|\mathrm e^{-x}\,\mathrm{d}x$，并解释为什么第二个积分不等于第一个积分的绝对值。

**C12-14**〔B〕对 $t\ge1$，设 $\displaystyle F(t)=\int_t^{+\infty}\frac{\ln x}{x^2}\,\mathrm{d}x$。求 $F(t)$、$F'(t)$（$t>1$）及 $\displaystyle\lim_{t\to+\infty}\frac{tF(t)}{\ln t}$。

**C12-15**〔B〕求实数 $a$ 的全部取值，使 $\displaystyle\int_{-\infty}^{+\infty}\frac{ax^3+x+1}{(1+x^2)^2}\,\mathrm{d}x$ 收敛，并求收敛时的积分值。若只算 $\displaystyle\lim_{R\to+\infty}\int_{-R}^R\frac{ax^3+x+1}{(1+x^2)^2}\,\mathrm{d}x$，能否得到同样的参数条件？
