# KaTeX 速查表

[toc]



> 块公式：`$$ ... $$`，独占一行；行内公式：`$ ... $`
> 块公式建议开头加上 `\displaystyle`，防止分式字体过小
> 下标内出现下划线：**`\_`，不能直接写`_`**

## 1 上下标

|源码|显示|说明|
|---|---|---|
|`x^2`|$x^2$|上标，单个字符|
|`x^{a+b}`|$x^{a+b}$|多字符上标加大括号|
|`f_{CK\_CNT}`|$f_{CK\_CNT}$|下标，内部下划线转义|
|`A_{i,j}`|$A_{i,j}$|多字符下标加大括号|

## 2 分式、根号
|源码|显示|
|---|---|
|`\frac{a}{b}`|$\frac{a}{b}$|
|`\dfrac{a}{b}`|$\dfrac{a}{b}$|强制大分式（等价`\displaystyle`）|
|`\sqrt{x}`|$\sqrt{x}$|
|`\sqrt[3]{x}`|$\sqrt[3]{x}$|开n次方|

示例
```latex
$$
\displaystyle
T_{update}=\frac{(PSC+1)(ARR+1)}{f_{CK\_PSC}}
$$
```

## 3 运算符
|源码|符号|
|---|---|
|`+ - *`|$+ \;-\; *$|
|`\times`|$\times$|乘号|
|`\cdot`|$\cdot$|点乘|
|`\div`|$\div$|除|
|`\pm`|$\pm$|正负|
|`\le`|$\le$|小于等于|
|`\ge`|$\ge$|大于等于|
|`\neq`|$\neq$|不等于|
|`\approx`|$\approx$|约等于|
|`\infty`|$\infty$|无穷|

## 4 希腊字母（常用）
|源码|符号|源码|符号|
|---|---|---|---|
|`\alpha`|$\alpha$|`\beta`|$\beta$|
|`\gamma`|$\gamma$|`\delta`|$\delta$|
|`\pi`|$\pi$|`\omega`|$\omega$|
|`\Omega`|$\Omega$|`\theta`|$\theta$|

## 5 括号
|源码|显示|说明|
|---|---|---|
|`\((a+b)\)`|$\((a+b)\)$|普通圆括号|
|`\([a+b]\)`|$\([a+b]\)$|方括号|
|`\{a,b\}`|$\{a,b\}$|花括号，必须转义`\{ \}`|
|`\left( \frac{A}{B} \right)`|$\displaystyle\left(\frac{A}{B}\right)$|自适应大小括号|

## 6 求和、积分
```latex
$$
\displaystyle
\sum_{k=1}^{n} k \quad \int_{0}^{t} f(x)dx
$$
```
$\displaystyle\sum_{k=1}^{n} k \quad \int_{0}^{t} f(x)dx$

## 7 多行对齐（写公式推导必备，`&`为对齐点，`\\`换行）
```latex
$$
\displaystyle
\begin{aligned}
f_{CK\_CNT} &= \frac{f_{CK\_PSC}}{PSC+1} \\[4pt]
T_{update} &= \frac{ARR+1}{f_{CK\_CNT}}
\end{aligned}
$$
```
- `\\[4pt]`：换行并增加间距

## 8 矩阵
```latex
$$
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
$$
```
`&`分列，`\\`换行；`bmatrix`带方括号，`matrix`无括号

## 9 空格
|源码|效果|
|---|---|
|`\,`|小空格|
|`\;`|中等空格|
|`\quad`|大空格|

## 10 字号（仅块公式内用）
`\tiny` < `\small` < `\normalsize` < `\large` < `\Large` < `\LARGE` < `\huge`
```latex
$$
\Large \displaystyle
E=mc^2
$$
```

## 11 条件分段函数
```latex
$$
f(x)=
\begin{cases}
1, &x>0 \\
0, &x\le0
\end{cases}
$$
```

## 🚨 高频踩坑
1. 下标变量含下划线：**`\_`**，例 `f_{CK\_PSC}`，直接写`_`公式直接灰掉
2. 分式很小：开头加 `\displaystyle`
3. 换行必须写 `\\`，不是`\`
4. 花括号 `{}` 在公式里有语法作用，输出字面大括号要写 `\{ \}`
5. 所有反斜杠为英文 `\`，不要中文反斜杠

## ✨嵌入式笔记直接复制模板
```markdown
$$
\Large \displaystyle
\begin{aligned}
f_{CK\_CNT} &= \frac{f_{CK\_PSC}}{PSC+1}\\[6pt]
T_{update} &= \frac{(PSC+1)(ARR+1)}{f_{CK\_PSC}}
\end{aligned}
$$
```

