## L.10 · 正交与最小二乘（答案）

**L10-01**
**答案：** $\boldsymbol p=(4/3,5/3,-1/3)^{\mathsf T}$，$\boldsymbol e=(-1/3,1/3,1/3)^{\mathsf T}$，$\lVert\boldsymbol e\rVert^2=1/3$。
设 $\boldsymbol p=x_1\boldsymbol a_1+x_2\boldsymbol a_2$。由 $\boldsymbol e\cdot\boldsymbol a_i=0$ 得 $2x_1+x_2=1$、$x_1+2x_2=3$，故 $x_1=-1/3,x_2=5/3$。验算 $\boldsymbol e\cdot\boldsymbol a_1=0$、$\boldsymbol e\cdot\boldsymbol a_2=0$。
区分点：不能把不正交方向的投影分别相加，必须同时解两个正交条件。

**L10-02**
**答案：** $\boldsymbol p=(5/3,1/3,4/3)^{\mathsf T}$，$\boldsymbol e=(1/3,-1/3,-1/3)^{\mathsf T}$。
两向量已规范正交，故系数是点积：$\boldsymbol q_1\cdot\boldsymbol b=\sqrt2$，$\boldsymbol q_2\cdot\boldsymbol b=4/\sqrt6$。于是 $\boldsymbol p=\sqrt2\boldsymbol q_1+(4/\sqrt6)\boldsymbol q_2$，相减得残差。
区分点：先验证正交和单位长度，才可把系数直接写成点积。

**L10-03**
**答案：** 选 B。$A$ 列满秩，所以 $P$ 是对称幂等矩阵。A 错在投影矩阵通常不可逆；C 错在 $r(P)=2<3$，不是 $E_3$；D 把投影矩阵和正交矩阵混淆，$P$ 不可逆。
区分点：$P^2=P$ 不等于 $P^{-1}$ 存在，更不等于 $P$ 是正交矩阵。

**L10-04**
**答案：** $C=0.9,D=0.9$，预测值为 $4.5$；残差按题目顺序为 $(0.1,0.2,-0.7,0.4)^{\mathsf T}$。
$\bar t=1.5,\bar y=2.25$，斜率 $D=4.5/5=0.9$，所以 $C=\bar y-D\bar t=0.9$。残差和为 $0$，且 $\sum t_ie_i=0+0.2-1.4+1.2=0$。
区分点：残差是竖直误差，正交条件对应设计矩阵的两列，而不是把点到直线的几何垂距代入。

**L10-05**
**答案：** 选 C。两列相关，$A^{\mathsf T}A$ 奇异，但正规方程仍有解；所有解满足 $x_1+x_2=17/14$，所以解不唯一而投影唯一。A 把奇异误判为无解；B 把方程个数当成唯一性的保证；D 的逆矩阵不存在。
区分点：要区分“正规方程有解”“参数解唯一”和“投影唯一”三个层次。

**L10-06**
**答案：** 先按讲义的三步秩比较得 $r(A^{\mathsf T}A)=r(A^{\mathsf T}A\mid A^{\mathsf T}\boldsymbol b)$，所以正规方程有解。若 $\boldsymbol x$ 也是解，则
$$A^{\mathsf T}A(\boldsymbol x-\boldsymbol x_0)=\boldsymbol0.$$
由 $N(A^{\mathsf T}A)=N(A)$，得 $\boldsymbol x-\boldsymbol x_0\in N(A)$；反过来，若 $\boldsymbol n\in N(A)$，则 $A^{\mathsf T}A(\boldsymbol x_0+\boldsymbol n)=A^{\mathsf T}\boldsymbol b$。因此全部解是 $\boldsymbol x_0+N(A)$，且 $A(\boldsymbol x_0+\boldsymbol n)=A\boldsymbol x_0$，投影唯一。
区分点：要把正规方程的零空间识别成 $N(A)$，才能同时说明参数解的全体形式和投影不变。

**L10-07**
**答案：** 选 A。正交矩阵定义就是 $Q^{\mathsf T}Q=E$，题设另给 $|Q|=-1$。B 无必然性；C 只有行列式条件远不足以保证列正交，错切矩阵就是反例；D 只有 $Q=E$ 才对所有向量不变，与行列式为 $-1$ 矛盾。
区分点：$|Q|=\pm1$ 是正交矩阵的必要条件，不是充分条件。

**L10-08**
**答案：** $\boldsymbol b_1=(1,1,0)^{\mathsf T}$，$\boldsymbol b_2=(1,-1,2)^{\mathsf T}$，$\boldsymbol b_3=(-1,1,1)^{\mathsf T}$，所以
$$\boldsymbol q_1=\frac{\boldsymbol b_1}{\sqrt2},\quad\boldsymbol q_2=\frac{\boldsymbol b_2}{\sqrt6},\quad\boldsymbol q_3=\frac{\boldsymbol b_3}{\sqrt3}.$$
若直接从 $\boldsymbol a_3$ 减去它在原 $\boldsymbol a_1,\boldsymbol a_2$ 上的投影，得到 $\boldsymbol a_3-\frac12\boldsymbol a_1-\frac12\boldsymbol a_2=(-1,\frac12,\frac12)^{\mathsf T}$，它与 $\boldsymbol b_1$、$\boldsymbol b_2$ 的点积分别为 $-\frac12$、$-\frac12$，不垂直，所以不能代替正确步骤。正确的 $\boldsymbol b_3$ 与前两者点积都为 0。
区分点：第二个投影必须落在已经正交化的方向上，不能直接对原向量逐个投影。

**L10-09**
**答案：** $C=9/35,D=3/10,E=15/14$。预测值为
$$(138/35,36/35,9/35,57/35,36/7)^{\mathsf T},$$
残差为
$$(2/35,-1/35,-9/35,13/35,-1/7)^{\mathsf T},$$
平方和为 $8/35$，并且残差分别与 $1,t,t^2$ 的内积都为 0。
区分点：对称取值只让部分交叉项消失，仍须解正规方程并核对三个正交条件。

**L10-10**
**答案：** $H^{\mathsf T}=E-2\boldsymbol\alpha\boldsymbol\alpha^{\mathsf T}=H$。展开得
$$H^{\mathsf T}H=(E-2\alpha\alpha^{\mathsf T})^2=E-4\alpha\alpha^{\mathsf T}+4\alpha(\alpha^{\mathsf T}\alpha)\alpha^{\mathsf T}=E,$$
因为 $\alpha^{\mathsf T}\alpha=1$。所以 $H$ 正交，且 $\lVert H\boldsymbol x\rVert^2=\boldsymbol x^{\mathsf T}H^{\mathsf T}H\boldsymbol x=\lVert\boldsymbol x\rVert^2$。
区分点：最后一项要用单位长度条件把 $(\alpha^{\mathsf T}\alpha)$ 化成 1；只证明对称还不能推出正交。

**L10-11**
**答案：** 令 $z=x_1+2x_2$，则 $A\boldsymbol x=z(1,2,3)^{\mathsf T}$。最小化 $\|(z,2z,3z)^{\mathsf T}-\boldsymbol b\|^2$ 得 $z=(1+0+3)/14=2/7$。故全部解为 $x_1+2x_2=2/7$；可写成 $\boldsymbol x=(2/7-2s,s)^{\mathsf T}$。投影 $\boldsymbol p=(2/7,4/7,6/7)^{\mathsf T}$，残差 $\boldsymbol e=(5/7,-4/7,1/7)^{\mathsf T}$，最小平方和 $6/7$。两列相关使 $A^{\mathsf T}A$ 不可逆，不能套逆矩阵公式。
区分点：最小二乘参数可不唯一，但列空间中的最近点仍唯一；先降为一个方向的系数最稳妥。

**L10-12**
**答案：** 施密特正交化可取
$$\boldsymbol b_1=(1,1,0,0),\quad \boldsymbol b_2=(1,-1,2,0),\quad \boldsymbol b_3=(1,-1,-1,3),$$
其长度平方为 $2,6,12$，故规范正交基为 $\boldsymbol b_1/\sqrt2,\boldsymbol b_2/\sqrt6,\boldsymbol b_3/\sqrt{12}$。逐方向投影得 $\boldsymbol p=(3,0,1,2)^{\mathsf T}$，$\boldsymbol e=(-2,2,2,2)^{\mathsf T}$。
区分点：先把原向量正交化，再用逐方向投影；不能把原向量的投影直接相加。

**L10-13**
**答案：** 初始梯度为 $(-10,-2)^{\mathsf T}$。取 $\eta=0.1$ 得 $\boldsymbol x_1=(1,1/5)^{\mathsf T}$，平方和为 $142/25$；取 $\eta=0.05$ 得 $\boldsymbol x_1=(1/2,1/10)^{\mathsf T}$，平方和为 $857/100$。正规方程给出精确解 $(5/3,1/2)^{\mathsf T}$，最小平方和为 $25/6$。
一步后的平方和为 $308\eta^2-104\eta+13$，所以严格小于初始值 $13$ 当且仅当 $0<\eta<26/77$。
区分点：学习率决定一步下降的幅度，有限步结果不是闭式最小二乘解；还要由二次式判断可下降的范围。

**L10-14**
**答案：** 两列为 $(1,1,2)^{\mathsf T}$、$(0,1,1)^{\mathsf T}$，线性无关，所以 $r(A)=2$。$A^{\mathsf T}A=\begin{pmatrix}6&3\\3&2\end{pmatrix}$，$A^{\mathsf T}\boldsymbol b=(3,2)^{\mathsf T}$，解得 $\hat{\boldsymbol x}=(0,1)^{\mathsf T}$。因此 $\boldsymbol p=(0,1,1)^{\mathsf T}$，$\boldsymbol e=(1,1,-1)^{\mathsf T}$，且 $r(A^{\mathsf T}A)=2=r(A)$。
区分点：先判列秩，再用正规方程判断参数是否唯一。

**L10-15**
**答案：** 令 $\boldsymbol n=(1,-1,1)^{\mathsf T}$。残差必须是 $\boldsymbol e=\lambda\boldsymbol n$，又 $\boldsymbol p=\boldsymbol b-\boldsymbol e\perp\boldsymbol n$，所以 $\lambda=(\boldsymbol b\cdot\boldsymbol n)/(\boldsymbol n\cdot\boldsymbol n)=1/3$。故
$$\boldsymbol e=(1/3,-1/3,1/3)^{\mathsf T},\quad \boldsymbol p=(5/3,4/3,-1/3)^{\mathsf T},\quad d(\boldsymbol b,S)=1/\sqrt3.$$ 
并且 $\boldsymbol p\cdot\boldsymbol n=0$，所以 $\boldsymbol p\in S$。
区分点：已知正交补时先沿法向确定残差，再由 $\boldsymbol b-\boldsymbol e$ 反求投影。

**L10-16**
**答案：** 这是 L.6 与方法 4。第二列必须是第一列的单位正交向量，只有
$$\boldsymbol q_2=(-12/13,5/13)^{\mathsf T}\quad\text{或}\quad(12/13,-5/13)^{\mathsf T}.$$
对应的矩阵行列式分别为 $1$ 和 $-1$。
区分点：只用单位长度条件会得到整条圆，正交条件才把方向限制到两个候选。

**L10-17**
**答案：** 这是 L.9 的秩知识和方法 2、4。由列满秩，$A^{\mathsf T}A$ 可逆。于是
$$P^2=A(A^{\mathsf T}A)^{-1}(A^{\mathsf T}A)(A^{\mathsf T}A)^{-1}A^{\mathsf T}=P,$$
转置可得 $P^{\mathsf T}=P$。又 $\operatorname{im}P=C(A)$，且对列空间中的向量 $P$ 保持不变，所以 $r(P)=\dim C(A)=2$。因此 $P$ 不可逆，而正交矩阵必须可逆，故 $P$ 不是正交矩阵。
区分点：幂等、对称是投影矩阵性质；正交矩阵还必须可逆，不能把两类矩阵混为一谈。
