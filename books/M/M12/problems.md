## M.12 · Transformer 的积木：多头、前馈层、LayerNorm、位置编码（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| M12-01 | A | 方法 1（选择） |
| M12-02 | A | 方法 3 |
| M12-03 | A | 方法 4（选择） |
| M12-04 | A | 方法 6 |
| M12-05 | B | 方法 2 |
| M12-06 | B | 方法 1 |
| M12-07 | B | 方法 3（选择） |
| M12-08 | B | 方法 3 |
| M12-09 | B | 方法 5 |
| M12-10 | B | 方法 8 |
| M12-11 | C | 方法 4（证明） |
| M12-12 | C | 方法 3、6 |
| M12-13 | B | 混合（答案里标） |
| M12-14 | B | 混合（答案里标） |
| M12-15 | C | 混合（答案里标） |

### A 基础

**M12-01**〔A｜方法 1 · 考查：分头不复制总维数〕（选择）设 $X\in\mathbb R^{4\times6}$，按讲义的方法分成 $h=3$ 个头，且 $d_k=d/h$。不计偏置，下列说法正确的是（　）。

(A) 每个头的 $Q$ 都有 $4\times6$ 个元素。

(B) 三个头的注意力权重合起来只有 $4\times4$ 个元素。

(C) 包含 $W_O$ 的全部投影矩阵共有 144 个参数。

(D) 把头数改为 6，总维数仍为 6，投影参数就增加为原来的两倍。

**M12-02**〔A｜方法 3 · 考查：保留稳定项与仿射变换〕对 $\boldsymbol x=(1,3)$，取 $\varepsilon=3$、$\boldsymbol\gamma=(2,1)$、$\boldsymbol\beta=(1,-1)$。求 $\mathrm{LN}(\boldsymbol x)$，并求乘 $\boldsymbol\gamma$、加 $\boldsymbol\beta$ 之前的标准化向量的方差。

**M12-03**〔A｜方法 4 · 考查：成对编码的频率与长度〕（选择）设 $\boldsymbol p_p$ 是 $d=4$ 的正弦位置编码。下列说法正确的是（　）。

(A) $\boldsymbol p_0=(0,0,0,0)$。

(B) 对每个实数 $p$，都有 $\lVert\boldsymbol p_p\rVert=1$。

(C) 两对分量的频率分别为 $1$ 和 $1/10000$。

(D) 对每个实数 $p$，都有 $\lVert\boldsymbol p_p\rVert=\sqrt2$。

**M12-04**〔A｜方法 6 · 考查：残差主干上的归一化位置〕设 $F(\boldsymbol z)\equiv(0,0)$，$\boldsymbol x=(1,5)$，LN 取 $\boldsymbol\gamma=\boldsymbol1$、$\boldsymbol\beta=\boldsymbol0$、$\varepsilon=0$。分别求 $\boldsymbol x+F(\mathrm{LN}(\boldsymbol x))$ 和 $\mathrm{LN}(\boldsymbol x+F(\boldsymbol x))$。哪一个等于原输入？

### B 进阶

**M12-05**〔B｜方法 2 · 考查：激活区间与输出中的抵消〕设

$$F(\boldsymbol x)=\mathrm{ReLU}(\boldsymbol xW_1+\boldsymbol b_1)W_2,\quad
W_1=\begin{pmatrix}1&-1&0\\0&0&1\end{pmatrix},\quad
\boldsymbol b_1=(-1,1,0),\quad
W_2=\begin{pmatrix}1&0\\-1&0\\0&1\end{pmatrix}.$$

对 $\boldsymbol x=(t,1)$，分别写出 $t<1$、$t=1$、$t>1$ 时的隐藏向量，并把输出化成一个对所有实数 $t$ 都成立的式子。求使 $F(t,1)=(0,1)$ 的全部 $t$。隐藏向量的表达式分段，是否意味着输出也不能合并成一个仿射式？

**M12-06**〔B｜方法 1 · 考查：不同权重模式能否合并〕给出两个头已经除以 $\sqrt{d_k}$ 的分数矩阵，以及值矩阵：

$$S_1=\begin{pmatrix}0&\ln3\\0&-\ln3\end{pmatrix},\quad S_2=\begin{pmatrix}0&0\\0&0\end{pmatrix},\quad
V_1=\begin{pmatrix}0\\4\end{pmatrix},\quad V_2=\begin{pmatrix}2\\0\end{pmatrix}.$$

逐行做 softmax 得 $A_1,A_2$，令 $W_O=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求 $Y=\mathrm{concat}(A_1V_1,A_2V_2)W_O$。是否存在同一个每行非负且行和为 1 的矩阵 $A$，使 $\mathrm{concat}(AV_1,AV_2)W_O=Y$？用第一行说明理由。

**M12-07**〔B｜方法 3 · 考查：统计轴与同批其他行的影响〕（选择）设

$$X=\begin{pmatrix}0&2\\2&4\\4&6\end{pmatrix},\qquad
\widetilde X=\begin{pmatrix}0&2\\2&4\\8&10\end{pmatrix}.$$

LN 按行计算，BN 用这三行的当前批统计量按列计算，RMSNorm 按行计算；均取缩放参数为 1、平移参数为 0、$\varepsilon=0$。比较两个矩阵的第一行输出，下列说法正确的是（　）。

(A) 因为第三行变了，所以 LN 的第一行输出也变了。

(B) 因为第一行没变，所以 BN 的第一行输出不变。

(C) 对 $X$，RMSNorm 与 LN 的第一行输出相同，因为两者都除以某种标准差。

(D) LN 的第一行输出不变，但 BN 的第一行输出改变了。

**M12-08**〔B｜方法 3 · 考查：缩放不变性的适用条件〕取 $\boldsymbol\gamma=\boldsymbol1$、$\boldsymbol\beta=\boldsymbol0$、$\varepsilon=3$。有人说：“只要 $a>0$，LN 就会把 $(-a,a)$ 和 $(-1,1)$ 变成同一个向量。”这个说法在本题 $\varepsilon=3$ 时成立吗？为什么？求所有满足

$$\mathrm{LN}(b-a,b+a)=\mathrm{LN}(-1,1),\qquad a>0$$

的实数对 $(a,b)$，并说明整体平移是否仍能抵消。

**M12-09**〔B｜方法 5 · 考查：相同位置差与不同内容〕对四维列向量，把前两分量和后两分量分别作为一对。在位置 $p$，两对分别乘旋转矩阵 $R(p\pi/2)$、$R(p\pi/4)$，把这样得到的向量记为 $\mathcal R_p\boldsymbol v$。这里 $R$ 与讲义的旋转矩阵相同，频率取本题给定值。设

$$\boldsymbol q=(1,0,1,0)^{\mathsf T},\quad
\boldsymbol k=(1,0,0,1)^{\mathsf T},\quad
\widetilde{\boldsymbol k}=(1,0,1,0)^{\mathsf T}.$$

记未除以 $\sqrt4$ 的点积分数为 $s(m,n;\boldsymbol v)=(\mathcal R_m\boldsymbol q)^{\mathsf T}(\mathcal R_n\boldsymbol v)$。

1. 对位置对 $(1,3)$ 与 $(4,6)$，分别写出两对分量的相对旋转角，并求 $s(1,3;\boldsymbol k)$、$s(4,6;\boldsymbol k)$。
2. 第二个位置对改用 $\widetilde{\boldsymbol k}$，求 $s(4,6;\widetilde{\boldsymbol k})$。比较 $\boldsymbol k$ 与 $\widetilde{\boldsymbol k}$ 的长度；说明“位置差相同且内容向量长度不变，分数就相同”是否成立，以及位置差相同究竟保证什么不变。

**M12-10**〔B｜方法 8 · 考查：按结构计数后反推预算〕一个模型有 $L=2$ 个块，$d=8$、$d_{\mathrm{ff}}=16$，词表大小为 10。每块注意力有四个 $8\times8$ 矩阵，门控前馈层有两个 $8\times16$ 矩阵和一个 $16\times8$ 矩阵。输入嵌入与输出矩阵不共享。不计偏置和归一化参数。

求参数量 $N$。有人用 $12Ld^2+|\mathcal V|d$ 得到 1616，指出其计算与本题结构不符的两处。若训练计算预算为 $864000$ 次运算，按 $C\approx6ND$ 最多能处理多少个词元？其中前向与反向各占多少次运算？

### C 提高

**M12-11**〔C｜方法 4 · 考查：相对位移的线性表示〕（证明）对 $d=4$，把编码写成列向量

$$\boldsymbol p_p=(\sin p,\cos p,\sin(p/100),\cos(p/100))^{\mathsf T}.$$

写出只依赖实数 $k$ 的 $4\times4$ 矩阵 $T(k)$，并用两角和公式证明 $\boldsymbol p_{p+k}=T(k)\boldsymbol p_p$。再证明

$$\boldsymbol p_p^{\mathsf T}\boldsymbol p_{p+k}=\cos k+\cos(k/100),$$

从而说明两编码的点积只依赖间隔。拆法：先做 M12-03、M12-09。

**M12-12**〔C｜方法 3、6 · 考查：第二次归一化与分段求解〕设 $\boldsymbol x=(t,0)$，$t>0$，LN 取 $\boldsymbol\gamma=\boldsymbol1$、$\boldsymbol\beta=\boldsymbol0$、$\varepsilon=0$。定义

$$F(z_1,z_2)=(z_2,z_1),\qquad G(z_1,z_2)=(\max(z_1,0),\max(z_2,0)),$$
$$\boldsymbol x'=\boldsymbol x+F(\mathrm{LN}(\boldsymbol x)),\qquad
\boldsymbol y=\boldsymbol x'+G(\mathrm{LN}(\boldsymbol x')).$$

求这个映射有定义时的全部 $t$，并分段写出 $\boldsymbol y$。再求使 $y_1+y_2=4$ 的全部 $t$。拆法：先做 M12-02、M12-04、M12-05。

### 章末混合练习

**M12-13**〔B · 考查：置换结论与固定因果掩码〕设 $X=(0,2)^{\mathsf T}$，$Q=K=0$，$V=X$，$P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$。定义 $U(X)$ 为不加掩码的注意力输出，$C(X)$ 为加固定因果掩码的输出：第 1 行只能看第 1 行，第 2 行可以看两行。交换输入后掩码规则不变。分别求 $U(X),U(PX),C(X),C(PX)$，判断 $U(PX)=PU(X)$ 和 $C(PX)=PC(X)$ 是否成立。

**M12-14**〔B · 考查：由概率比反求分数〕设

$$E=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix},\quad
\boldsymbol u=(t,-t),\quad \boldsymbol z=\boldsymbol uE^{\mathsf T},\quad
\boldsymbol p=\mathrm{softmax}(\boldsymbol z).$$

已知 $p_1/p_2=4$，求 $t$、完整的概率向量及 $-\ln p_3$。若三个分数都加上同一个实数 $c$，上述概率与 $-\ln p_3$ 是否改变？

**M12-15**〔C · 考查：嵌入、最后的归一化与目标错位〕一个简化模型的共享嵌入矩阵为

$$E=\begin{pmatrix}2&0\\0&2\\0&0\end{pmatrix}.$$

训练序列的词元编号依次为 $1,2,3$。只对前两个位置计算预测，它们的位置编号为 $0,1$，分别加上 $d=2$ 的正弦位置编码。所有 Pre-LN 块的两个修正子层恒为零；块后仍有最后一次 LN，取 $\boldsymbol\gamma=\boldsymbol1$、$\boldsymbol\beta=\boldsymbol0$、$\varepsilon=0$。求加位置编码后的矩阵 $X_0$、最后的隐藏矩阵 $H$、分数矩阵 $Z=HE^{\mathsf T}$，以及两次预测的平均交叉熵。若误把每行的目标设成该行输入词元，平均损失会是多少？两者相差多少？拆法：先做 M12-04、M12-14。
