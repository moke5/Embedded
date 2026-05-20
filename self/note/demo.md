# 一级标题

[toc]



## 二级标题

### 三级标题



## 文本格式

<center>
 区中   
</center>

**粗体文本**

*斜体文本*

***粗体斜体文本***

~~删除线文本~~

```
行内代码
```

## 链接

### 内联链接
[Google](https://www.google.com)

[Google](https://www.google.com "Google 搜索")

### 引用链接
[Google][1]

[百度][2]

[1]: https://www.google.com "Google 搜索"
[2]: https://www.baidu.com "百度搜索"

## 图片

![示例图片](assets/Typora_01.png "示例图片")

## 水平线

---

## 脚注

这是一个脚注引用[^1]。

[^1]: 这是脚注内容。

## 代码块

### Python 代码
```python
import numpy as np

def hello_world():
    print("Hello, World!")
    return "Success"

if __name__ == "__main__":
    result = hello_world()
    print(result)
```

## 引用块

> 这是默认引用块，是 Markdown 中最基本的引用形式。

> 这是嵌套引用块
> > 这是第二层引用
> > > 这是第三层引用

> 这是信息引用块，用于显示提示信息。通常使用蓝色边框和背景。
{:alt="info"}

> 这是警告引用块，用于显示警告信息。通常使用黄色边框和背景。
{:alt="warn"}

> 这是危险引用块，用于显示危险信息。通常使用红色边框和背景。
{:alt="danger"}

> 这是成功引用块，用于显示成功信息。通常使用绿色边框和背景。
{:alt="success"}

## 小标签

<font title="red">红色</font> <font title="yellow">黄色</font> <font title="green">绿色</font> <font title="blue">蓝色</font> <font title="gray">灰色</font>

## 强调型文本

<span alt="solid">下划线文本</span>

<span alt="dashed">虚线文本</span>

<span alt="dotted">点线文本</span>

<span alt="wavy">波浪线文本</span>

<span alt="delete">删除线文本</span>

<span alt="shadow">阴影文本</span>

## 高亮

==高亮文本==

## KBD

<kbd>Ctrl</kbd> + <kbd>C</kbd>

## 折叠标签

<details>
<summary>点击展开</summary>
这是折叠标签的内容，点击上方的标题可以展开或折叠。
</details>
## 列表

### 有序列表
1. 第一项内容
2. 第二项内容
   1. 子项 1
   2. 子项 2
3. 第三项内容

### 无序列表
- 第一项内容
- 第二项内容
  - 子项 1
  - 子项 2
- 第三项内容

### 任务列表
- [x] 已完成的任务
- [ ] 未完成的任务
- [ ] 待办任务

## 数学公式

### 行内公式
这是一个行内公式：$y = ax + b$

这是另一个行内公式：$E = mc^2$

### 块级公式
$$
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$

$$
\int_{a}^{b} f(x) dx
$$

$$
\frac{\partial^2 f}{\partial x \partial y}
$$

## 表格

### 普通表格

| 姓名 | 年龄 | 成绩 |
|------|------|------|
| 张三 | 18   | 90   |
| 李四 | 19   | 85   |
| 王五 | 17   | 95   |

### 三线表

| 姓名 | 年龄 | 成绩 |
| :--- | :--- | :--- |
| 张三 | 18   | 90   |
| 李四 | 19   | 85   |
| 王五 | 17   | 95   |


## 嵌套结构

### 列表中的引用

- 第一项
  > 这是引用内容
- 第二项

### 引用中的列表
> - 列表项 1
> - 列表项 2
> - 列表项 3

|      |      |      |
| ---- | ---- | ---- |
|      |      |      |
|      |      |      |
|      |      |      |