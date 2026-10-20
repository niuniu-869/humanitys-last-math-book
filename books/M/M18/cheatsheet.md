## M.18 · 读一篇真实论文（速记）

| 提示 | 内容 |
|---|---|
| 读公式四问 | ①符号是数/向量/矩阵，输入/参数/超参数/中间量 ②形状对不对（内侧维数、结果形状） ③在算什么、对应哪一节、用小数字代一遍 ④改一个超参数会怎样 |
| 论文式 (1) | $\mathrm{softmax}(QK^{\mathsf T}/\sqrt{d_k})V$；$Q\in\mathbb R^{n\times d_k}$，$K\in\mathbb R^{m\times d_k}$，$V\in\mathbb R^{m\times d_v}$，输出 $n\times d_v$；对应 M.11.3、M.11.4 |
| 多头 | $\mathrm{head}_i=\mathrm{Attention}(QW_i^Q,KW_i^K,VW_i^V)$；$W_i^{Q,K}\in\mathbb R^{d\times d_k}$，$W_i^V\in\mathbb R^{d\times d_v}$，$W^O\in\mathbb R^{hd_v\times d}$；基础模型 $d=512$，$h=8$，$d_k=d_v=64$；对应 M.12.1 |
| 注意力三种用法 | 编码器自注意力；解码器带掩码自注意力（M.11.5）；编码器–解码器交叉注意力（M.11.6） |
| 前馈层 | $\max(0,xW_1+b_1)W_2+b_2$，$512\to2048\to512$；逐位置，同一个 FFN 作用于每个位置；对应 M.12.2 |
| 嵌入与输出 | 两张嵌入表与输出矩阵共享权重，嵌入乘 $\sqrt{d}$；对应 M.9.3、M.12.7 |
| 位置编码 | $PE_{(pos,2i)}=\sin(pos/10000^{2i/d})$，$PE_{(pos,2i+1)}=\cos(\cdot)$，与嵌入相加；对应 M.12.4 |
| Post-LN 与 Pre-LN | 论文 $\mathrm{LN}(x+F(x))$，本书 $x+F(\mathrm{LN}(x))$；Pre-LN 的 $\partial y/\partial x=I+\cdots$ 有直通路径 |
| 结构差别 | 论文编码器–解码器（6+6 层，翻译）；本书只有解码器（续写），没有交叉注意力 |
| 每层参数 | 编码器层 $12d^2$（注意力 $4d^2$ + 前馈 $8d^2$），解码器层 $16d^2$；$d=512$ 时 $3145728$ 与 $4194304$ |
| 为什么用自注意力 | 每层 $O(n^2d)$、串行 $O(1)$、路径 $O(1)$；循环层 $O(nd^2)$、$O(n)$、$O(n)$；$n<d$ 时注意力更省 |
| 预热学习率 | $d^{-0.5}\min(\mathrm{step}^{-0.5},\mathrm{step}\cdot\mathrm{warmup}^{-1.5})$，预热 4000 步，峰值在 $\mathrm{step}=\mathrm{warmup}$ |
| 概念简答四段 | 定义（一句）→ 为什么需要（治什么病）→ 公式或机制（符号交代清）→ 一个例子（小数字算出结果） |
| 易错 | 只写公式不说为什么；只说"效果好"不说机制；例子的数没算出来；把 $d_{\text{model}}$ 与 $d_k$ 混为一谈 |
