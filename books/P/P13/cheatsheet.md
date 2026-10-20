| 提示 | 内容 |
|---|---|
| 平方和分解（方差分析） | $SS_T=SS_B+SS_W$，$SS_B=\sum n_i(\bar X_i-\bar X)^2$，$SS_W=\sum\sum(X_{ij}-\bar X_i)^2$；自由度 $n-1=(k-1)+(n-k)$；交叉项为 0 是因为组内偏差之和为 0 |
| 为什么不两两做 $t$ 检验 | 比较次数多，总的第一类错误高于 $\alpha$（三组模拟约 12%，五组约 29%）；改用一次 $F$ 检验 |
| 单因素 $F$ 检验 | $F=\dfrac{SS_B/(k-1)}{SS_W/(n-k)}\sim F(k-1,n-k)$（$H_0$ 下），只看右侧；$E\,MS_W=\sigma^2$，$E\,MS_B=\sigma^2+\sum n_i\tau_i^2/(k-1)$；两组时 $F=t^2$；要求正态、方差相同、观测独立，各组人数悬殊且小组方差大时，误判率可远高于 $\alpha$（模拟约 31%） |
| 拒绝之后 | 只说明均值不全相同；两两比较用 $MS_W$ 做分母，$t(n-k)$，$\alpha$ 除以比较的次数 |
| 双因素方差分析 | $SS_T=SS_{\text{行}}+SS_{\text{列}}+SS_E$，$SS_E$ 自由度 $(a-1)(b-1)$；有交互时每格重复 $m$ 次，多出 $SS_{\text{交互}}$，$SS_E$ 自由度 $ab(m-1)$；交互显著时按格子看，不读主效应 |
| 最小二乘直线 | $\hat\beta_1=S_{xy}/S_{xx}$，$\hat\beta_0=\bar y-\hat\beta_1\bar x$；残差满足 $\sum e_i=0$，$\sum x_ie_i=0$；直线过 $(\bar x,\bar y)$；要求 $x$ 不全相同（$S_{xx}>0$）；$\hat\beta_1=r\,s_y/s_x$ |
| 回归模型与估计量 | $y_i=\beta_0+\beta_1x_i+\varepsilon_i$，$\varepsilon_i\sim N(0,\sigma^2)$；正态噪声下最大似然就是最小二乘；$\hat\beta_1\sim N(\beta_1,\sigma^2/S_{xx})$；$\hat\sigma^2=SS_E/(n-2)$ |
| 回归到均值 | $|r|<1$ 时标准化后的预测斜率是 $r$；$y$ 对 $x$ 与 $x$ 对 $y$ 是两条不同的直线，斜率之积为 $r^2$ |
| 斜率的检验 | $H_0:\beta_1=0$ 下 $T=\hat\beta_1/(\hat\sigma/\sqrt{S_{xx}})\sim t(n-2)$；置信区间 $\hat\beta_1\pm t_{\alpha/2}(n-2)\hat\sigma/\sqrt{S_{xx}}$；一元回归中 $F=T^2$ |
| 判定系数 | $SS_T=SS_R+SS_E$，$R^2=SS_R/SS_T=r^2$；$R^2$ 高不保证直线合适，要看残差图 |
| 预测 | 平均值区间半宽 $t\hat\sigma\sqrt{h}$，新观测区间半宽 $t\hat\sigma\sqrt{1+h}$，$h=\frac1n+\frac{(x_0-\bar x)^2}{S_{xx}}$；离 $\bar x$ 越远越宽，外推不可靠 |
| 化为线性 | $y=ae^{bx}$ 与 $y=ax^b$ 取对数；$y=a+b/x$ 令 $u=1/x$；换回原形式再解读 |
| 多元回归 | $\hat{\boldsymbol\beta}=(X^{\mathsf T}X)^{-1}X^{\mathsf T}\boldsymbol y$，来自残差垂直于各列；$\hat\sigma^2=SS_E/(n-p-1)$；系数是「其他变量不变时」的变化；变量相关时系数不稳定；比较模型用调整 $R^2$ |
