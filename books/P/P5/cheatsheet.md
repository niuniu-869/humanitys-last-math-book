## P.5 · 随机变量的函数（速记）

| 提示 | 内容 |
|---|---|
| 离散的函数 | $P(Y=y)=\sum_{i:\,g(x_i)=y}p_i$：逐值代入，$g$ 值相同的合并相加，最后检查总和为 1 |
| 连续的函数 | 单点概率为 0，不能逐点代入；改求 $F_Y(y)=P(g(X)\le y)$，再求导 |
| 分布函数法四步 | 写 $Y$ 的取值范围；把 $\{g(X)\le y\}$ 翻译成 $X$ 的集合（画 $g$ 的图，看水平线下方）；用 $F_X$ 算；对 $y$ 求导并检查 $\int f_Y=1$ |
| 常见翻译 | $X^2\le y\iff -\sqrt y\le X\le\sqrt y$；$X\ge0$ 时只剩 $X\le\sqrt y$；$\lvert X\rvert\le y\iff -y\le X\le y$ |
| 范围截断 | $X$ 的取值范围会截掉区间的一端，要分段写 $F_Y$（如 $U(-1,2)$ 的 $\lvert X\rvert$） |
| 原子 | $g$ 把一整块质量压到一点（如 $\max(X,0)$），$F_Y$ 在该点有跳跃，高度就是那点的概率，没有单独的密度 |
| 单调变换公式 | $g$ 严格单调可导，$h=g^{-1}$：$f_Y(y)=f_X(h(y))\lvert h'(y)\rvert$，值域外为 0 |
| 绝对值的来源 | 减函数翻转不等号，$F_Y=1-F_X(h)$，求导得 $-f_X(h)h'$，而 $h'<0$，所以 $-h'=\lvert h'\rvert>0$ |
| 质量不变，长度改变 | $f_Y(y)=f_X(x)/\lvert g'(x)\rvert$：小段长度变成 $\lvert g'\rvert$ 倍，密度除以这个倍数 |
| 分支求和 | $g$ 不单调：$f_Y(y)=\sum_i f_X(h_i(y))\lvert h_i'(y)\rvert$，只算落在 $X$ 取值范围内的原像（$y\in g(I_i)$ 的那些段） |
| 正态的线性变换 | $X\sim N(\mu,\sigma^2)$，$a\ne0$：$aX+b\sim N(a\mu+b,\ a^2\sigma^2)$；标准化 $\frac{X-\mu}\sigma\sim N(0,1)$；造数 $x=\mu+\sigma\varepsilon$ |
| $F(X)$ 是均匀的 | $F$ 连续严格增时 $F(X)\sim U(0,1)$（事实 1），反过来 $F^{-1}(U)$ 服从 $F$（事实 2） |
| 逆变换采样 | 解 $u=F(x)$ 得 $x=F^{-1}(u)$；$E(\lambda)$：$x=-\ln(1-u)/\lambda$（$1-U$ 也服从 $U(0,1)$，写成 $-\ln u/\lambda$ 同分布）；离散：把 $[0,1)$ 按累积概率分段，$u$ 落进哪段取哪个值 |
