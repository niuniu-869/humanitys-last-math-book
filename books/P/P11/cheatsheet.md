## P.11 · 参数估计（速记）

| 提示 | 内容 |
|---|---|
| 估计量与估计值 | 估计量 $\hat\theta=T(X_1,\dots,X_n)$ 是随机变量，估计值是代入数据后的数；评价针对估计量，看重复抽样下的分布 |
| 矩估计 | 令前 $m$ 阶样本矩 $A_k=\frac1n\sum X_i^k$ 等于总体矩 $E(X^k)$，解出参数（$m$ 个参数用前 $m$ 阶）；一般用尽量低阶的矩；$\hat\sigma^2=A_2-\bar X^2$，分母是 $n$ |
| 最大似然 | $L(\theta)=\prod f(x_i;\theta)$，取 $\ln$、求导（多参数求偏导）、令其为 0，并确认是最大；$L$ 不是 $\theta$ 的概率分布 |
| 驻点不存在 | 看单调性与边界，真能取到最大值才有估计：$U(0,\theta)$ 的 $L=\theta^{-n}$（$\theta\ge\max x_i$）递减，所以 $\hat\theta=\max x_i$；泊松全零样本在 $\lambda>0$ 内无最大值 |
| 不变性 | $\hat\theta$ 是 $\theta$ 的最大似然估计，则 $g(\hat\theta)$ 是 $g(\theta)$ 的最大似然估计（无偏性没有此性质，如 $S$ 不是 $\sigma$ 的无偏估计） |
| 常见结果 | $B(1,p)$、$P(\lambda)$：$\bar X$；$E(\lambda)$：$1/\bar X$；$N(\mu,\sigma^2)$：$\bar X$ 与 $\frac1n\sum(X_i-\bar X)^2$；类别概率的最大似然 = 频率 |
| 截尾 | 失效的观察贡献密度，被截尾的贡献 $1-F(\tau)$；指数分布 $\hat\lambda=$ 失效数 ÷ 总工作时间；丢掉截尾观察会严重低估寿命 |
| 无偏 | $E\hat\theta=\theta$；$E\bar X=\mu$，$E S^2=\sigma^2$，$E\hat\sigma^2=\frac{n-1}n\sigma^2$（以 $\bar X$ 为中心的平方和少了 $n(\bar X-\mu)^2$）；$S$ 不是 $\sigma$ 的无偏估计 |
| 有效 | 两个无偏估计比方差，对一切 $\theta$ 都更小者更有效；$\sum c_iX_i$（$\sum c_i=1$）中 $c_i=\frac1n$ 的方差最小；$U(0,\theta)$ 里 $\frac{n+1}nM$ 比 $2\bar X$ 有效得多 |
| 相合 | $\hat\theta_n\xrightarrow{P}\theta$；均方误差 $=$ 方差 $+$ 偏差²，两项 $\to0$ 是相合的充分条件；$X_1$ 无偏不相合，$M$ 有偏相合 |
| 置信区间含义 | $P(\hat\theta_L\le\theta\le\hat\theta_U)=1-\alpha$，随机的是区间；95% 是方法的覆盖率，不是这一个区间含真值的概率 |
| 枢轴量法 | 找含 $\theta$ 且分布已知的 $G$，$P(a\le G\le b)=1-\alpha$，解出 $\theta$；半宽与 $\sqrt n$ 成反比，把握越高区间越宽 |
| 单正态 | $\mu$：$\sigma$ 已知 $\bar X\pm z_{\alpha/2}\frac\sigma{\sqrt n}$，未知 $\bar X\pm t_{\alpha/2}(n-1)\frac S{\sqrt n}$；$\sigma^2$：$\big[\frac{(n-1)S^2}{\chi^2_{\alpha/2}},\frac{(n-1)S^2}{\chi^2_{1-\alpha/2}}\big]$，端点顺序反过来 |
| 两正态 | 均值差：方差已知用 $z$，未知但相等用合并方差 $S_w^2$ 的 $t(n_1+n_2-2)$；方差比用 $F$，$F_{1-\alpha/2}(m,n)=1/F_{\alpha/2}(n,m)$；成对数据先取差再做单样本；不能当两个独立样本 |
| 0-1 与单侧 | $\hat p\pm z_{\alpha/2}\sqrt{\hat p(1-\hat p)/n}$（$n\hat p$、$n(1-\hat p)$ 不太小）；$n\ge z_{\alpha/2}^2/(4d^2)$；单侧限把 $\frac\alpha2$ 换成 $\alpha$ |
