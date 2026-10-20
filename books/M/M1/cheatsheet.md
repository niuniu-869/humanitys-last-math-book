| 提示 | 内容 |
|---|---|
| 训练要解的问题 | $L(\theta)=\frac1n\sum_i\ell(f_\theta(\boldsymbol x_i),y_i)$，$\theta^*=\arg\min L$；三件套：模型、损失、更新规则 |
| 梯度下降 | $\theta\leftarrow\theta-\eta\nabla L(\theta)$；负梯度是一阶近似下下降最快的方向 |
| 一维二次函数 | $L=\frac12\lambda\theta^2$ 每步乘 $1-\eta\lambda$；$0<\eta<2/\lambda$ 收敛，$\eta\lambda>1$ 开始来回摆 |
| 多维二次函数 | $\boldsymbol e\leftarrow(I-\eta H)\boldsymbol e$，对角化后每个特征方向乘 $1-\eta\lambda_i$；收敛当且仅当 $\eta<2/\lambda_{\max}$ |
| 条件数 | $\kappa=\lambda_{\max}/\lambda_{\min}$；最优 $\eta^*=2/(\lambda_{\max}+\lambda_{\min})$，每步因子 $(\kappa-1)/(\kappa+1)$；$\kappa$ 大则慢 |
| 下降引理 | 梯度满足 $\lVert\nabla L(a)-\nabla L(b)\rVert\le L_s\lVert a-b\rVert$（二阶可导时即 Hessian 特征值绝对值 $\le L_s$）且 $\eta\le1/L_s$ 时，$L$ 每步至少降 $\frac\eta2\lVert\nabla L\rVert^2$；$\theta^4$ 的曲率无上界，不满足 |
| 凸函数 | $f(\alpha x+(1-\alpha)y)\le\alpha f(x)+(1-\alpha)f(y)$，弦在曲线上方；二阶连续可导时，Hessian 处处半正定 $\iff$ 凸；局部最小就是全局最小，可导时梯度为零也是全局最小 |
| 判断凸性的信号 | 二阶：迹 $\ge0$ 且行列式 $\ge0$；驻点处行列式 $<0$ 是鞍点；$\frac25X^{\mathsf T}X$ 型的均方误差永远凸 |
| 小批量梯度 | $\boldsymbol g_B=\frac1B\sum_j\nabla\ell_{i_j}$；$E[\boldsymbol g_B]=\nabla L$（无偏），方差 $=\sigma^2/B$；$\eta$ 固定时在谷底附近抖动，$\eta$ 越大抖得越厉害 |
| 动量 | $\boldsymbol v\leftarrow\beta\boldsymbol v+\nabla L$，$\theta\leftarrow\theta-\eta\boldsymbol v$；同号梯度累积到 $1/(1-\beta)$ 倍，变号的抵消；损失可能先升后降 |
| Adam | $\boldsymbol m\leftarrow\beta_1\boldsymbol m+(1-\beta_1)\boldsymbol g$，$\boldsymbol s\leftarrow\beta_2\boldsymbol s+(1-\beta_2)\boldsymbol g\odot\boldsymbol g$；除以 $1-\beta^t$ 做偏差修正；更新 $\eta\hat{\boldsymbol m}/(\sqrt{\hat{\boldsymbol v}}+\epsilon)$ |
| Adam 的步长 | 梯度稳定时每个坐标步长约为 $\eta$，与梯度大小无关；第一步恰为 $\eta\,\mathrm{sign}(\boldsymbol g)$ |
| 预热与余弦衰减 | 前 $T_w$ 步线性升到 $\eta_{\max}$，再按 $\eta_{\min}+\frac12(\eta_{\max}-\eta_{\min})(1+\cos\frac{\pi(t-T_w)}{T-T_w})$ 降到 $\eta_{\min}$ |
| 易错 | 阈值是 $2/\lambda_{\max}$，不是 $1/\lambda_{\min}$；Adam 的 $\hat{\boldsymbol s}$ 是逐坐标的；两种动量写法差 $1/(1-\beta)$ 倍 |
