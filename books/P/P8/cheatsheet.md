## P.8 · 大数定律与中心极限定理（速记）

| 提示 | 内容 |
|---|---|
| 马尔可夫不等式 | $X\ge0$：$P(X\ge a)\le\frac{E(X)}a$；证明靠 $a\cdot\mathbf 1\{x\ge a\}\le x$ 取期望；没有“非负”就不成立 |
| 切比雪夫不等式 | $P(\lvert X-\mu\rvert\ge\varepsilon)\le\frac{\sigma^2}{\varepsilon^2}$，即 $\le\frac1{k^2}$（$\varepsilon=k\sigma$）；对任何分布成立，所以偏保守；下界写法 $P(\lvert X-\mu\rvert<\varepsilon)\ge1-\frac{\sigma^2}{\varepsilon^2}$ |
| 依概率收敛 | $X_n\xrightarrow{P}a$：对每个 $\varepsilon>0$，$P(\lvert X_n-a\rvert\ge\varepsilon)\to0$；不蕴含期望收敛（$X_n=n$ 的概率为 $\frac1n$，其余取 0） |
| 平均的方差 | $\mathrm{Var}(\bar X_n)=\frac{\sigma^2}n$，标准差 $\frac\sigma{\sqrt n}$；波动减半要把 $n$ 乘 4 |
| 切比雪夫大数定律 | 两两不相关且 $\mathrm{Var}(X_i)\le C$：$P(\lvert\bar X_n-E\bar X_n\rvert\ge\varepsilon)\le\frac C{n\varepsilon^2}$；$X_1=X_2=\cdots$ 是“不相关”条件的反例，$\mathrm{Var}(X_i)=i^2$ 是“方差有界”条件的反例 |
| 伯努利大数定律 | 频率 $f_n\xrightarrow{P}p$；保证精度所需次数 $n\ge\frac{p(1-p)}{\delta\varepsilon^2}$（切比雪夫版，偏大，如硬币 $\varepsilon=0.01,\delta=0.05$ 需 50000 次） |
| 辛钦大数定律 | 独立同分布，期望存在即可（方差不必存在，这是充分条件）：$\bar X_n\xrightarrow{P}\mu$；证明把变量切成有界的中等部分（切比雪夫）和罕见的大值（马尔可夫）；柯西分布期望不存在，平均不稳定 |
| 蒙特卡洛 | 用 $\frac1n\sum g(X_i)$ 估 $E\,g(X)$，误差 $\frac\sigma{\sqrt n}$ 量级，与维数无关；概率用指示变量；小批量梯度同理 |
| 棣莫弗–拉普拉斯 | $X\sim B(n,p)$ 时 $\frac{X-np}{\sqrt{npq}}\to N(0,1)$；$n$ 大且 $np$、$nq$ 都不太小时 $X\approx N(np,npq)$ |
| 连续性修正 | 整数 $a\le X\le b$ 改为 $a-\frac12\le X\le b+\frac12$；如 $P(X\ge75)=P(X\ge74.5)$；不修正会偏差明显 |
| 泊松还是正态 | $np$ 很小（如 2）用泊松近似；$np$、$nq$ 都较大用正态近似 |
| 中心极限定理 | 独立同分布，$\mathrm{Var}=\sigma^2\in(0,\infty)$（充分条件；去掉独立或用柯西都会失败）：$\frac{\sum X_i-n\mu}{\sigma\sqrt n}\to N(0,1)$；$\bar X_n\approx N(\mu,\frac{\sigma^2}n)$，$\sum X_i\approx N(n\mu,n\sigma^2)$ |
| 证明骨架 | 标准化 $\to$ 矩母函数 $1+\frac{t^2}2+o(t^2)$ $\to$ 求和得 $(1+\frac{t^2}{2n})^n\to\mathrm{e}^{t^2/2}$ |
| 大数 vs 中心极限 | 大数定律说平均**靠近**$\mu$；中心极限定理说偏差的**形状**与大小：$\approx\frac\sigma{\sqrt n}\times$ 标准正态；方差无限时两者都可能失效 |
