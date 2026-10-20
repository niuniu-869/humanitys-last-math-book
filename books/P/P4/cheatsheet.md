## P.4 · 连续随机变量（速记）

| 提示 | 内容 |
|---|---|
| 概率密度 | $f\ge0$，$\int_{-\infty}^{+\infty}f=1$；$P(a<X\le b)=\int_a^bf$；概率是面积，不是高度 |
| 分布函数与密度 | $F(x)=\int_{-\infty}^xf$，连续；$f$ 连续处 $F'(x)=f(x)$；含常数时用 $F(-\infty)=0,F(+\infty)=1$ 定 |
| 单点概率为 0 | 有密度的分布里 $P(X=a)=0$；端点带不带等号不影响概率；概率为 0 不等于不可能 |
| 密度不是概率 | $f$ 可以大于 1；窄条 $(x,x+\Delta x]$ 的概率 $\approx f(x)\Delta x$ |
| 均匀 $U(a,b)$ | $f=\frac1{b-a}$；$P(c<X<d)=\frac{d-c}{b-a}$（长度之比）；先把条件化成 $X$ 的范围，注意只取落在 $(a,b)$ 内的部分 |
| 随机数的起点 | $r\sim U(0,1)$ 时 $P(r<p)=p$；离散分布按累积概率切 $[0,1)$ 再看 $r$ 落在哪段 |
| 指数 $E(\lambda)$ | $f=\lambda e^{-\lambda x}$，$F=1-e^{-\lambda x}$，$P(X>x)=e^{-\lambda x}$（$x>0$）；平均 $\frac1\lambda$，中位数 $\frac{\ln2}\lambda$ 比平均小 |
| 指数与泊松 | $\lambda$ 与时间单位要一致；「$t$ 内没来电」$=\{T>t\}$，概率 $e^{-\lambda t}$ |
| 无记忆性 | $P(X>s+t\mid X>s)=P(X>t)$；已等多久不影响还要等多久；均匀分布没有这个性质；发生率不恒定（如灯泡越用越坏）就不是指数 |
| 正态 $N(\mu,\sigma^2)$ | $f=\frac1{\sqrt{2\pi}\sigma}e^{-\frac{(x-\mu)^2}{2\sigma^2}}$；$\mu$ 定位置，$\sigma$ 定宽度，拐点在 $\mu\pm\sigma$，峰高 $\frac1{\sqrt{2\pi}\sigma}$ |
| 读出参数 | 密度是 $ce^{\text{二次式}}$：配方成 $-\frac{(x-\mu)^2}{2\sigma^2}$，对照读 $\mu$、$\sigma^2$ |
| 标准化 | $Z=\frac{X-\mu}\sigma\sim N(0,1)$；$P(a<X\le b)=\Phi(\frac{b-\mu}\sigma)-\Phi(\frac{a-\mu}\sigma)$；$\Phi(-z)=1-\Phi(z)$ |
| 3σ 与分位数 | $P(\lvert X-\mu\rvert<k\sigma)=0.6827,0.9545,0.9973$（$k=1,2,3$）；$z_{0.05}=1.645$，$z_{0.025}=1.96$，$z_{0.005}=2.576$ |
| 易错 | $N(\mu,\sigma^2)$ 里第二个参数是方差，查表要除以 $\sigma$ 不是 $\sigma^2$；指数分布时间单位不一致 |
