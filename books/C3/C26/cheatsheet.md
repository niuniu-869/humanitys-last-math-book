## C.26 · 三重积分与重积分的应用（速记）

| 提示 | 内容 |
|---|---|
| 三重积分性质 | 线性、区域可加、$\iiint1\,\mathrm{d}V=V$、比较、中值（$f$ 连续、$\Omega$ 连通，不连通会错）；与二重积分逐条对应 |
| 对称性 | $\Omega$ 关于 $xOy$ 对称：$f$ 对 $z$ 奇 ⇒ 0，偶 ⇒ 2 倍上半；方程轮换不变 ⇒ $\iiint x=\iiint y=\iiint z$ |
| 投影法（先一后二） | $\iint_{D_{xy}}\mathrm{d}\sigma\int_{z_1(x,y)}^{z_2(x,y)}f\,\mathrm{d}z$；竖着穿线，穿入是下限 |
| 截面法（先二后一） | $\int_{c_1}^{c_2}\mathrm{d}z\iint_{D_z}f\,\mathrm{d}\sigma$；$f$ 只含 $z$ 时 $=\int f(z)A(z)\,\mathrm{d}z$ |
| 选投影还是截面 | 看被积函数含几个变量、截面面积好不好写 |
| 柱面坐标 | $x=r\cos\theta,\ y=r\sin\theta,\ z=z$，$\mathrm{d}V=r\,\mathrm{d}r\,\mathrm{d}\theta\,\mathrm{d}z$；投影是圆盘、含 $x^2+y^2$ |
| 球面坐标 | $x=\rho\sin\varphi\cos\theta,\ y=\rho\sin\varphi\sin\theta,\ z=\rho\cos\varphi$，$\varphi\in[0,\pi]$ 从 $z$ 轴量起 |
| 球面坐标体积元 | $\mathrm{d}V=\rho^2\sin\varphi\,\mathrm{d}\rho\,\mathrm{d}\varphi\,\mathrm{d}\theta$（三条边 $\mathrm{d}\rho$、$\rho\,\mathrm{d}\varphi$、$\rho\sin\varphi\,\mathrm{d}\theta$）；锥面 $z=\sqrt{x^2+y^2}$ 即 $\varphi=\frac\pi4$ |
| 一般换元 | $\mathrm{d}V=\lvert J\rvert\,\mathrm{d}u\,\mathrm{d}v\,\mathrm{d}w$，$J=\frac{\partial(x,y,z)}{\partial(u,v,w)}$ 是三阶行列式（混合积）；内部一一对应、偏导连续且 $J\ne0$（坐标轴、接缝等边界例外见正文）；椭球体积 $\frac43\pi abc$ |
| 曲面面积 | $f$ 有连续一阶偏导；$S=\iint_D\sqrt{1+f_x^2+f_y^2}\,\mathrm{d}\sigma$；$\mathrm{d}S=\mathrm{d}\sigma/\cos\gamma$ |
| 质心 | $\bar x=\frac1M\iiint x\mu\,\mathrm{d}V$ 等，$M=\iiint\mu\,\mathrm{d}V$；密度均匀时为形心；先同时核对区域与密度的对称性 |
| 转动惯量 | $I_z=\iiint(x^2+y^2)\mu\,\mathrm{d}V$，用到轴的距离平方，不是到原点；均匀球 $\frac25Ma^2$ |
| 吸引力 | 质点间 $Gm/d^2$；连续物体切成小块再把向量加起来，受力点在对称轴上且形状、密度都对称时，抵消垂直于轴的分量 |
| 易错 | 截面法里 $f$ 含 $x,y$ 时不能直接乘截面积（圆柱上 $\iiint x^2\,\mathrm{d}V=\frac\pi4$，不是 0）；$\theta$ 的范围取重会算两遍；漏乘 $r$ 或 $\rho^2\sin\varphi$ |
| 常用结果 | 半球体形心 $\bar z=\frac38a$；单位球 $\iiint\rho^2\,\mathrm{d}V=\frac{4\pi}5$ |
