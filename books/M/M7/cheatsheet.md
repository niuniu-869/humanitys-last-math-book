## M.7 · 多层网络与反向传播（速记）

| 提示 | 内容 |
|---|---|
| 为什么要非线性 | $W_2(W_1\boldsymbol x+\boldsymbol b_1)+\boldsymbol b_2=(W_2W_1)\boldsymbol x+(W_2\boldsymbol b_1+\boldsymbol b_2)$，线性层叠起来仍是一层；异或要隐藏层 + 非线性 |
| MLP 前向 | $\boldsymbol z_1=W_1\boldsymbol x+\boldsymbol b_1$，$\boldsymbol h=\varphi(\boldsymbol z_1)$，$\boldsymbol z_2=W_2\boldsymbol h+\boldsymbol b_2$；每个量先写形状 |
| 激活函数的导数 | $\sigma'=\sigma(1-\sigma)\le\tfrac14$；$\tanh'=1-\tanh^2\le1$；ReLU$'$ 为 1（$z>0$）或 0；GELU$'=\Phi+z\Phi'$ |
| 饱和与截断 | sigmoid、tanh 在 $\lvert z\rvert$ 大时导数趋近 0；ReLU 在 $z<0$ 时梯度为 0；阶跃函数导数几乎处处为 0，不能用 |
| 形状与参数 | 线性层 $d\to m$：$W\in\mathbb R^{m\times d}$，参数 $md+m$；批量 $Z=XW^{\mathsf T}+\boldsymbol b^{\mathsf T}$，$X$ 为 $B\times d$（样本为行）；批量不改变参数个数 |
| 计算图 | 把公式拆成基本运算，前向记下所有中间值；反向要用它们 |
| 反向传播的局部规则 | 上游梯度 × 局部导数：$\bar a=\bar c\cdot\partial c/\partial a$；加法原样分给两边；乘法乘另一个因子；$\sigma$：$\bar c\,c(1-c)$ |
| 交叉熵的梯度 | $-\ln p$ 的 $-1/p$ 与 $\sigma'=p(1-p)$ 相乘，$p$ 约掉，$\bar z=p-y$ |
| 分叉相加 | 一个量被多处用到：每条路径各贡献一项，梯度累加（`+=`）；共用参数的梯度 = 各样本梯度之和 |
| 为什么从后往前 | 损失只有一个数、参数有上亿个：反向一遍得到全部梯度，前向模式要跑 $N$ 遍；矩阵链 $J_3J_2J_1$ 先乘行向量一端最便宜；代价是存全部中间值，反向约为前向计算的 2 倍；输入少、输出多时反而前向模式省 |
| 向量的反向 | 雅可比 $J_{ij}=\partial y_i/\partial x_j$（$m\times d$）；$\bar{\boldsymbol x}=J^{\mathsf T}\bar{\boldsymbol y}$；梯度的形状必须与被求导的量相同（形状对上只是必要条件，方阵的转置写反查不出）|
| 线性层的反向 | $\partial W=\boldsymbol\delta\boldsymbol x^{\mathsf T}$，$\partial\boldsymbol b=\boldsymbol\delta$，$\partial\boldsymbol x=W^{\mathsf T}\boldsymbol\delta$；批量：$\Delta^{\mathsf T}X$、$\Delta^{\mathsf T}\boldsymbol1$、$\Delta W$ |
| 逐元素函数的反向 | 雅可比是对角阵，$\bar{\boldsymbol z}=\bar{\boldsymbol h}\odot\varphi'(\boldsymbol z)$；softmax 不是逐元素，不能套 |
| 逐层递推 | $\boldsymbol\delta_l=(W_{l+1}^{\mathsf T}\boldsymbol\delta_{l+1})\odot\varphi'(\boldsymbol z_l)$，$\partial W_l=\boldsymbol\delta_l\boldsymbol a_{l-1}^{\mathsf T}$；输出层 $\boldsymbol\delta_D$：sigmoid/softmax 配交叉熵为 $\hat y-y$ 或 $\boldsymbol p-\boldsymbol y$，平方损失为 $\boldsymbol z-\boldsymbol t$ |
| 数值梯度检验 | 中心差分 $\dfrac{L(\theta+\varepsilon)-L(\theta-\varepsilon)}{2\varepsilon}$，误差 $O(\varepsilon^2)$；$\varepsilon\approx10^{-5}$；只用于小网络调试 |
