| 提示 | 内容 |
|---|---|
| 信息量 | $I(p)=-\log p$（以 2 为底，单位比特；$\ln$ 为奈特，$1\text{ nat}\approx1.4427$ 比特）；由「独立事件信息相加」$I(pq)=I(p)+I(q)$ 推出，必须取对数 |
| 熵 | $H(p)=-\sum p\log p=E[-\log p(X)]$（离散，$0\log0=0$，有限熵时讨论）；$0\le H\le\log K$，均匀分布最大，确定的分布为 0；独立时 $H(X,Y)=H(X)+H(Y)$ |
| 熵与编码 | 可无歧义串接的二进制编码，其平均码长不小于熵；有限符号独立同分布信源的长串编码可使每符号平均长度任意接近 $H$（落在 $H$ 与 $H+1/n$ 之间），不要求单个符号恰好达到 |
| 二元熵 | $H(p)=-p\log p-(1-p)\log(1-p)$，$p=\frac12$ 时最大为 1 比特；$p=0.7$ 约 0.881，$p=0.9$ 约 0.469 |
| 四符号老朋友 | $p=(\frac12,\frac14,\frac18,\frac18)$：$H=\frac74$；按均匀分布编码交叉熵 2，KL $=\frac14$ |
| 交叉熵 | $H(p,q)=-\sum p\log q=E_p[-\log q]$：按 $q$ 的理想长度 $-\log q$ 在真相 $p$ 下的平均，理想长度未必是整数；不对称；$p>0,q=0$ 处为 $+\infty$；固定 $p$ 时 $H(p,q)\ge H(p)$，等号当且仅当 $q=p$ |
| KL 散度 | $D(p\|q)=\sum_{p>0}p\log\frac pq$，$H(p)$ 有限时等于 $H(p,q)-H(p)$；不对称，不是距离；$p>0$ 而 $q=0$ 时为 $+\infty$ |
| KL 非负的证明 | 先排除 $p>0,q=0$（此时 $D=\infty$）；再由 $\ln x\le x-1$：$-D=\sum p\ln\frac qp\le\sum_{p>0}(q-p)\le0$；等号当且仅当 $q=p$；$q$ 总和为 1 不能去掉（取 $p=(\frac12,\frac12)$、$q=(1,1)$、比特时 $D=-1<0$）；推论 $H(p,q)\ge H(p)$，$H(p)\le\log K$ |
| softmax | $\mathrm{softmax}(z)_i=e^{z_i}/\sum_je^{z_j}$；$q_i/q_j=e^{z_i-z_j}$，加常数不变，计算时先减最大值；$K=2$ 即 sigmoid |
| 温度 | $\mathrm{softmax}(z/T)$：打分不全相同时 $T$ 增大熵严格增大，全相同恒为均匀；$T\to0$ 时唯一最大分数的类趋于 1（并列最大的 $m$ 类各趋于 $1/m$），$T\to\infty$ 趋于均匀；$(2,1,0)$：$T=1$ 为 $(0.6652,0.2447,0.0900)$，$T=2$ 为 $(0.5065,0.3072,0.1863)$，$T=0.5$ 为 $(0.8668,0.1173,0.0159)$ |
| 分类损失 | $L=-\ln q_y=-z_y+\ln\sum e^{z_j}=\ln(1+\sum_{j\ne y}e^{z_j-z_y})$；正确类要比其余高出足够多才接近 0；$(2,1,0)$ 真实类为第 1 类时 $L\approx0.4076$ |
| 梯度 | $\partial L/\partial z_k=q_k-p_k$（预测分布减独热真相），各分量和为 0 |
| 最大似然 | 含输入：$\bar L=\sum_x\hat p_X(x)H(\hat p(\cdot\mid x),q_\theta(\cdot\mid x))$，每组再拆成熵加 KL；无输入：$-\frac1n\ln\mathcal L=H(\hat p,q_\theta)=H(\hat p)+D(\hat p\|q_\theta)$；最大似然 = 最小交叉熵 = 最小 KL；困惑度 $=e^{\text{平均损失}}$ |
