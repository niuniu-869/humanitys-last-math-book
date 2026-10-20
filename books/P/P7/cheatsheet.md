## P.7 · 数字特征（速记）

| 提示 | 内容 |
|---|---|
| 期望 = 平衡点 | 离散 $E(X)=\sum x_kp_k$，连续 $E(X)=\int xf(x)\mathrm{d}x$；要求绝对收敛（柯西分布、$P(X=2^k)=2^{-k}$ 的期望不存在）；$E(I_A)=P(A)$ |
| 函数的期望 | 离散型：$E\,g(X)=\sum g(x_k)p_k$；连续型：$E\,g(X)=\int g(x)f(x)\mathrm{d}x$，均要求绝对收敛；二维用联合分布；一般 $E\,g(X)\ne g(E X)$，如 $E(X^2)\ge(E X)^2$ |
| 期望的运算 | $E(aX+b)=aE(X)+b$；$E(X+Y)=E(X)+E(Y)$ 不需要独立；独立（且期望存在）是 $E(XY)=E(X)E(Y)$ 的充分条件，反过来等式成立推不出独立 |
| 指示变量法 | 计数 $X=I_1+\cdots+I_n$，$E(X)=\sum P(A_i)$，事件不必独立；超几何 $E=n\frac DN$，配对问题 $E=1$ |
| 全期望与首步分析 | $E(Y)=\sum E(Y\mid X=x)P(X=x)$；过程回到起点时，对第一步分类列方程；几何分布 $E=\frac1p$ |
| 方差 | $\mathrm{Var}(X)=E(X^2)-(E X)^2$；$\mathrm{Var}(aX+b)=a^2\mathrm{Var}(X)$；独立时 $\mathrm{Var}(X\pm Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)$；$X_1,\dots,X_n$ 独立同分布时 $\mathrm{Var}(\bar X)=\frac{\sigma^2}{n}$；方差运算均设二阶矩有限 |
| 常用分布 | $B(n,p)$：$np,\ np(1-p)$；几何：$\frac1p,\ \frac{1-p}{p^2}$；$P(\lambda)$：$\lambda,\ \lambda$；$U(a,b)$：$\frac{a+b}2,\ \frac{(b-a)^2}{12}$；$E(\lambda)$：$\frac1\lambda,\ \frac1{\lambda^2}$；$N(\mu,\sigma^2)$：$\mu,\ \sigma^2$ |
| 超几何方差 | $N>1$ 时 $n\frac DN\big(1-\frac DN\big)\frac{N-n}{N-1}$，比二项多有限总体修正因子（由负协方差来）；抽样比例 $n/N$ 很小时才近似二项 |
| 协方差 | $\mathrm{Cov}(X,Y)=E(XY)-E(X)E(Y)$；双线性；$\mathrm{Var}(X\pm Y)=\mathrm{Var}(X)+\mathrm{Var}(Y)\pm2\mathrm{Cov}(X,Y)$；独立 $\Rightarrow\mathrm{Cov}=0$ |
| 相关系数 | $\rho=\frac{\mathrm{Cov}(X,Y)}{\sigma_X\sigma_Y}$，$\lvert\rho\rvert\le1$（两个方差有限且为正）；$\lvert\rho\rvert=1$ 当且仅当存在 $a\ne0,b$ 使 $Y=aX+b$ 以概率 1 成立，$a>0$ 时 $\rho=1$，$a<0$ 时 $\rho=-1$；只量**线性**关系；最佳线性预测斜率 $\frac{\mathrm{Cov}}{\mathrm{Var}(X)}$，剩余方差 $(1-\rho^2)\mathrm{Var}(Y)$ |
| 不相关与独立 | 独立 $\Rightarrow$ 不相关，反之不成立（$X$ 对称、$Y=X^2$；圆盘上的均匀分布）；二维正态中 $\rho=0\iff$ 独立，只知边缘正态不够 |
| 协方差矩阵 | $\Sigma=E[(\boldsymbol X-\boldsymbol\mu)(\boldsymbol X-\boldsymbol\mu)^{\mathsf T}]$ 对称半正定，$\boldsymbol a^{\mathsf T}\Sigma\boldsymbol a=\mathrm{Var}(\boldsymbol a^{\mathsf T}\boldsymbol X)$；$\boldsymbol Y=A\boldsymbol X+\boldsymbol b$ 时 $\mathrm{Cov}(\boldsymbol Y)=A\Sigma A^{\mathsf T}$ |
| 二维正态的线性组合 | $a,b$ 不同时为零时 $aX+bY\sim N\big(a\mu_1+b\mu_2,\ a^2\sigma_1^2+2ab\rho\sigma_1\sigma_2+b^2\sigma_2^2\big)$；联合正态的两个线性组合不相关则独立 |
| $n$ 维正态 | $N(\boldsymbol\mu,\Sigma)$ 的等密度线是椭球，轴沿 $\Sigma$ 的特征向量，半轴 $\sqrt{c\lambda_i}$；$\boldsymbol\mu+L\boldsymbol Z\sim N(\boldsymbol\mu,LL^{\mathsf T})$；正交变换不改变标准正态向量 |
