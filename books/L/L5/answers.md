## L.5 · 逆矩阵（答案）

### A 基础

**L5-01**
**答案：** $ad-bc=3-2=1$，所以
\[
A^{-1}=\begin{pmatrix}1&-2\\-1&3\end{pmatrix},\qquad \boldsymbol{x}=A^{-1}(7,3)^{\mathsf T}=(1,2)^{\mathsf T}。
\]
直接相乘可得 $AA^{-1}=E$，代回原方程得到 $(7,3)^{\mathsf T}$。

**L5-02**
**答案：** (C)。因为转置会反转乘法次序，$A^{\mathsf T}(A^{-1})^{\mathsf T}=(A^{-1}A)^{\mathsf T}=E$。

(A) 把乘积逆矩阵的次序写反，正确式子是 $(AB)^{-1}=B^{-1}A^{-1}$；(B) 逆矩阵没有加法公式，例如 $A=B=E$ 时两边分别为 $\frac12E$ 与 $2E$；(D) 漏掉了比例因子，正确式子是 $(kA)^{-1}=\frac1kA^{-1}$。

**L5-03**
**答案：** 不可逆。消元得
\[
\begin{pmatrix}1&2&0\\0&1&1\\0&0&0\end{pmatrix}，
\]
只有两个主元。取自由变量 $x_3=1$，得 $x_2=-1,x_1=2$，所以可取 $\boldsymbol{x}=(2,-1,1)^{\mathsf T}$。

**L5-04**
**答案：** 右乘
\[
\begin{pmatrix}1&2\\0&1\end{pmatrix}^{-1}=\begin{pmatrix}1&-2\\0&1\end{pmatrix}
\]
得
\[
X=\begin{pmatrix}2&5\\1&3\end{pmatrix}\begin{pmatrix}1&-2\\0&1\end{pmatrix}=\begin{pmatrix}2&1\\1&1\end{pmatrix}。
\]

### B 进阶

**L5-05**
**答案：** (B)。同阶方阵满足 $AB=E$ 时，$B$ 的齐次方程只有零解，因而 $B$ 可逆；再右乘 $B^{-1}$ 得 $A=B^{-1}$，所以 $B=A^{-1}$。

(A) 的反例是
\[
A=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix},\quad B=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}：
\]
有 $AB=E_2$，但 $BA=\begin{pmatrix}1&0&0\\0&1&0\\0&0&0\end{pmatrix}\ne E_3$。(C) 非零矩阵也可能奇异；(D) 对某一个 $\boldsymbol b$ 有解，不能说明对所有右端都有唯一解。

**L5-06**
**答案：** 反设 $A$ 可逆。由 $A^2=A$ 两边左乘 $A^{-1}$，得 $A=E$，这与题设 $A\ne E$ 矛盾。因此 $A$ 不可逆。

**L5-07**
**答案：** 初等矩阵的逆分别为
\[
E_1^{-1}=E_1,\quad E_2^{-1}=\begin{pmatrix}1&0\\-2&1\end{pmatrix},\quad E_3^{-1}=\begin{pmatrix}1&-3\\0&1\end{pmatrix}。
\]
由乘积逆矩阵次序，
\[
P^{-1}=E_1^{-1}E_2^{-1}E_3^{-1}
=\begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}1&0\\-2&1\end{pmatrix}\begin{pmatrix}1&-3\\0&1\end{pmatrix}
=\begin{pmatrix}-2&7\\1&-3\end{pmatrix}。
\]
并且 $P=E_3E_2E_1=\begin{pmatrix}3&7\\1&2\end{pmatrix}$，直接相乘得 $PP^{-1}=E$。

**L5-08**
**答案：** 先移项得 $AX=2A-E$。因为 $A$ 可逆，左乘 $A^{-1}$：
\[
X=A^{-1}(2A-E)=\begin{pmatrix}\frac32&\frac16\\0&\frac53\end{pmatrix}。
\]
代回可得 $AX+E=2A$。

**L5-09**
**答案：** (C)。$A$ 的第二行是第一行的 2 倍，因此 $AX$ 的第二行也必是第一行的 2 倍；但 $B$ 的第二行不是第一行的 2 倍，故方程无解。

**L5-10**
**答案：** 若 $A_1,A_2$ 都可逆，则
\[
M\begin{pmatrix}A_1^{-1}&O\\O&A_2^{-1}\end{pmatrix}=\begin{pmatrix}E&O\\O&E\end{pmatrix}，
\]
所以 $M^{-1}=\begin{pmatrix}A_1^{-1}&O\\O&A_2^{-1}\end{pmatrix}$。反过来，若 $A_1$ 不可逆，取非零向量 $u$ 使 $A_1u=0$，则 $M(u,0)^{\mathsf T}=0$，所以 $M$ 不可逆；$A_2$ 不可逆时同理。

题给 $A_2$ 的两行相同，故 $A_2$ 不可逆，从而对应的 $M$ 不可逆。

**L5-11**
**答案：** 右乘 $A$ 得 $AX=X+3A$，即 $(A-E)X=3A$。因为
\[
\det(A-E)=2\ne0，
\]
所以 $A-E$ 可逆，且解唯一。计算得
\[
(A-E)^{-1}=\begin{pmatrix}1&-\frac12\\0&\frac12\end{pmatrix},\qquad
X=(A-E)^{-1}3A=\begin{pmatrix}6&-\frac32\\0&\frac92\end{pmatrix}。
\]

**L5-13**
**答案：** 设 $X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$。则
\[
XC=\begin{pmatrix}a+2b&2a+4b\\c+2d&2c+4d\end{pmatrix}。
\]
因此 (1) 的全部解为
\[
X=\begin{pmatrix}3-2s&s\\1-2t&t\end{pmatrix},\qquad s,t\in\mathbb R。
\]
参数 $s,t$ 可以任意取，所以解不唯一。 (2) 若第二行改为 $(1,3)$，第二行仍必须满足“第二个分量等于第一个分量的 2 倍”，但 $3\ne2\cdot1$，所以无解。

### C 提高

**L5-12**
**答案：** 由 $(E-C)\boldsymbol x=\boldsymbol d$ 的第一行，
\[
\frac{19}{4}-c\cdot\frac{21}{4}=3，
\]
所以 $c=\frac13$。此时 $C$ 是严格上三角矩阵，$C^3=O$，从而
\[
(E-C)^{-1}=E+C+C^2
\]
存在，因此方程的解唯一。矩阵 $C$ 的所有元素都非负，且 $c=\frac13\ge0$，符合非负直接消耗系数的要求。

### 章末混合练习

**L5-14**
**答案：** 由线性性，
\[
T(0,1)^{\mathsf T}=T(1,1)^{\mathsf T}-T(1,0)^{\mathsf T}=(1,2)^{\mathsf T}。
\]
所以 $X=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，进而 $T(2,-1)^{\mathsf T}=(3,0)^{\mathsf T}$。

**L5-15**
**答案：** $P=E_2E_1=\begin{pmatrix}-1&-1\\2&1\end{pmatrix}$，由乘积逆矩阵次序
\[
P^{-1}=E_1^{-1}E_2^{-1}=\begin{pmatrix}1&1\\-2&-1\end{pmatrix}，
\]
相乘得 $PP^{-1}=E$。

**L5-16**
**答案：** 右端为 $(3,6)^{\mathsf T}$ 时，全部解为
\[
\boldsymbol{x}=(3-2t,t)^{\mathsf T},\quad t\in\mathbb R。
\]
右端为 $(3,5)^{\mathsf T}$ 时，第二行减第一行的 2 倍得到矛盾 $0=-1$，所以无解。

**L5-17**
**答案：** $B\ne C$ 显然。又因为 $C-B=\begin{pmatrix}2&0\\-1&0\end{pmatrix}$，而
\[
A\begin{pmatrix}2\\-1\end{pmatrix}=\boldsymbol0，
\]
所以 $A(C-B)=O$，即 $AB=AC$。这个反例说明，约分需要 $A$ 可逆；$A$ 奇异时不能由 $AB=AC$ 推出 $B=C$。
