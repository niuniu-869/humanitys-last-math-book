## M.10 · 序列模型：语言模型、循环网络、LSTM 与编码器–解码器

手机输入法在你打完「我爱」之后，会在键盘上方列出几个候选词；翻译软件把一整句中文变成英文；大模型一个词一个词地写出一段回答。它们都可以按顺序预测下一个词，也就是给定前面已经出现的词，估计下一个词是什么；翻译还要把原句作为条件。句子是有先后的一串词，长度不固定，前面的词会影响后面的词。M.9 只教会了我们给每个词一个向量，还没有说怎样处理「一串」词。

这个任务的历史很长。1913 年，马尔可夫统计了普希金《叶甫盖尼·奥涅金》里元音和辅音一个接一个出现的频率，发现下一个字母的种类确实依赖前一个。1948 年，香农用同样的想法生成英文：只看前面几个字母，按统计出的概率抽下一个，写出来的东西越来越像英语。这种只看前几个词的模型叫 n 元语法，它简单有效，但看不到窗口以外的词。

1990 年，Elman 想到让模型自己带一个反复更新的状态，每读一个词就改写一次，让状态逐步概括前文，这就是循环网络。可是 1991 年，Hochreiter 分析发现，这类网络的梯度沿着时间传递时可能指数衰减，也可能急剧增长，难以学习长距离依赖；他和 Schmidhuber 在 1997 年提出了 LSTM，用加法式的更新让信息和梯度更容易传远（本章第 7 节讲的是后来加上遗忘门的常用形式）。2014 年，Sutskever 等人与 Cho 等人用两个循环网络做机器翻译：一个把原句读成一个向量，另一个由这个向量生成译文。同一年，Bahdanau、Cho 与 Bengio 指出，把整句话压进一个定长向量是瓶颈，提出让译文的每个词回头去看原句的每个词，这就是注意力。2016 年上线的谷歌神经机器翻译用的就是循环网络加注意力。注意力也是下一章的出发点。

本册每个模型都是同一个三件套。本章这一行是：模型 $f_\theta$ 是循环网络，每一步读一个词、更新一个状态、输出下一个词的概率分布；损失 $L$ 是下一个词的交叉熵（也就是平均负对数似然）；更新规则仍是梯度下降，只是梯度要沿着时间往回传。

第 1、2 节说清语言模型做什么、怎样评价；第 3 节看最简单的 n 元语法；第 4、5 节是循环网络和它的梯度；第 6、7 节讲远处传回的梯度为什么容易变小或变大，LSTM 怎样缓解（第 8 节的 GRU 是它的简化版）；第 9、10 节用两个循环网络做翻译，再让译文回头去看原句。

### 1. 语言模型每一步在做什么？

先看一个具体的句子：「我 爱 你 。」，4 个词（句号也算一个词）。它出现的概率是多少？P.2 的乘法公式把联合概率拆成条件概率的连乘：

$$P(w_1,w_2,w_3,w_4)=P(w_1)\,P(w_2\mid w_1)\,P(w_3\mid w_1,w_2)\,P(w_4\mid w_1,w_2,w_3).$$

每一个因子都是同一类问题：已知前面的词，下一个词的分布是什么。在句首补一个起始符 $\langle s\rangle$，$P(w_1)$ 也能写成 $P(w_1\mid\langle s\rangle)$，于是任何句子 $w_1,\dots,w_T$ 的概率都是

$$P(w_1,\dots,w_T)=\prod_{t=1}^{T}P(w_t\mid w_{<t}),$$

其中 $w_{<t}$ 表示 $w_1,\dots,w_{t-1}$。按这种从左到右的方式一个词一个词地预测，叫**自回归**，能给出这个分布的模型叫**语言模型**。

这里的连乘给出这 $T$ 个词依次出现的概率。本节例子用句号作结束符号，它已经是第 $T$ 个词；若只数到最后一个内容词，还要把结束符号作为最后一个预测目标。为什么要这样？如果不预测结束，模型读完 $T$ 个词后还可以接着写，长度为 $T$、$T+1$、$T+2$ 的序列各分到一部分概率；只有乘上一个「到此结束」的概率，所有长度的完整句子的概率加起来才是 1。

怎样让模型给出这个分布？词表（所有词的集合）记作 $\mathcal V$，它有 $|\mathcal V|$ 个词时，每一步让模型输出 $|\mathcal V|$ 个分数（logits），再用 M.2.7 的 softmax 变成概率。这正是老朋友④：下一个词只有三个候选，分数 $(2,1,0)$，softmax 得到 $(0.6652,0.2447,0.0900)$。若正确的下一个词是第一个，这一步的交叉熵是 $-\ln\dfrac{e^2}{e^2+e+1}\approx0.4076$（用未舍入的概率算；若先舍入成 0.6652 再取对数，会得到 0.4077）。

怎样训练？用最大似然（P.11）：让训练文本的概率尽量大。取对数以后，因为 $\ln(ab)=\ln a+\ln b$，连乘变成连加；再取负号，变成一个要最小化的数；最后对长度取平均，就得到训练的损失：

$$L=-\frac1T\sum_{t=1}^{T}\ln P_\theta(w_t\mid w_{<t}).$$

它就是每个位置上「正确词的交叉熵」的平均（P.14）。注意这一个句子同时提供了 $T$ 个训练样本：每个位置都是一道「看前文，猜下一个词」的题，答案就在句子里，不需要人来标注。

**方法 1（自回归分解与平均负对数似然）**

1. 把句子拆成 $T$ 个位置，第 $t$ 个位置的输入是 $w_{<t}$，目标是 $w_t$。
2. 取模型给目标词的概率 $p_t=P_\theta(w_t\mid w_{<t})$，句子的概率是 $\prod p_t$。
3. 损失是 $L=\frac1T\sum(-\ln p_t)$。用平均而不是求和，是为了让不同长度的句子可比。

**例 1**　给四个正数 $p_1=\dfrac{e^2}{e^2+e+1},\ p_2=\dfrac12,\ p_3=\dfrac14,\ p_4=\dfrac45$，求 $F=p_1p_2p_3p_4$ 和 $G=-\dfrac14\sum_{t=1}^{4}\ln p_t$。

可以把这四个数看成某个模型读「我 爱 你 。」时，四个位置上给正确词的概率：那么 $F$ 是句子的概率，$G$ 是损失 $L$。其中 $p_1\approx0.6652409558$ 正是老朋友④里分数 $(2,1,0)$ 经 softmax 得到的第一个概率。下面用未舍入的值计算，结果再取近似值。

乘积是

$$F=0.6652410\times0.5\times0.25\times0.8\approx0.0665241.$$

每个位置的 $-\ln p_t$ 分别是

$$0.4076,\qquad 0.6931,\qquad 1.3863,\qquad 0.2231,$$

其中第三个是 $-\ln0.25=2\ln2$。以上逐项展示的值保留了四位小数；用未舍入的负对数相加，得到约 $2.7101911$，除以 4 得 $G\approx0.6775478\approx0.6775$。

注意连乘的结果 0.0665 很小，句子再长就会小到计算机存不下（下溢），所以实际计算总是取了对数以后相加。

> 一个模型读三个词的句子，正确词的概率是 $0.5,\ 0.5,\ 0.25$，求 $L$。
>
> 答案：$-\ln0.5=0.6931$，$-\ln0.25=1.3863$，$L=(0.6931+0.6931+1.3863)/3\approx0.9242$。

合上书，写出句子概率的连乘分解，再说明损失为什么是每个位置交叉熵的平均。

这个 $L$ 是对数尺度上的数，它的大小本身还说不出模型好坏。下一节把它换成一个更直观的数。

### 2. 两个语言模型哪个更好，怎样用一个数来比？

例 1 里的 $L=0.6775$（按语言模型的说法，$G$ 就是损失 $L$）到底是好还是坏，没有参照物很难说。能不能把它换成一个更直观的数？

直接的想法是把各位置的概率取算术平均，再取倒数。这样不行：句子的概率是各位置概率的连乘，不是连加，算术平均对应不了任何一个句子的概率；而几何平均 $\bar p=(\prod p_t)^{1/T}$ 恰好满足「每一步都取 $\bar p$，连乘 $T$ 次得到的就是句子的概率」。所以要用几何平均，它的倒数就是下面的困惑度。

先看一个极端情形：模型对每一步都在 $k$ 个词里均匀地猜，即每个位置给正确词的概率都是 $1/k$。这时 $-\ln p_t=\ln k$，平均也是 $\ln k$。要想从 $L$ 还原出 $k$，两边取指数。把这个想法用到一般的模型上，定义

$$\mathrm{PPL}=e^{L}=\Bigl(\prod_{t=1}^{T}p_t\Bigr)^{-1/T},$$

叫**困惑度**。第二个等号分两步：$\sum\ln p_t=\ln\prod p_t$，所以 $e^{L}=\bigl(e^{\ln\prod p_t}\bigr)^{-1/T}=\bigl(\prod p_t\bigr)^{-1/T}$。它是各位置概率的几何平均的倒数。解释是：模型平均而言，相当于每一步在 $\mathrm{PPL}$ 个词里均匀地猜。均匀地猜 $|\mathcal V|$ 个词的困惑度恰好是 $|\mathcal V|$，每步都百分百猜对时是 1。所以困惑度最小是 1，超过 $|\mathcal V|$ 就说明模型还不如均匀地乱猜。

**方法 2（困惑度）**

1. 先按方法 1 算出平均负对数似然 $L$（自然对数）。
2. $\mathrm{PPL}=e^{L}$；若 $L$ 用以 2 为底的对数算（单位是比特），则 $\mathrm{PPL}=2^{L}$，结果相同。
3. 比较两个模型时，必须用同一份测试文本、同一个词表和切词方式，数小的更好。

**例 2**　接例 1。第一组正数就是例 1 的 $p_1,\dots,p_4$，第二组是 $0.4,\ 0.4,\ 0.2,\ 0.5$。分别求各组四个数的几何平均的倒数，比较大小。

把两组数看成模型 A、B 在同一句话的四个位置上给正确词的概率，这两个数就是两个模型的困惑度。例 1 已经给出第一组的平均负对数 $L=0.6775$，所以

$$\mathrm{PPL}_A=e^{0.6775}\approx1.97.$$

第二组的四个负对数分别是 $0.9163,\ 0.9163,\ 1.6094,\ 0.6931$，平均 $L=1.0338$，

$$\mathrm{PPL}_B=e^{1.0338}\approx2.81.$$

模型 A 的困惑度小，所以更好。直观上，A 每一步平均相当于在不到 2 个词里选，B 要在近 3 个词里选。

和例 1 不同的是，这里已经不再关心每个位置的细节，只比较一个数。

下面这道题请对比两种平均。

> 两个位置上正确词的概率是 $1/2$ 和 $1/8$。分别求 $\mathrm{PPL}$，以及「平均猜词数」$\frac12(2+8)$。
>
> 答案：$L=\frac12(\ln2+\ln8)=2\ln2$，$\mathrm{PPL}=e^{2\ln2}=4$；而算术平均是 5。困惑度是各位置概率倒数的几何平均，本题为 $\sqrt{2\cdot8}=4$，小于算术平均 5；难预测的位置仍会提高困惑度，只是两种平均汇总它的方式不同。

困惑度有两处容易误读。它依赖词表和切词方式：把同一段文字切成字和切成词，$T$ 与 $p_t$ 都变了，两个数不能直接比。它也只衡量「预测得准不准」，不衡量生成的句子好不好读。

合上书，说出困惑度为什么等于「均匀猜多少个词」，并写出当每个位置的概率都是 $1/k$ 时它等于几。

困惑度要用模型给出的概率来算。最简单的模型是什么，它的概率又从哪里来？下一节看一个只靠数数的办法。

### 3. 只看前面几个词，能不能估出下一个词的概率？

这一节先了解做法即可。

要估 $P(\text{你}\mid\text{我},\text{爱})$，最直接的办法是在语料里数「我 爱」出现了多少次，其中后面跟「你」的有几次。前文只有两个词时还行；一般地估 $P(w_t\mid w_1,\dots,w_{t-1})$，条件越来越长，不同的前文太多，数据里几乎没有重复。马尔可夫的办法是只看最近的几个词：**二元语法**（bigram）假设

$$P(w_t\mid w_{<t})\approx P(w_t\mid w_{t-1}),$$

只看前一个词。这个假设就叫**马尔可夫假设**。一般的 $n$ 元语法使用最近的 $n-1$ 个词预测下一个词，$n$ 是这个连续片段的总词数，二元语法就是 $n=2$。估计的方法是数数：

$$\widehat P(b\mid a)=\frac{c(a,b)}{\sum_{v\in\mathcal V}c(a,v)},\qquad \sum_{v\in\mathcal V}c(a,v)>0.$$

$c(a,b)$ 是相邻符号对 $(a,b)$ 的次数，分母是以 $a$ 为前项的全部符号对的次数。句末的终止符不再作为前项；若某个前项一次也没有出现过，这个比值不能计算，需要另作约定，例如后面说的平滑。

为什么数频率就是对的？对一个已有后继计数的前项 $a$，它后面接各个词的次数 $c_b=c(a,b)$ 是已知的，最大似然（P.11.3 中类别分布的结论）要最大化 $\sum_bc_b\ln p_b$，约束是 $\sum p_b=1$，解正是 $p_b=c_b/\sum c_b$。也就是说，这一行的相对频率就是最大似然估计。

**方法 3（n 元语法的计数估计）**

1. 在句首补 $\langle s\rangle$，句末补句号，数出所有相邻词对的次数 $c(a,b)$。
2. 条件概率 = $c(a,b)$ ÷ 以 $a$ 为前项的全部词对次数之和（要求这个和大于零）。
3. 句子概率是各个条件概率之积。

**例 3**　给有限符号集合 $\{a,b,c,d\}$ 上的相邻对计数，起点记 $\langle s\rangle$，终点记 $\langle/s\rangle$：

| 前项 | 后接的符号和次数 |
|---|---|
| $\langle s\rangle$ | $a$ 2 次，$c$ 1 次 |
| $a$ | $b$ 2 次，$\langle/s\rangle$ 1 次 |
| $b$ | $c,d,a$ 各 1 次 |
| $c$ | $\langle/s\rangle$ 1 次，$b$ 1 次 |
| $d$ | $\langle/s\rangle$ 1 次 |

逐行归一化，求路径 $\langle s\rangle,a,b,c,\langle/s\rangle$ 的概率，并判断路径 $\langle s\rangle,d,b,c,\langle/s\rangle$ 的概率。

例 1、例 2 的概率是现成给出的，这次要自己从计数表里一行一行除出来，再连乘。把 $a,b,c,d$ 想成词，这就是二元语法在小语料上的估计。

先看每一行的总数：$\langle s\rangle$ 行共 3 次，$a$ 行共 3 次，$b$ 行共 3 次，$c$ 行共 2 次。于是 $\hat P(a\mid\langle s\rangle)=2/3$，$\hat P(b\mid a)=2/3$，$\hat P(c\mid b)=1/3$，$\hat P(\langle/s\rangle\mid c)=1/2$。

$$\frac23\cdot\frac23\cdot\frac13\cdot\frac12=\frac{2}{27}\approx0.0741.$$

再看第二条路径。$\langle s\rangle$ 行里没有 $d$，$\hat P(d\mid\langle s\rangle)=0$（后面 $d$ 行里也没有 $b$，$\hat P(b\mid d)=0$），整个连乘变成 0，困惑度成了无穷大。可是这条路径完全可能出现，只是计数太少，没见过。

这就是 n 元语法的第一个毛病：**数据稀疏**。$n$ 越大，可能的词组合越多，没见过的就越多。

> 沿用例 3 的表，求路径 $\langle s\rangle,c,b,a,\langle/s\rangle$ 的概率。
>
> 答案：$\hat P(c\mid\langle s\rangle)=\frac13$，$\hat P(b\mid c)=\frac12$，$\hat P(a\mid b)=\frac13$，$\hat P(\langle/s\rangle\mid a)=\frac13$，连乘得 $\frac1{54}\approx0.0185$。

补救办法是**平滑**：给每个次数都加 1，让没见过的组合也有一点概率，但这只是治标。

> 设某个前项后面接三个候选符号 $c,d,a$ 的次数是 $(1,0,1)$。对每个候选的次数都加 1，求这一行新的条件分布。
>
> 答案：加 1 后次数是 $(2,1,2)$，原来的总数 2 加上三个候选各加的 1，新总数是 5，所以分布为 $(2/5,\ 1/5,\ 2/5)$。平滑时分母也要随着加上候选个数，不能只改分子。

第二个毛病是**窗口太短**：二元语法只看前一个词，远处的词管不到。「那几个昨天刚从外地赶来的学生，现在都坐在……」，决定后面用什么词的是句首的「学生」，中间隔了十几个字。窗口开大到十几个词，需要数的组合就多到不可能。

循环网络的想法是换一种记忆方式：不用数前文的每一种组合，而是把前文压成一个固定大小的向量，由网络去学这个向量里该放什么。

合上书，写出二元语法的估计公式，并说明为什么没见过的词对会让困惑度变成无穷大。

### 4. 怎样让模型记住任意长的前文？

我们要一个对任意长的前文都管用的办法，而且参数不能随句子变长。做法是让模型带着一个固定大小的**状态** $\boldsymbol h_t\in\mathbb R^{d_h}$，每读一个词就更新一次。每一步做三件事，依次是更新状态、算输出分数、把分数变成概率：

$$\boldsymbol h_t=\tanh(W\boldsymbol h_{t-1}+U\boldsymbol x_t+\boldsymbol b),$$

$$\boldsymbol o_t=W_{\mathrm{out}}\boldsymbol h_t+\boldsymbol b_{\mathrm{out}},$$

$$\boldsymbol p_t=\mathrm{softmax}(\boldsymbol o_t).$$

各个量的形状分四组交代。输入：$\boldsymbol x_t\in\mathbb R^{d_x}$ 是第 $t$ 个词的词向量（M.9.3 的嵌入）。状态：$\boldsymbol h_t\in\mathbb R^{d_h}$，初始状态 $\boldsymbol h_0=\boldsymbol 0$。输出：$\boldsymbol o_t,\boldsymbol p_t\in\mathbb R^{|\mathcal V|}$。参数：$W\in\mathbb R^{d_h\times d_h}$，$U\in\mathbb R^{d_h\times d_x}$，$\boldsymbol b\in\mathbb R^{d_h}$，$W_{\mathrm{out}}\in\mathbb R^{|\mathcal V|\times d_h}$，$\boldsymbol b_{\mathrm{out}}\in\mathbb R^{|\mathcal V|}$。输出层的矩阵和偏置记作 $W_{\mathrm{out}}$、$\boldsymbol b_{\mathrm{out}}$（out 是 output 的缩写），这样 $V$、$\boldsymbol c$ 这些字母留给后面的注意力和细胞状态用（粗体 $\boldsymbol c_t$ 是向量，与计数、阈值里的标量 $c$ 不同）。

这里用的是列向量，$W\boldsymbol h$ 是矩阵乘向量（L.3）。$\tanh$ 是 M.7.2 的激活函数，把每个分量压进 $(-1,1)$。

两个要点。第一，$\boldsymbol h_t$ 里有 $\boldsymbol h_{t-1}$，而 $\boldsymbol h_{t-1}$ 里有 $\boldsymbol h_{t-2}$，一直追到开头，所以 $\boldsymbol h_t$ 是 $\boldsymbol x_1,\dots,\boldsymbol x_t$ 的函数：它是全部前文的概括。第二，**每一步用的是同一组 $W,U,\boldsymbol b$**。所以把输入词向量视为给定，只统计这里的循环单元和输出层，参数个数是 $d_h^2+d_hd_x+d_h+|\mathcal V|d_h+|\mathcal V|$，与句子多长无关。

把循环画成按时间展开的样子，就是一条链：同一个格子被复制 $T$ 份，每份接收上一份的状态。展开以后它是一张很深的普通网络（M.7.4 的计算图），深度等于句子长度，只是各层共享参数。

![展开后的循环网络：每个时刻的格子共用同一组 $W,U,\boldsymbol b$（同一线型的标注表示同一参数）；实线箭头向右传状态，虚线向上经输出层 $W_{\mathrm{out}},\boldsymbol b_{\mathrm{out}}$（各时刻也共用）和 softmax 给出概率分布](fig/M10-n1.pdf){width=85%}

从这里开始，$t$ 表示一次读入并预测的步骤。读入 $w_t$ 后，$\boldsymbol p_t$ 给出下一个词 $w_{t+1}$ 的分布，$\boldsymbol y_t$ 表示这一步目标词对应的独热向量。若需要计入首词的概率，就先读入起始符再预测首词。下面的例 4 只计算「给定我，预测爱」和「给定我、爱，预测你」这两个目标位置，因此求的是两步条件损失，不含首词和终止符的损失。这里的下标比第 1 节错开了一位，用例 4 对一下：

| 步骤 $t$ | 读入 | 给出的分布 | 目标 |
|---|---|---|---|
| 1 | 我（$\boldsymbol x_1$） | $\boldsymbol p_1$ | 爱 |
| 2 | 爱（$\boldsymbol x_2$） | $\boldsymbol p_2$ | 你 |

**方法 4（前向展开）**

1. 从 $\boldsymbol h_0=\boldsymbol 0$ 出发，依次算 $\boldsymbol a_t=W\boldsymbol h_{t-1}+U\boldsymbol x_t+\boldsymbol b$，$\boldsymbol h_t=\tanh\boldsymbol a_t$。
2. 每步算 $\boldsymbol o_t=W_{\mathrm{out}}\boldsymbol h_t+\boldsymbol b_{\mathrm{out}}$，再 softmax 得 $\boldsymbol p_t$。
3. 目标词的概率 $p_t$ 按方法 1 汇总成损失。

**例 4**　取词表 $\{\text{我},\text{爱},\text{你}\}$，词向量用老朋友③的三个向量：我 $=(1,0)$，爱 $=(0,1)$，你 $=(1,1)$。参数取 $W=\begin{pmatrix}0.5&-0.5\\0.25&0.5\end{pmatrix}$（老朋友②里的 $W_1$），$U=I$，$\boldsymbol b=\boldsymbol 0$，$W_{\mathrm{out}}=\begin{pmatrix}1&0\\0&1\\-1&-1\end{pmatrix}$（三行依次对应我、爱、你），$\boldsymbol b_{\mathrm{out}}=\boldsymbol 0$。训练句子是「我 爱 你」：输入「我」，目标「爱」；输入「爱」，目标「你」。求损失。

这里是把方法 4 的前向算出的概率交给方法 1 取平均负对数。参数是随手取的，还没有训练，预测应当不好。

第 1 步，$\boldsymbol h_0=\boldsymbol0$，所以 $\boldsymbol a_1=U\boldsymbol x_1=(1,0)$，

$$\boldsymbol h_1=\tanh(1,0)=(0.7616,\ 0),\qquad \boldsymbol o_1=W_{\mathrm{out}}\boldsymbol h_1=(0.7616,\ 0,\ -0.7616).$$

softmax 得 $\boldsymbol p_1=(0.5935,\ 0.2771,\ 0.1294)$。目标词是「爱」，$p=0.2771$，$-\ln p=1.2833$。

第 2 步，现在要用到上一步的状态：

$$\boldsymbol a_2=W\boldsymbol h_1+U\boldsymbol x_2=\begin{pmatrix}0.3808\\0.1904\end{pmatrix}+\begin{pmatrix}0\\1\end{pmatrix}=\begin{pmatrix}0.3808\\1.1904\end{pmatrix},$$

$$\boldsymbol h_2=\tanh\boldsymbol a_2=(0.3634,\ 0.8307),\qquad \boldsymbol o_2=(0.3634,\ 0.8307,\ -1.1941),\qquad \boldsymbol p_2=(0.3563,\ 0.5686,\ 0.0751).$$

目标词是「你」，$p=0.0751$，$-\ln p=2.5894$。

两步的平均是 $L=(1.2833+2.5894)/2\approx1.9364$。这个模型的困惑度 $e^{1.9364}\approx6.9$，比三个词均匀地猜（困惑度 3）还差，原因是参数没有训练过。

> 同样的参数，输入「你」再输入「我」，求 $\boldsymbol h_1$ 与 $\boldsymbol h_2$。
>
> 答案：$\boldsymbol a_1=(1,1)$，$\boldsymbol h_1=(0.7616,0.7616)$；$\boldsymbol a_2=W\boldsymbol h_1+(1,0)=(1,\ 0.5712)$，$\boldsymbol h_2=(0.7616,\ 0.5162)$。

下一步的问题是：参数 $W,U$ 都出现在每个时刻里，求梯度时它们怎么算。合上书，写出循环网络的状态更新式，说出哪些量在不同时刻共用。

### 5. 循环网络的梯度怎么求？

展开以后，循环网络就是一张深度为 $T$ 的计算图。M.7 的反向传播规则可以原样用，只需要处理一件事：同一个参数出现在很多个位置。

先看三个词的情形。$\boldsymbol h_1=\tanh(U\boldsymbol x_1+\boldsymbol b)$ 里没有 $W$（因为 $\boldsymbol h_0=\boldsymbol0$），$\boldsymbol h_2=\tanh(W\boldsymbol h_1+\cdots)$ 与 $\boldsymbol h_3=\tanh(W\boldsymbol h_2+\cdots)$ 里各有一个 $W$。把 $W$ 改动一点，$\boldsymbol h_2$ 和 $\boldsymbol h_3$ 都会变，损失沿两条路受到影响，所以 $W$ 的梯度应当是两项之和。一般有 $T$ 项，其中第一步 $\boldsymbol h_0=\boldsymbol0$，这一项为零。下面把一般情形的推导写完整。

记号：$\ell_t=-\ln(\boldsymbol p_t)_{y_t}$ 是第 $t$ 步的损失，其中 $y_t$ 是本步目标类别的编号（$(\boldsymbol p_t)_{y_t}$ 即模型给目标词的概率），$L=\frac1T\sum\ell_t$，这里 $T$ 是计入损失的步数。引入「误差信号」$\boldsymbol\delta_t:=\partial L/\partial\boldsymbol a_t\in\mathbb R^{d_h}$，也就是损失对第 $t$ 步线性部分 $\boldsymbol a_t$ 的梯度。

**第 1 步：输出层。** 由 M.2.7，softmax 加交叉熵对分数的梯度是概率减独热向量：$\partial\ell_t/\partial\boldsymbol o_t=\boldsymbol p_t-\boldsymbol y_t$，其中 $\boldsymbol y_t$ 是目标词的独热向量。因为 $L$ 里有因子 $1/T$，所以 $\partial L/\partial\boldsymbol o_t=(\boldsymbol p_t-\boldsymbol y_t)/T$。再由 M.7.9 的线性层反向公式，传给 $\boldsymbol h_t$ 的是 $W_{\mathrm{out}}^{\mathsf T}(\boldsymbol p_t-\boldsymbol y_t)/T$。

**第 2 步：$\boldsymbol h_t$ 的梯度有两个来源。** $\boldsymbol h_t$ 被用了两次：一次给第 $t$ 步的输出层，一次进入第 $t+1$ 步的 $\boldsymbol a_{t+1}=W\boldsymbol h_t+\dots$。这是 M.7.6 的分叉，两条路上的梯度相加：

$$\frac{\partial L}{\partial\boldsymbol h_t}=\frac{1}{T}W_{\mathrm{out}}^{\mathsf T}(\boldsymbol p_t-\boldsymbol y_t)+W^{\mathsf T}\boldsymbol\delta_{t+1}.$$

最后一步 $t=T$ 之后没有下一步，约定 $\boldsymbol\delta_{T+1}=\boldsymbol0$。第二项 $W^{\mathsf T}\boldsymbol\delta_{t+1}$ 也是 M.7.9 的线性层反向公式。

**第 3 步：穿过 $\tanh$。** 第 2 步得到的是 $\partial L/\partial\boldsymbol h_t$，还要再往前穿过 $\boldsymbol h_t=\tanh\boldsymbol a_t$ 才是 $\boldsymbol\delta_t$。$\tanh$ 是逐元素函数，M.7.10 说梯度是对应相乘，$\tanh$ 的导数是 $1-\tanh^2$：

$$\boldsymbol\delta_t=(1-\boldsymbol h_t^{\,2})\odot\frac{\partial L}{\partial\boldsymbol h_t}.$$

这里 $\odot$ 是逐元素相乘，$\boldsymbol h_t^{\,2}$ 也逐元素平方。第 2、3 步合起来是一个从 $t=T$ 倒着到 $t=1$ 的递推：每一步的 $\boldsymbol\delta_t$ 由「本步输出带来的」和「下一步传回来的」两部分组成。

**第 4 步：共享参数的梯度是各时刻之和。** 把每个时刻用到的 $W$ 看成 $T$ 个互不相干的副本 $W^{(1)},\dots,W^{(T)}$，它们的值恰好相等。对某一个副本求偏导时，其他副本都固定不动，这正是多元函数偏导的意思。M.7.9 告诉我们副本 $W^{(t)}$ 的梯度是 $\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T}$。要注意 $\boldsymbol\delta_t$ 是按整条链算出的总误差信号：第 2 步已经把 $t$ 之后各时刻传回来的梯度累加进它里面了。所以副本 $W^{(t)}$ 虽然只在第 $t$ 步出现，它的梯度里仍然带着未来各步的影响。真正的 $W$ 同时是这 $T$ 个副本，一个变量沿着 $T$ 条路进入损失，由 M.7.6 把各条路上的梯度相加：

$$\frac{\partial L}{\partial W}=\sum_{t=1}^{T}\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T},\qquad \frac{\partial L}{\partial U}=\sum_{t=1}^{T}\boldsymbol\delta_t\boldsymbol x_t^{\mathsf T},\qquad \frac{\partial L}{\partial\boldsymbol b}=\sum_{t=1}^{T}\boldsymbol\delta_t.$$

形状核对：$\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T}$ 是 $d_h\times d_h$，与 $W$ 同形；$\boldsymbol\delta_t\boldsymbol x_t^{\mathsf T}$ 是 $d_h\times d_x$，与 $U$ 同形。

输出层的两个参数也是每一步共用的。第 1 步已经得到 $\partial L/\partial\boldsymbol o_t=(\boldsymbol p_t-\boldsymbol y_t)/T$，仍由线性层公式，第 $t$ 步给出的贡献是它乘 $\boldsymbol h_t^{\mathsf T}$（对 $W_{\mathrm{out}}$）和它本身（对 $\boldsymbol b_{\mathrm{out}}$），再跨时刻相加：

$$\frac{\partial L}{\partial W_{\mathrm{out}}}=\frac1T\sum_{t=1}^{T}(\boldsymbol p_t-\boldsymbol y_t)\boldsymbol h_t^{\mathsf T},\qquad \frac{\partial L}{\partial\boldsymbol b_{\mathrm{out}}}=\frac1T\sum_{t=1}^{T}(\boldsymbol p_t-\boldsymbol y_t).$$

这种按时间展开再做反向传播的算法叫**沿时间反向传播**（BPTT）。序列很长时，实际常常只往回传固定的 $k$ 步，叫截断 BPTT。

![沿时间反向传播：两路梯度先相加得到 $\partial L/\partial\boldsymbol h_t$，再逐分量乘 $1-\boldsymbol h_t^{\,2}$ 得到 $\boldsymbol\delta_t$；向前一时刻传回的是 $W^{\mathsf T}\boldsymbol\delta_t$，共享参数 $W$ 的梯度是各时刻 $\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T}$ 之和](fig/M10-n2.pdf){width=85%}

**方法 5（沿时间反向传播）**

1. 前向展开，记下每个时刻的 $\boldsymbol h_t$ 和 $\boldsymbol p_t$。
2. 令 $\boldsymbol\delta_{T+1}=\boldsymbol0$，对 $t=T,T-1,\dots,1$ 依次做下面两步。先算两路梯度之和：

   $$\frac{\partial L}{\partial\boldsymbol h_t}=\frac1TW_{\mathrm{out}}^{\mathsf T}(\boldsymbol p_t-\boldsymbol y_t)+W^{\mathsf T}\boldsymbol\delta_{t+1}.$$

3. 再穿过 $\tanh$：

   $$\boldsymbol\delta_t=(1-\boldsymbol h_t^{\,2})\odot\frac{\partial L}{\partial\boldsymbol h_t}.$$

4. 参数的梯度是各时刻之和：$\sum\boldsymbol\delta_t\boldsymbol h_{t-1}^{\mathsf T}$、$\sum\boldsymbol\delta_t\boldsymbol x_t^{\mathsf T}$、$\sum\boldsymbol\delta_t$；输出层是 $\frac1T\sum(\boldsymbol p_t-\boldsymbol y_t)\boldsymbol h_t^{\mathsf T}$ 和 $\frac1T\sum(\boldsymbol p_t-\boldsymbol y_t)$。

**例 5**　取例 4 的矩阵 $W,U,W_{\mathrm{out}}$ 和 $\boldsymbol b=\boldsymbol b_{\mathrm{out}}=\boldsymbol 0$，$\boldsymbol h_0=\boldsymbol 0$，$\boldsymbol x_1=(1,0)$，$\boldsymbol x_2=(0,1)$；$\boldsymbol h_t=\tanh(W\boldsymbol h_{t-1}+U\boldsymbol x_t)$，$\boldsymbol o_t=W_{\mathrm{out}}\boldsymbol h_t$，$p_{t,j}=e^{o_{t,j}}/\sum_ke^{o_{t,k}}$，$L=-\frac12[\ln p_{1,2}+\ln p_{2,3}]$（$p_{t,j}$ 是 $\boldsymbol p_t$ 的第 $j$ 个分量）。用方法 5 求 $\partial L/\partial U$、$\partial L/\partial W$。

这个 $L$ 就是例 4 的两步损失（目标分别是第 2 个和第 3 个词），所以例 4 已经把前向做完了。先算输出层的梯度，这里 $T=2$，每个位置的 $(\boldsymbol p_t-\boldsymbol y_t)/2$ 是

$$t=1:\ \tfrac12(0.5935,\ 0.2771-1,\ 0.1294)=(0.2967,\ -0.3614,\ 0.0647),$$

$$t=2:\ \tfrac12(0.3563,\ 0.5686,\ 0.0751-1)=(0.1782,\ 0.2843,\ -0.4625).$$

从后往前。$t=2$ 是最后一步，$\boldsymbol\delta_3=\boldsymbol0$：

$$\frac{\partial L}{\partial\boldsymbol h_2}=W_{\mathrm{out}}^{\mathsf T}(0.1782,\ 0.2843,\ -0.4625)^{\mathsf T}=(0.6406,\ 0.7468),$$

$$\boldsymbol\delta_2=(1-0.3634^2,\ 1-0.8307^2)\odot(0.6406,\ 0.7468)=(0.8679\times0.6406,\ 0.3099\times0.7468)=(0.5560,\ 0.2314).$$

退到 $t=1$。这一步的梯度除了本步输出，还要加上从第 2 步传回来的 $W^{\mathsf T}\boldsymbol\delta_2$：

$$W_{\mathrm{out}}^{\mathsf T}(0.2967,\ -0.3614,\ 0.0647)^{\mathsf T}=(0.2320,\ -0.4261),\qquad W^{\mathsf T}\boldsymbol\delta_2=\begin{pmatrix}0.5&0.25\\-0.5&0.5\end{pmatrix}\begin{pmatrix}0.5560\\0.2314\end{pmatrix}=(0.3359,\ -0.1623),$$

$$\frac{\partial L}{\partial\boldsymbol h_1}=(0.5679,\ -0.5884),\qquad \boldsymbol\delta_1=(1-0.7616^2,\ 1-0)\odot(0.5679,\ -0.5884)=(0.2385,\ -0.5884).$$

这里 $\boldsymbol\delta_1$ 的第二个分量里，$W^{\mathsf T}\boldsymbol\delta_2$ 的贡献不小，说明第 2 步的损失确实在影响第 1 步的参数。

参数的梯度，每个都是两个时刻之和。$\boldsymbol x_1=(1,0)$，$\boldsymbol x_2=(0,1)$：

$$\frac{\partial L}{\partial U}=\boldsymbol\delta_1\boldsymbol x_1^{\mathsf T}+\boldsymbol\delta_2\boldsymbol x_2^{\mathsf T}=\begin{pmatrix}0.2385&0\\-0.5884&0\end{pmatrix}+\begin{pmatrix}0&0.5560\\0&0.2314\end{pmatrix}=\begin{pmatrix}0.2385&0.5560\\-0.5884&0.2314\end{pmatrix}.$$

$W$ 的梯度里，$t=1$ 那一项是 $\boldsymbol\delta_1\boldsymbol h_0^{\mathsf T}=O$（因为 $\boldsymbol h_0=\boldsymbol0$），只剩

$$\frac{\partial L}{\partial W}=\boldsymbol\delta_2\boldsymbol h_1^{\mathsf T}=\begin{pmatrix}0.4235&0\\0.1763&0\end{pmatrix}.$$

用中心差分对每个参数各算一次数值梯度（方法见 M.7.12），结果与未经舍入的解析梯度相差不到 $10^{-6}$；上面只保留四位小数，与它们相差在 $10^{-4}$ 以内。

> 求 $\partial L/\partial\boldsymbol b$。
>
> 答案：$\boldsymbol\delta_1+\boldsymbol\delta_2=(0.2385+0.5560,\ -0.5884+0.2314)=(0.7945,\ -0.3570)$。

合上书，写出 $\boldsymbol\delta_t$ 的递推式，并说明为什么共享参数的梯度要把各时刻的贡献加起来。

BPTT 的递推里，每往回一步都要乘一次 $W^{\mathsf T}$。句子很长时，这样连乘几十次会发生什么，下一节来看。

### 6. 远处传回的梯度为什么容易变小或变大？

BPTT 的递推里反复出现 $W^{\mathsf T}\boldsymbol\delta_{t+1}$：每往回走一步，梯度就乘一次 $W^{\mathsf T}$ 再乘一次 $\tanh$ 的导数。先看例 5 里走过的那一步：$\boldsymbol\delta_2=(0.5560,0.2314)$ 长度约 $0.60$，传回第 1 步的 $W^{\mathsf T}\boldsymbol\delta_2=(0.3359,-0.1623)$ 长度约 $0.37$，这一步缩短了约四成。只走一步没什么，走几十步呢？这和 M.8.2 里梯度穿过很多层是同一个问题，只是这里「层」变成了「时刻」，而且每层的矩阵都是同一个 $W$。

我们想知道，远处的状态 $\boldsymbol h_t$ 对当前状态 $\boldsymbol h_T$ 有多大影响。由 $\boldsymbol h_k=\tanh(W\boldsymbol h_{k-1}+\dots)$，记 $D_k=\mathrm{diag}(1-\boldsymbol h_k^{\,2})$，它是以各分量的 $\tanh$ 导数 $1-h_{k,j}^2$ 为对角元的对角矩阵（$\mathrm{diag}(\boldsymbol v)$ 表示把向量 $\boldsymbol v$ 放在对角线上的矩阵）。一步的雅可比矩阵（M.7.8）是一张偏导表：第 $i$ 行第 $j$ 列放 $\partial h_{k,i}/\partial h_{k-1,j}$，也就是 $\boldsymbol h_{k-1}$ 的第 $j$ 个分量动一点，$\boldsymbol h_k$ 的第 $i$ 个分量跟着动多少。由链式法则，先经过线性部分 $W\boldsymbol h_{k-1}$（偏导表是 $W$），再经过逐元素的 $\tanh$（偏导表是 $D_k$），所以

$$\frac{\partial\boldsymbol h_k}{\partial\boldsymbol h_{k-1}}=D_kW.$$

连乘两步：$\boldsymbol h_{t+2}$ 先通过 $\boldsymbol h_{t+1}$ 依赖 $\boldsymbol h_t$，由链式法则，

$$\frac{\partial\boldsymbol h_{t+2}}{\partial\boldsymbol h_t}=(D_{t+2}W)(D_{t+1}W).$$

较晚时刻的因子写在左边，因为它最后作用在传入的变化上；这些矩阵一般不能交换，次序不能乱。推广到 $T-t$ 步：

$$\frac{\partial\boldsymbol h_T}{\partial\boldsymbol h_t}=(D_TW)(D_{T-1}W)\cdots(D_{t+1}W),$$

一共 $T-t$ 个因子。取矩阵的谱范数（最大奇异值，L.15.5）$\lVert\cdot\rVert_2$，它满足 $\lVert AB\rVert_2\le\lVert A\rVert_2\lVert B\rVert_2$。又因为 $0<1-\tanh^2\le1$，对角矩阵 $D_k$ 的范数 $\le1$。于是

$$\Bigl\lVert\frac{\partial\boldsymbol h_T}{\partial\boldsymbol h_t}\Bigr\rVert_2\le\lVert W\rVert_2^{\,T-t}.$$

如果 $\lVert W\rVert_2<1$，这个上界按指数衰减：隔得越远，$\boldsymbol h_t$ 对 $\boldsymbol h_T$ 的影响越小，远处损失沿这条路径传回的梯度会被明显缩小，长距离依赖因而更难学习。这叫**梯度消失**。

$\lVert W\rVert_2<1$ 只是消失的一个充分条件。$\lVert W\rVert_2\ge1$ 时这个上界什么也说明不了，并不表示梯度一定不消失，下一段就是例子。

反方向的情形是**梯度爆炸**。为了看清爆炸可能怎样发生，先看标量线性递推 $h_k=wh_{k-1}+r_k$，求导时各 $r_k$ 固定。因为一步的导数是 $w$，隔 $m$ 步的导数恰好是 $w^m$；若 $|w|>1$，其绝对值按指数增长。保留 $\tanh$ 时，每一步还要乘 $1-h_k^2$。例如标量 $w=2$，若 $h_k=0.9$，一步的导数是 $2\times(1-0.81)=0.38<1$。所以仅凭 $|w|>1$，或矩阵的范数大于 1，都不能断定实际梯度会爆炸，还要看各步导数的连乘。上面的上界只能证明消失，爆炸不是由它推出的。

这个线性递推还有一点值得看清：状态本身和它对初值的导数可以是两回事。取 $s_{k+1}=as_k+b$，$a\ne1$，设 $s_*=\dfrac{b}{1-a}$，它满足 $s_*=as_*+b$。两式相减得 $s_{k+1}-s_*=a(s_k-s_*)$，每一步差距乘 $a$，所以 $s_k=s_*+a^k(s_0-s_*)$。例如 $a=\frac13$，$b=1$，$s_0=2$：$s_*=\frac32$，$s_k=\frac32+\frac12\left(\frac13\right)^k$。状态趋于非零的极限 $\frac32$，而对初值的导数（求导时 $a,b$ 固定）$\partial s_k/\partial s_0=a^k=3^{-k}$ 趋于 0。两者并不矛盾：极限由 $b$ 决定，初值的影响则在逐步消失。

> 取 $a=\frac12$，$b=1$，$s_0=0$，求 $s_k$ 和 $\partial s_k/\partial s_0$。
>
> 答案：$s_*=2$，$s_k=2+(0-2)\cdot2^{-k}=2-2^{1-k}$；$\partial s_k/\partial s_0=2^{-k}$。

先猜一猜：每往回一步只缩小一成（乘 $0.9$），走 50 步以后还剩多少？再看每步放大一成（乘 $1.1$）的情形。标量时算出来是：

| 隔多少步 | $0.9^k$ | $1.1^k$ |
|---|---|---|
| 10 | 0.349 | 2.59 |
| 20 | 0.122 | 6.73 |
| 50 | 0.0052 | 117 |

![梯度沿时间往回传：每步乘 0.9 时 50 步后只剩 0.005，每步乘 1.1 时涨到 117；点线是留给第 7 节的对照，每步乘 0.99 时 50 步后还有 0.61（第 7 节会看到，这是遗忘门固定为 0.99 时沿细胞状态直接路径的倍率）（实线 0.9，虚线 1.1，点线 0.99，纵轴为对数坐标）](fig/M10-n3.pdf){width=70%}

**方法 6（沿时间连乘估计梯度大小）**

1. 写出一步的雅可比 $D_kW$（$D_k=\mathrm{diag}(1-\boldsymbol h_k^{\,2})$），隔 $m$ 步的影响是 $m$ 个这样的矩阵按时间次序相乘，较晚的在左。
2. 用谱范数给上界：$\lVert W\rVert_2^{\,m}$。小于 1 时上界按指数缩小（这只是充分条件，大于等于 1 不能推出不消失）。
3. 梯度爆炸用**梯度裁剪**：若梯度 $\boldsymbol g$ 的范数超过阈值 $c$，就缩放成 $\boldsymbol g\cdot c/\lVert\boldsymbol g\rVert$，方向不变，长度压到 $c$。这里 $\lVert\boldsymbol g\rVert$ 是向量的长度，有的书写作 $|\boldsymbol g|$；用双竖线是为了与数的绝对值区别。上面的 $\lVert W\rVert_2$ 则是矩阵最多把向量长度放大的倍数。

**例 6**　取 $W=\begin{pmatrix}0.5&-0.5\\0.25&0.5\end{pmatrix}$（老朋友②里的 $W_1$），再给任意 20 个对角元都在 $(0,1]$ 里的对角矩阵 $D_1,\dots,D_{20}$，估计 $\bigl\lVert(D_{20}W)\cdots(D_1W)\bigr\rVert_2$ 的上界。再对梯度 $\boldsymbol g=(30,40)$，取阈值 $c=5$，做裁剪。

例 5 算的是某一个具体的梯度，这次沿用同一个 $W$，改问连乘最多能把梯度压到多小；这个连乘就是循环网络隔 20 步的雅可比。先求 $W$ 的谱范数，也就是最大奇异值，它是 $W^{\mathsf T}W$ 的最大特征值的算术平方根。先算

$$W^{\mathsf T}W=\begin{pmatrix}5/16&-1/8\\-1/8&1/2\end{pmatrix}.$$

它的特征方程是 $\lambda^2-\frac{13}{16}\lambda+\frac{9}{64}=0$（迹 $\frac{13}{16}$，行列式 $\frac{9}{64}$），两个根是 $\frac9{16}$ 和 $\frac14$，开方得奇异值 $\frac34$ 和 $\frac12$。用 $\det W=0.375=0.75\times0.5$ 复核一下，但这个乘积只是复核，单凭乘积不能认定两个值正确。所以 $\lVert W\rVert_2=0.75<1$。每个 $D_k$ 的范数不超过 1，所以每个因子 $D_kW$ 的范数不超过 $0.75$，

$$\bigl\lVert(D_{20}W)\cdots(D_1W)\bigr\rVert_2\le0.75^{20}\approx0.0032.$$

这个上界说明：来自末端的梯度沿这 20 步状态路径传回时，其长度至多乘以约 $0.0032$。这里估计的是传递倍率，它提示长距离学习困难，不能据此断言 20 步以前的信息完全学不到。

再看裁剪。$\lVert\boldsymbol g\rVert=\sqrt{30^2+40^2}=50>5$，所以乘以 $5/50=0.1$，得 $(3,4)$。方向不变，长度正好是 5。

裁剪只能压住爆炸，不能放大消失的梯度：消失时梯度本来就很小，无从放大。所以消失要从结构上治，这就是下一节。

> 标量的 $w=0.95$，隔多少步以后上界小于 $0.01$？
>
> 答案：$0.95^k<0.01$ 等价于 $k>\ln0.01/\ln0.95=89.8$，所以至少隔 90 步。

合上书，写出隔 $m$ 步的雅可比连乘，并说出它在什么条件下指数衰减。

### 7. 怎样让信息和梯度沿时间一路传下去？

问题出在每一步都把状态乘一次矩阵再压一次 $\tanh$。能不能让信息有一条不被反复乘矩阵的通路？M.8.5 的残差连接给过答案：$\boldsymbol y=\boldsymbol x+F(\boldsymbol x)$，对 $\boldsymbol x$ 的导数是 $I+\dots$，多出一条直通的路。LSTM 用的是同一个想法：让「记忆」以加法的方式更新。

直接的想法是把 $W$ 换成单位矩阵，让旧状态原样搬过来。只这样做还保留着 $\tanh$，更新仍是 $\boldsymbol h_t=\tanh(\boldsymbol h_{t-1}+\cdots)$，导数仍可能被压小。那就另设一条只做加法的记忆通路；可是这样记忆只会不断累加，旧信息永远擦不掉，新信息也不能挑着写，很快就被塞满。所以要让网络自己决定什么时候保留、什么时候写入，这就是门。

LSTM 在隐藏状态 $\boldsymbol h_t$ 之外，加一个**细胞状态** $\boldsymbol c_t\in\mathbb R^{d_h}$，专门用来保存长期记忆。更新式如下，所有量都在 $\mathbb R^{d_h}$ 里，$\sigma$ 是 M.2.3 的 sigmoid（把每个分量压进 $(0,1)$）。三个门各占一行：

$$\boldsymbol f_t=\sigma(W_f\boldsymbol h_{t-1}+U_f\boldsymbol x_t+\boldsymbol b_f),$$

$$\boldsymbol i_t=\sigma(W_i\boldsymbol h_{t-1}+U_i\boldsymbol x_t+\boldsymbol b_i),$$

$$\boldsymbol g_t=\sigma(W_g\boldsymbol h_{t-1}+U_g\boldsymbol x_t+\boldsymbol b_g).$$

候选内容、记忆更新和读出各占一行：

$$\tilde{\boldsymbol c}_t=\tanh(W_c\boldsymbol h_{t-1}+U_c\boldsymbol x_t+\boldsymbol b_c),$$

$$\boldsymbol c_t=\boldsymbol f_t\odot\boldsymbol c_{t-1}+\boldsymbol i_t\odot\tilde{\boldsymbol c}_t,$$

$$\boldsymbol h_t=\boldsymbol g_t\odot\tanh\boldsymbol c_t.$$

输出门记作 $\boldsymbol g_t$，不用 $\boldsymbol o_t$，因为第 4 节里 $\boldsymbol o_t$ 已经是词表维的输出分数；它也不是第 6 节的梯度 $\boldsymbol g$，这里带下标 $t$ 的是门。

这一堆式子怎么读？分成三层。

第一层是三个**门** $\boldsymbol f_t,\boldsymbol i_t,\boldsymbol g_t$。它们是 sigmoid 的输出，每个分量在 $(0,1)$ 里，与别的向量逐元素相乘时，起一个「旋钮」的作用：0 是关死，1 是全开。0 和 1 在这里表示理想的全关、全开，有限输入下只能无限接近。三个门分别叫遗忘门、输入门、输出门。

第二层是候选内容 $\tilde{\boldsymbol c}_t$，和普通循环网络的 $\boldsymbol h_t$ 的计算形式一样，是「这一步想写进记忆的新内容」。

第三层是更新：新的记忆 = 旧记忆按遗忘门保留一部分 + 新内容按输入门写入一部分。然后输出门决定把记忆的多少读出来作为 $\boldsymbol h_t$。

只统计循环单元，不含词向量和输出层时，一组参数 $(W,U,\boldsymbol b)$ 有 $d_h^2+d_hd_x+d_h$ 个；这里的 LSTM 使用四组（三个门和候选内容）。

**为什么梯度不再被矩阵反复乘？** 看 $\boldsymbol c_t$ 对 $\boldsymbol c_{t-1}$ 的直接依赖。$\boldsymbol c_t=\boldsymbol f_t\odot\boldsymbol c_{t-1}+\dots$，逐元素相乘的导数是对角矩阵：

$$\frac{\partial\boldsymbol c_t}{\partial\boldsymbol c_{t-1}}=\mathrm{diag}(\boldsymbol f_t)\quad(\text{沿直接的这一条路}).$$

连乘两步，对角矩阵相乘就是对角元逐项相乘：$\mathrm{diag}(\boldsymbol f_t)\,\mathrm{diag}(\boldsymbol f_{t-1})=\mathrm{diag}(\boldsymbol f_t\odot\boldsymbol f_{t-1})$。一般地，只沿直接路径隔 $m$ 步，导数是 $\mathrm{diag}(\boldsymbol f_t\odot\boldsymbol f_{t-1}\odot\cdots\odot\boldsymbol f_{t-m+1})$，只是各步遗忘门的逐元素乘积，不再有同一个矩阵 $W$ 被反复相乘，也没有 $\tanh$ 的导数来压。

沿细胞状态直接相连的路径，隔 $m$ 步的导数是对应遗忘门值的乘积。当这些门值足够接近 1，而且连乘以后仍接近 1 时，这条路径能较好地保留梯度。门值若持续小于 1，连乘很多步后仍可能很小。

细胞状态还会经隐藏状态影响后续各个门。总导数要把所有路径的贡献相加，这些贡献可能缩小、放大或抵消。因此 LSTM 提供了更容易保留信息的路径，但不保证任何参数、任何长度下的总梯度都不会消失或爆炸。把遗忘门偏置设为正数，是让门在其他输入项较小时更偏向保留旧值，并不自动保证门值接近 1。

两种循环网络放在一起对照：

| 比较项 | 普通循环网络 | LSTM（沿细胞状态的直接路径） |
|---|---|---|
| 一步的更新 | $\boldsymbol h_t=\tanh(W\boldsymbol h_{t-1}+\dots)$ | $\boldsymbol c_t=\boldsymbol f_t\odot\boldsymbol c_{t-1}+\dots$ |
| 一步的雅可比 | $\mathrm{diag}(1-\boldsymbol h_t^{\,2})\,W$ | $\mathrm{diag}(\boldsymbol f_t)$ |
| 连乘 $m$ 步 | $m$ 个 $\mathrm{diag}(1-\boldsymbol h_k^{\,2})W$ 按序相乘 | 遗忘门的逐元素乘积 |
| 何时有利于保持导数 | $\tanh$ 在零点的导数为 1，但总传递还取决于 $W$ 及经过的状态 | 遗忘门连乘接近 1 时有利于保留；门值为 1 是理想极限 |

这和残差连接的相同点是都让输出里多出一项「原样搬过来的旧值」，区别是这里搬运的多少还可以由门来调节。

![LSTM 的一个时刻：上方水平的实线是细胞状态 $\boldsymbol c$，旧记忆先乘遗忘门再加上输入门放行的新内容；下方的状态 $\boldsymbol h$ 和输入 $\boldsymbol x$ 进入四个小方框算出门（$\boldsymbol f,\boldsymbol i,\boldsymbol g$）和候选内容，虚线表示门对相乘的控制](fig/M10-n4.pdf){width=80%}

**方法 7（LSTM 单步）**

1. 由 $(\boldsymbol h_{t-1},\boldsymbol x_t)$ 算出 $\boldsymbol f_t,\boldsymbol i_t,\boldsymbol g_t$ 和 $\tilde{\boldsymbol c}_t$。
2. 记忆更新 $\boldsymbol c_t=\boldsymbol f_t\odot\boldsymbol c_{t-1}+\boldsymbol i_t\odot\tilde{\boldsymbol c}_t$。
3. 读出 $\boldsymbol h_t=\boldsymbol g_t\odot\tanh\boldsymbol c_t$。
4. 估计梯度时，沿细胞状态的直路是 $\mathrm{diag}(\boldsymbol f_t)$ 的连乘。

**例 7**　按下面的标量公式计算（$h=0.5$，$c=1$，$x=1$ 是给定的值）：

$$f=\sigma(h+x+1),\quad i=\sigma(h+x-1),\quad g=\sigma(h+1),\quad \tilde c=\tanh(h-x),$$

$$c'=fc+i\tilde c,\qquad h'=g\tanh c'.$$

求 $c',h'$。

这组式子就是 $d_h=d_x=1$ 时 LSTM 的单步，$f,i,g$ 依次是遗忘门、输入门、输出门，$\tilde c$ 是候选内容，$c'$ 和 $h'$ 是新的细胞状态和隐藏状态。和例 4 里的普通循环网络相比，多了三个门和一个细胞状态；数据取成一维是为了手算，这一题只算前向，不涉及梯度。先算四个预激活，每个都是括号里的线性组合：

$$f:\ 0.5+1+1=2.5,\qquad i:\ 0.5+1-1=0.5,$$

$$g:\ 0.5+0+1=1.5,\qquad \tilde c:\ 0.5-1+0=-0.5.$$

逐个过激活函数：

$$f=\sigma(2.5)=0.9241,\quad i=\sigma(0.5)=0.6225,\quad g=\sigma(1.5)=0.8176,\quad \tilde c=\tanh(-0.5)=-0.4621.$$

更新记忆，旧值 1 保留了 92.4%，再写入新内容的 62.3%：

$$c'=0.9241\times1+0.6225\times(-0.4621)=0.9241-0.2876=0.6365.$$

最后读出：

$$h'=0.8176\times\tanh0.6365=0.8176\times0.5625=0.4599.$$

再用这个遗忘门做一个估计：如果把门值固定为常数，20 步里遗忘门一直是 0.9241，沿细胞状态直接路径的导数是 $0.9241^{20}\approx0.206$；若训练把遗忘门调到 0.99，则 $0.99^{20}\approx0.818$。而例 6 里 $\lVert W\rVert_2=0.75$ 给出的上界是 $0.75^{20}\approx0.003$，直接路径的倍率大得多（这只是两个不同量的粗略对照）。

> 标量更新 $c_t=f c_{t-1}+i\tilde c_t$、$h_t=g\tanh c_t$ 中，$c_{t-1}=2$，$f=\frac34$，$i=\frac14$，$g=\frac12$，$\tilde c_t=-\frac12$。求 $c_t,h_t$，并判断本步能否有 $h_t=c_t$。
>
> 答案：$c_t=\frac34\cdot2+\frac14\cdot(-\frac12)=\frac{11}8$，$h_t=\frac12\tanh\frac{11}8\approx0.4399$。因为 $|h_t|<\frac12$ 而 $c_t>1$，所以 $h_t\ne c_t$：细胞状态先累加，隐藏状态还要经过非线性函数和输出门。

> 把门值理想化为常数，若遗忘门 $f=1$ 且输入门 $i=0$，$c_t$ 与 $c_{t-1}$ 什么关系？
>
> 答案：$c_t=1\cdot c_{t-1}+0=c_{t-1}$，记忆原样保存，沿所示直接路径的导数为 1。

合上书，写出 $\boldsymbol c_t$ 的更新式，并推出沿细胞状态的直路上，一步的导数是 $\mathrm{diag}(\boldsymbol f_t)$。

LSTM 缓解了梯度问题，代价是每个单元要四组参数。能不能少用几个门？下一节看一个简化版。

### 8. LSTM 能不能更简单一些？

这一节先了解做法即可。

LSTM 有三个门和两个状态，只统计循环单元时用四组参数。2014 年 Cho 等人提出了更简单的 **GRU**（门控循环单元），把状态合并成一个 $\boldsymbol h_t$，只留两个门：

$$\boldsymbol z_t=\sigma(W_z\boldsymbol h_{t-1}+U_z\boldsymbol x_t+\boldsymbol b_z),\qquad \boldsymbol r_t=\sigma(W_r\boldsymbol h_{t-1}+U_r\boldsymbol x_t+\boldsymbol b_r),$$

$$\tilde{\boldsymbol h}_t=\tanh\bigl(W(\boldsymbol r_t\odot\boldsymbol h_{t-1})+U\boldsymbol x_t+\boldsymbol b\bigr),\qquad \boldsymbol h_t=(1-\boldsymbol z_t)\odot\boldsymbol h_{t-1}+\boldsymbol z_t\odot\tilde{\boldsymbol h}_t.$$

$\boldsymbol z_t$ 叫更新门：决定新状态里有多少来自候选，多少保留旧值，两部分的比例加起来是 1（一次插值）。$\boldsymbol r_t$ 叫重置门：算候选内容时，决定看旧状态的多少。

最后一个式子里的 $(1-\boldsymbol z_t)\odot\boldsymbol h_{t-1}$ 与 LSTM 的 $\boldsymbol f_t\odot\boldsymbol c_{t-1}$ 作用相同：沿旧状态这条直接路径的导数是 $\mathrm{diag}(1-\boldsymbol z_t)$。在这一项上，GRU 相当于把遗忘门和输入门绑成「$f=1-z$，$i=z$」。

**例 8**　(1) 给 $u=0.5$，$v=0.8$，$z=0.2$，求 $(1-z)u+zv$，并说明结果离 $u$ 近还是离 $v$ 近。(2) 一组参数由形状为 $256\times256$、$256\times256$、$256$ 的三个数组组成，问三组、四组各有多少个元素。

例 7 里新记忆由遗忘门和输入门分别控制；这里只算 GRU 的一个分量，$u=h_{t-1}$ 是旧状态，$v=\tilde h$ 是候选，$z$ 是更新门。更新是一次插值，一个 $z$ 同时管保留和写入，所以比 LSTM 少一个门。

$$h_t=0.8\times0.5+0.2\times0.8=0.56.$$

更新门小，状态主要保留旧值，只往候选移了一点。

只统计循环单元，按本节每组一个偏置向量的公式：一组 $(W,U,\boldsymbol b)$ 有 $256\times256+256\times256+256=131328$ 个，普通循环网络是 1 组，GRU 是 3 组，共 393984，LSTM 是 4 组，共 525312。

> 把门值理想化为常数，更新门 $z\equiv0$ 时，GRU 的 $\boldsymbol h_t$ 怎样变？
>
> 答案：$\boldsymbol h_t=\boldsymbol h_{t-1}$，状态不变，沿所示旧状态直接路径的导数是单位矩阵。

GRU 的循环单元参数较少；它与 LSTM 哪个效果更好，需要在相同任务和数据上比较。合上书，说出 GRU 里的哪一项扮演了 LSTM 的遗忘门。

到这里为止，模型读一个序列、预测同一个序列的下一个词。翻译的输入和输出是两个不同的句子，下一节处理这个问题。

### 9. 输入和输出长度不同（比如翻译）时，怎样建模？

翻译的输入是一句话 $x_1,\dots,x_S$，输出是另一句话 $w'_1,\dots,w'_{T}$，两者长度不同，词序也不一样。前面的语言模型只有一个序列。

2014 年的办法是用两个循环网络。**编码器**读原句，读完以后的最后一个状态 $\boldsymbol m=\boldsymbol h_S$（m 取 memory 的首字母）就是整句话的概括。**解码器**是一个以 $\boldsymbol m$ 为条件的语言模型：先用两侧隐藏状态维数相同的普通循环网络说明，取解码器的初始状态 $\boldsymbol s_0=\boldsymbol m$，每一步读上一个输出的词，更新状态 $\boldsymbol s_t$，输出下一个词的分布。写成概率：

$$P(w'_1,\dots,w'_T\mid x_1,\dots,x_S)=\prod_{t=1}^{T}P(w'_t\mid w'_{<t},\boldsymbol m).$$

这和第 1 节的连乘分解一模一样，只是每个条件多了一项 $\boldsymbol m$。所以它就是**条件语言模型**：「在给定原句的条件下，译文的语言模型」。译文的开头与结尾用特殊符号 $\langle\text{bos}\rangle$、$\langle\text{eos}\rangle$ 标出，模型输出 $\langle\text{eos}\rangle$ 就停止。

训练时把目标序列的真实前文送给解码器，这叫 teacher forcing。例如目标译文是 $b,\langle\text{eos}\rangle$ 时，解码器两步的输入依次是 $\langle\text{bos}\rangle,b$，两步的目标依次是 $b,\langle\text{eos}\rangle$。理由直接来自似然的连乘式：第 $t$ 项要计算的就是在真实前文 $w'_{<t}$ 条件下，目标词 $w'_t$ 的概率。如果换成模型自己生成的前文，计算的就不再是同一条目标序列的这些条件概率。使用真实前文时，各位置仍通过隐藏状态和共享参数相互关联，求共享参数的梯度仍要沿时间反向传播。生成时没有真实的后续词，只能把刚生成的词作为下一步输入。

这个结构有一个明显的毛病。无论原句是 5 个词还是 50 个词，编码器最后都只交给解码器一个固定维数的向量 $\boldsymbol m$。这个向量的坐标共同表示原句，不能按词数把坐标平均分给各个词。困难在于：解码器此后只能依靠这一份概括，不能回到原句各位置重新读取细节。原句越长，需要保留和区分的内容通常越多，这种结构就越容易丢失有用信息。Cho 等人 2014 年的观察也是，译文质量随原句变长明显变差。

此外，译文的损失若要影响原句很早的位置，通常还要沿编码器的多步状态传回梯度。下面的注意力同时改变了读取信息和传回梯度的路径。

**方法 8（编码器–解码器的损失）**

1. 编码器读原句，取最后状态 $\boldsymbol m$。
2. 解码器以 $\boldsymbol m$ 为初始状态（$\boldsymbol s_0=\boldsymbol m$），输入是 $\langle\text{bos}\rangle,w'_1,\dots,w'_{T-1}$（teacher forcing），每一步预测 $w'_t$。
3. 损失是 $-\frac1T\sum\ln P(w'_t\mid w'_{<t},\boldsymbol m)$，和方法 1 相同。

**例 9**　已知 $X$ 是已经给定的条件，三个事件的条件概率为 $P(A\mid X)=0.7$，$P(B\mid A,X)=0.5$，$P(C\mid A,B,X)=0.9$。求联合条件概率 $P(A,B,C\mid X)$，以及这三个概率的几何平均的倒数。

可以把 $X$ 看成原句，$A,B,C$ 看成译文的三个词（最后一个是 $\langle\text{eos}\rangle$）：那么联合条件概率就是译文的条件概率，几何平均的倒数就是困惑度。和例 1 相比，只变了一样：每个概率都以 $X$ 为条件，算法完全相同。

第一步，联合概率是连乘：

$$P(A,B,C\mid X)=0.7\times0.5\times0.9=0.315.$$

第二步，三个负对数分别是 $0.3567,\ 0.6931,\ 0.1054$，和为 $1.1552$，平均

$$L=\frac{1.1552}{3}=0.3851.$$

第三步，几何平均的倒数就是困惑度：

$$e^{0.3851}\approx1.47=0.315^{-1/3}.$$

要注意，例 9 的三个概率和例 2 的四个概率不是同一份文本上的结果，这两个困惑度不能拿来比较模型优劣；方法 2 要求的是同一份测试文本、同一个词表。

> 三个条件概率为 $P(A\mid X)=0.5$，$P(B\mid A,X)=0.5$，$P(C\mid A,B,X)=0.8$，求联合条件概率和三个概率几何平均的倒数。
>
> 答案：联合概率 $0.5\times0.5\times0.8=0.2$；平均负对数 $(0.6931+0.6931+0.2231)/3\approx0.5365$，几何平均的倒数 $e^{0.5365}\approx1.71$，也就是 $0.2^{-1/3}$。

合上书，写出条件语言模型的连乘分解，并说明定长向量 $\boldsymbol m$ 为什么是瓶颈。

### 10. 解码的每一步，能不能回头去看原句的每个词？

既然压成一个向量会丢信息，那就不压。编码器在每个位置的状态 $\boldsymbol h_1,\dots,\boldsymbol h_S$ 都保留下来，解码的每一步自己决定回头看哪些位置。人翻译长句时也是这样，写每个词的时候眼睛会回到原文对应的位置。

做法分三步。设解码器在写第 $t$ 个词时，上一步的状态是 $\boldsymbol s_{t-1}$。

第一步，给每个编码器状态打分，看它和当前要写的词有多相关。设编码器状态有 $d_h$ 个分量，解码器状态有 $d_s$ 个分量。打分时先把两者变成同样的 $d_a$ 维：$W_s\in\mathbb R^{d_a\times d_s}$，$W_h\in\mathbb R^{d_a\times d_h}$，$\boldsymbol v\in\mathbb R^{d_a}$ 是把这 $d_a$ 个分量合成一个分数的参数向量，这三个参数都由训练确定。Bahdanau 用一个小网络打分：

$$u_{t,j}=\boldsymbol v^{\mathsf T}\tanh(W_s\boldsymbol s_{t-1}+W_h\boldsymbol h_j),\qquad j=1,\dots,S.$$

第二步，用 softmax（M.2.7）把分数变成权重：

$$\alpha_{t,j}=\frac{e^{u_{t,j}}}{\sum_{k=1}^{S}e^{u_{t,k}}}.$$

第三步，用权重对编码器状态做加权平均，得到这一步专用的**上下文向量**：

$$\bar{\boldsymbol h}_t=\sum_{j=1}^{S}\alpha_{t,j}\boldsymbol h_j.$$

$\bar{\boldsymbol h}_t$ 和第 9 节的 $\boldsymbol m$ 不同：它每一步都重新算，权重大的位置就是模型此刻「在看」的位置。解码器保留自己的上一状态，同时把本步上下文作为额外输入，并不重新设置初始状态。例如可以用下面的简化更新说明信息流：

$$\boldsymbol s_t=\tanh(A\boldsymbol s_{t-1}+B\boldsymbol x'_{t-1}+C\bar{\boldsymbol h}_t+\boldsymbol b_s).$$

这里 $\boldsymbol x'_{t-1}$ 是上一个译文符号的向量，第一步用起始符；$A,B,C$ 分别把上一状态、输入向量和上下文变成 $d_s$ 维，$\boldsymbol b_s$ 是同维偏置。再由 $\boldsymbol s_t$ 经过输出层给出本步词的概率。这只是说明信息流的简化形式，真实模型更复杂，交叉注意力留到 M.11.6，完整结构见 M.12。

权重 $\alpha_{t,j}\ge0$ 且和为 1，所以 $\bar{\boldsymbol h}_t$ 是编码器状态的加权平均，落在这些向量的凸组合里。为什么用加权平均，而不是直接挑出得分最高的那个位置？原因分三层看。第一，若直接挑分数最大的一个位置，只要被选位置不变，分数的细小变化不会改变选出的向量，所以对打分参数的导数是 0，梯度给不出调整方向。第二，分数变到让被选位置切换时，选出的向量突然跳到另一个，那一点不可导。第三，两处合起来，当前这套直接求导的方法就难以调整打分参数。softmax 加权平均随分数连续可导，可以把损失的变化传回打分参数，这种做法叫**软对齐**。

**方法 9（加性注意力）**

1. 对每个编码器位置 $j$ 算分数 $u_{t,j}=\boldsymbol v^{\mathsf T}\tanh(W_s\boldsymbol s_{t-1}+W_h\boldsymbol h_j)$。
2. 对 $j$ 做 softmax 得权重 $\alpha_{t,j}$。
3. 上下文向量 $\bar{\boldsymbol h}_t=\sum_j\alpha_{t,j}\boldsymbol h_j$，形状与一个 $\boldsymbol h_j$ 相同。

**例 10**　三个编码器状态取老朋友③的三个向量：$\boldsymbol h_1=(1,0)$，$\boldsymbol h_2=(0,1)$，$\boldsymbol h_3=(1,1)$。解码器状态 $\boldsymbol s_{t-1}=(1,0)$，取 $d_h=d_s=d_a=2$，$W_s=W_h=I$，$\boldsymbol v=(1,1)$。求权重和上下文向量。

和第 9 节相比，解码器不再只拿到一个固定的向量，而是对三个编码器状态各打一个分，再加权平均；编码器状态沿用老朋友③的三个向量，为的是只学新的这一步。

先打分。$u_j=\boldsymbol v^{\mathsf T}\tanh(\boldsymbol s+\boldsymbol h_j)$，即把 $\tanh$ 后的两个分量相加：

$$u_1=\tanh2+\tanh0=0.9640,\quad u_2=\tanh1+\tanh1=1.5232,\quad u_3=\tanh2+\tanh1=1.7256.$$

再做 softmax。$e^{0.9640}=2.622$，$e^{1.5232}=4.587$，$e^{1.7256}=5.616$，三者之和 12.825：

$$\boldsymbol\alpha=(0.2045,\ 0.3576,\ 0.4379).$$

最后加权平均：

$$\bar{\boldsymbol h}_t=0.2045(1,0)+0.3576(0,1)+0.4379(1,1)=(0.6424,\ 0.7955).$$

第 3 个状态得分最高，权重也最大。

> 若三个分数全相等，$\bar{\boldsymbol h}_t$ 是什么？
>
> 答案：权重各为 $1/3$，$\bar{\boldsymbol h}_t=\frac13[(1,0)+(0,1)+(1,1)]=(2/3,\ 2/3)$，是三个状态的平均。

![注意力的三步：左边的编码器状态各有一个权重（柱高），解码器此刻的状态打分、softmax 之后，上下文向量是按柱高加权的平均；梯度经本步上下文向量直接连到每个 $\boldsymbol h_j$，权重很小时这条路径的贡献也小](fig/M10-n5.pdf){width=80%}

这样改完以后有两个好处。信息不再被压进一个向量，每个原句的词都保留着自己的状态。梯度也多了一条近路：译文第 $t$ 个词的损失通过 $\alpha_{t,j}$ 和 $\bar{\boldsymbol h}_t$ 直接连到 $\boldsymbol h_j$，不必只靠沿编码器逐时刻传回；权重很小时，这条路径的贡献仍可能很小。

但这个结构仍然是循环的：编码器一个词一个词地读，解码器一个词一个词地写，后一步要等前一步算完，没法让所有位置同时算。打分用的也是一个带 $\tanh$ 的小网络。如果把打分换成两个向量的点积，再把注意力用到同一句话内部，会怎样？这就是下一章。

合上书，写出注意力的三步（打分、softmax、加权平均），并说明为什么用加权平均而不是挑得分最高的那个位置。

回到开头的问题：怎样处理一串长度不固定、前后相关的词？循环网络的做法是让一个固定大小的状态逐词更新（第 4 节），参数个数与句子多长无关。例 4 的网络（$d_h=d_x=2$，词表 3 个词）一共是 $2^2+2\times2+2+3\times2+3=19$ 个数，读 3 个词和读 300 个词都是这 19 个。训练靠沿时间反向传播（第 5 节）；远处的信息容易衰减，所以有门（第 7 节）；输入输出是两个句子时，用编码器和解码器，再用注意力让解码每一步回头看原句（第 9、10 节）。

### 本章小结

在「模型、损失、更新规则」的三件套里，本章新增的是模型：循环网络（以及它的门控版本和注意力）；损失是语言模型的交叉熵（困惑度是它的指数）；更新规则仍是梯度下降，只是梯度要沿时间往回传，这一步要小心共享参数要求和、小心梯度可能变小或变大。

| 方法 | 什么时候用 | 对应题号 |
|---|---|---|
| 方法 1（自回归分解与平均负对数似然） | 算句子概率；写语言模型的训练损失 | M10-01、06、12 |
| 方法 2（困惑度） | 比较两个语言模型；把 $L$ 翻译成「均匀猜几个词」 | M10-02、06、12 |
| 方法 3（n 元语法的计数估计） | 用频率估计条件概率；判断数据稀疏 | 第 3 节随堂题 |
| 方法 4（前向展开） | 手算循环网络的状态和损失 | M10-03、07 |
| 方法 5（沿时间反向传播） | 求循环网络的参数梯度 | M10-07、13 |
| 方法 6（沿时间连乘估计梯度大小） | 判断梯度缩小还是放大；做梯度裁剪 | M10-04、09、10、11、13 |
| 方法 7（LSTM 单步） | 手算 LSTM；比较直接路径上的梯度 | M10-11，例 7 后随堂题 |
| 方法 8（编码器–解码器的损失） | 条件语言模型的概率、损失、困惑度 | M10-08 |
| 方法 9（加性注意力） | 算权重和上下文向量 | M10-05、14 |

本册两张逐章长大的表，本章各加了一行。

| 损失或做法 | 背后的概率假设 | 本章 |
|---|---|---|
| 语言模型的交叉熵、困惑度 | 下一个词服从类别分布（条件于前文） | 本章新增 |

| 技巧 | 治什么病 | 为什么能治 |
|---|---|---|
| 梯度裁剪 | 梯度爆炸 | 梯度范数超过阈值就缩短，方向不变 |
| LSTM / GRU 的加性更新 | 缓解沿时间传递时梯度缩小的问题 | LSTM 的细胞状态直接路径乘遗忘门，GRU 的旧状态直接路径乘 $1-z_t$；门值的连乘决定这条路径能保留多少，不保证总梯度始终不变 |
| 注意力 | 定长向量装不下整句 | 解码每一步重新加权平均全部编码器状态 |
