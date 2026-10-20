## M.9 · 词向量与表示学习：从独热向量到 word2vec

在购物网站搜「手机壳」，结果里常有标成「保护套」的商品；看过一件商品，页面下方会推荐「相似商品」。搜索引擎和推荐系统做到这一点，靠的是把词（或商品）变成一串数，再比较两串数的方向有多接近，也就是 L.2.5 的余弦相似度。变成的这串数叫**词向量**。

前面八章的输入都是现成的数：表格里的数、图像的像素。语言的输入是词，要先把词变成向量。常见的语言模型，第一层都是把词变成向量的一张表，叫嵌入矩阵。这张表怎样得到，就是本章的内容。

办法是被一个问题逼出来的：怎样让计算机知道两个词意思相近？1954 年，语言学家 Harris 提出，出现在相似上下文里的词意思相近；这个想法后来常被概括成 Firth 1957 年的一句话 You shall know a word by the company it keeps，也就是「观其伴而知其词」。照这个想法，数一数每个词周围常出现哪些词，每个词就得到一行计数，但这行计数的长度等于词表的大小，而且几乎全是 0。1990 年，Deerwester 等人用截断 SVD（L.15.5）把词与文档的计数表压成几百维的稠密向量，这就是潜在语义分析；同样的方法也可以用在词与上下文词的计数表上。2013 年，Mikolov 等人的 word2vec 把模型简化到极致，按论文报告，在十几亿词的语料上一天之内就能训完，「国王 − 男人 + 女人 ≈ 女王」这个例子由此出名。

按本册的三件套来填：模型是两张嵌入矩阵（中心词、上下文词各一张）加一个 softmax，用中心词预测它周围的词；损失是预测对的概率的负对数，也就是交叉熵；更新规则仍是梯度下降。

本章先看最省事的独热向量错在哪里（第 1 节），再从「看上下文」的想法出发做出共现向量（第 2 节）；第 3 节把它压成稠密的嵌入，第 4 节说明为什么要让向量自己从语料里学出来，并写出 skip-gram 的目标；第 5 节推它的梯度，第 6 节用负采样把每步的计算量从词表大小降到几个词；最后两节是两个延伸：类比为什么成立（第 7 节），以及同样的损失怎样把图片和文字放进同一个空间（第 8 节）。

### 1. 一段文字怎样变成计算机能处理的向量？最省事的办法错在哪里？

计算机处理的是数，第一步是把文字切成基本单位，叫**词元**。英文可以按空格切；中文没有空格，要先**分词**。现代大模型多半切成比词更小的**子词**，这个留到 M.10。

把语料里所有不同的词列成一张表，叫**词表**，大小记作 $V$，并给每个词一个编号 $0,1,\dots,V-1$。后面几节都用同一份小语料，五句话，已经分好词：

> 猫 吃 鱼　／　猫 喝 牛奶　／　狗 吃 骨头　／　狗 喝 水　／　狗 吃 鱼

词表是 8 个词：猫、狗、吃、喝、鱼、骨头、牛奶、水，所以 $V=8$。

最直接的想法是把编号本身当成词的数值：猫是 0，狗是 1，水是 7。可是这样「猫」和「狗」差 1，「猫」和「水」差 7，看上去前者更近，只因为编号恰好这样排；换一种排序，远近就变了。编号的大小没有任何意思，不能拿来比远近。

避开这个问题的最省事的办法是**独热向量**：词 $i$ 对应一个 $V$ 维向量 $\boldsymbol e_i$，第 $i$ 个分量是 1，其余都是 0。例如「猫」编号 0，$\boldsymbol e_{\text{猫}}=(1,0,0,0,0,0,0,0)^{\mathsf T}$。

这个办法还有一个根本的毛病。先看两个具体的词：猫是 $\boldsymbol e_0=(1,0,0,\dots,0)^{\mathsf T}$，狗是 $\boldsymbol e_1=(0,1,0,\dots,0)^{\mathsf T}$。对应分量相乘再相加，每一项都有一个因子是 0，点积是 0；差向量 $(1,-1,0,\dots,0)$ 的长度是 $\sqrt{1^2+1^2}=\sqrt2$。换成「猫」和「水」，算出来一模一样。一般地：**任意两个不同的词，向量都互相正交**。

$$\boldsymbol e_i^{\mathsf T}\boldsymbol e_j=\begin{cases}1,&i=j\\0,&i\ne j\end{cases},\qquad \lVert\boldsymbol e_i-\boldsymbol e_j\rVert=\sqrt{1+1}=\sqrt2\quad(i\ne j).$$

这里 $\lVert\boldsymbol a\rVert$ 就是向量 $\boldsymbol a$ 的长度（有的书写成 $|\boldsymbol a|$；这里用双竖线，是为了和数的绝对值区分开，数学和 AI 论文里都这样写）。第一个式子说余弦相似度是 0，第二个式子说任意两词的距离都是 $\sqrt2$：「猫」和「狗」的距离，与「猫」和「水」的距离一样大。向量里没有任何关于意思的信息。

**方法 1（词表与独热向量）**

1. 切词，列出词表，编号 $0,\dots,V-1$。
2. 词 $i$ 的独热向量是 $\boldsymbol e_i\in\mathbb R^V$。
3. 一句话的 $T_{\text{句}}$ 个词按顺序排成 $T_{\text{句}}\times V$ 的矩阵 $O$，每行是对应词的独热向量。

**例 1**　用上面的小语料，把第一句「猫 吃 鱼」排成矩阵 $O$（词表顺序：猫、狗、吃、喝、鱼、骨头、牛奶、水）。算 $OO^{\mathsf T}$，并说出 $O^{\mathsf T}O$ 是什么。

这道题只做方法 1 的排矩阵，再用 L.3 的矩阵乘法看它的乘积。第一步，$O$ 是 $3\times8$ 矩阵，三行分别是 $\boldsymbol e_0,\boldsymbol e_2,\boldsymbol e_4$（猫、吃、鱼的编号）：

$$O=\begin{pmatrix}1&0&0&0&0&0&0&0\\0&0&1&0&0&0&0&0\\0&0&0&0&1&0&0&0\end{pmatrix}.$$

第二步，$OO^{\mathsf T}$ 的 $(i,j)$ 元是第 $i$ 行与第 $j$ 行的点积，也就是上面的 $\boldsymbol e^{\mathsf T}\boldsymbol e$，三个词互不相同，所以

$$OO^{\mathsf T}=I_3 .$$

第三步，$O^{\mathsf T}O$ 是 $8\times8$ 矩阵，写成外积之和（L.3）$O^{\mathsf T}O=\sum_{t}\boldsymbol e_{w_t}\boldsymbol e_{w_t}^{\mathsf T}$，每个出现的词在对角线上加 1，所以它是对角矩阵，对角元是各词在这句话里出现的次数：猫、吃、鱼的位置是 1，其余是 0。

> 词表大小 $V=5$，句子「$w_2$ $w_0$ $w_2$」（用编号表示）排成矩阵 $O$。写出 $O^{\mathsf T}O$ 的对角元。
>
> 答案：$O$ 是 $3\times5$，三行是 $\boldsymbol e_2,\boldsymbol e_0,\boldsymbol e_2$。$O^{\mathsf T}O=\mathrm{diag}(1,0,2,0,0)$，词 0 出现 1 次，词 2 出现 2 次。

独热向量作为「编号」没有错，错在把编号当成了意思。独热向量本身不提供「猫」和「狗」相近的信息：它们的向量互相正交，从「猫吃鱼」学到的东西不会自动用到「狗吃鱼」上。独热向量把词区分开了，却没法表达哪些词相近。下一节问：能不能从文本里找出两个词相近的证据？

合上书，写出独热向量的定义，推出任意两个不同词的距离都是 $\sqrt2$，并说出这个事实为什么意味着独热向量表达不了「意思相近」。

### 2. 怎样从大量文本里看出两个词意思相近？

「猫」和「狗」都能出现在「吃」前面，也都能出现在「喝」前面；「鱼」和「骨头」都出现在「吃」后面。这提示一个办法：**一个词的意思，由它周围常出现的词来刻画**。这就是分布假说。

具体地，取一个窗口半径 $m$：对语料中每个词，看它前后各 $m$ 个位置上的词。用 $X_{ij}$ 记词 $j$ 出现在词 $i$ 的窗口里的次数，这张 $V\times V$ 的表叫**共现矩阵**，第 $i$ 行 $\boldsymbol x_i$ 就是词 $i$ 的**共现向量**。用 L.2.5 的余弦相似度比较两行：

$$\cos(\boldsymbol x_a,\boldsymbol x_b)=\frac{\boldsymbol x_a^{\mathsf T}\boldsymbol x_b}{\lVert\boldsymbol x_a\rVert\,\lVert\boldsymbol x_b\rVert}.$$

**方法 2（共现向量与余弦）**

1. 取窗口半径 $m$，对每个词扫描它前后各 $m$ 个位置，累计 $X_{ij}$。
2. 词 $i$ 的向量是 $X$ 的第 $i$ 行。
3. 两个词的相似程度用两行的余弦。

**例 2**　对小语料取 $m=1$（只看紧邻的前后词，不跨句），求「猫」和「狗」的余弦。

沿用第 1 节的小语料，这次不再给每个词一个编号，而是数每个词的邻居。

第一步，数「猫」的邻居。「猫 吃 鱼」里猫的邻居是吃；「猫 喝 牛奶」里是喝。所以「猫」的共现向量只有两个非零分量：吃 1、喝 1。

第二步，数「狗」的邻居。「狗 吃 骨头」「狗 吃 鱼」各贡献一次吃，「狗 喝 水」贡献一次喝：吃 2、喝 1。

第三步，两行在其余位置都是 0，所以

$$\cos(\text{猫},\text{狗})=\frac{1\times2+1\times1}{\sqrt{1^2+1^2}\,\sqrt{2^2+1^2}}=\frac{3}{\sqrt2\sqrt5}\approx0.9487 .$$

完整的共现矩阵（行、列顺序同词表）是：

| | 猫 | 狗 | 吃 | 喝 | 鱼 | 骨头 | 牛奶 | 水 |
|---|---|---|---|---|---|---|---|---|
| 猫 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 狗 | 0 | 0 | 2 | 1 | 0 | 0 | 0 | 0 |
| 吃 | 1 | 2 | 0 | 0 | 2 | 1 | 0 | 0 |
| 喝 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 1 |
| 鱼 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| 骨头 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 牛奶 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 水 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |

![共现矩阵的行向量：「猫」与「狗」的两行在「吃」「喝」两列上都有非零的计数，方向相近；「鱼」与「牛奶」的非零列完全不重合](fig/M9-n1.pdf){width=70%}

> 在小语料后面再加一句「猫 吃 骨头」，重新算 $\cos(\text{猫},\text{狗})$。
>
> 答案：新句子让「猫」多了一次吃：猫的向量变成吃 2、喝 1，与狗的向量完全相同，所以 $\cos=1$。

**例 3**　用同一张表，这次比较的不再是「猫」「狗」这两个主语，而是两个宾语，再加两对不相干的词。算 $\cos(\text{鱼},\text{骨头})$、$\cos(\text{鱼},\text{牛奶})$、$\cos(\text{猫},\text{鱼})$。

「鱼」的行只有「吃」一列（2），「骨头」的行也只有「吃」一列（1）：两个向量同向，余弦是 1。「牛奶」的行只有「喝」一列，与「鱼」的非零列不重合，点积为 0，余弦是 0。

「猫」的行是吃 1、喝 1，「鱼」的行是吃 2，点积 $1\times2=2$，$\cos=\dfrac{2}{\sqrt2\times2}\approx0.7071$。

吃的东西（鱼、骨头）互相靠近，喝的东西（牛奶、水）互相靠近，两类之间没有重合；「猫」和「鱼」得到 0.7071：猫的上下文有吃、喝两个，鱼只有吃一个，两行的夹角就是这份计数决定的 45°。语料变大后这个数会改变；哪些词互相靠近，取决于数据和上下文的定义，没有一般的保证。

共现向量有两个明显的缺点。一是维数等于 $V$，而且大部分元素是 0。二是出现很多次的词（「的」「吃」）计数很大，会盖过有区别的信息；常见的补救是先对计数取对数，压低大数的影响，本章不展开。本章只顺着第一个缺点往下走：能不能用几百个数就表示一个词？

合上书，写出共现矩阵的定义，用它算出例 2 的 $\cos(\text{猫},\text{狗})$，并说出为什么「鱼」和「牛奶」的余弦是 0。

### 3. 能不能用几百个数表示一个词，并让意思相近的词向量也相近？

例 2 的共现向量是 8 维，8 个词时还看得过来；词表有 5 万个词，一个词就是 5 万个数，其中绝大多数是 0。我们想要一个短得多的向量：词 $i$ 用 $d$ 个数表示（$d$ 通常是 100 到 1000，远小于 $V$），并且意思相近的词，向量也相近。这样的向量叫**分布式表示**或**嵌入**，每个分量不再对应某个具体的上下文词。

把全部词的向量按行排成一个 $V\times d$ 的矩阵 $E$，叫**嵌入矩阵**，第 $i$ 行 $\boldsymbol v_i^{\mathsf T}$ 是词 $i$ 的向量。它与独热向量的联系非常简单：

$$\boldsymbol e_i^{\mathsf T}E=E\text{ 的第 }i\text{ 行}=\boldsymbol v_i^{\mathsf T}.$$

因为 $\boldsymbol e_i^{\mathsf T}$ 只有第 $i$ 个分量是 1，乘上矩阵时只留下第 $i$ 行（L.3 的「按行看」）。所以「把词变成向量」就是**查表**：编号为 $i$ 的词，取出 $E$ 的第 $i$ 行。一句话的 $T$ 个词排成 $T\times V$ 的矩阵 $O$（方法 1），$OE$ 就是 $T\times d$ 的矩阵，每行是一个词的向量。

程序里直接按编号取行，`E[ids]` 就是 $OE$。

$E$ 共有 $V\cdot d$ 个数，由训练得到时它们就是参数：$V=5\times10^4$、$d=300$ 时是 $1.5\times10^7$ 个。

![独热向量里任意两个不同词的距离都是 $\sqrt2$，嵌入向量里「猫」与「狗」靠得近、与「鱼」几乎垂直（实心点是例 4 的四个词）](fig/M9-n2.pdf){width=70%}

**方法 3（嵌入查表）**

1. 词的编号 $i$ → 取 $E$ 的第 $i$ 行 $\boldsymbol v_i$（等价于 $\boldsymbol e_i^{\mathsf T}E$）。
2. 一句话 → $OE$，形状 $T_{\text{句}}\times d$。
3. 参数个数 $=V\cdot d$；两个词的相似程度用 $\boldsymbol v_a,\boldsymbol v_b$ 的余弦。

**例 4**　$V=8$、$d=2$ 的嵌入矩阵（手造的数，只为演示）的几行是：猫 $(1.0,0.2)$、狗 $(0.9,0.4)$、吃 $(-0.5,0.8)$、鱼 $(0.1,-0.9)$。对句子「猫 吃 鱼」算 $OE$，并算 $\cos(\text{猫},\text{狗})$ 与 $\cos(\text{猫},\text{鱼})$。

句子仍是例 1 的「猫 吃 鱼」，矩阵 $O$ 也不变，变的只是右边多乘了一个 $E$，看乘法怎样变成取行。向量是手造的，要的是只用 2 个数也能让「猫」「狗」靠近，像例 2 里共现向量得到的 0.9487 那样。

查表得 $OE$ 的三行依次是 $(1.0,0.2)$、$(-0.5,0.8)$、$(0.1,-0.9)$，形状 $3\times2$。

余弦：

$$\cos(\text{猫},\text{狗})=\frac{1.0\times0.9+0.2\times0.4}{\sqrt{1.04}\,\sqrt{0.97}}\approx0.976,\qquad \cos(\text{猫},\text{鱼})=\frac{1.0\times0.1+0.2\times(-0.9)}{\sqrt{1.04}\,\sqrt{0.82}}\approx-0.087 .$$

「猫」与「狗」靠得很近，与「鱼」几乎垂直：这正是我们想让嵌入具备的样子。独热向量下这两个余弦都是 0。

> 某词表 $V=3\times10^4$，嵌入维数 $d=256$。嵌入矩阵有多少个参数？一个含 10 个词的句子，$OE$ 的形状是什么？
>
> 答案：$3\times10^4\times256=7\,680\,000$ 个参数；$O$ 是 $10\times30000$，$OE$ 是 $10\times256$。

那么 $E$ 从哪里来？最直接的想法是拿共现矩阵 $X$ 本身当 $E$，但它有 $V$ 列，正是要压掉的。**怎样把 $V$ 列压成 $d$ 列，又尽量保住词与词的关系？** 一类做法是**截断 SVD**（L.15.5）：$X=U\Sigma W^{\mathsf T}$，只保留最大的 $d$ 个奇异值，$X_d=U_d\Sigma_dW_d^{\mathsf T}$。埃卡特–扬定理说，在秩不超过 $d$ 的矩阵里，$X_d$ 与 $X$ 的元素误差平方和最小。

**取哪一块当词向量？** 词与词的关系由行内积决定（余弦也由它算出），所以要让 $E_d$ 的行内积等于 $X_d$ 的行内积。取 $E_d=U_d\Sigma_d$ 的各行就做到了：$W_d$ 的列互相正交，$W_d^{\mathsf T}W_d=I$，所以

$$X_dX_d^{\mathsf T}=U_d\Sigma_dW_d^{\mathsf T}W_d\Sigma_dU_d^{\mathsf T}=U_d\Sigma_d^2U_d^{\mathsf T}=E_dE_d^{\mathsf T}.$$

若只取 $U_d$，行内积成了 $U_dU_d^{\mathsf T}$，奇异值的大小信息丢掉，就不再等于 $X_d$ 的行内积。

**压到多小才不丢东西？** 保留了全部非零奇异值（$d\ge\mathrm{rank}\,X$）时 $X_d=X$，行内积和非零行的余弦都和原来完全相同；$d$ 更小时只是近似。小语料的共现矩阵秩为 4（奇异值约 3.35、3.35、1.66、1.66，其余为 0），所以取 $d=4$ 没有损失：$E_4$ 的各行之间余弦与原来的八维完全相同，例如 $\cos(\text{猫},\text{狗})\approx0.9487$ 不变。真实语料里 $V$ 有几十万，要先攒出 $V\times V$ 的大矩阵再分解，代价很高。

于是有了另一条路：不先数再压，而是直接让 $E$ 成为参数，用一个预测任务训练它。预测得越准，$E$ 里就越能装下词的意思：要把邻居猜准，$\boldsymbol v_c$ 就得把「这个词常和谁在一起」编码进去，两个词的邻居分布越像，它们的向量就越被推向相近的位置（第 7 节会把这一点说得更准确）。下一节讲 word2vec 怎样把这个预测任务写成损失。

合上书，说明 $\boldsymbol e_i^{\mathsf T}E$ 为什么是 $E$ 的第 $i$ 行，以及嵌入矩阵的形状和参数个数。

### 4. 怎样让词向量从语料里自己学出来？

先看一个具体的情形。小语料里有「猫 吃 鱼」，取窗口半径 $m=1$，中心词是「吃」，它的两个邻居是「猫」和「鱼」。如果「吃」的向量里编码了「猫和鱼常在我旁边」，那么给出「吃」，模型就应该能把「猫」和「鱼」猜出来。让模型做这件事，并按猜得准不准来调向量，就是训练词向量的办法。word2vec 里这样的模型叫 **skip-gram**：给一个中心词 $c$，预测它窗口里的每一个上下文词 $o$。预测得好，说明中心词的向量里装进了它的上下文信息，这就是分布假说的直接实现。

每个词用**两个**向量：作为中心词时用 $\boldsymbol v_w$，作为上下文词时用 $\boldsymbol u_w$，各自排成矩阵 $V_{\text{in}}$、$U_{\text{out}}$，形状都是 $V\times d$。为什么不共用一个？如果共用，中心词和它自己的得分是 $\boldsymbol v_c^{\mathsf T}\boldsymbol v_c=\lVert\boldsymbol v_c\rVert^2$，这个得分是向量长度的平方，往往很大，模型就会倾向于认为一个词的邻居是它自己；而且交换中心词与上下文词，得分完全相同，这个对称性也未必符合语言。两张表解除了这两个限制。训练完通常用 $\boldsymbol v_w$ 作为词向量。

给定中心词 $c$，第 $w$ 个词作为上下文词的**得分**是 $z_w=\boldsymbol u_w^{\mathsf T}\boldsymbol v_c$。点积越大，模型越认为 $w$ 会出现在 $c$ 旁边。再用 softmax 把得分变成概率：

$$p(o\mid c)=\frac{\exp(\boldsymbol u_o^{\mathsf T}\boldsymbol v_c)}{\sum_{w=1}^{V}\exp(\boldsymbol u_w^{\mathsf T}\boldsymbol v_c)} .$$

形状账本：$\boldsymbol v_c\in\mathbb R^d$，$\boldsymbol z=U_{\text{out}}\boldsymbol v_c\in\mathbb R^V$，$\boldsymbol p=\mathrm{softmax}(\boldsymbol z)\in\mathbb R^V$。这正是 M.2.7 的 softmax 回归：「特征」是 $\boldsymbol v_c$，类别是 $V$ 个词。

训练样本是语料里所有的（中心词，上下文词）对。把语料里所有句子的词依次编号 $t=1,\dots,T$（$T$ 是总词数，小语料里 $T=15$），窗口半径 $m$，要最大化平均对数似然（P.11.3），等价于最小化

$$J=-\frac1{N_{\text{对}}}\sum_{t=1}^{T}\ \sum_{\substack{-m\le j\le m\\ j\ne0}}\log p(w_{t+j}\mid w_t),$$

其中 $N_{\text{对}}$ 是配出的词对总数；窗口只在同一句内取，位置 $t+j$ 超出句子的不算，$N_{\text{对}}>0$。本章的 $\log$ 都是自然对数，也写作 $\ln$；$p(o\mid c)$ 读作「给定中心词 $c$ 时上下文词是 $o$ 的概率」。一个词对的损失 $\ell=-\log p(o\mid c)$ 就是正确上下文词的交叉熵，背后假设「上下文词服从类别分布」。小语料取 $m=1$：每句 3 个词，配出 4 对，五句共 $N_{\text{对}}=20$ 对。

![skip-gram 的前向：中心词的编号查 $V_{\text{in}}$ 得 $\boldsymbol v_c$，乘 $U_{\text{out}}$ 得 $V$ 个得分，softmax 后和真实词的独热向量比较，各处标出形状](fig/M9-n3.pdf){width=70%}

**方法 4（skip-gram 的前向）**

1. 取中心词向量 $\boldsymbol v_c$（查 $V_{\text{in}}$ 的一行）。
2. 对每个候选词算得分 $z_w=\boldsymbol u_w^{\mathsf T}\boldsymbol v_c$，softmax 得 $p_w$。
3. 损失 $\ell=-\log p_o=-z_o+\log\sum_w e^{z_w}$。

**例 5**　为了手算，只看三个候选上下文词：鱼、骨头、牛奶。中心词是「吃」，$\boldsymbol v_{\text{吃}}=(1,1)^{\mathsf T}$；三个词的上下文向量是 $\boldsymbol u_{\text{鱼}}=(1,1)^{\mathsf T}$、$\boldsymbol u_{\text{骨头}}=(1,0)^{\mathsf T}$、$\boldsymbol u_{\text{牛奶}}=(1,-1)^{\mathsf T}$。真实的上下文词是「鱼」。求 $\boldsymbol p$ 和损失。

这是上面「给定『吃』，猜它的邻居」的缩小版：三个候选的得分 $(2,1,0)$ 正是 M 册老朋友 ④ 的那组，只是现在由点积算出。

第一步，得分：$z_{\text{鱼}}=1+1=2$，$z_{\text{骨头}}=1$，$z_{\text{牛奶}}=1-1=0$，即 $\boldsymbol z=(2,1,0)$。

第二步，softmax：分母 $e^2+e^1+e^0\approx7.389+2.718+1=11.107$，

$$\boldsymbol p\approx(0.6652,\ 0.2447,\ 0.0900).$$

第三步，真实词是「鱼」，$\ell=-\ln0.6652\approx0.4076$。（也可由 $\ell=-z_o+\log\sum e^{z_w}=-2+2.4076$ 得到。）

> 同样的 $\boldsymbol v_{\text{吃}}$ 和 $\boldsymbol u$，真实的上下文词改成「牛奶」，$\ell$ 是多少？
>
> 答案：$p_{\text{牛奶}}=0.0900$，$\ell=-\ln0.0900\approx2.408$（即 $-0+2.4076$）。得分最低的词做了答案，损失就大。

**例 6**　一个纯计数的小题：窗口半径 $m=2$，一句 10 个词的话，一共配出多少个（中心词，上下文词）对？

这道题不再算概率，只数训练样本有多少：例 5 只处理了一个词对，整个语料有多少个词对，决定了训练的总量。

对第 $t$ 个词，上下文是它前后各 2 个位置里实际存在的词。位置 1 和 10 各有 2 个，位置 2 和 9 各有 3 个，位置 3 到 8 这六个位置各有 4 个：

$$2+3+4\times6+3+2=34 .$$

句子很长时总数近似 $2mT$。

损失 $J$ 写出来了，下一步是让它下降，也就是求梯度。

合上书，写出 $p(o\mid c)$、单个词对的损失，以及这个模型为什么是一个 softmax 回归。

### 5. skip-gram 的梯度怎样推？

回到例 5：「吃」的向量是 $(1,1)$，真实邻居「鱼」只得到概率 0.6652，损失 0.4076。要让这个概率变大，$\boldsymbol v_{\text{吃}}$ 该往哪个方向挪？这要对 $\boldsymbol v_c$ 求导；$\boldsymbol u_w$ 同样是要学的参数，一并求。先把损失写成不含分数线的形式（对数把商变成差，$\log\frac{e^{z_o}}{\sum_we^{z_w}}=z_o-\log\sum_we^{z_w}$）：

$$\ell=-\boldsymbol u_o^{\mathsf T}\boldsymbol v_c+\log\sum_{w=1}^{V}\exp(\boldsymbol u_w^{\mathsf T}\boldsymbol v_c).$$

**对 $\boldsymbol v_c$ 求导。** 第一项的梯度是 $-\boldsymbol u_o$（点积对其中一个向量的梯度是另一个向量，L.14.8）。第二项用链式法则（C.21）：对数的导数是 $\dfrac1{\sum_w e^{z_w}}$，求和里每一项 $e^{z_w}$ 对 $\boldsymbol v_c$ 的梯度是 $e^{z_w}\boldsymbol u_w$（因为 $z_w=\boldsymbol u_w^{\mathsf T}\boldsymbol v_c$，内层求导得 $\boldsymbol u_w$，再乘外层指数函数的导数 $e^{z_w}$），所以

$$\nabla_{\boldsymbol v_c}\log\sum_we^{z_w}=\frac{\sum_we^{z_w}\boldsymbol u_w}{\sum_{w'}e^{z_{w'}}}=\sum_wp_w\,\boldsymbol u_w .$$

合起来：

$$\boxed{\ \frac{\partial\ell}{\partial\boldsymbol v_c}=-\boldsymbol u_o+\sum_{w=1}^{V}p_w\boldsymbol u_w\ }$$

右边的 $\sum_wp_w\boldsymbol u_w$ 是按模型的概率对上下文向量求加权平均，可以理解成「模型预期的上下文向量」。所以：**梯度 = 模型预期的上下文向量 − 真实上下文词的向量**。梯度下降是 $\boldsymbol v_c\leftarrow\boldsymbol v_c-\eta\nabla$，于是更新量是 $\eta(\boldsymbol u_o-\bar{\boldsymbol u})$：$\boldsymbol v_c$ 沿着从预期向量指向真实向量的方向移动。严格地说，步长足够小时这能保证损失下降，但不保证每个点积都单调变化。$\bar{\boldsymbol u}=\boldsymbol u_o$ 时梯度为 0（例如 $p_o=1$ 时）。

**对 $\boldsymbol u_w$ 求导。** 第一项只有当 $w=o$ 时含 $\boldsymbol u_w$，贡献 $-\boldsymbol v_c$；第二项里只有 $e^{z_w}$ 含 $\boldsymbol u_w$，内层求导得 $\boldsymbol v_c$，所以对每个 $\boldsymbol u_w$ 贡献 $e^{z_w}\boldsymbol v_c\big/\sum_{w'}e^{z_{w'}}=p_w\boldsymbol v_c$。所以

$$\frac{\partial\ell}{\partial\boldsymbol u_w}=(p_w-y_w)\,\boldsymbol v_c,\qquad y_w=\begin{cases}1,&w=o\\0,&w\ne o\end{cases}.$$

这就是 M.2.7 的 $\boldsymbol p-\boldsymbol y$ 又出现了一次：对分数的梯度是 $\partial\ell/\partial z_w=p_w-y_w$，其余只是链式法则再乘上 $\partial z_w/\partial\boldsymbol u_w=\boldsymbol v_c$ 和 $\partial z_w/\partial\boldsymbol v_c=\boldsymbol u_w$。写成矩阵，$\boldsymbol z=U_{\text{out}}\boldsymbol v_c$：

$$\frac{\partial\ell}{\partial\boldsymbol z}=\boldsymbol p-\boldsymbol y,\qquad \frac{\partial\ell}{\partial\boldsymbol v_c}=U_{\text{out}}^{\mathsf T}(\boldsymbol p-\boldsymbol y),\qquad \frac{\partial\ell}{\partial U_{\text{out}}}=(\boldsymbol p-\boldsymbol y)\,\boldsymbol v_c^{\mathsf T}.$$

形状核对（M.7.9 的线性层反向公式）：$U_{\text{out}}^{\mathsf T}$ 是 $d\times V$，乘 $V$ 维的 $\boldsymbol p-\boldsymbol y$ 得 $d$ 维，与 $\boldsymbol v_c$ 同形；外积是 $V\times d$，与 $U_{\text{out}}$ 同形。

**中心词的查表也要反向。** $\boldsymbol v_c$ 是 $V_{\text{in}}$ 的第 $c$ 行，别的行没有参与这一步的计算，所以对 $V_{\text{in}}$ 来说，梯度只在第 $c$ 行可能非零，其余行为 0（这就是方法 3 里「按编号取行」的反向）。

![一次更新：$\boldsymbol v_c$ 沿「模型预期的上下文向量 $\bar{\boldsymbol u}$ 指向真实上下文向量 $\boldsymbol u_o$」的方向移动，虚线箭头是 $\bar{\boldsymbol u}-\boldsymbol u_o$ 的反方向](fig/M9-n4.pdf){width=70%}

**方法 5（skip-gram 的梯度）**

1. 先算 $\boldsymbol p-\boldsymbol y$（$\boldsymbol y$ 是真实词的独热向量）。
2. $\nabla_{\boldsymbol v_c}\ell=U_{\text{out}}^{\mathsf T}(\boldsymbol p-\boldsymbol y)=\bar{\boldsymbol u}-\boldsymbol u_o$，其中 $\bar{\boldsymbol u}=\sum_wp_w\boldsymbol u_w$。
3. $\nabla_{\boldsymbol u_w}\ell=(p_w-y_w)\boldsymbol v_c$，每个候选词一个。
4. 沿负梯度更新。

**例 7**　接例 5，求 $\nabla_{\boldsymbol v_c}\ell$、$\nabla_{\boldsymbol u_w}\ell$，并取 $\eta=1$ 更新一步，比较更新后的损失。

仍用例 5 的数据和算出的 $\boldsymbol p$，新的只有梯度和更新。

第一步，$\boldsymbol p-\boldsymbol y=(0.6652-1,\ 0.2447,\ 0.0900)=(-0.3348,\ 0.2447,\ 0.0900)$。

第二步，预期上下文向量 $\bar{\boldsymbol u}=0.6652(1,1)+0.2447(1,0)+0.0900(1,-1)\approx(1.0000,\ 0.5752)$，所以

$$\nabla_{\boldsymbol v_c}\ell=\bar{\boldsymbol u}-\boldsymbol u_{\text{鱼}}=(1.0000,\ 0.5752)-(1,1)=(0,\ -0.4248).$$

第一分量是 0，因为三个候选词的第一分量都是 1，无论怎样都不能区分它们。第二分量为负，下降时 $\boldsymbol v_c$ 的第二个分量会增大，使它更靠近第二分量最大的「鱼」。

第三步，$\nabla_{\boldsymbol u_w}\ell=(p_w-y_w)\boldsymbol v_c$：「鱼」$(-0.3348,-0.3348)$，「骨头」$(0.2447,0.2447)$，「牛奶」$(0.0900,0.0900)$。

第四步，$\eta=1$ 更新：$\boldsymbol v_c\to(1,\ 1.4248)$；$\boldsymbol u_{\text{鱼}}\to(1.3348,\ 1.3348)$，$\boldsymbol u_{\text{骨头}}\to(0.7553,\ -0.2447)$，$\boldsymbol u_{\text{牛奶}}\to(0.9100,\ -1.0900)$。重新算得分，得到新的 $\boldsymbol p\approx(0.9262,0.0547,0.0191)$，损失 $\approx0.0767$，比 0.4076 小得多。

> 把例 5 的真实词改成「牛奶」，求 $\nabla_{\boldsymbol v_c}\ell$。
>
> 答案：$\bar{\boldsymbol u}=(1.0000,0.5752)$（与真实词无关），$\boldsymbol u_{\text{牛奶}}=(1,-1)$，梯度 $=\bar{\boldsymbol u}-\boldsymbol u_{\text{牛奶}}=(0,\ 1.5752)$。下降时第二分量减小，$\boldsymbol v_c$ 向「牛奶」的方向移动。

这个梯度的计算量要看清楚。分母要对全部 $V$ 个词求和：算 $\boldsymbol p$ 要 $V$ 次点积；$\bar{\boldsymbol u}$ 要把 $V$ 个向量加权相加；对 $U_{\text{out}}$ 的梯度要更新**全部 $V$ 行**。每个词对一步的代价与 $V\cdot d$ 成正比，记作 $O(Vd)$。词表越大越慢，下一节问：这笔账能不能省？

合上书，推出 $\partial\ell/\partial\boldsymbol v_c=\bar{\boldsymbol u}-\boldsymbol u_o$，并说出这一步和 M.2.7 的 $\boldsymbol p-\boldsymbol y$ 有什么关系。

### 6. 词表有十万个词，每一步都要算十万项的分母吗？

例 5 只有 3 个候选，三个指数就算完了分母。真实的词表是 $V=10^5$，取 $d=300$，一个词对就要做 $3\times10^7$ 次乘加，语料有百亿词对。而一个词对真正关心的只是「正确答案」和少数几个容易混淆的词。

读者自然会想：只对得分最高的几个词算分母，不就省了吗？有两个问题：要知道哪几个最高，仍得先算出全部 $V$ 个得分；只在选定的候选里归一化，得到的也不再是原来全词表上的分布。

负采样的想法是换一个问题：**不再在全词表里猜哪个是上下文词，而是判断一对词是从语料里取出的，还是随机配出的**。对真实词对 $(c,o)$ 说「来自语料」（标签 1）；再从词表里随机抽 $K$ 个词 $n_1,\dots,n_K$，配成 $(c,n_k)$，说「随机配出」（标签 0）。随机配出的词对偶尔也会在语料里出现，这一点训练时不去区分。每个判断是一个逻辑回归（M.2.3）：词对 $(c,w)$ 带标签 1 的概率是 $\sigma(\boldsymbol u_w^{\mathsf T}\boldsymbol v_c)$。损失是二元交叉熵（M.2.4）：

$$\ell_{\text{NS}}=-\log\sigma(\boldsymbol u_o^{\mathsf T}\boldsymbol v_c)-\sum_{k=1}^{K}\log\sigma(-\boldsymbol u_{n_k}^{\mathsf T}\boldsymbol v_c).$$

负样本的项里用 $\sigma(-s)=1-\sigma(s)$，所以「标签 0 的二元交叉熵 $-\log(1-\sigma(s))$」写成 $-\log\sigma(-s)$。它背后的假设是：一个词对带标签 1 还是标签 0 服从伯努利分布。

为什么一定要有负词？如果只留第一项 $-\log\sigma(\boldsymbol u_o^{\mathsf T}\boldsymbol v_c)$，只要让所有向量指向同一个方向并不断变长，每个点积都趋于 $+\infty$，$\sigma\to1$，损失趋于 0，可是词与词一点也没有被区分开。负词那一项正是把「乱配的词对也得高分」罚回来。

**梯度。** 记 $s_o=\boldsymbol u_o^{\mathsf T}\boldsymbol v_c$，$s_k=\boldsymbol u_{n_k}^{\mathsf T}\boldsymbol v_c$。先对两种项各求对 $s$ 的导数。真词的项 $-\log\sigma(s)$：$\dfrac{\mathrm{d}}{\mathrm{d}s}(-\log\sigma(s))=-(1-\sigma(s))=\sigma(s)-1$（因为 $\sigma'=\sigma(1-\sigma)$，M.2.5）。负词的项：$\sigma(-s)=\dfrac1{1+e^{s}}$，所以 $-\log\sigma(-s)=\log(1+e^{s})$，导数 $\dfrac{e^s}{1+e^s}=\sigma(s)$。所以

$$\frac{\partial\ell_{\text{NS}}}{\partial s_o}=\sigma(s_o)-1,\qquad \frac{\partial\ell_{\text{NS}}}{\partial s_k}=\sigma(s_k),$$

这正是 M.2.5 的 $p-y$，真词的标签 $y=1$，负词的 $y=0$。再乘 $\partial s/\partial\boldsymbol v_c=\boldsymbol u$ 与 $\partial s/\partial\boldsymbol u=\boldsymbol v_c$：

$$\frac{\partial\ell_{\text{NS}}}{\partial\boldsymbol v_c}=(\sigma(s_o)-1)\boldsymbol u_o+\sum_{k=1}^{K}\sigma(s_k)\boldsymbol u_{n_k},\qquad \frac{\partial\ell_{\text{NS}}}{\partial\boldsymbol u_o}=(\sigma(s_o)-1)\boldsymbol v_c,\qquad \frac{\partial\ell_{\text{NS}}}{\partial\boldsymbol u_{n_k}}=\sigma(s_k)\boldsymbol v_c .$$

每步至多涉及 $1+K$ 个不同的上下文向量（若同一个词被重复抽中，就把它的各项梯度累加）和 1 个中心词向量，计算量是 $O((K+1)d)$。$K$ 常取 5 到 20，比 $V$ 小四个数量级。

**方法 6（负采样）**

1. 抽 $K$ 个负词，算 $s_o$ 和各个 $s_k$。
2. $\ell_{\text{NS}}=-\log\sigma(s_o)-\sum_k\log\sigma(-s_k)$。
3. 梯度：真词系数 $\sigma(s_o)-1$，负词系数 $\sigma(s_k)$，各自乘对方的向量。

**例 8**　中心词 $\boldsymbol v_c=(1,1)^{\mathsf T}$，真词 $\boldsymbol u_o=(1,1)^{\mathsf T}$，$K=2$ 个负词：$\boldsymbol u_{n_1}=(1,-1)^{\mathsf T}$，$\boldsymbol u_{n_2}=(0,-1)^{\mathsf T}$。求 $\ell_{\text{NS}}$ 和 $\nabla_{\boldsymbol v_c}\ell_{\text{NS}}$。

沿用例 5、例 7 的 $\boldsymbol v_c=(1,1)$ 和真词「鱼」，不再用 softmax，换成负采样：两个负词里，一个是例 5 里的「牛奶」$(1,-1)$，另一个是新的 $(0,-1)$。这次不用在全词表上归一化，只比较三个词与中心词的点积。

第一步，得分：$s_o=2$，$s_1=0$，$s_2=-1$。

第二步，损失：

$$\ell_{\text{NS}}=-\ln\sigma(2)-\ln\sigma(0)-\ln\sigma(1)\approx0.1269+0.6931+0.3133=1.1333 .$$

（负词 2 的项是 $-\ln\sigma(-s_2)=-\ln\sigma(1)$。）

第三步，梯度的系数：$\sigma(2)-1\approx-0.1192$，$\sigma(0)=0.5$，$\sigma(-1)\approx0.2689$。所以

$$\nabla_{\boldsymbol v_c}\ell_{\text{NS}}=-0.1192(1,1)+0.5(1,-1)+0.2689(0,-1)\approx(0.3808,\ -0.8881).$$

第四步，$\boldsymbol v_c$ 沿负梯度走一步（步长 $\eta$）。点积的变化量是 $-\eta\,\nabla\!\cdot\boldsymbol u$：真词 $+0.507\eta$，两个负词 $-1.269\eta$、$-0.888\eta$，也就是与真词的点积变大，与两个负词的点积变小。

> 同样的 $\boldsymbol v_c$，只用一个负词 $\boldsymbol u_{n}=(1,-1)^{\mathsf T}$（$K=1$）。求 $\ell_{\text{NS}}$。
>
> 答案：$s_o=2$，$s=0$，$\ell_{\text{NS}}=-\ln\sigma(2)-\ln\sigma(0)\approx0.12693+0.69315=0.82008\approx0.8201$。

**负词怎么抽？** 按词频直接抽，「的」「是」会占去大部分名额；按均匀抽，罕见词又抽得太多。Mikolov 等人的经验做法是按词频的 $3/4$ 次方抽（$3/4$ 是实验里选出的经验值）：$P(w)\propto f(w)^{3/4}$。

**例 9**　小语料的词频是：猫 2、狗 3、吃 3、喝 2、鱼 2、骨头 1、牛奶 1、水 1（共 15 个）。按 $f^{3/4}$ 抽，求「狗」和「水」被抽到的概率，并与直接按频率比较。

例 8 的负词是给定的，这里算负词按什么概率被抽出来，词频取第 1 节小语料里的次数。

$f^{3/4}$ 的值：$3^{0.75}\approx2.2795$，$2^{0.75}\approx1.6818$，$1^{0.75}=1$。八个词的总和是 $2.2795\times2+1.6818\times3+1\times3\approx12.604$。所以

$$P(\text{狗})\approx\frac{2.2795}{12.604}=0.1809\ (\text{按频率是 }0.2),\qquad P(\text{水})\approx\frac{1}{12.604}=0.0793\ (\text{按频率是 }0.0667).$$

下面两种训练方式放在一起对照。负采样换了一个目标，并不是完整 softmax 的数值近似：

| | 完整 softmax | 负采样 |
|---|---|---|
| 要回答的问题 | 全词表里哪个词是上下文词（$V$ 选 1） | 这一对词来自语料还是随机配出（$1+K$ 个是非题） |
| 损失 | 交叉熵 $-\log p(o\mid c)$ | $K+1$ 个二元交叉熵之和 |
| 每步用到的上下文向量 | $V$ 个 | $1+K$ 个 |
| 梯度中的 $p-y$ | 对 $V$ 个分数 | 对 $1+K$ 个分数 |

![完整 softmax 每步更新 $U_{\text{out}}$ 的全部 $V$ 行；负采样每步只更新真词和 $K$ 个负词的共 $K+1$ 行，阴影行是被更新的](fig/M9-n5.pdf){width=70%}

负采样让训练可行了，但它换了损失，训练出来的向量满足什么关系？下一节顺着这个损失的最优点回答，也借此解释那个出名的例子。

合上书，写出负采样的损失，推出 $\partial\ell_{\text{NS}}/\partial s$ 在两种情形下的值，并说明它为什么比完整 softmax 省。

### 7. 「国王 − 男人 + 女人 ≈ 女王」为什么能成立？

先看一个小情形。例 10 的手造二维向量里，国王减男人是 $(0.9,2.1)-(1.0,0.1)=(-0.1,\,2.0)$，女王减女人是 $(-1.1,1.9)-(-1.0,0.0)=(-0.1,\,1.9)$，两个差几乎相同：从「男人」到「国王」的那一段，和从「女人」到「女王」的那一段差不多。真实的词向量训练完成后也有这个性质：「国王 − 男人 + 女人」最接近「女王」。先猜一猜，这是巧合，还是训练目标逼出来的？答案是后者，下面把它推出来。

第 6 节的负采样损失，在最优点上有一个简洁的形式，类比就是由它推出来的（Levy 与 Goldberg 2014）。取一对中心词 $a$ 和上下文词 $k$，设语料里以 $a$ 为中心词配出的词对共 $N_a$ 个，其中上下文词是 $k$ 的有 $N_{ak}$ 个（$N_{ak}>0$），$P(k\mid a)=N_{ak}/N_a$。每个词对配 $K$ 个负词，负词按分布 $q$ 抽取，$k$ 被抽中的概率是 $q_k$。于是这一对词在全部训练中的损失，期望上是

$$-N_{ak}\log\sigma(s)-K\,N_a\,q_k\log\sigma(-s),\qquad s=\boldsymbol u_k^{\mathsf T}\boldsymbol v_a .$$

假设向量维数足够高（例如 $d\ge V$ 时，可以把每个词对安排在互不干扰的方向上），每一对的得分 $s$ 可以独立取值；$d$ 小时各得分通过共享的向量相互牵制，结论只是近似。那么最优的 $s$ 让上式对 $s$ 的导数为 0（两项系数都为正，二阶导数为正，驻点就是最小点）。用第 6 节的结果（$\sigma(s)-1$ 与 $\sigma(s)$ 两种导数）：

$$-N_{ak}\bigl(1-\sigma(s)\bigr)+KN_aq_k\,\sigma(s)=0\ \Longrightarrow\ e^{s}=\frac{\sigma(s)}{1-\sigma(s)}=\frac{N_{ak}}{KN_aq_k}.$$

（中间一步是 $\sigma(s)=\dfrac1{1+e^{-s}}$，所以 $\dfrac{\sigma(s)}{1-\sigma(s)}=e^{s}$。）

取对数：

$$\boldsymbol u_k^{\mathsf T}\boldsymbol v_a=\log P(k\mid a)-\log q_k-\log K .$$

有了它，对任意两个词 $a,b$ 和上下文词 $k$，两式相减，与 $a,b$ 无关的 $\log q_k$ 和 $\log K$ 都约掉了：

$$(\boldsymbol v_a-\boldsymbol v_b)^{\mathsf T}\boldsymbol u_k\approx\log\frac{P(k\mid a)}{P(k\mid b)} .$$

向量之差与每个上下文向量的点积，等于两个词的**概率之比**取对数。现在设「国王」之于「男人」的关系（王室）与「女王」之于「女人」的关系相同，具体就是：对每个上下文词 $k$，

$$\frac{P(k\mid\text{国王})}{P(k\mid\text{男人})}\approx\frac{P(k\mid\text{女王})}{P(k\mid\text{女人})}.$$

比如与王位相关的上下文词，对国王和女王都被放大，且倍数相近。这个条件不是白给的：只要有一个上下文词 $k$，国王与女王的放大倍数不一样，下面的差就不为 0，国王 − 男人 + 女人就不会正好落在女王上，这也是类比只对规律性强的关系成立的原因。两边取对数，两个对数比相等；再用上面的式子，两个点积就相等：

$$(\boldsymbol v_{\text{国王}}-\boldsymbol v_{\text{男人}})^{\mathsf T}\boldsymbol u_k\approx(\boldsymbol v_{\text{女王}}-\boldsymbol v_{\text{女人}})^{\mathsf T}\boldsymbol u_k\quad\text{对每个 }k .$$

记差向量 $\boldsymbol w=(\boldsymbol v_{\text{国王}}-\boldsymbol v_{\text{男人}})-(\boldsymbol v_{\text{女王}}-\boldsymbol v_{\text{女人}})$，上式说 $\boldsymbol w^{\mathsf T}\boldsymbol u_k\approx0$ 对每个 $k$ 成立。如果 $\boldsymbol u_k$ 张成整个 $\mathbb R^d$（即每个向量都能写成 $\boldsymbol u_k$ 的线性组合），就有 $\boldsymbol w=\sum_kc_k\boldsymbol u_k$。于是 $\boldsymbol w^{\mathsf T}\boldsymbol w=\sum_kc_k\,\boldsymbol w^{\mathsf T}\boldsymbol u_k\approx0$；而 $\boldsymbol w^{\mathsf T}\boldsymbol w=\lVert\boldsymbol w\rVert^2$，长度平方约等于 0，所以 $\boldsymbol w\approx\boldsymbol 0$，也就是 $\boldsymbol v_{\text{国王}}-\boldsymbol v_{\text{男人}}\approx\boldsymbol v_{\text{女王}}-\boldsymbol v_{\text{女人}}$，移项就是类比。**一种关系，在概率之比里是一个乘法因子，到了对数和向量里就是一个固定的差。**

**方法 7（类比）**

1. 算查询向量 $\boldsymbol q=\boldsymbol v_{\text{国王}}-\boldsymbol v_{\text{男人}}+\boldsymbol v_{\text{女人}}$。
2. 在词表里找与 $\boldsymbol q$ 余弦最大的词，**排除三个输入词本身**。

**例 10**　手造的二维词向量（第一维大致表示性别，第二维表示王室程度）：国王 $(0.9,2.1)$、女王 $(-1.1,1.9)$、男人 $(1.0,0.1)$、女人 $(-1.0,0.0)$、王子 $(0.8,1.2)$、公主 $(-0.9,1.1)$、苹果 $(0.1,-1.5)$。求「国王 − 男人 + 女人」最近的词。

就是上面用过的那几个向量，现在把完整的一步做完：先算查询向量，再按余弦在全部词里找最近的词。

查询向量：$\boldsymbol q=(0.9-1.0-1.0,\ 2.1-0.1+0.0)=(-1.1,\ 2.0)$。与几个词的余弦：女王 $0.9998$，公主 $0.9833$，王子 $0.4617$，苹果 $-0.9063$（国王本身是 0.6155，被排除）。最近的是「女王」。

> 同样的向量，求「王子 − 男人 + 女人」最近的词（排除三个输入词）。
>
> 答案：查询向量 $(0.8-1.0-1.0,\ 1.2-0.1+0.0)=(-1.2,\ 1.1)$；余弦：公主 $0.9898$，女王 $0.9541$，国王 $0.3307$，苹果 $-0.7233$。最近的是「公主」。

![类比是一个平行四边形：国王与男人的差、女王与女人的差近似是同一个方向，平行四边形的第四个顶点是查询向量，落在女王附近](fig/M9-n6.pdf){width=70%}

必须排除输入词本身，是因为 $\boldsymbol q$ 有时会靠近某个输入词；例 10 里 $\boldsymbol q$ 离女王更近，但国王的余弦也有 0.6155。类比也不是处处成立：关系越有规律，结果通常越好，其余情形的准确率要低得多。

类比只用到词和它的上下文词的关系。下一节问：如果「词」换成图片，「上下文」换成配对的说明文字，同样的损失还能用吗？

合上书，推出 $(\boldsymbol v_a-\boldsymbol v_b)^{\mathsf T}\boldsymbol u_k$ 与对数概率比的关系，并解释类比为什么需要「每个 $k$ 的概率比相同」这个条件。

### 8. 图片和文字能不能放进同一个向量空间？

词向量学到的是「文字之间」的相近。2021 年，OpenAI 的 CLIP 把同样的想法用到文字和图片之间：用约 4 亿对（图片，说明文字），训练一个图像编码器（把图片变成向量的网络，常用 M.8 的卷积网络或 Transformer）和一个文本编码器，把图片和文字都映射到同一个向量空间，使得**配对的图文向量靠得近，不配对的离得远**。

先看最小的情形，一批只有 2 对：猫的图片配「一只猫」，狗的图片配「一条狗」。对猫的图片，两段文字是候选，正确的是前一段。这和 skip-gram 里「从候选词里挑出真实的上下文词」是同一类问题，只是候选换成了批内的文字。

怎么写成损失？取一个批次，$N$ 对（图片，文字），图片向量 $\boldsymbol a_i$、文字向量 $\boldsymbol b_j$，都已经归一成长度 1。相似度矩阵 $S_{ij}=\boldsymbol a_i^{\mathsf T}\boldsymbol b_j=\cos$，除以**温度** $\tau>0$（它控制 softmax 有多尖：$\tau$ 小，分数之间的差距被放大，配对与不配对的区别就被强调），得到分数 $z_{ij}=S_{ij}/\tau$。对第 $i$ 张图片，把批内 $N$ 段文字都看作候选，正确答案是第 $i$ 段，这就是一个 $N$ 选 1 的分类问题（M.2.7）：

$$\ell_i=-\log\frac{\exp(z_{ii})}{\sum_{j=1}^{N}\exp(z_{ij})}.$$

这个损失叫 **InfoNCE**。它**就是 softmax 交叉熵**，标签是对角线；梯度也是 $\partial\ell_i/\partial z_{ij}=p_{ij}-y_{ij}$，$y_{ij}=1$ 当且仅当 $j=i$。对照第 4 节：skip-gram 是「中心词的候选是全词表」，InfoNCE 是「图片的候选是批内的其他文字」，把其他样本当作免费的负样本。CLIP 还对文字做同样的一遍（对第 $j$ 段文字，在批内 $N$ 张图片里选），两个方向取平均。

**方法 8（InfoNCE）**

1. 算相似度矩阵 $S$，除以 $\tau$ 得 $Z$。
2. 对每一行做 softmax，取对角元的 $-\log$，得到 $\ell_i$；对每一列做同样的事得到另一个方向的损失。
3. 总损失是行损失平均与列损失平均的均值。

**例 11**　$N=3$，$\tau=0.5$，相似度矩阵（行：图片，列：文字）

$$S=\begin{pmatrix}0.8&0.1&0.3\\0.2&0.7&0.0\\0.1&0.2&0.9\end{pmatrix}.$$

求第一张图片的损失 $\ell_1$，以及三个行损失的平均。

和例 5 相比，三个候选词的得分换成了一张图片对三段文字的相似度除以 $\tau$，其余完全一样：对一行做 softmax，取正确位置的 $-\log$。

分数 $Z=S/0.5$，第一行是 $(1.6,0.2,0.6)$。分母 $e^{1.6}+e^{0.2}+e^{0.6}\approx4.953+1.221+1.822=7.997$，所以 $p_{11}=4.953/7.997\approx0.6194$，

$$\ell_1=-\ln0.6194\approx0.4790 .$$

同样算得 $\ell_2\approx0.4790$，$\ell_3\approx0.3705$，平均 $\approx0.4428$。按列做另一个方向，列损失平均 $\approx0.4440$，总损失 $\approx0.4434$。如果所有相似度都相等，每行的 $p_{ii}=1/3$，损失是 $\ln3\approx1.0986$。0.44 远低于它，说明对角线（配对）的分数明显高于其余。

> 温度减小到 $\tau=0.1$，其余同例 11，第一行的 $p_{11}$ 是变大还是变小？
>
> 答案：变大。$\tau=0.1$ 时第一行分数是 $(8,1,3)$，$p_{11}=\dfrac{e^8}{e^8+e^1+e^3}\approx0.9924$。温度越低，softmax 越尖，已经分对的样本损失越小。

![相似度矩阵：对角线是配对，每一行做一次 softmax，阴影的对角格是这一行要最大化概率的目标（即最小化它的负对数）](fig/M9-n7.pdf){width=70%}

**回到开头的问题。** 搜「手机壳」为什么能找到「保护套」？把词变成向量，再比余弦。独热向量下任何两个不同词的余弦都是 0，无从比较；共现向量下「猫」「狗」是 0.9487（例 2）；嵌入下是 0.976（例 4，手造的数）。真正的词向量由 skip-gram（配合负采样）在大语料上训练出来，第 5、6 节算出了每一步怎样更新；图片搜索则靠本节的损失，把图片和文字放进同一个空间，再比余弦。

合上书，写出 InfoNCE 的损失，说明它为什么是 softmax 交叉熵，以及它和 skip-gram 的损失相差在哪里。

### 本章小结

按本册的三件套，这一章的模型是两张嵌入矩阵加 softmax，损失是上下文词的交叉熵（负采样时换成二元交叉熵），更新仍是梯度下降；梯度里再一次出现 $\boldsymbol p-\boldsymbol y$。

本册的「损失 ⇐ 概率假设」表，本章新增三行：

| 损失或做法 | 背后的概率假设 | 出现章 |
|---|---|---|
| skip-gram 的交叉熵 | 上下文词服从类别分布（softmax） | M.9 |
| 负采样的二元交叉熵 | 词对带标签 1 还是 0 服从伯努利分布 | M.9 |
| InfoNCE | 配对是哪一个，服从批内的类别分布 | M.9 |

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（词表与独热向量） | 编号、独热、正交；独热矩阵的乘积 | M9-01 |
| 方法 2（共现向量与余弦） | 数窗口里的共现；比较两个词 | M9-05 |
| 方法 3（嵌入查表） | 取行；算 $OE$ 的形状和参数个数 | M9-02 |
| 方法 4（skip-gram 的前向） | 算得分、概率和单个词对的损失 | M9-03、M9-05、M9-06、M9-12 |
| 方法 5（skip-gram 的梯度） | 求 $\nabla_{\boldsymbol v_c}$、$\nabla_{\boldsymbol u_w}$ 并更新 | M9-07、M9-11、M9-12 |
| 方法 6（负采样） | 算 $\ell_{\text{NS}}$、梯度和采样概率 | M9-08、M9-09 |
| 方法 7（类比） | 算查询向量，按余弦找最近词 | M9-15（混合） |
| 方法 8（InfoNCE） | 由相似度矩阵算行、列损失 | M9-04、M9-10 |
