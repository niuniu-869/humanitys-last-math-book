| 提示 | 内容 |
|---|---|
| 训练误差与泛化误差 | 训练误差是训练集上的平均损失，会越训越低；泛化误差是新样本上的期望损失，只能用没参与训练的数据估计。训练集拟合参数，验证集挑超参数，测试集只用一次 |
| 过拟合与欠拟合 | 训练误差很小而验证误差大是过拟合（方差大）；两者都大是欠拟合（偏差大）；验证误差随复杂度先降后升 |
| 偏差–方差分解 | $E[(y-\hat f)^2]=\sigma^2+(f-\bar f)^2+\mathrm{Var}\,\hat f$，期望对训练集和噪声求；证明两步：先分离噪声，再加减 $\bar f=E\hat f$ |
| 复杂度的代价 | 线性模型有 $p$ 个参数、$n$ 个点：真实函数在列空间内、且在同样的 $n$ 个输入处换新标签时，训练误差期望 $\sigma^2(1-p/n)$，新数据上 $\sigma^2(1+p/n)$（有偏差时再加偏差项）；依据 $\mathrm{tr}H=p$ |
| k 折交叉验证 | 分 $k$ 折，轮流留一折验证，取平均验证误差最小的超参数，再用全部训练数据重训；预处理要放进每一轮；时间序列不能随机打乱 |
| 岭回归 | 最小化 $\frac12\lVert\boldsymbol y-X\boldsymbol w\rVert^2+\frac\lambda2\lVert\boldsymbol w\rVert^2$，解 $(X^{\mathsf T}X+\lambda I)^{-1}X^{\mathsf T}\boldsymbol y$；$\lambda>0$ 时必可逆；各列尺度不同时先标准化，偏置不罚 |
| 权重衰减 | 普通 SGD 的梯度步 $\boldsymbol w\leftarrow(1-\eta\lambda)\boldsymbol w-\eta\nabla L$；AdamW 把衰减单独做，不经过梯度缩放 |
| L2 即高斯先验 | 噪声 $N(0,\sigma^2)$、权重先验 $N(0,\tau^2)$，取负对数乘 $\sigma^2$，得 $\lambda=\sigma^2/\tau^2$；数据越多先验影响越小 |
| L1 即拉普拉斯先验 | 先验 $\propto e^{-\lvert w\rvert/\kappa}$，$\lambda=\sigma^2/\kappa$；一维解是软阈值 $\mathrm{sign}(z)\max(\lvert z\rvert-\lambda,0)$，小系数直接为 0；逐坐标软阈值只在各列单位正交（$X^{\mathsf T}X=I$）时成立 |
| L1 与 L2 对照 | L2 按比例缩小 $z/(1+\lambda)$、保留全部特征；L1 减去 $\lambda$、产生稀疏解；约束区域一个是圆盘，一个是有尖角的菱形 |
| ROC 与 AUC | 阈值从高到低扫，$\mathrm{TPR}=\mathrm{TP}/(\mathrm{TP}+\mathrm{FN})$，$\mathrm{FPR}=\mathrm{FP}/(\mathrm{FP}+\mathrm{TN})$；AUC $=P(\text{正例分数}>\text{负例分数})$，并列算一半 |
| AUC 的性质 | 随机猜是 0.5；严格递增变换分数不变；负例复制多少倍都不变（精确率会变）；只看排序，不看概率是否校准 |
| 易错点 | 用测试集调参等于偷看；先标准化再切分会漏信息；以为训练误差为 0 就是好模型 |
