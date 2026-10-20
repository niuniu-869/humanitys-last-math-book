## M.7 · 多层网络与反向传播（答案）

### A 基础

**M7-01**
**答案：** $\boldsymbol z_1=(2,0)^{\mathsf T}$，$\boldsymbol h=(2,0)^{\mathsf T}$，$z_2=1$。因为 $W_1\boldsymbol x+\boldsymbol b_1=(2,0)^{\mathsf T}$，ReLU 不改变这两个非负分量，代入输出层得 $1\cdot2+2\cdot0-1=1$。

区分点：要按预激活、激活、输出的顺序计算，不能把偏置漏在某一层之外。

**M7-02**
**答案：** (B)。$\sigma'=\sigma(1-\sigma)\approx0.2350$，$\tanh'=1-\tanh^2(0.5)\approx0.7864$，而 $0.5>0$ 所以 ReLU 导数为 1。(A) 把 sigmoid 函数值当成导数，并误用 ReLU 的非正分支；(C) 把 $\tanh'$ 算成了 $\tanh^2z$；(D) 把 sigmoid 导数写成了 $\sigma(-z)$。

区分点：能分别调用三个导数公式，而不是只记住激活函数的函数值。

**M7-03**
**答案：** 两个输出形状为 $7\times4$、$7\times3$；$W_1$ 为 $4\times5$，$W_2$ 为 $3\times4$；参数数为 $(20+4)+(12+3)=39$。批量维只增加样本行数，不增加参数。

区分点：先固定输出维在矩阵的前一维，再把每层偏置计入参数数。

**M7-04**
**答案：** (B)。掩码为 $(0,0,1)$，前两个上游分量乘零后都消失，第三个必须等于 $3$。(A) 错在把一个可行解当成唯一解；(C) 把第二分量固定在 0（只是可行值之一），又把必须等于 $3$ 的第三分量写成任意 $c$；(D) 被 $(0,0,3)^{\mathsf T}$ 这个可行解否定。

区分点：被掩码截断的分量不能从反向结果唯一恢复，边界按题中约定处理。

### B 进阶

**M7-05**
**答案：** $\partial L/\partial w\approx6.1816$，$\partial L/\partial b\approx3.0908$。前向有 $u=2,p=\sigma(2)$。三条路径对 $\bar u$ 的贡献分别为 $p$、$up(1-p)$ 和 $2(u-1)$，所以
\[
\bar u=p+up(1-p)+2(u-1)\approx3.0908。
\]
因为 $\partial u/\partial w=2,\partial u/\partial b=1$，参数梯度分别为 $2\bar u,\bar u$。直接对 $u\sigma(u)+(u-1)^2$ 求导，乘积法则给出 $\sigma(u)+u\sigma'(u)$，再加平方项的 $2(u-1)$，与三条路径相加一致。

区分点：同一个量既直接参与乘积又通过 sigmoid 参与乘积，三条路径（含平方项）都不能漏。

**M7-06**
**答案：** $J$ 为 $3\times2$，$\bar{\boldsymbol x}=(1,6)^{\mathsf T}$。按输出排成行、输入排成列，得
\[
J=\begin{pmatrix}2x_1&1\\x_2&x_1\\1&-1\end{pmatrix}=\begin{pmatrix}4&1\\-1&2\\1&-1\end{pmatrix},\qquad
J^{\mathsf T}\bar{\boldsymbol y}=\begin{pmatrix}4-2-1\\1+4+1\end{pmatrix}=\begin{pmatrix}1\\6\end{pmatrix}。
\]

$J\bar{\boldsymbol y}$ 的内侧维数是 $2$ 和 $3$，不能相乘；$J^{\mathsf T}\bar{\boldsymbol y}$ 则是 $(2\times3)(3\times1)$。

区分点：雅可比的行对应输出、列对应输入，反向时要乘 $J^{\mathsf T}$，不能直接乘 $J$。

**M7-07**
**答案：**
\[
\frac{\partial L}{\partial X}=\begin{pmatrix}3/2&2\\-5/2&-2\end{pmatrix},\quad
\frac{\partial L}{\partial W}=\begin{pmatrix}-1&-2\\5/2&2\end{pmatrix},\quad
\frac{\partial L}{\partial\boldsymbol b}=(0,1)^{\mathsf T}。
\]
由于损失取平均，传到 $Y$ 的梯度是 $\Delta=G/2$。因此 $\partial L/\partial W=G^{\mathsf T}X/2$，$\partial L/\partial\boldsymbol b=G^{\mathsf T}\boldsymbol1/2$，$\partial L/\partial X=GW/2$。前两式对两个样本的贡献求和，第三式按行保留每个样本的输入梯度。若直接使用 $G$，三个结果都会变成正确值的两倍。

区分点：先辨明给出的上游量是否已经包含平均系数，不能漏除或重复除以样本数。

**M7-08**
**答案：** $\partial L/\partial W=\boldsymbol\delta\boldsymbol x^{\mathsf T}$；接 tanh 时 $\delta_i=\bar h_i(1-h_i^2)$。固定一个元素 $W_{ab}$，只有 $z_a$ 含有它，且 $\partial z_a/\partial W_{ab}=x_b$。由链式法则，
\[
\frac{\partial L}{\partial W_{ab}}=\sum_{i=1}^m\frac{\partial L}{\partial z_i}\frac{\partial z_i}{\partial W_{ab}}=\delta_a x_b。
\]
把全部 $(a,b)$ 分量排成 $m\times d$ 矩阵，即为所证外积。接 tanh 时，$h_i$ 只依赖 $z_i$，用方法 2 的 $\tanh' z_i=1-\tanh^2z_i=1-h_i^2$，再乘上游 $\bar h_i$。

区分点：先确定一个权重影响哪个输出分量，再由分量式识别外积，避免凭形状猜公式。

**M7-09**
**答案：** (C)。在原点 $\boldsymbol u=\boldsymbol h=\boldsymbol0$，tanh 导数为 $1$，先得 $\bar{\boldsymbol u}=(1,2)^{\mathsf T}$。再用
\[
\frac{\partial\boldsymbol u}{\partial\boldsymbol z}=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad
\bar{\boldsymbol z}=\begin{pmatrix}1&0\\1&1\end{pmatrix}\begin{pmatrix}1\\2\end{pmatrix}=(1,3)^{\mathsf T}。
\]
(A) 漏了 $z_2$ 经 $u_1$ 的贡献；(B) 把雅可比直接乘在上游向量上，未转置；(D) 混淆了 tanh 的函数值与导数。方法 9 可用于 $\boldsymbol u\to\boldsymbol h$，不能直接用于整个 $\boldsymbol z\to\boldsymbol h$。

区分点：要检查输出究竟依赖哪些输入，不能因最后一步是激活函数就省略前面的混合运算。

### C 提高

**M7-10**
**答案：** 令 $s=\tanh1$，则 $\partial L/\partial w=s^2+s(1-s^2)$，$\partial L/\partial b=s(1-s^2)$，$\partial L/\partial c=s$。所有量均为标量，按矩阵约定可视为 $1\times1$。

前向为 $z_1=1,h=s,z_2=s,L=s^2/2$。反向先得 $\delta_2=s$，再得
\[
\bar h=w\delta_2=s,\qquad \delta_1=\bar h(1-h^2)=s(1-s^2)。
\]
输出层的 $w$ 贡献 $\delta_2h=s^2$，隐藏层的 $w$ 贡献 $\delta_1x=s(1-s^2)$。暂记作独立参数时，这两项分别是 $\partial L/\partial w_2$ 与 $\partial L/\partial w_1$；共享后须相加。两个偏置各只出现一次，故偏导分别为 $\delta_1,\delta_2$。

区分点：逐层得到的是参数在各处的贡献，共享参数的最终梯度须汇总全部贡献。

**M7-11**
**答案：** 三层参数梯度为
\[
\partial W_3=(-1,-1),\ \partial b_3=-1;
\quad \partial W_2=\begin{pmatrix}-2&0\\1&0\end{pmatrix},\ \partial\boldsymbol b_2=(-2,1)^{\mathsf T};
\]
\[
\partial W_1=\begin{pmatrix}-2&2\\0&0\end{pmatrix},\quad \partial\boldsymbol b_1=(-2,0)^{\mathsf T}。
\]

前向得到 $\boldsymbol z_1=(1,-2)^{\mathsf T}$、$\boldsymbol a_1=(1,0)^{\mathsf T}$、$\boldsymbol z_2=\boldsymbol a_2=(1,1)^{\mathsf T}$、$z_3=1$，故 $\delta_3=z_3-2=-1$。第二层掩码为 $(1,1)$，于是 $\boldsymbol\delta_2=W_3^{\mathsf T}\delta_3=(-2,1)^{\mathsf T}$。再算 $W_2^{\mathsf T}\boldsymbol\delta_2=(-2,-3)^{\mathsf T}$，乘第一层掩码 $(1,0)$，得 $\boldsymbol\delta_1=(-2,0)^{\mathsf T}$。每层权重梯度是该层误差信号与该层输入的外积，偏置梯度就是误差信号。

区分点：每向前一层都要先乘下一层权重的转置，再乘当前层的 ReLU 掩码，不能只重复最后一层的公式。

**M7-12**
**答案：** $g\approx0.84755063$，中心差分也约为 $0.84755063$，相对误差小于 $10^{-8}$。前向有 $h_1=\sigma(0.2),h_2=\sigma(0.4)$。损失中的平均系数给出 $\partial L/\partial a_r=a_r/2$，再经过固定系数 $2$ 和 sigmoid，得
\[
g=\sum_{r=1}^2(a_r/2)\cdot2\cdot h_r(1-h_r)x_r
=\sum_{r=1}^2 2h_r^2(1-h_r)x_r。
\]
将同一 $w$ 在两个样本中同时改为 $0.2\pm10^{-5}$，分别算完整的 $L$，代入 $g_{\rm num}=[L(0.2+10^{-5})-L(0.2-10^{-5})]/(2\times10^{-5})$。

相对误差为 $|g-g_{\rm num}|/\max(|g|,|g_{\rm num}|)$，分母取两者绝对值的较大者；两者均为零时分母为零，不作除法，改报绝对误差为零。

区分点：扰动的是一个共享参数，它在所有样本中的使用都要一起更新；解析求导与数值求导必须使用同一个平均损失。

### 章末混合练习

**M7-13**
**答案：** $w'\approx0.4510$、$b'\approx-0.0245$。用 M.2 的二元交叉熵、本章方法 4、5 和 M.1 的梯度下降，先算 $p=\sigma(0.5)\approx0.6225$，再得 $\partial L/\partial w=(p-1)x\approx-0.7551$、$\partial L/\partial b=p-1\approx-0.3775$。两个参数都从旧值减去 $0.2$ 倍的各自梯度。

区分点：先得到分数对参数的梯度，再乘学习率更新，不能直接用 $p$ 当作梯度。

**M7-14**
**答案：** $W_2$ 为 $3\times2$，$\boldsymbol b_2$ 为 $3\times1$，共有 $6+3=9$ 个参数；$\boldsymbol p\approx(0.6652,0.2447,0.0900)^{\mathsf T}$，$\boldsymbol\delta_2\approx(0.6652,-0.7553,0.0900)^{\mathsf T}$。

结合 M.2 的 softmax 交叉熵与本章方法 3、8、10，令 $S=e+1+e^{-1}$，则 $\boldsymbol p=(e/S,1/S,e^{-1}/S)^{\mathsf T}$，$\boldsymbol\delta_2=\boldsymbol p-\boldsymbol y$。外积给出
\[
\frac{\partial L}{\partial W_2}=\boldsymbol\delta_2\boldsymbol h^{\mathsf T}\approx\begin{pmatrix}0.6652&1.3305\\-0.7553&-1.5105\\0.0900&0.1801\end{pmatrix}。
\]

区分点：输出层的误差信号是 $\boldsymbol p-\boldsymbol y$，而不是逐元素把 softmax 导数乘上标签误差。

**M7-15**
**答案：** 合成权重为 $W_3W_2W_1$，偏置为 $W_3W_2\boldsymbol b_1+W_3\boldsymbol b_2+\boldsymbol b_3$。给定数值时 $z=(4,6)\boldsymbol x+9$，指定输入的输出为 $7$；含 ReLU 的 $f$ 不能在全实数范围写成 $ax+b$。

结合矩阵分配律与本章方法 1，先合并前两层，得权重 $(2,3)$、偏置 $5$；第三层再乘 $2$、加 $-1$，得 $(4,6)$ 和 $9$。逐层核对：$\boldsymbol a_1=(0,-1)^{\mathsf T},a_2=4,z=7$，与 $4-6+9=7$ 一致。

对反例，$f(-2)=-1,f(-1)=-1,f(0)=1$。若存在 $ax+b$，前两点给出 $a=0,b=-1$，但第三点要求 $b=1$，矛盾。因此这里的 ReLU 不能被合并进一个仿射表达式。

区分点：每一层的偏置还会被后续权重相乘；含非线性时要用具体反例检验能否合并。
