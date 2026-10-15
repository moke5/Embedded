---
type: 概念
tags:
  - C
status:
target:
input:
output:
review:
created: 2026-10-15
updated: 2026-10-15
related: []
---
### printf

- 格式化输出数据

```c
相关函数 scanf, snprintf
头文件 #include <stdio.h>
定义函数 int printf(const char * format, ...);
函数说明 printf()会根据参数 format 字符串来转换并格式化数据, 然后将结果写出到标准输出设备, 直到出现
字符串结束('\0')为止. 参数 format 字符串可包含下列三种字符类型
1. 一般文本, 伴随直接输出.
2. ASCII 控制字符, 如\t、 \n 等.
3. 格式转换字符.
格式转换为一个百分比符号(%)及其后的格式字符所组成. 一般而言, 每个%符号在其后都必需有一
printf()的参数与之相呼应 (只有当%%转换字符出现时会直接输出%字符), 而欲输出的数据类型必须与其相对应
的转换字符类型相同.

Printf()格式转换的一般形式如下
%(flags)(width)(. prec)type
以中括号括起来的参数为选择性参数, 而%与 type 则是必要的. 底下先介绍 type 的几种形式
整数
%d 整数的参数会被转成--有符号的十进制数字
%u 整数的参数会被转成--无符号的十进制数字
%o 整数的参数会被转成--无符号的八进制数字
%x 整数的参数会被转成--无符号的十六进制数字, 并以小写 abcdef 表示
%X 整数的参数会被转成--无符号的十六进制数字, 并以大写 ABCDEF 表示浮点型数
%f double 型的参数会被转成十进制数字, 并取到小数点以下六位, 四舍五入.
%e double 型的参数以指数形式打印, 有一个数字会在小数点钱, 六位数字在小数点后, 而在
指数部分会以小写的 e 来表示.
%E 与%e 作用相同, 唯一区别是指数部分将以大写的 E 来表示.
%g double 型的参数会自动选择以%f 或%e 的格式来打印, 其标准是根据打印的数值及所设置
的有效位数来决定.
%G 与%g 作用相同, 唯一区别在以指数形态打印时会选择%E 格式.
字符及字符串
%c 整型数的参数会被转成 unsigned char 型打印出.
%s 指向字符串的参数会被逐字输出, 直到出现 NULL 字符为止
%p 如果是参数是"void *"型指针则使用十六进制格式显示.

prec 有几种情况
1. 正整数的最小位数.
2. 在浮点型数中代表小数位数
3. 格式代表有效位数的最大值.
4. 在%s 格式代表字符串的最大长度.
5.若为×符号则代表下个参数值为最大长度.
width 为参数的最小长度, 若此栏并非数值, 而是*符号, 则表示以下一个参数当做参数长度.
flags 有下列几种情况
#NAME?
+ 一般在打印负数时, printf ()会加印一个负号, 整数则不加任何负号. 此旗标会使得在打印正
数前多一个正号 (+).Linux 常用 C 函数
第 77 页 共 115 页
# 此旗标会根据其后转换字符的不同而有不同含义. 当在类型为 o 之前 (如%#o), 则会在打印八进
制数值前多印一个 o.
而在类型为 x 之前 (%#x)则会在打印十六进制数前多印'0x', 在型态为 e、 E、 f、 g 或 G 之前则会强
迫数值打印小数点. 在类型为 g 或 G 之前时则同时保留小数点及小数位数末尾的零.
0 当有指定参数时, 无数字的参数将补上 0.默认是关闭此旗标, 所以一般会打印出空白字符.
返回值 成功则返回实际输出的字符数, 失败则返回-1, 错误原因存于 errno 中.
范例
    #include <stdio.h>
    main()
    {
        int i = 150;
        int j = -100;
        double k = 3.14159;
        printf("%d %f %x\n", j, k, i);
        printf("%2d %*d\n", i, 2, i); //参数 2 会代入格式*中, 而与%2d 同意义
    }
执行 -100 3.14159 96
    150 150
```


### framebuffer
```c
    #include <unistd.h>
    sleep(2);

    scanf("%d", &num); // 切换缓冲区导致 hello被刷新
```



### getchar

```c
相关函数 fopen, fread, fscanf, getc
头文件 #include <stdio.h>
定义函数 int getchar(void);
函数说明 getchar()用来从标准输入设备中读取一个字符.然后将该字符从 unsignedchar 转换成 int 后返回.
返回值 getchar()会返回读取到的字符, 若返回 EOF 则表示有错误发生.
附加说明 getchar()非真正函数, 而是 getc(stdin)宏定义.
范例
    #include <stdio.h>
    main()
    {
        FILE * fp;
        int c, i;
        for(i = 0; i < 5; i++)
        {
        c = getchar();
            putchar(c);
        }
    }
执行 1234 //输入
1234 //输出
```

不管是scanf还是getchar发现程序内存储有剩余字符都会直接读取残留的字符而不不是重新接受用户的输入


### sqrt

- 计算平方根值

```c
相关函数 hypotq
头文件 #include <math.h>
定义函数 double sqrt(double x);
函数说明 sqrt()用来计算参数 x 的平方根, 然后将结果返回. 参数 x 必须为正数.
返回值 返回参数 x 的平方根值.
错误代码 EDOM 参数 x 为负数.
附加说明 使用 GCC 编译时请加入-lm.
范例 /* 计算 200 的平方根值 */
    #include <math.h>
    main()
    {
        double root;
        root = sqrt(200);
        printf("answer is %f\n", root);
    }
执行 answer is 14.142136
```



### malloc

- 配置内存空间

```c
相关函数 calloc, free, realloc, brk
头文件 #include <stdlib.h>
定义函数 void *malloc(size_t size);
函数说明 malloc()用来配置内存空间, 其大小由指定的 size 决定.
返回值 若配置成功则返回一指针, 失败则返回 NULL.
范例
void p = malloc(1024); //配置 1k 的内存
```


### calloc

- 配置内存空间

```c
相关函数 malloc, free, realloc, brk
头文件 #include <stdlib.h>
定义函数 void *calloc(size_t nmemb, size_t size);
函数说明 calloc()用来配置nmemb个相邻的内存单位,每一单位的大小为size,并返回指向第一个元素的指针.
这和使用下列的方式效果相同:malloc(nmemb*size);不过, 在利用 calloc()配置内存时会将内存内容初始化
为 0.
返回值 若配置成功则返回一指针, 失败则返回 NULL.
范例 /* 动态配置 10 个 struct test 空间 */
#include <stdlib.h>
struct test
{
    int a[10];
    char b[20];
}
main()
{
    struct test *ptr = calloc(sizeof(struct test), 10);
}
```



### free

- 释放原先配置的内存

```c
相关函数 malloc, calloc, realloc, brk
头文件 #include <stdlib.h>
定义函数 void free(void *ptr);
函数说明 参数 ptr 为指向先前由 malloc()、 calloc()或 realloc()所返回的内存指针. 调用 free()后 ptr
所指的内存空间便会被收回. 假若参数 ptr 所指的内存空间已被收回或是未知的内存地址, 则调用 free()可能会
有无法预期的情况发生. 若参数 ptr 为 NULL, 则 free()不会有任何作用.
```

不会自动指向NULL



### bzero

- 将一段内存内容全部清0

```c
相关函数 memset, swab
头文件 #include <string.h>
定义函数 void bzero(void *s, int n);
函数说明 bzero()会将参数 s 所指的内存区域前 n 个字节, 全部设为零值. 相当于调用 memset((void*)s, 0,
size_tn);
返回值
附加说明 建议使用 memset 取代
范例 参考 memset().
```


### memset

- 将一段内存空间填入某值  

```c
头文件 #include <string.h>
定义函数 void * memset(void *s, int c, size_t n);
函数说明 memset()会将参数 s 所指的内存区域前 n 个字节以参数 c 填入, 然后返回指向 s 的指针. 在编写程序
时, 若需要将某一数组作初始化, memset()会相当方便.
返回值 返回指向 s 的指针.
附加说明 参数 c 虽声明为 int, 但必须是 unsigned char, 所以范围在 0 到 255 之间.
范例
    
#include <string.h>
main()
{
    char s[30];
    memset (s, 'A', sizeof(s));
    s[30] = '\0';
    printf("%s\n", s);
}

执行 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```


### puts

```c
puts
puts() writes the string s and a trailing newline to stdout.
puts() 函数会将字符串 s 以及其后的换行符输出到标准输出设备上。
```


### sprintf

相关函数 printf, sprintf 

头文件 \#include <stdio.h> 

定义函数 int sprintf(char *str, const char * format, ...); 

函数说明 sprintf()会根据参数 format 字符串来转换并格式化数据, 然后将结果复制到参数 str 所指的字符串

数组, 直到出现字符串结束('\0')为止. 关于参数 format 字符串的格式请参考 printf(). 

返回值 成功则返回参数 str 字符串长度, 失败则返回-1, 错误原因存于 errno 中. 

附加说明 使用此函数得留意堆栈溢出, 或改用 snprintf (). 

范例

```c
#include <stdio.h> 
main() 
{ 
    char * a = "This is string A!"; 
    char buf[80]; 
    sprintf(buf, ">>> %s<<<\n", a); 
    printf("%s", buf); 
}
```

执行 >>>This is string A!<<<

## 字符串函数

### strstr
> 查找字串
![9string_strstrpng](./img/9string_strstrpng.png)

- 示例：

```c
char *s = "abcd.txt";
char *p = strstr(s, ".wps");

if(p == NULL)
    printf("文件[%s]不是WPS文件\n", s);
else
    printf("文件[%s]是WPS文件\n", s);
```

### strchr()和strtchr()
> 查找字符
![9strchr_strrchr](./img/9strchr_strrchr.png)

- 注意：
  1. 这两个函数的功能，都是在指定的字符串 s 中，试图找到字符 c。
  2. strchr() 从左往右找，strrchr() 从右往左找。
  3. 字符串结束标记 ‘\0’ 被认为是字符串的一部分。
- 示例：

```c
char *p;

p = strchr("www.qq.com", '.'); // 从左到右找到第一个出现的字符'.'
printf("%s\n", p);             // 输出 ".qq.com"

p = strrchr("www.qq.com", '.');// 从右到左找到第一个出现的字符'.'
printf("%s\n", p);             // 输出 ".com"
```

### strlen()
> 计算字符串长度

![9stringstrlen](./img/9stringstrlen.png)

- 示例：

```c
char *s = "www.yueqian.com.cn";
printf("strlen(s) = %d\n", strlen(s));
```

### strtok()
> 字串切割
![9stringstrtok](./img/9stringstrtok.png)

- 注意：
  1. 该函数会将改变原始字符串 str，使其所包含的所有分隔符变成结束标记 ‘\0’ 。
  2. 由于该函数需要更改字符串 str，因此 str 指向的内存必须是可写的。
  3. 首次调用时 str 指向原始字符串，此后每次调用 str 用 NULL 代替。
- 示例：

```c
char s[20] = "www.yueqian.com.cn";

char *p = strtok(s, ".");  // 首次调用时，s 指向需要分割的字符串
while(p != NULL)
{
    printf("%s\n", p);
    p = strtok(NULL, "."); // 此后每次调用，均使用 NULL 代替。
}
```

*注：上述代码的运行结果就是将字符串 s 拆解为"www"、“yueqian”、“com” 和 “cn”*

### strcat()和strncat()
> 字串拼接
![9strcatstrncat](./img/9strcatstrncat.png)

- 注意：
  1. 这两个函数的功能，都是将 src 中的字符串，复制拼接到 dest 的末尾。
  2. strcat() 没有边界控制，因此可能会由于 src 的过长而导致内存溢出。
  3. strncat() 有边界控制，最多复制 n+1 个字符（其中最后一个是 ‘\0’ ）到 dest 的末尾。
- 示例：

```c
char s1[10] = "abc";
strcat(s1, "xyz");
printf("%s\n", s1); // 输出 "abcxyz"

char s2[10] = "abc";
strcat(s3, "123456789"); // 此处操作内存溢出，可能会发生内存崩溃


char s[10]  = "abc";
strncat(s, "123456789", sizeof(s)-strlen(s)-1);
printf("%s\n", s); // 输出 "abc123456"，两个字符串被拼接到了一起，且不会溢出
```

- 注意：strncat()是具备边界检查的安全版本，推荐使用。

### strcpy()和strncpy()
> 字串拷贝
![9strcpystrncpy](./img/9strcpystrncpy.png)

- 注意：
  1. 这两个函数的功能，都是将 src 中的字符串，复制到 dest 中。
  2. strcpy() 没有边界控制，因此可能会由于 src 的过长而导致内存溢出。
  3. strncpy() 有边界控制，最多复制 n+1 个字符（其中最后一个是 ‘\0’ ）到 dest 中。
- 示例：

```c
char s1[5] = "abc";
strcpy(s1, "xyz);
printf("%s\n", s1); // 输出 "xyz"，原有的"abc"被覆盖

char s2[5] = "abc";
strcpy(s2, "123456789"); // 此处操作内存溢出，可能会发生内存崩溃
```



```c
char s[5] = "abc";
strncpy(s, "123456789", sizeof(s)-1);
printf("%s\n", s); // 输出 "1234"，有边界保护，不会溢出
```

- 注意：strncpy()是具备边界检查的安全版本，推荐使用。

### strcmp()和strncmp()
> 字串比较
![8strcmpstrncmp](./img/8strcmpstrncmp.png)

- 注意：
  - 比较字符串大小，实际上比较的是字符的 ASCII码值的大小。
  - 从左到右逐个比较两个字符串的每一个字符，当能“决出胜负”时立刻停止比较。
- 示例：

```c
printf("%d\n", strcmp("abc", "abc")); // 输出0，两个字符串相等
printf("%d\n", strcmp("abc", "aBc")); // 输出1，"abc" 大于 "aBc"
printf("%d\n", strcmp("999", "aaa")); // 输出-1，"999" 小于 "aaa"
```

