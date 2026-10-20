## M.10 · 序列模型：语言模型、循环网络、LSTM 与编码器–解码器（速记）

| 提示 | 内容 |
|---|---|
| 自回归语言模型 | $P(w_1,\dots,w_T)=\prod_tP(w_t\mid w_{<t})$；每个位置一道「看前文猜下一个词」的题；损失 $L=-\frac1T\sum\ln p_t$，是各位置交叉熵的平均 |
| 困惑度 | $\mathrm{PPL}=e^{L}=(\prod p_t)^{-1/T}$：平均相当于在 PPL 个词里均匀地猜；最小 1，均匀猜 $\lvert\mathcal V\rvert$ 个词是 $\lvert\mathcal V\rvert$；要同一份文本、同一个词表才能比 |
| n 元语法 | 二元：$\hat P(b\mid a)=c(a,b)\big/\sum_vc(a,v)$（分母是以 $a$ 为前项的全部次数之和，须大于 0；这一行的相对频率就是最大似然）；毛病：没见过的组合概率为 0（数据稀疏），窗口太短 |
| 循环网络前向 | $\boldsymbol h_t=\tanh(W\boldsymbol h_{t-1}+U\boldsymbol x_t+\boldsymbol b)$，$\boldsymbol p_t=\mathrm{softmax}(W_{\mathrm{out}}\boldsymbol h_t+\boldsymbol b_{\mathrm{out}})$；每步共用同一组参数，参数个数与句长无关 |
| BPTT 递推 | 先两路相加 $\frac{\partial L}{\partial\boldsymbol h_t}=\frac1TW_{\mathrm{out}}^{\mathsf T}(\boldsymbol p_t-\boldsymbol y_t)+W^{\mathsf T}\boldsymbol\delta_{t+1}$，再穿过 $\tanh$：$\boldsymbol\delta_t=(1-\boldsymbol h_t^{\,2})\odot\frac{\partial L}{\partial\boldsymbol h_t}$；$\boldsymbol\delta_{T+1}=\boldsymbol0$ |
| 共享参数的梯度 | $\frac{\partial L}{\partial W}=\sum_t\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T}$，$\frac{\partial L}{\partial U}=\sum_t\boldsymbol\delta_t\boldsymbol x_t^{\mathsf T}$，$\frac{\partial L}{\partial\boldsymbol b}=\sum_t\boldsymbol\delta_t$（同一参数的各个副本之和）；输出层 $\frac{\partial L}{\partial W_{\mathrm{out}}}=\frac1T\sum_t(\boldsymbol p_t-\boldsymbol y_t)\boldsymbol h_t^{\mathsf T}$ |
| 梯度缩小与爆炸 | $\frac{\partial\boldsymbol h_T}{\partial\boldsymbol h_t}=(D_TW)\cdots(D_{t+1}W)$，$D_k=\mathrm{diag}(1-\boldsymbol h_k^{\,2})$（较晚的在左），范数 $\le\lVert W\rVert_2^{\,T-t}$；$\lVert W\rVert_2<1$ 时上界指数缩小，上界大于 1 不能推出爆炸；爆炸用梯度裁剪 $\boldsymbol g\to\boldsymbol g\,c/\lVert\boldsymbol g\rVert$（只治爆炸） |
| LSTM | $\boldsymbol c_t=\boldsymbol f_t\odot\boldsymbol c_{t-1}+\boldsymbol i_t\odot\tilde{\boldsymbol c}_t$，$\boldsymbol h_t=\boldsymbol g_t\odot\tanh\boldsymbol c_t$（$\boldsymbol g_t$ 是输出门）；沿细胞状态直接路径 $\partial\boldsymbol c_t/\partial\boldsymbol c_{t-1}=\mathrm{diag}(\boldsymbol f_t)$，门值连乘接近 1 才保留得好，不保证总梯度；循环单元用四组参数 |
| GRU | $\boldsymbol h_t=(1-\boldsymbol z_t)\odot\boldsymbol h_{t-1}+\boldsymbol z_t\odot\tilde{\boldsymbol h}_t$；两个门，循环单元用三组参数；旧状态直接路径的导数 $\mathrm{diag}(1-\boldsymbol z_t)$ |
| 编码器–解码器 | 编码器最后状态 $\boldsymbol m$ → 解码器（条件语言模型）$\prod_tP(w'_t\mid w'_{<t},\boldsymbol m)$；训练用 teacher forcing；定长 $\boldsymbol m$ 是瓶颈 |
| 加性注意力 | $u_{t,j}=\boldsymbol v^{\mathsf T}\tanh(W_s\boldsymbol s_{t-1}+W_h\boldsymbol h_j)$，$\alpha_{t,j}=\mathrm{softmax}_j(u_{t,j})$，$\bar{\boldsymbol h}_t=\sum_j\alpha_{t,j}\boldsymbol h_j$（加权平均，软对齐） |
| 高频易错 | 只用最后一步的概率算困惑度；把 $\mathrm{PPL}$ 说成算术平均；漏加 $W^{\mathsf T}\boldsymbol\delta_{t+1}$ 那一项；忘了共享参数梯度要对时间求和；以为裁剪能治消失 |
