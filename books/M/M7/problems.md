## M.7 · 多层网络与反向传播（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| M7-01 | A | 方法 1 |
| M7-02 | A | 方法 2 |
| M7-03 | A | 方法 3 |
| M7-04 | A | 方法 9 |
| M7-05 | B | 方法 4、5、6 |
| M7-06 | B | 方法 7 |
| M7-07 | B | 方法 8 |
| M7-08 | B | 方法 2、8、9 |
| M7-09 | B | 方法 7、9 |
| M7-10 | C | 方法 9、10 |
| M7-11 | C | 方法 9、10 |
| M7-12 | C | 方法 10、11 |
| M7-13 | B | 混合练习 |
| M7-14 | B | 混合练习 |
| M7-15 | C | 混合练习 |

### A 基础

**M7-01**〔A｜方法 1 · 考查：逐层前向计算〕设
\[
W_1=\begin{pmatrix}1&-1\\2&1\end{pmatrix},\quad \boldsymbol b_1=(0,-1)^{\mathsf T},\quad \boldsymbol x=(1,-1)^{\mathsf T},
\]
隐藏层用 ReLU，输出层为 $W_2=(1,2)$、$b_2=-1$。求 $\boldsymbol z_1$、$\boldsymbol h$ 和 $z_2$。

**M7-02**〔A｜方法 2 · 考查：激活函数导数〕在 $z=0.5$ 处，下列三元组分别表示 $(\sigma'(z),\tanh'(z),\operatorname{ReLU}'(z))$，正确的是（　）。

(A) $(0.6225,0.7864,0)$　(B) $(0.2350,0.7864,1)$　(C) $(0.2350,0.2136,1)$　(D) $(0.3775,0.7864,1)$

**M7-03**〔A｜方法 3 · 考查：批量形状与参数数〕一个网络的维数为 $5\to4\to3$，一次输入 $7$ 个样本。写出两个线性层输出的形状、$W_1,W_2$ 的形状，并求全部参数个数（偏置也计入）。

**M7-04**〔A｜方法 9 · 考查：由反向结果判断上游分量〕设 $\boldsymbol h=\operatorname{ReLU}(\boldsymbol z)$，$\boldsymbol z=(-1,0,2)^{\mathsf T}$，目标反向结果为 $\bar{\boldsymbol z}=(0,0,3)^{\mathsf T}$。本书在 $z=0$ 处约定 ReLU 导数取 $0$。下列哪项完整描述了上游梯度的全部可能值（　）？

(A) 只能是 $(0,0,3)^{\mathsf T}$　(B) 可以是 $(a,b,3)^{\mathsf T}$，其中 $a,b$ 任意　(C) 可以是 $(a,0,c)^{\mathsf T}$，其中 $a,c$ 任意　(D) 不存在

### B 进阶

**M7-05**〔B｜方法 4、5、6 · 考查：分叉处梯度相加〕设
\[
u=wx+b,\quad p=\sigma(u),\quad L=up+(u-1)^2,
\]
其中 $x=2,w=1,b=0$。分别写出 $u$ 经乘积的直接因子、经 $p$、经平方项这三条路径的贡献，求 $\partial L/\partial w$ 和 $\partial L/\partial b$，并用直接求导核对。结果保留四位小数。

**M7-06**〔B｜方法 7 · 考查：雅可比转置与形状〕设
\[
\boldsymbol y=\begin{pmatrix}x_1^2+x_2\\x_1x_2\\x_1-x_2\end{pmatrix},\quad \boldsymbol x=(2,-1)^{\mathsf T},\quad \bar{\boldsymbol y}=(1,2,-1)^{\mathsf T}。
\]
先由输入、输出维数确定 $J$ 的形状，再求 $J$ 和 $\bar{\boldsymbol x}$。说明为何 $J\bar{\boldsymbol y}$ 在这里不能相乘。

**M7-07**〔B｜方法 8 · 考查：批量平均与求和〕两个样本按行放入 $X$，经过线性层 $Y=XW^{\mathsf T}+\boldsymbol1\boldsymbol b^{\mathsf T}$，其中 $\boldsymbol1=(1,1)^{\mathsf T}$。取
\[
X=\begin{pmatrix}1&-1\\2&1\end{pmatrix},\quad
W=\begin{pmatrix}1&2\\-1&0\end{pmatrix},\quad
G=\begin{pmatrix}2&-1\\-2&3\end{pmatrix}。
\]
第 $r$ 个样本的损失为 $\ell_r$，$G$ 的第 $r$ 行是 $\partial\ell_r/\partial\boldsymbol y_r$ 的转置，尚未除以样本数。总损失为 $L=(\ell_1+\ell_2)/2$。求 $\partial L/\partial X,\partial L/\partial W,\partial L/\partial\boldsymbol b$，并说明若误把 $G$ 当成 $\partial L/\partial Y$，结果会怎样。

**M7-08**〔B｜方法 2、8、9 · 考查：从分量证明参数梯度〕设 $\boldsymbol z=W\boldsymbol x+\boldsymbol b$，$W\in\mathbb R^{m\times d}$，$L$ 是 $\boldsymbol z$ 的可微标量函数，记 $\delta_i=\partial L/\partial z_i$。固定 $\boldsymbol x,\boldsymbol b$，从 $z_i=\sum_jW_{ij}x_j+b_i$ 出发，证明 $\partial L/\partial W=\boldsymbol\delta\boldsymbol x^{\mathsf T}$。若再接 $h_i=\tanh z_i$，且 $L$ 仅通过 $\boldsymbol h$ 依赖 $\boldsymbol z$，上游梯度为 $\bar h_i$，写出 $\delta_i$ 并说明所用的激活导数。

**M7-09**〔B｜方法 7、9 · 考查：逐元素公式的适用范围〕设 $u_1=z_1+z_2,u_2=z_2$，$h_i=\tanh u_i$。在 $\boldsymbol z=(0,0)^{\mathsf T}$ 处，上游梯度为 $\bar{\boldsymbol h}=(1,2)^{\mathsf T}$。关于反向结果，正确的是（　）。

(A) $\bar{\boldsymbol z}=(1,2)^{\mathsf T}$，直接与 tanh 导数对应相乘即可

(B) $\bar{\boldsymbol z}=(3,2)^{\mathsf T}$，应把两条贡献加在第一分量

(C) $\bar{\boldsymbol z}=(1,3)^{\mathsf T}$，先从 $\boldsymbol h$ 传到 $\boldsymbol u$，再从 $\boldsymbol u$ 传到 $\boldsymbol z$

(D) $\bar{\boldsymbol z}=(0,0)^{\mathsf T}$，因为 tanh 在原点的值为零

### C 提高

**M7-10**〔C｜方法 9、10 · 考查：跨层共享参数〕设两个线性层共用同一个标量参数 $w$：
\[
z_1=wx+b,\quad h=\tanh z_1,\quad z_2=wh+c,\quad L=\tfrac12z_2^2。
\]
取 $x=w=1,b=c=0$。先标出各层量及参数的形状，再求前向值及 $\partial L/\partial w,\partial L/\partial b,\partial L/\partial c$。把 $w$ 在两层的贡献分别列出；若暂把两处的 $w$ 记为独立的 $w_1,w_2$，它们的偏导与共享参数的偏导是什么关系？可用 $s=\tanh1$ 表示。

拆法：先做 M7-06、M7-07，再用 tanh 的逐元素反向；共享参数处按 M7-05 将贡献相加。

**M7-11**〔C｜方法 9、10 · 考查：三层网络逐层递推〕设 $\boldsymbol x=(1,-1)^{\mathsf T}$，两层隐藏层都用 ReLU：
\[
W_1=\begin{pmatrix}1&0\\-1&1\end{pmatrix},\quad \boldsymbol b_1=\boldsymbol0,\quad
W_2=\begin{pmatrix}1&2\\0&1\end{pmatrix},\quad \boldsymbol b_2=(0,1)^{\mathsf T},
\]
输出层为 $W_3=(2,-1)$、$b_3=0$，损失为 $L=\tfrac12(z_3-2)^2$。求三层权重矩阵和偏置的全部梯度。

拆法：先做 M7-04、M7-07。

**M7-12**〔C｜方法 10、11 · 考查：两样本共享参数的数值检验〕两个样本 $x_1=1,x_2=2$ 共用参数 $w$，各自经过
\[
u_r=wx_r,\quad h_r=\sigma(u_r),\quad a_r=2h_r,\quad
L=\frac12\sum_{r=1}^2\frac12(a_r-0)^2。
\]
取 $w=0.2$，输出系数 $2$ 固定。逐样本反向求 $g=\partial L/\partial w$，再用 $\varepsilon=10^{-5}$ 的中心差分核对；每次扰动同一个 $w$ 后须重算两个样本。写出相对误差所用的分母，说明两个梯度均为零时如何报告误差。

拆法：先做 M7-05、M7-10。

### 章末混合练习

**M7-13**〔B〕单个样本 $x=2,y=1$ 经过 $p=\sigma(wx+b)$，取 $w=0.3,b=-0.1$，损失为二元交叉熵，学习率为 $\eta=0.2$。用一次反向传播和梯度下降同时求 $w',b'$。

**M7-14**〔B〕三分类输出的分数为 $\boldsymbol z=(1,0,-1)^{\mathsf T}$，真实标签为 $\boldsymbol y=(0,1,0)^{\mathsf T}$，隐藏层输出为 $\boldsymbol h=(1,2)^{\mathsf T}$。输出层为 $\boldsymbol z=W_2\boldsymbol h+\boldsymbol b_2$，接 softmax 交叉熵。先确定 $W_2,\boldsymbol b_2$ 的形状和该输出层的参数数，再求 $\boldsymbol p$、$\boldsymbol\delta_2$ 和 $\partial L/\partial W_2$。

**M7-15**〔C〕设三个仿射层依次为 $\boldsymbol a_1=W_1\boldsymbol x+\boldsymbol b_1$、$\boldsymbol a_2=W_2\boldsymbol a_1+\boldsymbol b_2$、$\boldsymbol z=W_3\boldsymbol a_2+\boldsymbol b_3$，各矩阵维数相容。求合成后的权重和偏置。再取
\[
W_1=\begin{pmatrix}1&2\\0&1\end{pmatrix},\quad \boldsymbol b_1=(1,0)^{\mathsf T},\quad W_2=(2,-1),\quad b_2=3,\quad W_3=2,\quad b_3=-1。
\]
写出合成式，并逐层计算 $\boldsymbol x=(1,-1)^{\mathsf T}$ 的输出来核对。最后考察标量复合 $f(x)=2\operatorname{ReLU}(x+1)-1$：用 $x=-2,-1,0$ 三点证明不存在对所有实数 $x$ 都成立的 $f(x)=ax+b$。

拆法：先做 M7-01、M7-04，再用矩阵乘法的结合律与分配律逐层合并。
