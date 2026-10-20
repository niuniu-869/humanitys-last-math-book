## M.12 · Transformer 的积木：多头、前馈层、LayerNorm、位置编码（速记）

| 提示 | 内容 |
|---|---|
| 多头注意力 | $h$ 个头各用 $d_k=d/h$ 维，各做一次注意力，沿列拼成 $n\times d$，再右乘 $W_O\in\mathbb R^{d\times d}$；参数 $4d^2$，与 $h$ 无关；计算量也基本不变 |
| 前馈层 | $\phi(XW_1+\boldsymbol b_1)W_2+\boldsymbol b_2$，$d\to4d\to d$，每一行（每个位置）共用同一个 MLP；参数 $8d^2$；注意力混合位置，前馈层混合通道 |
| LayerNorm | 对一个位置的 $d$ 个数：$\boldsymbol\gamma\odot(\boldsymbol x-\mu)/\sqrt{\sigma^2+\varepsilon}+\boldsymbol\beta$，方差除以 $d$；统计量沿行求，批归一化沿列求；$\varepsilon=0$ 时对正倍数缩放和整体平移不变；$\varepsilon>0$ 时平移不变仍精确，尺度不变只是近似 |
| RMSNorm | $\boldsymbol\gamma\odot\boldsymbol x/\sqrt{\frac1d\sum x_i^2+\varepsilon}$：不减均值，不要 $\boldsymbol\beta$，只对尺度不敏感；$(1,2,3,6)\mapsto(0.2828,0.5657,0.8485,1.6971)$ |
| 为什么不用批归一化 | 统计量依赖同批样本和补齐位置；批小不准；推理要换滑动平均；一个样本的输出会受别的样本影响 |
| 注意力对词序不敏感 | 输入 $PX$ 时 $S'=PSP^{\mathsf T}$，$\mathrm{softmax}(PSP^{\mathsf T})=PAP^{\mathsf T}$，输出 $PAV$：行跟着换序，每个词得到的向量不变 |
| 正弦位置编码 | $p_{p,2i}=\sin(p/10000^{2i/d})$，$p_{p,2i+1}=\cos(\cdot)$，加到词向量上；每对是一根指针；$\boldsymbol p_{p+k}$ 是 $\boldsymbol p_p$ 的旋转（矩阵只含 $k$） |
| RoPE | 位置 $m$ 的 $\boldsymbol q$、位置 $n$ 的 $\boldsymbol k$ 各转 $m\theta$、$n\theta$：$\boldsymbol q^{\mathsf T}R(m\theta)^{\mathsf T}R(n\theta)\boldsymbol k=\boldsymbol q^{\mathsf T}R((n-m)\theta)\boldsymbol k$；只转 $Q,K$，不转 $V$ |
| Pre-LN 块 | $X'=X+\mathrm{MHA}(\mathrm{LN}(X))$，$Y=X'+\mathrm{FFN}(\mathrm{LN}(X'))$；形状始终 $n\times d$；主干上只有恒等，梯度有直路；Post-LN 把 LN 放在相加之后 |
| 整体结构 | 查表 $E$（$n\times d$）→ $L$ 个块 → 最后 LN → $HE_{\mathrm{out}}^{\mathsf T}$（$n\times\lvert\mathcal V\rvert$）→ 逐行 softmax；第 $t$ 行的目标是第 $t+1$ 个词 |
| 参数量 | 每块 $4d^2+8d^2=12d^2$；$N\approx12Ld^2+\lvert\mathcal V\rvert d$；GPT-3：$L=96$，$d=12288$ 得约 1750 亿；Llama-2 7B 精确 $6.74\times10^9$ |
| 计算量 | 前向 $2N$，反向 $4N$，每个词元训练约 $6N$；$C\approx6ND$；注意力部分与权重部分之比约 $n/(6d)$ |
| 高频易错 | 以为头数多参数就多；LN 的方差除成 $d-1$；把 LN 的统计量沿列求；RoPE 旋转了 $V$；忘了输出投影 $W_O$；$6N$ 里把嵌入也算成矩阵乘 |
