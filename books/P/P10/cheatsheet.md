## P.10 · 统计量与抽样分布（速记）

| 提示 | 内容 |
|---|---|
| 简单随机样本 | $X_1,\dots,X_n$ 独立同分布于总体；联合分布律或密度是各项之积；样本是随机变量，样本值是数；不放回抽样在总体远大于 $n$ 时可近似当作独立 |
| 五数概括、箱线图 | 最小值、$Q_1$、中位数、$Q_3$、最大值；$\mathrm{IQR}=Q_3-Q_1$；超出 $Q_1-1.5\,\mathrm{IQR}$、$Q_3+1.5\,\mathrm{IQR}$ 的点是异常点；右侧拖尾的数据常有平均数大于中位数，仅作线索，须结合图形；直方图柱高 $=\dfrac{\text{个数}}{n\times\text{组宽}}$ |
| 样本均值、方差 | $\bar X=\frac1n\sum X_i$，$S^2=\frac1{n-1}\sum(X_i-\bar X)^2$（分母 $n-1$）；$E\bar X=\mu$，$\mathrm{Var}\bar X=\sigma^2/n$，$ES^2=\sigma^2$（不要求正态，$n\ge2$，方差有限） |
| 偏差分解 | $\sum(X_i-\mu)^2=\sum(X_i-\bar X)^2+n(\bar X-\mu)^2$；分母取 $n$ 的 $B_2$ 期望是 $\frac{n-1}n\sigma^2$，偏小 |
| $\chi^2(n)$ | $n$ 个独立 $N(0,1)$ 的平方和；$E=n$，$\mathrm{Var}=2n$；可加；$n=2$ 是 $E(\frac12)$；用 $\chi^2_\alpha(n)$ 查上侧，下侧用 $\chi^2_{1-\alpha}(n)$；不对称，左右分位数要分别查 |
| 标准化 | $\sum\big(\frac{X_i-\mu}\sigma\big)^2\sim\chi^2(n)$（$\mu$ 已知）；用 $\bar X$ 时自由度降为 $n-1$ |
| 正态样本定理 | $\bar X\sim N(\mu,\frac{\sigma^2}n)$；$\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)$；$\bar X$ 与 $S^2$ 独立（$n\ge2$，$\sigma>0$；正交变换：一个方向给均值，$n-1$ 个方向给偏差平方和）；$\mathrm{Var}S^2=\frac{2\sigma^4}{n-1}$ |
| $t(n)$ | $T=Z/\sqrt{V/n}$，$Z\sim N(0,1)$，$V\sim\chi^2(n)$ 独立；$\sigma$ 未知：$\frac{\bar X-\mu}{S/\sqrt n}\sim t(n-1)$；关于 0 对称，$t_{1-\alpha}=-t_\alpha$；尾比正态厚，$n\to\infty$ 趋于 $N(0,1)$；$t_{0.025}(4)=2.776$；$t_\alpha(n)$ 是上侧分位数；$n>2$ 时 $\mathrm{Var}\,T=\frac n{n-2}$ |
| 两样本合并方差 | 两组独立简单随机样本，$m,n\ge2$，方差相同且为正：$S_w^2=\frac{(m-1)S_1^2+(n-1)S_2^2}{m+n-2}$，$\frac{(\bar X-\bar Y)-(\mu_1-\mu_2)}{S_w\sqrt{1/m+1/n}}\sim t(m+n-2)$ |
| $F(m,n)$ | $\frac{U/m}{V/n}$；方差比 $\frac{S_1^2/\sigma_1^2}{S_2^2/\sigma_2^2}\sim F(n_1-1,n_2-1)$（两组独立正态样本；只有 $\sigma_1^2=\sigma_2^2$ 才约成 $S_1^2/S_2^2$）；$\frac1F\sim F(n,m)$ |
| $F$ 的下侧分位数 | $F_{1-\alpha}(m,n)=\dfrac1{F_\alpha(n,m)}$（自由度对调）；$T\sim t(n)\Rightarrow T^2\sim F(1,n)$ |
| 易错 | 自由度写成 $n$ 而不是 $n-1$；$\sigma$ 未知却按正态查表；$F$ 的两个自由度顺序；$\chi^2$ 当成对称分布；$\bar X$、$S^2$ 独立只对正态总体成立 |
