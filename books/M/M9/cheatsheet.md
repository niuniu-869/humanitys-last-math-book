## M.9 · 词向量与表示学习：从独热向量到 word2vec（速记）

| 提示 | 内容 |
|---|---|
| 独热向量 | 词 $i$ ↦ $\boldsymbol e_i\in\mathbb R^V$；$\boldsymbol e_i^{\mathsf T}\boldsymbol e_j=0$（$i\ne j$），任意两个不同词的距离都是 $\sqrt2$，表达不了「意思相近」；一句话排成 $O\in\mathbb R^{T_{\text{句}}\times V}$，$OO^{\mathsf T}=I$（词互异时） |
| 分布假说 | 一个词的意思由它周围常出现的词刻画；窗口半径 $m$ 内累计 $X_{ij}$ 得共现矩阵，行向量用余弦比较 |
| 共现向量的缺点 | 维数 $=V$ 且大多为 0；高频词的计数会盖过有区别的信息（补救之一：先对计数取对数） |
| 嵌入查表 | $E\in\mathbb R^{V\times d}$，$\boldsymbol e_i^{\mathsf T}E=E$ 的第 $i$ 行；$OE\in\mathbb R^{T_{\text{句}}\times d}$；参数 $V\cdot d$；反向时只有被查到的行有梯度 |
| 截断 SVD | $X\approx U_d\Sigma_dW_d^{\mathsf T}$ 是秩不超过 $d$ 的矩阵中元素误差平方和最小的（埃卡特–扬）；$E_d=U_d\Sigma_d$ 的行内积 $=X_dX_d^{\mathsf T}$；$d\ge\mathrm{rank}\,X$ 时与 $X$ 的行内积、非零行余弦完全相同；$V$ 大时代价高 |
| skip-gram | 每词两个向量（中心 $\boldsymbol v_w$、上下文 $\boldsymbol u_w$，共用时词与自己的得分 $\lVert\boldsymbol v\rVert^2$ 往往很大）；$p(o\mid c)=\dfrac{\exp(\boldsymbol u_o^{\mathsf T}\boldsymbol v_c)}{\sum_w\exp(\boldsymbol u_w^{\mathsf T}\boldsymbol v_c)}$；$\ell=-\log p(o\mid c)$；窗口 $m$ 约配出 $2mT$ 对 |
| skip-gram 的概率假设 | 上下文词服从类别分布，损失是交叉熵，就是 $V$ 类的 softmax 回归 |
| skip-gram 的梯度 | $\partial\ell/\partial\boldsymbol z=\boldsymbol p-\boldsymbol y$；$\nabla_{\boldsymbol v_c}\ell=U_{\text{out}}^{\mathsf T}(\boldsymbol p-\boldsymbol y)=\sum_wp_w\boldsymbol u_w-\boldsymbol u_o$（预期上下文向量 − 真实的）；$\nabla_{\boldsymbol u_w}\ell=(p_w-y_w)\boldsymbol v_c$ |
| 完整 softmax 的代价 | 每个词对 $O(Vd)$，要更新 $U_{\text{out}}$ 的全部 $V$ 行 |
| 负采样 | $\ell_{\text{NS}}=-\log\sigma(s_o)-\sum_{k=1}^K\log\sigma(-s_k)$，$s=\boldsymbol u^{\mathsf T}\boldsymbol v_c$；$\partial/\partial s_o=\sigma(s_o)-1$，$\partial/\partial s_k=\sigma(s_k)$；每步至多 $K+1$ 个不同的上下文行，$O((K+1)d)$；标签 1（语料）或 0（随机配出）服从伯努利分布；只有正例时可让所有得分趋于 $+\infty$ 使损失趋于 0，负词防止这种退化 |
| 负采样的梯度 | $\nabla_{\boldsymbol v_c}=(\sigma(s_o)-1)\boldsymbol u_o+\sum_k\sigma(s_k)\boldsymbol u_{n_k}$；$\nabla_{\boldsymbol u_o}=(\sigma(s_o)-1)\boldsymbol v_c$；$\nabla_{\boldsymbol u_{n_k}}=\sigma(s_k)\boldsymbol v_c$ |
| 负词的抽法 | $P(w)\propto f(w)^{3/4}$：压低高频词、抬高罕见词；它是另一个目标，不是完整 softmax 的数值近似 |
| 类比 | 理想最优时 $\boldsymbol u_k^{\mathsf T}\boldsymbol v_a=\log P(k\mid a)-\log q_k-\log K$（$q$ 为负词分布），故 $(\boldsymbol v_a-\boldsymbol v_b)^{\mathsf T}\boldsymbol u_k\approx\log\frac{P(k\mid a)}{P(k\mid b)}$；各 $k$ 的概率比相同 $\Rightarrow$ 向量差相等（任一 $k$ 的比不等，差就不为 0）；找最近词时排除三个输入词 |
| InfoNCE | $z_{ij}=\cos(\boldsymbol a_i,\boldsymbol b_j)/\tau$；$\ell_i=-\log\dfrac{e^{z_{ii}}}{\sum_je^{z_{ij}}}$ 是以对角线为标签的 softmax 交叉熵，梯度 $p-y$；行、列两个方向取平均；$\tau$ 小则 softmax 尖；全相等时损失 $\ln N$ |
