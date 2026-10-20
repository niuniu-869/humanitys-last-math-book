## L.10 · 正交与最小二乘（题目）

| 题号 | 档 | 方法 |
|---|---|---|
| L10-01 | A | 方法 1 |
| L10-02 | A | 方法 3 |
| L10-03 | A | 方法 4 |
| L10-04 | A | 方法 6 |
| L10-05 | B | 方法 2 |
| L10-06 | B | 方法 2 |
| L10-07 | B | 方法 4 |
| L10-08 | B | 方法 5 |
| L10-09 | B | 方法 6 |
| L10-10 | B | 方法 4 |
| L10-11 | C | 方法 2 |
| L10-12 | C | 方法 3、5 |
| L10-13 | C | 方法 6 |
| L10-14 | 混合 | L.9、方法 2 |
| L10-15 | 混合 | L.8、方法 1 |
| L10-16 | 混合 | L.6、方法 4 |
| L10-17 | 混合 | L.9、方法 2、方法 4 |

### A 基础

**L10-01**〔A｜方法 1 · 考查：用残差正交条件求斜投影〕设
$$\boldsymbol a_1=(1,0,1)^{\mathsf T},\qquad \boldsymbol a_2=(1,1,0)^{\mathsf T},\qquad \boldsymbol b=(1,2,0)^{\mathsf T}.$$
求 $\boldsymbol b$ 在 $S=\operatorname{span}(\boldsymbol a_1,\boldsymbol a_2)$ 上的投影 $\boldsymbol p$、残差 $\boldsymbol e$ 和最小平方和 $\lVert\boldsymbol e\rVert^2$，并验算正交条件。

**L10-02**〔A｜方法 3 · 考查：规范正交方向下逐个投影〕设
$$\boldsymbol q_1=\frac1{\sqrt2}(1,1,0)^{\mathsf T},\qquad \boldsymbol q_2=\frac1{\sqrt6}(1,-1,2)^{\mathsf T},\qquad \boldsymbol b=(2,0,1)^{\mathsf T}.$$
求 $\boldsymbol b$ 在 $\operatorname{span}(\boldsymbol q_1,\boldsymbol q_2)$ 上的投影和残差。

**L10-03**〔A｜方法 4 · 考查：投影矩阵与正交矩阵的区分〕设
$$A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix},\qquad P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}.$$
下列说法正确的是（ ）。

A. 因为 $A^{\mathsf T}A$ 可逆，所以 $P$ 可逆。

B. $P^2=P$ 且 $P^{\mathsf T}=P$。

C. $P=E_3$，因为投影矩阵会把所有向量保持不变。

D. $P$ 是正交矩阵，所以 $P^{-1}=P^{\mathsf T}$。

**L10-04**〔A｜方法 6 · 考查：斜率公式、残差正交和预测〕观测点为 $(0,1),(1,2),(2,2),(3,4)$。用最小二乘直线 $y=C+Dt$ 拟合，求 $C,D$、在 $t=4$ 时的预测值，以及四个残差，并验证残差与设计矩阵的两列正交。

### B 进阶

**L10-05**〔B｜方法 2 · 考查：列不满秩时最小二乘解不唯一〕设
$$A=\begin{pmatrix}1&1\\2&2\\3&3\end{pmatrix},\qquad \boldsymbol b=(1,2,4)^{\mathsf T}.$$
关于正规方程和最小二乘解，下列说法正确的是（ ）。

A. 因为 $A^{\mathsf T}A$ 不可逆，正规方程无解。

B. 正规方程是二元方程，所以最小二乘解唯一。

C. 最小二乘解有无穷多个，但投影 $A\hat{\boldsymbol x}$ 唯一。

D. 可以直接使用 $A(A^{\mathsf T}A)^{-1}A^{\mathsf T}$ 求投影矩阵。

**L10-06**〔B｜方法 2 · 考查：列相关时写出全部参数解并保持投影唯一〕设 $\boldsymbol x_0$ 是正规方程
$$A^{\mathsf T}A\boldsymbol x=A^{\mathsf T}\boldsymbol b$$
的一个解。证明所有正规方程的解恰好是 $\boldsymbol x_0+N(A)$，并说明这些解给出的 $A\boldsymbol x$ 都相同。证明中先用讲义的三步秩比较说明 $\boldsymbol x_0$ 存在，再完成上述两点。

**L10-07**〔B｜方法 4 · 考查：正交矩阵的必要条件与错误逆命题〕设 $Q$ 是三阶正交矩阵且 $|Q|=-1$。下列说法中必然正确的是（ ）。

A. $Q^{\mathsf T}Q=E$ 且 $|Q|=-1$。

B. $Q+E$ 一定也是正交矩阵。

C. $|Q|=-1$ 本身就足以推出 $Q$ 是正交矩阵。

D. 对任意 $\boldsymbol x$ 都有 $Q\boldsymbol x=\boldsymbol x$。

**L10-08**〔B｜方法 5 · 考查：施密特正交化必须减去已正交化方向的投影〕对
$$\boldsymbol a_1=(1,1,0)^{\mathsf T},\quad \boldsymbol a_2=(1,0,1)^{\mathsf T},\quad \boldsymbol a_3=(0,1,1)^{\mathsf T}$$
做施密特正交化，并写出一组规范正交基。有人把第三步写成“从 $\boldsymbol a_3$ 中减去它在原来的 $\boldsymbol a_1,\boldsymbol a_2$ 上的投影”，请算出这个向量并说明它为什么不能代替正确的第三步；最后验算正确的第三个中间向量与前两个都正交。

**L10-09**〔B｜方法 6 · 考查：三列设计矩阵的正规方程和对称性〕对数据
$$(-2,4),\ (-1,1),\ (0,0),\ (1,2),\ (2,5),$$
用模型 $y=C+Dt+Et^2$ 做最小二乘拟合，求 $C,D,E$，并验证残差分别与 $1,t,t^2$ 的内积为零。

**L10-10**〔B｜方法 4 · 考查：Householder 型矩阵的对称正交性〕设 $\boldsymbol\alpha\in\mathbb R^n$ 且 $\lVert\boldsymbol\alpha\rVert=1$，令
$$H=E-2\boldsymbol\alpha\boldsymbol\alpha^{\mathsf T}.$$
证明 $H^{\mathsf T}=H$、$H^{\mathsf T}H=E$，并说明 $H$ 对任意向量保持长度。

### C 提高

**L10-11**〔C｜方法 2 · 考查：列相关时写出全部最小二乘解并找唯一投影〕设
$$A=\begin{pmatrix}1&2\\2&4\\3&6\end{pmatrix},\qquad \boldsymbol b=(1,0,1)^{\mathsf T}.$$
求全部最小二乘解、唯一投影、残差和最小平方和，并说明为什么不能套用含 $(A^{\mathsf T}A)^{-1}$ 的投影矩阵公式。

拆法：先做 L10-05、L10-06。

**L10-12**〔C｜方法 3、5 · 考查：三步施密特正交化后直接投影〕对
$$\boldsymbol a_1=(1,1,0,0)^{\mathsf T},\quad \boldsymbol a_2=(1,0,1,0)^{\mathsf T},\quad \boldsymbol a_3=(1,0,0,1)^{\mathsf T},$$
求由它们得到的一组规范正交基，并求 $\boldsymbol b=(1,2,3,4)^{\mathsf T}$ 在其张成空间上的投影和残差。

拆法：先做 L10-08、L10-02。

**L10-13**〔C｜方法 6 · 考查：比较学习率、正规方程和一步下降范围〕对数据点 $(-1,2),(0,0),(1,3)$，模型为 $y=C+Dt$。从 $(C_0,D_0)=(0,0)$ 出发，分别取学习率 $\eta=0.1$ 和 $\eta=0.05$，各手算一步并比较平方和；再求精确最小二乘解和最小平方和，并求使一步后的平方和严格小于初始平方和的 $\eta>0$ 范围。

拆法：先做 L10-04、L10-09。

### 章末混合练习

**L10-14**〔B〕设
$$A=\begin{pmatrix}1&0\\1&1\\2&1\end{pmatrix},\qquad \boldsymbol b=(1,2,0)^{\mathsf T}.$$
先求 $r(A)$，再用正规方程求最小二乘解、投影和残差，并验证 $r(A^{\mathsf T}A)=r(A)$。（答案中标明所用方法及 L.9 知识点。）

**L10-15**〔B〕已知 $S^{\perp}=\operatorname{span}\{(1,-1,1)^{\mathsf T}\}$，且 $\boldsymbol b=(2,1,0)^{\mathsf T}$。求 $\boldsymbol b$ 在 $S$ 上的投影 $\boldsymbol p$、残差 $\boldsymbol e$ 和到 $S$ 的距离，并由 $\boldsymbol p\perp S^{\perp}$ 验证 $\boldsymbol p\in S$。（答案中标明所用方法及 L.8 知识点。）

**L10-16**〔A〕设 $Q$ 是二阶正交矩阵，第一列为 $(5/13,12/13)^{\mathsf T}$。求所有可能的第二列，并分别求 $|Q|$。（答案中标明所用方法及 L.6 知识点。）

**L10-17**〔C〕设 $A\in\mathbb R^{3\times2}$ 的两列线性无关，且
$$P=A(A^{\mathsf T}A)^{-1}A^{\mathsf T}.$$
证明 $P^2=P$、$P^{\mathsf T}=P$、$r(P)=2$，并说明 $P$ 为什么不是正交矩阵。（答案中标明所用方法及 L.9 知识点。）
