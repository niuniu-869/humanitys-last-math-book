## P.10 · 统计量与抽样分布（答案）

**P10-01**
**答案：** $p^3(1-p)^1$；$p=0.7$ 时为 $0.1029$。

四个样本值独立，三个 1 各贡献一个 $p$，一个 0 贡献一个 $1-p$，所以联合概率是 $p^3(1-p)$。

区分点：先把样本值中的 1 和 0 数清楚，再用独立性连乘，不能把样本容量直接当作指数。

**P10-02**
**答案：** $\bar x=\frac32$，$s^2=7$，$s=\sqrt7$，$B_2=\frac{21}4=5.25$。

偏差为 $-\frac52,-\frac32,\frac12,\frac72$，平方和为 $21$。因此 $s^2=21/(4-1)=7$，而 $B_2=21/4$。

区分点：$S^2$ 的分母是 $n-1$，$B_2$ 的分母才是 $n$。

**P10-03**
**答案：** $Y\sim\chi^2(6)$，$E(Y)=6$，$\operatorname{Var}(Y)=12$。

每个 $(X_i-3)/2$ 都是独立标准正态，所以平方和有 6 个自由度；由 $\chi^2(k)$ 的期望和方差分别为 $k$、$2k$，得到上述数值。

区分点：自由度数的是独立标准正态项，不是原变量的均值或方差参数。

**P10-04**
**答案：** (C)。

A 错，$\bar X\sim N(\mu,\sigma^2/5)$；B 错，$4S^2/\sigma^2\sim\chi^2(4)$，自由度是 $5-1$；C 对，正态样本中 $\bar X$ 与 $S^2$ 独立；D 错，这个独立性需要总体正态，独立同分布本身不够。

区分点：要同时检查分布形式、自由度和正态条件，不能只看到“独立同分布”就套定理。

**P10-05**
**答案：** $E(U)=\sigma^2$。证明分四步。

1. 两组的样本均值都以 $\mu$ 为期望，所以 $E(\bar X-\bar Y)=\mu-\mu=0$。
2. $\operatorname{Var}(\bar X)=\sigma^2/4$，$\operatorname{Var}(\bar Y)=\sigma^2/6$；两组相互独立，差的方差相加：
$$\operatorname{Var}(\bar X-\bar Y)=\sigma^2\Big(\frac14+\frac16\Big).$$
3. 把平方的期望写成“方差加均值的平方”：
$$E\big[(\bar X-\bar Y)^2\big]=\operatorname{Var}(\bar X-\bar Y)+\big[E(\bar X-\bar Y)\big]^2=\sigma^2\Big(\frac14+\frac16\Big).$$
4. $U$ 是 $(\bar X-\bar Y)^2$ 除以常数 $\frac14+\frac16$，由期望的线性性，$E(U)=\sigma^2$。

整个过程只用到期望和方差，不需要总体是正态。

区分点：要主动把 $E[(\bar X-\bar Y)^2]$ 化成方差，而方差能相加靠的是两组独立；不能把 $S^2$ 无偏性的证明照搬过来。

**P10-06**
**答案：** $Q\sim\chi^2(6)$，$E(Q)=6$，$\operatorname{Var}(Q)=12$。

第一项：由第 3 节的偏差分解（总体均值取 1，$n=3$），
$$\sum_{i=1}^3(X_i-\bar X)^2+3(\bar X-1)^2=\sum_{i=1}^3(X_i-1)^2,$$
所以第一项等于 $\sum_{i=1}^3\Big(\dfrac{X_i-1}2\Big)^2$，是 3 个独立标准正态的平方和，服从 $\chi^2(3)$。

第二项：$\sum_{j=1}^4(Y_j-\bar Y)^2=3S_Y^2$，由正态样本定理 $\dfrac{3S_Y^2}{9}\sim\chi^2(4-1)=\chi^2(3)$。

两项分别只依赖两组样本，相互独立，由可加性 $Q\sim\chi^2(6)$，期望 6、方差 $2\times6=12$。

区分点：第一组把 $3(\bar X-1)^2$ 加了回去，被样本均值占用的那个方向又恢复了，自由度是 3 而不是 2；第二组仍按 $n-1=3$ 计。

**P10-07**
**答案：** $\operatorname{Cov}(\bar X,S^2)=0$，但 $\bar X$ 与 $S^2$ 不独立：$P(\bar X=0,S^2=\tfrac12)=0\ne\tfrac18=P(\bar X=0)P(S^2=\tfrac12)$。

四种样本值等可能，各 $\tfrac14$：$(0,0)$ 给 $(\bar X,S^2)=(0,0)$，$(1,1)$ 给 $(1,0)$，$(0,1)$、$(1,0)$ 都给 $(\tfrac12,\tfrac12)$。于是
$$E(\bar X)=\tfrac12,\qquad E(S^2)=\tfrac12\cdot\tfrac12=\tfrac14,\qquad E(\bar XS^2)=\tfrac12\cdot\tfrac12\cdot\tfrac12=\tfrac18,$$
$\operatorname{Cov}(\bar X,S^2)=\tfrac18-\tfrac12\cdot\tfrac14=0$。

协方差为 0 不能推出独立。$\bar X=0$ 只在 $(0,0)$ 时发生，此时 $S^2=0$，所以联合概率为 0；而 $P(\bar X=0)=\tfrac14$、$P(S^2=\tfrac12)=\tfrac12$，乘积为 $\tfrac18$。两者不等，所以不独立。

区分点：不相关不等于独立（P.7）；$\bar X$ 与 $S^2$ 独立是正态总体才有的结论。

**P10-08**
**答案：** (A)。

先把 $B_2$ 写回 $S^2$：$B_2=\frac56S^2$，所以 $\sqrt{B_2}=S\sqrt{5/6}$，
$$R=\frac{\sqrt5\,(\bar X-\mu)}{S\sqrt5/\sqrt6}=\frac{\bar X-\mu}{S/\sqrt6}\sim t(5).$$
A 对。B 中的量等于 $\sqrt{6/5}\,R$，是 $t(5)$ 变量再乘一个不等于 1 的常数，方差变成 $\frac65\cdot\frac53=2\ne\frac53$，不服从 $t(5)$。C 的自由度应是 $n-1=5$。D 中分母是随机的 $\sqrt{B_2}$，不是正态。

区分点：分母换成 $B_2$ 时先校正尺度，把它写回 $S$，再认 $t$ 分布；自由度跟着 $S^2$ 的 $n-1$ 走。

**P10-09**
**答案：** (C)。

两组独立正态样本，$\dfrac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2}\sim F(7,5)$。代入 $\sigma_1^2=2\sigma_2^2$，左边就是 $\dfrac{S_1^2}{2S_2^2}$，所以 $\dfrac{S_1^2}{2S_2^2}\sim F(7,5)$，取倒数 $\dfrac{2S_2^2}{S_1^2}\sim F(5,7)$，C 对。A 中 $S_1^2/S_2^2$ 是 $F(7,5)$ 变量的 2 倍，不服从 $F(7,5)$；B 把自由度顺序颠倒；D 把自由度写成了样本容量。

区分点：总体方差不相等时，先用已知的方差之比把比值标准化，再按 $n_i-1$ 和分子、分母的顺序定自由度。

**P10-10**
**答案：** $U\sim F(1,3)$，$V\sim\chi^2(3)$；$E(U)=E(V)=3$，但 $E(UV)=3\ne9$，所以 $U$ 与 $V$ 不独立。

1. **分布。** $\operatorname{Var}(\bar X)=\tfrac14$，所以 $2\bar X\sim N(0,1)$，$4\bar X^2\sim\chi^2(1)$。由正态样本定理，$V=3S^2=\dfrac{(4-1)S^2}{1}\sim\chi^2(3)$，并且与 $\bar X$ 独立。于是 $U=\dfrac{4\bar X^2/1}{3S^2/3}\sim F(1,3)$。
2. **两个期望。** $E(V)=3$；第 7 节给出 $n>2$ 时 $F(m,n)$ 的期望为 $\dfrac n{n-2}$，这里 $n=3$，$E(U)=3$。
3. **乘积的期望。** $UV=\dfrac{4\bar X^2}{S^2}\cdot3S^2=12\bar X^2$，所以 $E(UV)=12\cdot\tfrac14=3$。
4. **判断。** 如果 $U$ 与 $V$ 独立，应有 $E(UV)=E(U)E(V)=9$。实际是 3，所以不独立。

区分点：$\bar X$ 与 $S^2$ 独立，不代表共用同一个 $S^2$ 的两个新量独立；$U$ 里有 $1/S^2$，$V$ 里有 $S^2$，二者一起变动。

**P10-11**
**答案：** （1）恒等式成立，分解见下；（2）$E(S_w^2)=E(S_{\mathrm{all}}^2)=\sigma^2$，$\operatorname{Var}(S_w^2)=\dfrac{\sigma^4}4$，$\operatorname{Var}(S_{\mathrm{all}}^2)=\dfrac{2\sigma^4}9$，$S_{\mathrm{all}}^2$ 的方差更小。

（1）对第一组，用第 3 节的偏差分解，只是把中心换成常数 $\bar Z$（交叉项因 $\sum(X_i-\bar X)=0$ 消失）：
$$\sum_{i=1}^4(X_i-\bar Z)^2=3S_1^2+4(\bar X-\bar Z)^2;$$
同样 $\sum_{j=1}^6(Y_j-\bar Z)^2=5S_2^2+6(\bar Y-\bar Z)^2$。又
$$\bar X-\bar Z=\frac{3}{5}(\bar X-\bar Y),\qquad \bar Y-\bar Z=-\frac25(\bar X-\bar Y),$$
所以两项合起来是 $\Big(4\cdot\dfrac9{25}+6\cdot\dfrac4{25}\Big)(\bar X-\bar Y)^2=\dfrac{12}5(\bar X-\bar Y)^2$，相加即得所证等式。

（2）$\dfrac{3S_1^2}{\sigma^2}\sim\chi^2(3)$、$\dfrac{5S_2^2}{\sigma^2}\sim\chi^2(5)$，两组独立，所以 $\dfrac{8S_w^2}{\sigma^2}\sim\chi^2(8)$，$E(S_w^2)=\sigma^2$，$\operatorname{Var}(S_w^2)=\dfrac{\sigma^4}{64}\cdot16=\dfrac{\sigma^4}4$。

两组来自同一个 $N(\mu,\sigma^2)$，合起来的 10 个观测仍是简单随机样本，所以 $\dfrac{9S_{\mathrm{all}}^2}{\sigma^2}\sim\chi^2(9)$，$E(S_{\mathrm{all}}^2)=\sigma^2$，$\operatorname{Var}(S_{\mathrm{all}}^2)=\dfrac{\sigma^4}{81}\cdot18=\dfrac{2\sigma^4}9$。由于 $\dfrac29<\dfrac14$，$S_{\mathrm{all}}^2$ 更稳定：它比 $S_w^2$ 多用了 $(\bar X-\bar Y)^2$ 这一个自由度。

区分点：多出的自由度来自“两组均值也相同”；若两组总体均值不同，$(\bar X-\bar Y)^2$ 会把均值差也算进方差，$S_{\mathrm{all}}^2$ 就不再无偏，只能用 $S_w^2$。

**P10-12**
**答案：** $\dfrac5{16}\big[2\Phi(1)-1\big]\approx0.2133$。（方法 4 与二项分布）

设第 $i$ 次的处理时长为 $X_i$，成功指标为 $Y_i$（成功取 1，否则取 0），成功次数 $K=\sum_{i=1}^4Y_i\sim B(4,\tfrac12)$。所求事件是 $\{K\le1\}$ 与 $\{|\bar X-10|\le\tfrac12\}$ 同时发生。

- $P(K\le1)=\dfrac{1+4}{16}=\dfrac5{16}$。
- $\bar X\sim N(10,\tfrac14)$，标准差 $\tfrac12$，所以 $P(|\bar X-10|\le\tfrac12)=P(|Z|\le1)=2\Phi(1)-1\approx0.6827$。
- $K$ 只依赖成功指标，$\bar X$ 只依赖处理时长，两组变量独立，所以两个概率相乘：$\dfrac5{16}\times0.6827\approx0.2133$。

区分点：能相乘是因为两个事件来自相互独立的两组变量，这和“同一正态样本的 $\bar X$ 与 $S^2$ 独立”不是一回事。

**P10-13**
**答案：** $n\ge225$。（方法 2 与前面不等式工具）

简单随机样本保证 $\operatorname{Var}(\bar X)=9/n$。切比雪夫不等式给出
$$P(|\bar X-\mu|\ge1)\le\frac{\operatorname{Var}(\bar X)}{1^2}=\frac9n.$$
令 $9/n\le0.04$，得 $n\ge225$。

区分点：这里求的是保证上界的样本量，不能把 $9/n$ 当成事件的精确概率；没有独立同分布的抽样条件，$\operatorname{Var}(\bar X)=9/n$ 也不成立。

**P10-14**
**答案：** $E(\bar X)=0.4$，$\operatorname{Var}(\bar X)=0.0096$，且
$$P\left(\sum X_i=8\right)=\binom{25}{8}0.4^8 0.6^{17}\approx0.1200.$$（方法 2 与 P.3 的二项分布）

单个 $X_i$ 的期望为 $0.4$、方差为 $0.4\times0.6=0.24$，平均后方差除以 25。和服从 $B(25,0.4)$，代入二项分布律得到所求概率。

区分点：样本均值的方差要除以样本容量，而样本总和的分布参数是次数 25，二者不能混用。
