## C.19 · 空间向量与解析几何（速记）

| 提示 | 内容 |
|---|---|
| 距离与位移 | $d(P_1,P_2)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}$；$\overrightarrow{AB}=$ 终点减起点；加法、数乘逐坐标；$\boldsymbol b\ne\boldsymbol 0$ 时 $\boldsymbol a\parallel\boldsymbol b$ 等价于存在同一个 $\lambda$ 使 $\boldsymbol a=\lambda\boldsymbol b$（零向量另按约定） |
| 长度与方向 | $\lVert\boldsymbol a\rVert=\sqrt{a_x^2+a_y^2+a_z^2}$；单位化要求 $\boldsymbol a\ne\boldsymbol 0$，单位向量 $\boldsymbol a/\lVert\boldsymbol a\rVert$ 的坐标就是方向余弦，$\cos^2\alpha+\cos^2\beta+\cos^2\gamma=1$ |
| 数量积 | $\boldsymbol a\cdot\boldsymbol b=\lVert\boldsymbol a\rVert\lVert\boldsymbol b\rVert\cos\theta=a_xb_x+a_yb_y+a_zb_z$；两个向量非零时，垂直 $\iff$ 为 0（夹角公式、投影方向同样要求非零）；$\boldsymbol b$ 在 $\boldsymbol a$ 上的投影 $=\boldsymbol a\cdot\boldsymbol b/\lVert\boldsymbol a\rVert$（除以被投影到的向量的长度，可为负）；$\lVert\boldsymbol a\pm\boldsymbol b\rVert^2=\lVert\boldsymbol a\rVert^2\pm2\boldsymbol a\cdot\boldsymbol b+\lVert\boldsymbol b\rVert^2$ |
| 向量积 | 遮列法，中间一项加负号：$(a_yb_z-a_zb_y,\ a_zb_x-a_xb_z,\ a_xb_y-a_yb_x)$；垂直于 $\boldsymbol a,\boldsymbol b$，右手法则；$\lVert\boldsymbol a\times\boldsymbol b\rVert$ = 平行四边形面积；$\boldsymbol b\times\boldsymbol a=-\boldsymbol a\times\boldsymbol b$；为 $\boldsymbol 0$ $\iff$ 平行（零向量按约定），此时不能当法向量 |
| 数量积 vs 向量积 | 数 / 向量；$\cos\theta$ / $\sin\theta$；为 0 表示垂直 / 平行；交换不变 / 变号 |
| 混合积 | $[\boldsymbol a,\boldsymbol b,\boldsymbol c]=(\boldsymbol a\times\boldsymbol b)\cdot\boldsymbol c=$ 三阶行列式（三个向量按行排）；绝对值 = 平行六面体体积，四面体是 $\frac16$；为 0 $\iff$ 共面；轮换不变，交换两个变号 |
| 平面 | 点法式 $A(x-x_0)+B(y-y_0)+C(z-z_0)=0$，$(A,B,C)$ 是法向量；$(A,B,C)\ne\boldsymbol 0$；三点不共线时才能用 $\overrightarrow{M_1M_2}\times\overrightarrow{M_1M_3}$ 定面；$d=\frac{\lvert Ax_1+By_1+Cz_1+D\rvert}{\sqrt{A^2+B^2+C^2}}$ |
| 直线 | 点向式 $\frac{x-x_0}{m}=\frac{y-y_0}{n}=\frac{z-z_0}{p}$（分母为 0 则分子为 0）；一般式的方向取 $\boldsymbol n_1\times\boldsymbol n_2$，点由令一个变量为定值解出（选 $\boldsymbol s$ 里非零的分量对应的变量） |
| 位置关系 | 面面、线线用 $\cos\varphi=\frac{\lvert\cdot\rvert}{\cdots}$；线面用 $\sin\varphi$；方向平行后再代一点区分平行与重合、包含；线面平行 $\boldsymbol s\cdot\boldsymbol n=0$，线面垂直 $\boldsymbol s\parallel\boldsymbol n$；两直线（方向不平行）共面 $\iff(\boldsymbol s_1\times\boldsymbol s_2)\cdot\overrightarrow{M_1M_2}=0$，不为 0 是异面 |
| 点到直线 | $d=\lVert\overrightarrow{M_0M_1}\times\boldsymbol s\rVert/\lVert\boldsymbol s\rVert$；垂足设 $M_0+t\boldsymbol s$，令 $\overrightarrow{MM_1}\cdot\boldsymbol s=0$ |
| 球面与柱面 | 球面 $(x-a)^2+(y-b)^2+(z-c)^2=R^2$；缺一个变量时，先看另两个变量的方程在坐标面上是否表示曲线；是则沿缺失变量的轴平移成柱面 |
| 旋转曲面 | 绕哪个轴转，哪个坐标不动，另一个坐标换成 $\pm\sqrt{\text{除轴坐标外两个坐标的平方和}}$ |
| 二次曲面 | 先配方，检查平方项是否齐全及符号；三项齐全且恰有一项为负时，右边 $1,-1,0$ 则分别对应单叶、双叶、锥面；有一次项且另两个平方项齐全，同号椭圆抛物面、异号马鞍；其他情形用截痕判断 |
| 曲线与投影 | 一般方程 = 两曲面交线；参数方程先参数化柱面再解第三个坐标；不能直接令该变量为 0 代回；消去垂直于该坐标面的变量得必要条件，再检查被消去的变量有实数解；立体投影区域由「哪些 $(x,y)$ 配得上至少一个 $z$」确定（上下夹层：共同定义域内下界不超过上界） |
