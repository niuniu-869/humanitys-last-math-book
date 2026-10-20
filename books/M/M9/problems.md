## M.9 · 词向量与表示学习：从独热向量到 word2vec（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| M9-01 | A | 方法 1（选择） |
| M9-02 | A | 方法 3 |
| M9-03 | A | 方法 4 |
| M9-04 | A | 方法 8 |
| M9-05 | B | 方法 2、4 |
| M9-06 | B | 方法 4 |
| M9-07 | B | 方法 5（选择） |
| M9-08 | B | 方法 6 |
| M9-09 | B | 方法 6 |
| M9-10 | B | 方法 8（选择） |
| M9-11 | C | 方法 5（证明） |
| M9-12 | C | 方法 4、5 |
| M9-13 | B | 混合（答案里标） |
| M9-14 | B | 混合（答案里标） |
| M9-15 | B | 混合（答案里标） |

### A 基础

**M9-01**〔A｜方法 1 · 考查：独热向量能否给出相近程度的先后〕（选择）设 $\boldsymbol e_0,\boldsymbol e_1,\boldsymbol e_2$ 是 $\mathbb R^3$ 中三个独热向量。要按余弦相似度比较后两个向量谁与 $\boldsymbol e_0$ 更相近，下列说法正确的是（　）。

(A) 编号相邻，所以 $\cos(\boldsymbol e_0,\boldsymbol e_1)=1$。

(B) 编号差较小，所以 $\cos(\boldsymbol e_0,\boldsymbol e_1)>\cos(\boldsymbol e_0,\boldsymbol e_2)$。

(C) 因为有两个非零分量，所以 $\lVert\boldsymbol e_0-\boldsymbol e_1\rVert=2$。

(D) 两个余弦都为 0，因此这个比较不能排出先后。

**M9-02**〔A｜方法 3 · 考查：由查表结果反求矩阵中的已知行〕$E$ 是 $3\times2$ 的矩阵，行编号从 0 开始。已知

$$O=\begin{pmatrix}0&0&1\\1&0&0\\0&0&1\end{pmatrix},\qquad OE=\begin{pmatrix}-1&2\\3&0\\-1&2\end{pmatrix}.$$

求所有可能的 $E$，并指出它的 6 个元素中有几个被唯一确定。

**M9-03**〔A｜方法 4 · 考查：点积得分与指数归一化〕设

$$U=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix},\qquad \boldsymbol v=(\ln2,\ln3)^{\mathsf T}.$$

三个候选编号为 $0,1,2$，得分是 $\boldsymbol z=U\boldsymbol v$。求 softmax 概率向量，以及真实编号为 1 时的损失 $\ell=-\ln p_1$。

**M9-04**〔A｜方法 8 · 考查：两个方向的损失如何平均〕给定

$$S=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad \tau=\frac1{\ln3}.$$

以对角元为正确位置，求每行正确位置的 softmax 概率、行损失平均、列损失平均以及两个方向平均后的总损失。

### B 进阶

**M9-05**〔B｜方法 2、4 · 考查：相同词的相邻位置与句子边界〕词表按 $a,b,c$ 排列，语料只有两句：「$a\ a\ b$」和「$b\ c$」。窗口半径为 1，不跨句，中心位置本身不算上下文。

1. 求共现矩阵 $X$，并求有向的（中心词，上下文词）训练样本总数，重复的词对按出现次数计。
2. 求 $\cos(\boldsymbol x_a,\boldsymbol x_c)$ 和 $\cos(\boldsymbol x_b,\boldsymbol x_c)$。直接相邻过的 $b,c$ 是否一定比从未相邻的 $a,c$ 有更大的行向量余弦？

**M9-06**〔B｜方法 4 · 考查：由概率比恢复点积参数〕设

$$U=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\qquad \boldsymbol v=(x,y)^{\mathsf T}.$$

候选编号为 $0,1,2$。已知 $\operatorname{softmax}(U\boldsymbol v)=(1/6,1/3,1/2)^{\mathsf T}$，求所有可能的 $(x,y)$，并求真实编号为 2 时的损失。

**M9-07**〔B｜方法 5 · 考查：一个参数块的梯度为零意味着什么〕（选择）设

$$U=\begin{pmatrix}1&0\\-1&0\\0&0\end{pmatrix},\qquad \boldsymbol v=(0,2)^{\mathsf T},\qquad \boldsymbol y=(0,0,1)^{\mathsf T}.$$

令 $\boldsymbol p=\operatorname{softmax}(U\boldsymbol v)$，$\ell=-\ln p_2$。把 $U$ 的元素和 $\boldsymbol v$ 的分量都视为可变参数，下列说法正确的是（　）。

(A) $\nabla_{\boldsymbol v}\ell=\boldsymbol0$，但 $\nabla_U\ell\ne0$。

(B) 因为 $\nabla_{\boldsymbol v}\ell=\boldsymbol0$，所以 $\nabla_U\ell$ 也为零矩阵。

(C) $\nabla_U\ell$ 只有真实编号对应的第 2 行非零。

(D) 因为 $\nabla_{\boldsymbol v}\ell=\boldsymbol0$，所以 $\ell=0$。

**M9-08**〔B｜方法 6 · 考查：重复负样本的梯度如何累计〕设

$$\boldsymbol v=(0,\ln2)^{\mathsf T},\quad \boldsymbol u_o=(1,0)^{\mathsf T},\quad \boldsymbol u_n=(0,1)^{\mathsf T}.$$

有放回抽样得到两个负样本，恰好都对应同一个参数向量 $\boldsymbol u_n$，因此

$$\ell=-\ln\sigma(\boldsymbol u_o^{\mathsf T}\boldsymbol v)-2\ln\sigma(-\boldsymbol u_n^{\mathsf T}\boldsymbol v).$$

求损失及对 $\boldsymbol v,\boldsymbol u_o,\boldsymbol u_n$ 的梯度。如果删除重复项，只保留一次负样本损失，损失和对 $\boldsymbol v$ 的梯度各变成什么？

**M9-09**〔B｜方法 6 · 考查：由抽样概率比反求频数〕三个正频数满足 $f_0=81,f_2=1$。按 $P_i=f_i^{3/4}/\sum_{j=0}^2f_j^{3/4}$ 归一化后，已知 $P_0/P_1=27/8$。求 $f_1$ 和三个 $P_i$，并判断 $P_1$ 比直接按频数归一化得到的概率大还是小。

**M9-10**〔B｜方法 8 · 考查：降低温度对错误排序的影响〕（选择）给定

$$S=\begin{pmatrix}0&1\\1&0\end{pmatrix},\qquad \tau>0.$$

正确位置仍在对角线上，总损失按方法 8 对两个方向取平均。将温度从 $\tau$ 改为 $\tau/2$，下列说法正确的是（　）。

(A) softmax 更集中，所以正确位置的概率增大，总损失减小。

(B) 正确位置的概率减小，总损失增大。

(C) 因为 $S$ 对称，所以两个温度下的总损失都为 $\ln2$。

(D) 新总损失为 $2\ln(1+e^{2/\tau})$，因为要把两个方向的损失相加。

### C 提高

**M9-11**〔C｜方法 5 · 考查：链式法则与各候选梯度之和〕设 $U$ 的第 $w$ 行为 $\boldsymbol u_w^{\mathsf T}$，$\boldsymbol p=\operatorname{softmax}(U\boldsymbol v)$，$\boldsymbol y$ 是真实编号 $o$ 的独热向量。令 $\ell=-\ln p_o$。

1. 从 $\ell=-\boldsymbol u_o^{\mathsf T}\boldsymbol v+\ln\sum_w e^{\boldsymbol u_w^{\mathsf T}\boldsymbol v}$ 出发，证明 $\nabla_{\boldsymbol v}\ell=U^{\mathsf T}(\boldsymbol p-\boldsymbol y)=\sum_wp_w\boldsymbol u_w-\boldsymbol u_o$。
2. 推出 $\sum_w\nabla_{\boldsymbol u_w}\ell=\boldsymbol0$，并据此证明：用同一个学习率、同一次计算得到的梯度更新所有 $\boldsymbol u_w$，它们的向量和保持不变。

拆法：先做 M9-03、M9-07。

**M9-12**〔C｜方法 4、5 · 考查：平均损失的最优参数与一步更新〕固定 $\boldsymbol u_0=(1,0)^{\mathsf T},\boldsymbol u_1=(-1,0)^{\mathsf T}$，令 $\boldsymbol v=(t,0)^{\mathsf T}$，只允许改变实数 $t$。四个样本共用同一个 $\boldsymbol v$，真实编号依次为 $0,0,0,1$。

1. 写出四个 softmax 交叉熵的平均值 $J(t)$。
2. 求使 $J(t)$ 最小的 $t$、此时的概率向量和最小损失，并用导数符号说明它是全局最小值。
3. 从 $t=0$ 出发，以学习率 1 对 $J$ 做一步梯度下降。求新参数和新损失，并与初始损失、最小损失比较。小数保留四位。

拆法：先做 M9-06、M9-11。

### 章末混合练习

**M9-13**〔B〕设

$$O=\begin{pmatrix}1&0\\0&1\\1&0\end{pmatrix},\qquad E=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad H=OE.$$

某可微标量函数 $J(H)$ 在当前 $H$ 处的梯度矩阵为

$$G=\frac{\partial J}{\partial H}=\begin{pmatrix}1&2\\3&4\\-1&1\end{pmatrix}.$$

求 $\partial J/\partial E$，再以学习率 $1/10$ 更新 $E$。同一行被查到两次时，为什么不能只保留最后一次的梯度？

**M9-14**〔B〕对两个可独立变化的分数 $s_0,s_1$，定义

$$L=-s_0+\ln(e^{s_0}+e^{s_1}),\qquad B=-\ln\sigma(s_0)-\ln\sigma(-s_1).$$

在 $(s_0,s_1)=(\ln3,0)$ 处，分别求 $L,B$ 及它们对 $(s_0,s_1)$ 的梯度。两个函数能否在该点给出完全相同的梯度下降更新方向？

**M9-15**〔B〕给定六个向量

$$\boldsymbol v_a=(2,1)^{\mathsf T},\quad\boldsymbol v_b=(1,0)^{\mathsf T},\quad\boldsymbol v_c=(0,-1)^{\mathsf T},$$

$$\boldsymbol v_d=(4,0)^{\mathsf T},\quad\boldsymbol v_e=(1,1/2)^{\mathsf T},\quad\boldsymbol v_f=(-1,0)^{\mathsf T}.$$

求 $\boldsymbol q=\boldsymbol v_a-\boldsymbol v_b+\boldsymbol v_c$。排除三个输入向量后，按余弦相似度最大的规则选出候选；再按欧氏距离最小的规则选择，并说明两个规则在这里为何给出不同结果。
