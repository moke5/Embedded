# 自定义IC芯片元件

[toc]



## **1.问题的引入**

我们在进行PCB设计中，有时候会用到一些非标准的IC芯片或者特制的芯片，那么这些芯片在嘉立创软件上是无法找到对应的型号，因此我们需要去自定义该IC芯片元件以及创建它的封装。

## **2.创建IC芯片元件符号**

1.新建元件

![img](./img/52753.png)

2.以CH340N芯片为例子，先创建一个IC芯片分类

![img](./img/52719.png)

 

![img](./img/52781.png)

3.查看芯片的数据手册，获取芯片的每个引脚

﻿[数据手册](https://item.szlcsc.com/datasheet/CH340N/3390257.html?spm=sc.it.xds.a&lcsc_vid=Q1cMU1ZVT1ReAVIHQwNfUQIHQgAMBlYCEQIIAlAER1MxVlNSQFlXU11STlZWVzsOAxUeFF5JWAIASQYPGQZABAsLWA%3D%3D)﻿

![img](./img/52741.png)

4.使用向导方式去创建该元件符号，该元件是SOP-8类型，也就是小型贴片封装，跟DIP封装类似，引脚都是在两边，只不过SOP是贴片类型的，因此创建向导的时候可以使用DIP即可。

![img](./img/52757.png)

![img](./img/52723.png)

5.修改元件的每个引脚名称

![img](./img/52773.png)

 

 

## **3.创建IC芯片封装**

1.创建封装

![img](./img/52733.png)

2.执行封装名称和 创建一个封装分类

![img](./img/52749.png)

 

![img](./img/52726.png)

3.查看数据手册，获取芯片的封装尺寸

﻿[数据手册](https://item.szlcsc.com/datasheet/CH340N/3390257.html?spm=sc.it.xds.a&lcsc_vid=Q1cMU1ZVT1ReAVIHQwNfUQIHQgAMBlYCEQIIAlAER1MxVlNSQFlXU11STlZWVzsOAxUeFF5JWAIASQYPGQZABAsLWA%3D%3D)﻿

![img](./img/52715.png)

可知，封装形式是SOP-8，而且是标准的8引脚贴片

同时，去该芯片对应的官网上获取SOP的封装相关信息

﻿[芯片官网](https://www.wch.cn/search.html)﻿

![img](./img/52737.png)

下载该文件，打开之后，查询到SOP封装信息

![img](./img/52769.png)

4.使用向导方式快速创建

 

![img](./img/52761.png)

填写相关尺寸信息

![img](./img/52765.png)

 

![img](./img/52745.png)

生成封装

![img](./img/52777.png)

## **4.关联符号和封装**

![img](./img/52730.png)

 

![img](./img/52711.png)

 