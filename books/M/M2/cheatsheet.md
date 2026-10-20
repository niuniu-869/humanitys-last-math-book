| 提示 | 内容 |
|---|---|
| 高斯噪声的最大似然 | $y=\boldsymbol w^{\mathsf T}\boldsymbol x+\varepsilon$，$\varepsilon\sim N(0,\sigma^2)$ $\Rightarrow$ 对数似然 $=-\frac n2\ln(2\pi\sigma^2)-\frac1{2\sigma^2}\sum(\hat y_i-y_i)^2$，最大化它就是最小二乘；$\hat\sigma^2=$ 均方误差 |
| 线性回归梯度 | $L=\frac1n\lVert X\boldsymbol w-\boldsymbol y\rVert^2$，$\nabla L=\frac2nX^{\mathsf T}(X\boldsymbol w-\boldsymbol y)$，与 $\boldsymbol w$ 同形状 |
| 贝叶斯分类器 | 取后验 $P(y\mid\boldsymbol x)$ 最大的类，错误率最低；朴素贝叶斯：类内特征独立，$P(\boldsymbol x\mid y)=\prod_jP(x_j\mid y)$ |
| 对数几率是线性的 | 二值特征的朴素贝叶斯、同方差高斯两类，都有 $\ln\frac{P(1\mid\boldsymbol x)}{P(0\mid\boldsymbol x)}=\boldsymbol w^{\mathsf T}\boldsymbol x+b$ |
| 逻辑回归 | $p=\sigma(z)=\frac1{1+e^{-z}}$，$z=\boldsymbol w^{\mathsf T}\boldsymbol x+b$；$\sigma(-z)=1-\sigma(z)$，$\sigma'=\sigma(1-\sigma)\le\frac14$ |
| 分界面 | $p=\frac12\iff z=0$，是超平面，$\boldsymbol w$ 是法向量；$z=\lVert\boldsymbol w\rVert\times$有符号距离（$\boldsymbol w\ne\boldsymbol0$），固定 $\boldsymbol w$ 时概率由距离决定 |
| 二元交叉熵 | $L=-\frac1n\sum[y_i\ln p_i+(1-y_i)\ln(1-p_i)]$，伯努利似然取负对数；$w=b=0$ 时 $=\ln2$ |
| 为什么不用平方误差 | 对分数的梯度多一个 $\sigma'(z)=p(1-p)$，错得离谱（$p\to0,y=1$）时几乎为 0；交叉熵的 $\ln$ 抵消了它 |
| 梯度 $p-y$ | $\frac{\partial\ell}{\partial z}=p-y$；$\nabla_{\boldsymbol w}L=\frac1nX^{\mathsf T}(\boldsymbol p-\boldsymbol y)$，$\frac{\partial L}{\partial b}=\frac1n\sum(p_i-y_i)$ |
| 凸性与训练 | $H=\frac1nX^{\mathsf T}DX$，$D=\mathrm{diag}(p_i(1-p_i))$，半正定，$L$ 凸；$L_s\le\frac14\lambda_{\max}(\frac1nX^{\mathsf T}X)$，$\eta<2/L_s$ 是保证下降的充分条件，不是临界值；数据严格线性可分且不加正则时最大似然解不存在 |
| softmax 回归 | $\boldsymbol z=W\boldsymbol x+\boldsymbol b$，$p_k=e^{z_k}/\sum e^{z_j}$，$\ell=-z_c+\ln\sum e^{z_j}$；$\nabla_{\boldsymbol z}\ell=\boldsymbol p-\boldsymbol y$，$\nabla_W\ell=(\boldsymbol p-\boldsymbol y)\boldsymbol x^{\mathsf T}$（$K\times d$） |
| 混淆矩阵 | 精确率 $\frac{TP}{TP+FP}$，召回率 $\frac{TP}{TP+FN}$，准确率 $\frac{TP+TN}n$；阈值降低，召回率不降、精确率可升可降 |
| 易错 | 类别极不平衡时准确率会骗人；二分类是 softmax 回归 $K=2$ 的特例（$z=z_1-z_0$）；$\boldsymbol p-\boldsymbol y$ 各分量之和为 0 |
