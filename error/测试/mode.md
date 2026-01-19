### 质数

```c
#include<stdio.h>
#include<math.h>

int main(int argc, char const *argv[])
{
    int num, flag=1;
    printf("Input the integer:");
    scanf("%d", &num);
    if (num < 2) {
        printf("%d不是质数\n", num);
        flag = 0;
    } else if(num == 2) {
        printf("%d是质数\n", num);
        flag = 1;
    } else if (!(num % 2)) {
        printf("%d不是质数\n", num);
        flag = 0;
    } else{
        for (int i = 3; i <= sqrt(num); i += 2) {
            if (num % i == 0){
                printf("%d不是质数\n", num);
                flag = 0;
            }
        }
    }
    if (flag) {
        printf("%d是质数\n", num);
    }
    return 0;
}
```





### 输入获取字符数

编写一个程序，该程序读取输入直到遇到#字符，然后报告读取的空格数目、读取的换行符数目以及读取的所有其他字符数目。
例如：输入:a 3 b
          c%#
      输出:spaces = 2, lines = 1, characters= 5

```c
#include<stdio.h>

int main(int argc, char const *argv[])
{
    int spaces = 0, lines = 0, characters = 0;
    int ch;
    while ((ch = getchar()) != '#' && ch != EOF)
    {
        if (ch == ' ') {
            spaces++;
        } else if (ch == '\n'){
            lines++;
        } else {
            characters++;
        }
    }
    printf("space = %d\tlines = %d\tcharacters = %d\n", spaces, lines, characters);
    
    return 0;
}
```



```c
#include<stdio.h>
int main(int argc, char const *argv[])
{
    int spaces = 0, lines = 0, characters = 0;
    char ch;
    while ((ch = getchar()) != '#')
    {
        switch (ch)
        {
        case ' ':
            spaces++;
            break;
        case '\n':
            lines++;
            break;
        default:
            characters++;
            break;
        }
    }
    printf("spaces = %d, lines = %d, characters = %d", spaces, lines, characters);
    return 0;
}
```



### 字符串去空格

编写一个程序，清除用户输入字符串中的空格符并将之输出。（例如用户输入”a b”，输出”ab”）

```c
#include<stdio.h>

int main(int argc, char const *argv[])
{
    int i=0;
    char ch, str[100];
    while ((ch = getchar()) != '\n') {
        if (ch != ' ') {
            str[i] = ch;
            i++;
        }
    }
    printf("%s", str);
    return 0;
}
```



```c
#include<stdio.h>
#include<stdlib.h>
#include<string.h>

int main(int argc, char const *argv[])
{
    // char str[100];
    // char *p = str;
    
    char *ps = malloc(sizeof(char) * 100);
    
    printf("Input :");
    scanf("%[^\n]", ps);

    size_t len = strlen(ps);

    for (int i = 0, j = 0; i <= len; ++i)
    {
        if (ps[i] != ' ')
        {
            ps[j++] = ps[i];
        }
    }
    printf("%s", ps);
    free(ps);
    ps = NULL;
    
    return 0;
}
```



### 字符串去重

将字符串中的重复字符删除，并输出新字符串。 
例如： gooogggle --->  输出 gole

```c
#include<stdio.h>

int main(int argc, char const *argv[])
{
    char str1[100], str2[100];
    int ascii[256] = {0}, j = 0;
    unsigned char ch;

    while ((ch = getchar()) != '\n')
    {
        str1[j++] = ch;
    }
    str1[j] = '\0';
    j = 0;
    
    for (int i = 0; str1[i] != '\0'; i++)
    {
        ch = str1[i];
        if (!ascii[ch]) {
            str2[j++] = ch;
            ascii[ch] = 1;
        }
    }
    str2[j] = '\0';
    printf("%s", str2);
    return 0;
}
```



### 字符串压缩

字符串压缩。利用字符重复出现的次数，编写一种方法，实现基本的字符串压缩功能。比如，字符串aabcccccaaa会变为2ab5c3a。若“压缩”后的字符串没有变短，则返回原先的字符串。

你可以假设字符串中只包含大小写英文字母（a至z）。例:

输入：“aabcccccaaa”

输出：“2ab5c3a”

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char *countchar(char *s);

int main(int argc, char const *argv[])
{
    char *str = "aabcccccaaa";
    char *s = countchar(str);

    printf("%s\n", str);
    printf("%s\n", s);

    return 0;
}

char *countchar(char *s)
{
    int len = strlen(s);
    char *str = malloc(sizeof(char) * (2 * len + 1));
    int index = 0, count = 1, current = s[0];

    for (int i = 1; i < len; i++) {
        if (s[i] == current) {
            count++;
        } else {
            if (count > 1) {
                str[index] = '0' + count;
                index++;
            }
            str[index] = current;
            index++;

            current = s[i];
            count = 1;
        }
    }
    if (count > 1) {
        str[index] = '0' + count;
        index++;
    }
    str[index] = current;
    index++;
    str[index] = '\0';

    int strsize = strlen(str);
    if (strsize >= len) {
        free(str);
        char *ret = malloc(sizeof(char) * (2 * len + 1));
        for (int i = 0; i < len; i++)
        {
            ret[i] = s[i];
        }
        return ret;
    }
    
    return str;
}
```



### 猴子吃桃子

> 递归

C 语言编程面试题：猴子吃桃子问题
题目描述
有一只猴子吃一堆桃子，它每天都会吃掉当前桃子数量的一半多一个。当吃到第 n 天（n≥1）时，发现只剩下 1 个桃子。请编写 C 语言程序，计算这堆桃子最初有多少个。
要求
输入：从控制台输入一个正整数 n（表示第 n 天只剩 1 个桃子）。
输出：输出桃子最初的数量。



### 打印二进制

使用递归 将十进制输出为2进制 
