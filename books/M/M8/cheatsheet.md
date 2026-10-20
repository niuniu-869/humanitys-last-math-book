## M.8 · 训练深网络与卷积：初始化、批归一化、残差、Dropout（速记）

| 提示 | 内容 |
|---|---|
| 一步训练 | 前向（记下中间值）→ 反向（$\delta$ 递推）→ 批内平均 → 更新 $\theta\leftarrow\theta-\eta g$；梯度与参数同形（$\partial L/\partial W_1=\boldsymbol\delta_1\boldsymbol x^{\mathsf T}$） |
| 误差信号连乘 | $\boldsymbol\delta_l=\operatorname{diag}(\sigma'(\boldsymbol z_l))W_{l+1}^{\mathsf T}\boldsymbol\delta_{l+1}$；每层因子的长度 $r<1$ 消失、$r>1$ 爆炸；sigmoid 的 $\sigma'\le\tfrac14$（$z=0$ 取到） |
| 消失与爆炸可并存 | 矩阵的最大奇异值 $>1$、最小 $<1$ 时，不同方向一个放大一个缩小；爆炸用梯度裁剪应急 |
| 方差保持 | $w$ 均值 0、与 $x$ 独立：$\mathrm{Var}(wx)=\mathrm{Var}(w)E[x^2]$；$\mathrm{Var}(z)=n\mathrm{Var}(w)E[x^2]$，取 $\mathrm{Var}(w)=1/n_{\text{in}}$ 保持不变 |
| He 与 Xavier | ReLU 砍掉一半二阶矩：$E[\mathrm{ReLU}(z)^2]=\tfrac12\mathrm{Var}(z)$，所以 He 取 $2/n_{\text{in}}$；Xavier 取 $2/(n_{\text{in}}+n_{\text{out}})$（折中前向 $n_{\text{in}}$ 与反向 $n_{\text{out}}$），推导默认 0 附近近似恒等，tanh 适用，sigmoid 只是常用起点；$U(-a,a)$ 的方差 $a^2/3$ |
| 初始化的坑 | 全取 0 或全取同一个数，同层单元永远一样（对称）；太小的随机数照样逐层衰减 |
| 批归一化 | $\hat x=\dfrac{x-\mu}{\sqrt{\sigma^2+\varepsilon}}$，$y=\gamma\hat x+\beta$，$\mu,\sigma^2$ 在批内逐特征算；$\gamma,\beta$ 可学，取 $\gamma=\sqrt{\sigma^2+\varepsilon}$、$\beta=\mu$ 能还原 |
| BN 训练与推理 | 训练用批内统计并更新滑动平均 $r\leftarrow\rho r+(1-\rho)\text{统计}$；推理用滑动平均；忽略 $\varepsilon$ 时前一层权重乘 $a>0$，BN 输出不变 |
| 残差块 | $\boldsymbol y=\boldsymbol x+F(\boldsymbol x)$，$\partial\boldsymbol y/\partial\boldsymbol x=I+\partial F/\partial\boldsymbol x$；$\partial\boldsymbol x_D/\partial\boldsymbol x_l=\prod(I+J_i)=I+\sum J_i+\cdots$（$k$ 块 $2^k$ 项），$I$ 是直通项；恒等映射只需 $F=0$ |
| 残差的边界 | 直通项只保证有一条不被连乘压小的路，总梯度仍可能抵消；$a>0$ 时 $(1+a)^D$ 也会爆炸，需配合初始化或归一化 |
| Dropout | $y_i=m_ix_i/q$，$P(m_i=1)=q$；$E[y_i]=x_i$，$\mathrm{Var}(y_i)=x_i^2\frac{1-q}{q}$；反向用同一掩码 $\boldsymbol m\odot\boldsymbol\delta/q$；推理不丢 |
| Dropout 与 L2 | 线性预测加平方损失、独立掩码：$E[(\hat y-y)^2]=(\boldsymbol w^{\mathsf T}\boldsymbol x-y)^2+\frac{1-q}{q}\sum w_j^2x_j^2$ |
| 卷积 | 局部连接 + 权重共享：$y_i=\sum_jK_jx_{i+j}+b$（互相关）；参数个数与输入大小无关；$\partial L/\partial K_j=\sum_i\delta_ix_{i+j}$，$\partial L/\partial x_m=\sum_{i+j=m}\delta_iK_j$ |
| 输出尺寸与参数 | $h'=\lfloor(h+2p-k)/s\rfloor+1$；参数 $C_{\text{out}}(C_{\text{in}}k^2+1)$；输出通道数 = 核的个数；$s=1,p=(k-1)/2$（$k$ 为奇数）时尺寸不变 |
| 池化 | 无参数，尺寸公式同卷积，通道独立；最大池化梯度只给最大值位置，平均池化平分 |
