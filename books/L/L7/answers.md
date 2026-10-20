## L.7 · 线性相关与秩（答案）

### A 基础

**L7-01**
**答案：** 线性相关，且 $\boldsymbol a_1+\boldsymbol a_2-\boldsymbol a_3=\boldsymbol0$。把三列排成矩阵后，第三列就是前两列之和，所以主元只有 2 个，少于向量个数 3。

区分点：要先把向量关系写成齐次组合，不能只说“第三个看起来像前两个相加”。

**L7-02**
**答案：** $r(A)=3$。行变换得 $\begin{pmatrix}1&2&0&1\\0&0&1&1\\0&1&1&1\end{pmatrix}$，再交换后两行可见有 3 个主元。左上角两行两列的子式 $\begin{vmatrix}1&2\\2&4\end{vmatrix}=0$ 不合适，但取第 1、2 行和第 1、3 列得 $\begin{vmatrix}1&0\\2&1\end{vmatrix}=1\ne0$。

区分点：秩由非零行数决定，找子式时还要选到真正非零的行列交叉部分。

**L7-03**
**答案：** (B)。由“无关组添一个向量后相关”的性质，$\boldsymbol\beta$ 能由 $\boldsymbol\alpha_1,\boldsymbol\alpha_2$ 表示，而且表示唯一。(A) 没有相应的无关前提；(C) 相关不等于含零向量；(D) 三个向量相关只说明整体有关系，不说明任意两个都相关。

区分点：记住唯一表示的方向是“新添的向量由原无关组表示”，不能任意交换角色。

**L7-04**
**答案：** $r(\boldsymbol u\boldsymbol v^{\mathsf T}+\boldsymbol w\boldsymbol z^{\mathsf T})=2$。把矩阵写成
\[
\begin{pmatrix}\boldsymbol u&\boldsymbol w\end{pmatrix}\begin{pmatrix}\boldsymbol v^{\mathsf T}\\\boldsymbol z^{\mathsf T}\end{pmatrix}.
\]
两边的两个向量都分别线性无关，所以两个因子秩都是 2，乘积秩至多为 2；直接算得左上二阶子式为 $-1\ne0$，故秩恰为 2。

区分点：两个秩一矩阵相加的秩不一定仍为 1，要先找上界，再用低阶子式给下界。
### B 进阶

**L7-05**
**答案：** 由定义直接算出
\[
\boldsymbol\beta_1+\boldsymbol\beta_2-\boldsymbol\beta_3=\boldsymbol0。
\]
因此三个向量线性相关，非零系数为 $(1,1,-1)$。

区分点：先逐项展开，识别出 $\boldsymbol\beta_3=\boldsymbol\beta_1+\boldsymbol\beta_2$，再写成齐次关系。
**L7-06**
**答案：** 系数矩阵按列写为
\[
K=\begin{pmatrix}1&0&1&2\\1&1&0&1\\0&1&1&1\end{pmatrix}.
\]
因为 $K$ 有 4 列而只有 3 行，所以 $K\boldsymbol x=\boldsymbol0$ 有非零解。直接看列关系得第 4 列等于第 1、3 列之和，因此全部关系为
\[
\boldsymbol x=s(1,0,1,-1)^{\mathsf T},
\]
其中 $s$ 任意；$s\ne0$ 时给出非零关系。

区分点：非方阵不能算行列式，要用未知数多于方程数或直接求零空间。
**L7-07**
**答案：** (B)。只做初等行变换不改变各列之间的线性关系，因此阶梯形的主元位置要对应回原矩阵的同号列。(A) 列变换会改变列的对应关系；(C) 非零行属于行向量，不是原列向量；(D) 非零行数只给秩，不能保证任取的原向量无关。

区分点：方法 5 的“主元列”指原矩阵的列，不能把变换后的新列直接抄回去。

**L7-08**
**答案：** $\boldsymbol a_3=\boldsymbol a_1+\boldsymbol a_2$。而
\[
\det(\boldsymbol a_1,\boldsymbol a_2,\boldsymbol a_4)=t-3.
\]
所以 $t\ne3$ 时，$\boldsymbol a_1,\boldsymbol a_2,\boldsymbol a_4$ 是极大无关组；$t=3$ 时秩为 2，可取 $\boldsymbol a_1,\boldsymbol a_2$，并有 $\boldsymbol a_4=\boldsymbol a_1+2\boldsymbol a_2$。

区分点：固定的 $\boldsymbol a_3$ 已经多余，参数只决定第四个向量是否离开原来的平面。
**L7-09**
**答案：** $|A(t)|=t(t-1)^2$。当 $t\ne0,1$ 时秩为 3；$t=0$ 时第二、三列相同，且有非零二阶子式，秩为 2；$t=1$ 时三行都为 $(1,1,1)$，秩为 1。

区分点：行列式为零后还要逐个代回，才能区分秩为 1 还是 2。
**L7-10**
**答案：** (A)。同型矩阵秩相等当且仅当矩阵等价。(B) 向量组秩相等不保证互相表示；(C) 矩阵等价只要求存在可逆的左右乘变换，不要求对应列互相表示；(D) 向量组互相表示还要实际给出系数关系。

区分点：矩阵等价只看同型与秩，向量组等价还要看张成关系，二者不能混用。

### C 提高

**L7-11**
**答案：** 前三个向量满足 $\boldsymbol a_3=\boldsymbol a_1+\boldsymbol a_2$，所以它们的秩为 2。又 $\boldsymbol a_4$ 在前两向量张成的平面上当且仅当其第三分量等于前两分量之和，即 $t=3$。
当 $t=3$ 时，秩为 2，取 $\boldsymbol a_1,\boldsymbol a_2$ 为极大无关组，并有 $\boldsymbol a_3=\boldsymbol a_1+\boldsymbol a_2$、$\boldsymbol a_4=\boldsymbol a_1+2\boldsymbol a_2$。当 $t\ne3$ 时，前三列中取 $\boldsymbol a_1,\boldsymbol a_2,\boldsymbol a_4$，其行列式为 $t-3\ne0$，故秩为 3。

区分点：先识别固定的相关关系，再用参数判断第四个向量是否离开原平面；不能只看向量个数。

**L7-12**
**答案：** $A(t)$ 的两行不成比例，且取前两列的二阶子式 $\begin{vmatrix}1&t\\0&1\end{vmatrix}=1$，所以 $r(A(t))=2$ 对所有 $t$ 成立。$B$ 是上三角矩阵且对角线全为 1，因此可逆；右乘可逆矩阵不改变秩，所以 $r(A(t)B)=2$。

区分点：非方阵没有行列式可用，要先找非零低阶子式，再利用可逆因子保持秩。
**L7-13**
**答案：** 该矩阵就是两个秩至多为 1 的外积之和：
\[
\Delta(t)=(1,0,1)^{\mathsf T}(1,1,0)+(0,1,1)^{\mathsf T}(t,0,t),
\]
所以 $r(\Delta)\le2$。当 $t=0$ 时秩为 1；当 $t\ne0$ 时左上二阶子式为 $-t\ne0$，故秩为 2。

区分点：和的秩不等式只给上界，还要用子式排除秩 1。
### 章末混合练习

**L7-14**
**答案：** 令 $x\boldsymbol b_1+y\boldsymbol b_2=\boldsymbol0$，比较 $\boldsymbol a_1,\boldsymbol a_2$ 的系数得 $x+2y=0$、$x-y=0$，故 $x=y=0$，所以 $\boldsymbol b_1,\boldsymbol b_2$ 无关。求 $\boldsymbol a_1=x\boldsymbol b_1+y\boldsymbol b_2$ 时得 $x+2y=1$、$x-y=0$，从而 $x=y=\frac13$，即 $\boldsymbol a_1=\frac13(\boldsymbol b_1+\boldsymbol b_2)$。（方法 2、方法 4）

区分点：没有坐标时要依靠已知无关组比较系数，而不是凭图形猜共线。

**L7-15**
**答案：** 与 L7-09 同样先算 $|C(t)|=t(t-1)^2$。因此 $t\ne0,1$ 时秩为 3；$t=0$ 时秩为 2，二阶子式取前两行前两列为 $-1$；$t=1$ 时秩为 1。

区分点：同一个行列式根可能对应不同的秩，必须检查特殊矩阵本身。
**L7-16**
**答案：** 总有 $r(PA+PAP^{-1})\le2$，因为
\[
PA+PAP^{-1}=P(A+AP^{-1})=P A(I+P^{-1}),
\]
左、右乘可逆矩阵不增加秩，而 $r(A)=2$。等号可以取
\[
P=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix},\quad A=\begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix},
\]
此时
\[
PA+PAP^{-1}=\begin{pmatrix}2&1&0\\0&2&-1\\0&0&0\end{pmatrix},
\]
所以秩为 $2$，正好取到上界。

区分点：先把两项提取成 $PA(I+P^{-1})$，再用秩不增加的性质得到紧上界，并验证可以取到。
**L7-17**
**答案：** 设 $\boldsymbol x=(x_1,x_2,x_3,x_4)^{\mathsf T}$。方程组给出 $x_1=-x_3-2x_4$、$x_2=-x_3-x_4$，所以
\[
\boldsymbol x=s(-1,-1,1,0)^{\mathsf T}+q(-2,-1,0,1)^{\mathsf T}.
\]
秩为 2。除 $s=q=0$ 外的每个解都给出一个非零线性关系，因而全部关系由
\[
-\boldsymbol a_1-\boldsymbol a_2+\boldsymbol a_3=\boldsymbol0,\quad -2\boldsymbol a_1-\boldsymbol a_2+\boldsymbol a_4=\boldsymbol0
\]
的线性组合组成。

区分点：题目要的是全部关系，必须写出带两个自由参数的通解，不能只给一个特解。