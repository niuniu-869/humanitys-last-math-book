## M.17 · 扩散模型的前向过程：高斯噪声的叠加与闭式解（速记）

| 提示 | 内容 |
|---|---|
| 整体框架 | 前向：$x_0\to x_1\to\dots\to x_T$ 逐步加噪，固定不学；反向：网络学 $p_\theta(x_{t-1}\mid x_t)$；$x_{1:T}$ 是隐变量，目标仍是 M.16.3 的 ELBO |
| 单步加噪 | $x_t=\sqrt{1-\beta_t}\,x_{t-1}+\sqrt{\beta_t}\,\varepsilon_t$，即 $q(x_t\mid x_{t-1})=N(\sqrt{1-\beta_t}\,x_{t-1},\beta_tI)$；记 $\alpha_t=1-\beta_t$ |
| 为什么先缩小 | $\mathrm{Var}(x_t)=(1-\beta_t)s+\beta_t$，$s=1$ 是不动点，数值始终保持同一量级；不缩小则方差每步加 $\beta_t$ |
| 独立高斯噪声合并 | $N(0,a)+N(0,b)=N(0,a+b)$（独立）；标准差不能直接相加，按勾股合成，方差相加；每步必须新抽噪声，共用同一个 $\varepsilon$ 会得到错误的方差；合成的是新的标准正态 |
| 两步合并 | $\alpha_2\beta_1+\beta_2=1-\alpha_1\alpha_2$；信号系数² + 噪声系数² = 1 |
| 闭式解 | $\bar\alpha_t=\prod_{s\le t}\alpha_s$；$x_t=\sqrt{\bar\alpha_t}\,x_0+\sqrt{1-\bar\alpha_t}\,\varepsilon$，$q(x_t\mid x_0)=N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I)$；归纳证明 |
| 常用数值例（$\beta=0.1$，$x_0=2$） | $\beta=0.1$，$x_0=2$，$t=3$：$\bar\alpha_3=0.729$，$x_3\sim N(1.7076,0.271)$ |
| 为什么能一步跳 | 训练只需要 $x_t$ 的分布，不需要中间路径；随机抽 $t$，一行得到 $x_t$ |
| 终点近似标准正态 | $\bar\alpha_T\le e^{-\sum\beta_t}$；线性表（$10^{-4}\to0.02$，$T=1000$）$\bar\alpha_T\approx4\times10^{-5}$ |
| 信噪比 | $\mathrm{SNR}_t=\bar\alpha_t/(1-\bar\alpha_t)$；线性表 SNR 恰为 1 在第 259、260 步之间 |
| 训练目标 | $E\lVert\varepsilon-\varepsilon_\theta(\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\varepsilon,\,t)\rVert^2$；预测 $\varepsilon$ 等价于预测 $x_0$：$x_0=(x_t-\sqrt{1-\bar\alpha_t}\varepsilon)/\sqrt{\bar\alpha_t}$ |
| 均方误差的最优解 | 最优预测是条件期望 $E[\varepsilon\mid x_t]$（交叉项为 0）；$x_0\sim N(0,1)$ 时最小损失 $=\bar\alpha_t$ |
| 前向后验（$t\ge2$） | $q(x_{t-1}\mid x_t,x_0)=N(\tilde\mu_t,\tilde\beta_t)$，$\tilde\beta_t=\frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\beta_t$，$\tilde\mu_t=\frac1{\sqrt{\alpha_t}}\big(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\varepsilon\big)$；两个高斯相乘：精度相加 |
| 采样 | $x_{t-1}=\frac1{\sqrt{\alpha_t}}\big(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\varepsilon_\theta\big)+\sigma_tz$，最后一步 $z=0$；简单损失是 ELBO 去掉 $t$ 的系数后的版本（不再是 ELBO 本身） |
