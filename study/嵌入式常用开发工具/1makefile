# make

[toc]



## 基础语法

### **1. 基本概念**

#### **1.1 make是什么**

当一个项目中要编译的文件很多时，手工使用编译器一个个进行编译，很明显不具有可操作性，此时必须借助某些软件，协助我们有序地、正确地自动编译整个工程的所有该编译的文件。这样的软件被称为 **工程管理器**，`make` 就是一款工程管理器软件。

#### **1.2 Makefile是什么**

`make` 正常工作时，会读取一个称为 `Makefile` 的配置文件，该配置文件可以为 `make` 指明细致的工作规则，比如所使用的工具链、要编译的目标文件名称、要递归编译的子文件夹路径等等。

对工程管理器软件的学习，主要就是对其配置文件 `Makefile` 的语法的学习。

#### **1.3 Makefile在哪里**

`Makefile` 是用来指导make对源代码进行编译的，因此在一个多目录结构的工程项目中，凡是有源码出现的目录，都会有一个 `Makefile` 去管理，而所有的 `Makefile`，都通过工程项目顶层目录下的 `Makefile` 去直接或简洁调用。

### **2. 目标与依赖**

目标和依赖是 `Makefile` 语法中最基本的概念，假设有一个源文件 `a.c`，编译生成 `a.o` ，那么前者是依赖，后者 `a.o` 是目标，但进一步将 `a.o` 编译成可执行文件 `a`，那么 `a.o` 此时就变成依赖，最终的文件 `a` 是目标，因此目标和依赖是相对的概念。

![image-20260516144757846](./img/image-20260516144757846.png)

在 `Makefile` 中，使用冒号来区隔它们：

```makefile
# 目标:依赖
a.o:a.c

# 目标:依赖列表
image:a.o b.o c.o d.o
```



### **3. 规则**

在目标与依赖下面，使用一种特殊的语法 `"<tab>语句"` 来构成一个规则，比如：

```makefile
# 一套规则：
a.o:a.c 
    gcc a.c -o a.o -c -fPIC  # 行首必须是制表符tab
```



请注意：在上述语句中，目标与依赖、命令共同构成了一个规则，命令的行首必须是制表符 `tab` 键，不能是空格，否则会报错。另外，命令可以是多行：

```makefile
image:a.o b.o c.o d.o 
    gcc a.c -o a.o -c -fPIC
    gcc b.c -o b.o -c -fPIC
    gcc c.c -o c.o -c -fPIC
    gcc d.c -o d.o -c -fPIC
    gcc a.o b.o c.o d.o -o image
```



**重点：规则中的各个命令什么时候被执行？**

- 当目标文件不存在时。
- 当目标文件存在，但时间戳比依赖列表中的某一文件旧时。

因此，当目标文件已经被编译且其依赖文件没有修改，那么再次执行make就不会触发任何动作，这就是make和 `Makefile` 的最基本的逻辑：只在有需要的时候编译，尽量提高编译效率。



### **4. 终极目标**

在一个 `Makefile` 中，可以有多套规则，也就说可以有多个目标，在这多个目标中，最先出现的被称为终极目标，它是执行make时默认的目标，比如：

```makefile
a:a.c
    gcc a.c -o a

b:b.c
    gcc b.c -o b
```



以上 `Makefile` 中，a是终极目标，b不是，因此直接执行make时，只会针对第一套规则进行推导：

```shell
gec@ubuntu:~$ ls
a.c b.c Makefile
gec@ubuntu:~$ make
gcc a.c -o a
```



要执行第二套规则，则需要在执行make命令时特意指定，比如：

```shell
gec@ubuntu:~$ make b
gcc b.c -o b
```



或令其间接依赖于终极目标，比如：

```makefile
a:a.c b
    gcc a.c -o a

b:b.c
    gcc b.c -o b
```



执行结果是：

```shell
gec@ubuntu:~$ make
gcc b.c -o b
gcc a.c -o a
```



### **5. 多目标编译**

从上述第4小节可见， `Makefile` 中可以通过目标的相互依赖来递推整条编译链，当然像上述那样将a强行依赖于b并不是一种可取的做法，因为这么做虽然可以达到目的，但在逻辑上却让人陷入困惑，毕竟在上述例子中，a和b是两个不相干的程序，他们之间并没有依赖关系。

对于这种多目标编译，更传统的做法是，虚构一个被大家共同依赖的**伪目标**，利用 `Makefile` 编译链自动编译所有的目标，比如：

```makefile
all:a b

a:a.c
    gcc a.c -o a

b:b.c
    gcc b.c -o b
```



执行结果是：

```shell
gec@ubuntu:~$ make
gcc a.c -o a
gcc b.c -o b
```



### **6. 隐式规则**

> 头文件发生变化不会自动推导

`Makefile` 会根据目标和依赖简单地自动推导出编译语句，这种情况叫隐式规则，比如：

```makefile
all:a b
```



在上述 `Makefile` 中，没有任何编译语句，甚至连a和b的依赖文件都没写，但这个 `Makefile` 可以正常执行：

```shell
gec@ubuntu:~$ make
cc a.c -o a
cc b.c -o b
```



此时，`Makefile` 的执行逻辑是：监测到终极目标的依赖文件a和b不存在，就会自动寻找以a和b为目标的规则，在本文件中没有，然后就会尝试在本目录中寻找 a.c 和 b.c ，如果找到了就以它们为依赖文件，自动编译它们，这个过程就是隐式规则。

注意到，隐式规则可以帮忙处理一些比较简单地编译，它要求目标文件和依赖文件同名（除了后缀不同），不支持多文件编译，也不支持个性化编译选项。

### **7. 伪目标**

由于有隐式规则的存在，因此伪目标在某些极端情况下可能会被**误编译**，比如上述例子中，`all` 是伪目标，不是真正要编译生成的目标，但如果源码目录中恰巧有一个文件叫 `all.c` ，那么根据 `Makefile` 的隐式规则，将会触发 all.c 的编译动作。

如何规避隐式规则这种误操作呢？很简单，明确告诉 `Makefile` ，`all`是伪目标，不要编译他：

```makefile
all:a b

.PHONY:all
```



上述语句中，`.PHONY` 是 `Makefile` 的一个关键字，用来声明伪目标，防止隐式规则滥用。

在 `Makefile` 中，常见的伪目标除了all之外，还有clean、distclean等，用来清除生成的中间文件，例如：

```makefile
all:a b

clean:  # 清除所有目标文件、可重定位文件
    rm a b *.o

distclean:clean  # 先执行clean，然后清除所有交换文件、核心转储文件
    rm .*.sw? core

.PHONY:all clean
```



## 变量

### **1. 自定义变量**

类似于shell脚本，可以在 `Makefile` 定义变量和引用变量：

```makefile
BIN=a b

all:$(BIN)

clean:
    rm $(BIN)
```



### **2. 内置变量**

`Makefile`有许多跟编译相关的内置变量，比如：

```makefile
CFLAGS  = "-O2 -Wall" # C编译选项
LDFLAGS = "-lpthread" # 链接器参数
CC  = aarch-linux-gnu-gcc # C编译器名称
CXX = aarch-linux-gnu-g++ # C编译器名称
```



可以通过修改上述变量的值，来个性化各种编译场景，例如：

```makefile
CC  = gcc
CXX = aarch64-linux-gnu-g++

CFLAGS  = -O2 -Wall
LDFLAGS = -lpthread

ELF = a b

all:a b

a:a.c
	$(CC) a.c -o a $(CFLAGS) $(LDFLAGS)

b:b.cpp
	$(CXX) b.cpp -o b

clean:
	rm a b

.PHONY:all
```



### **3. 变量的定义引用**

所谓定义引用，指的是在定义一个变量的时候引用了另一个变量的值。比如下面定义变量B的时候，其值引用了变量A：

```makefile
A = China
B = I love $(A)

all:
    echo $(B)
```



执行结果：

```shell
gec@ubuntu:~$ make
echo I love China
I love China
```



#### **3.1 全文搜索模式**

注意到，上述变量A和B的定义，可以任意调换其顺序，比如：

```makefile
B = I love $(A) # 照样可以引用出现在后面的变量A的值

all:
    echo $(B)

A = China
```



这不会有任何影响，这是因为 `Makefile` 中直接用等号 “`=`” 定义变量时若存在对其他变量的引用，会采取**全文搜索**的策略去找引用值。

#### **3.2 简单定义模式**

如果不想要 `Makefile` 的这种全文搜索的特性，而希望只引用定义语句之前出现过的变量的值的话，就要用 “`:=`” 简单模式，例如：

```makefile
B := I love $(A) # 只引用在此之前有定义的A的值

all:
    echo $(B)    # 输出"I love"

A = China
```



#### **3.3 变量追加**

`Makefile` 中的变量都是字符串，可以使用 “`+=`” 进行追加，例如：

```makefile
CFLAGS  = -O2    # 全文搜索模式
CFLAGS += -Wall
CFLAGS += -Werror

# 等价于
CFLAGS = -O2 -Wall -Werror
```



#### **3.4 变量值修改**

`Makefile` 中的变量本质是一连串单词，通常是待处理的一系列文件名称，在实际操作中经常需要对这些文件名进行模式替换，比如有一串由C语言源文件组成的字串，希望将其中的文件后缀 *.c 变成 *.o，可以这么做：

```makefile
A = srt.c string.c tcl.c
B = $(A:%.c=%.o)  # 此处，变量B的值是 srt.o string.o tcl.o
```



### **4. override**

在执行make时，通常可以在命令行中携带一个变量的定义，如果这个变量跟Makefile中出现的某一变量重名，那么命令行变量的定义将会覆盖Makefile中的变量。就是说，对于一个在Makefile中使用常规方式（使用“=”、“:=”或者“define”）定义的变量，我们可以在执行make时通过命令行方式重新指定这个变量的值，命令行指定的值将替代出现在Makefile中此变量的值。比如：

```makefile
A = an apple tree
all:
	@echo $(A)  # 输出变量A的值，符号@代表不输出命令本身
```



直接执行 make 的结果是：

```shell
gec@ubuntu:~$  make A="an elephant"
an elephant
```



可见，虽然Makefile定义了A的值为”an apple tree”，但被命令行定义的A的值覆盖了，变成了”an elephant”。如果不想被覆盖，则可以写成：

```makefiel
override A = an apple tree
all:
	@echo $(A)
```



此时，执行结果是：

```shell
gec@ubuntu:~$  make A="an elephant"
an apple tree
```



但是**请注意**：指示符 `override` 并不是用来防止Makefile的内部变量被命令行参数覆盖的，其真正存在的目的是：

- 为了使用户可以改变或者追加那些使用make的命令行指定的变量的定义。
- 即：实现了在Makefile中增加或者修改命令行参数的一种机制。

通常，我们会通过命令行来指定一些附加的、个性化的编译参数，而对一些通用的参数或者必需的编译参数，我们则在Makefile中指定，为了使两个地方指定的参数和谐相处，不相互覆盖，一般就用指示符 `override` 来实现。

例如，无论命令行指定那些编译参数，必须打开所有的编译警告信息“-Wall”，则 `Makefile` 的变量 `CFLAGS` 应该这样写：

```makefile
override CFLAGS += -Wall
test:test.c
```



执行结果是：

```shell
gec@ubuntu:~$ make CFLAGS="-g"
cc -g -Wall a.c -o a
```

​	

### **6. 静态规则与自动化变量**

所谓静态规则，就是可以使用模式匹配的方式，自动生成若干规则的机制。例如：

```makefile
OBJ = a.o b.o c.o

image:$(OBJ)
	$(CC) $(OBJ) -o image

#静态规则
$(OBJ):%.o:%.c  
	$(CC) $^ -o $@ -c # 运用了自动化变量自适应不同的目标和依赖

clean:
	$(RM) $(OBJ) image

.PHONY: clean
```



在上述静态规则中，从变量OBJ中按模式%.o抽取单词出来，作为新规则的目标，然后又从模式%.c匹配出来的单词，作为新规则的依赖，这样一来就形成了3组目标与依赖：


静态规则生成目标和依赖

最后，每个规则都生成了：

```makefile
#静态规则
a.o:a.c
	$(CC) $^ -o $@ -c
b.o:b.c
	$(CC) $^ -o $@ -c
c.o:c.c
	$(CC) $^ -o $@ -c
```



注意到，自动生成的规则中的编译语句包含了自动化变量：

- ^ ：代表所在规则的依赖列表
- @ ：代表所在规则的目标

所谓自动化变量，指的是它们的值会随着规则**自动地**发生变化，它们的含义是确定的，但是它们的值会自适应不同的规则，这个特性刚好与静态规则自动产生规则像。除了上面两个常见的自动化变量外，还有下述这些自动化变量。

| **变量名** | **含义**                                            | **备注**                                              |
| ---------- | --------------------------------------------------- | ----------------------------------------------------- |
| @          | 代表其所在规则的目标的完整名称                      |                                                       |
| %          | 代表其所在规则的静态库文件的一个成员名              |                                                       |
| <          | 代表其所在规则的依赖列表的第一个文件的完整名称      |                                                       |
| ?          | 代表所有时间戳比目标文件新的依赖文件列表 用空格隔开 |                                                       |
| ^          | 代表其所在规则的依赖列表da                          | 同一文件不可重复                                      |
| +          | 代表其所在规则的依赖列表                            | 同一文件可重复 主要用在程序链接时，库的交叉引用场合。 |



## 函数

###  **Makefile函数**

`Makefile` 中的函数可以实现一些特性的功能，其基本语法是：

```makefile
VAR = $(函数 参数1[,参数2,参数3,...])
```



语法要点有：

- 函数及其参数用 `$()` 包含
- 函数与参数之间用空格隔开
- 若函数需要多个参数，则参数之间用逗号隔开
- 若函数有返回值，其值可以直接赋值给变量

### **1. 内置文本处理函数**

#### **1.1 `$(subst FROM,TO,TEXT)`**

功能：
  将字符串TEXT中的字符FROM替换为TO。
返回：
  替换之后的新字符串。
范例：

```makefile
A = $(subst pp,PP,apple tree)
```



替换之后变量A的值是"aPPle tree"

#### **1.2 `$(patsubst PATTERN,REPLACEMENT,TEXT)`**

功能：
  按照PATTERN搜索TEXT中所有以空格隔开的单词，并将它们替换为REPLACEMENT。**注意：** 参数PATTERN可以使用模式通配符%来代表一个单词中的若干字符，如果此时REPLACEMENT中也出现%，那么REPLACEMENT中的%跟PATTERN中的%是一样的。
返回：
  替换之后的新字符串。
范例：

```makefile
A = $(patsubst %.c,%.o,a.c b.c)
```



替换之后变量A的值是 `a.o b.o`

#### **1.3 `$(strip STRING)`**

功能：
  去掉字符串中开头和结尾的多余的空白符（掐头去尾），并将其中连续的多个空白符合并为一个。**注意：** 所谓的空白符指的是空格、制表符。
返回：
  去掉多余空白符之后的新字符串。
范例：

```makefile
A = $(strip "  apple     tree  ")
```



处理之后，变量A的值是 `apple tree`

#### **1.4 `$(findstring NEEDLE, HAYSTACK)`**

功能：
  在给定的字符串HAYSTACK中查找子串NEEDLE。
返回：
  找到则返回NEEDLE，否额返回空。
范例：

```makefile
A = $(findstring pp, apple tree)
B = $(findstring xx, apple tree)
```



变量A的值是`pp`，变量B的值是空。

#### **1.5 `$(filter PATTERN,TEXT)`**

功能：
  过滤掉TEXT中所有不符合给定模式PATTERN的单词。其中PATTERN可以是多个模式的组合。
返回：
  TEXT中所有符合模式组合PATTERN的单词组成的子串。
范例：

```makefile
A = a.c b.o c.s d.txt
B = $(filter %.c %.o,$(A))
```



过滤后变量B的值是 `a.c b.o`

#### **1.6 `$(filter-out PATTERN,TEXT)`**

功能：
  过滤掉TEXT中所有符合给定模式PATTERN的单词，与函数filter功能相反。
返回：
  TEXT中所有不符合模式组合PATTERN的单词组成的子串。
范例：

```makefile
A = a.c b.o c.s d.txt
B = $(filter %.c %.o,$(A))
```



过滤后变量B的值是 `c.s d.txt`

#### **1.7 `$(sort LIST)`**

功能：
  将字符串LIST中的单词按字母升序的顺序排序，并且去掉重复的单词。
返回：
  排完序且没有重复单词的新字符串。
范例：

```makefile
A = foo bar lose foo ugh
B = $(sort $(A))
```



处理后变量B的值是 `bar foo lose ugh`

#### **1.8 `$(word N,TEXT)`**

功能：
  取字符串TEXT中的第N个单词。注意，N必须为正整数。
返回：
  第N个单词（如果N大于TEXT中单词的总数则返回空）。
范例：

```makefile
A = an apple tree
B = $(word 2 $(A))
```



处理后变量B的值是 `apple`

#### **1.9 `$(wordlist START,END,TEXT)`**

功能：
  取字符串TEXT中介于START和END之间的子串。
返回：
  介于START和END之间的子串（如果START大于TEXT中单词的总数或者START大于END时返回空，否则如果END大于TEXT中单词的总数则返回从START开始到TEXT的最后一个单词的子串）。
范例：

```makefile
A = the apple tree is over 5 meters tall
B = $(wordlist 4,100,$(A))
```



处理后变量B的值是 `is over 5 meters tall`

以上9个函数是make内嵌的的文本处理函数。在书写Makefile时可搭配使用，来实现复杂功能。

### **2. 文件名处理函数**

GNU make除了这些内嵌的文本处理函数之外，还存在一些针对于文件名的处理函数。这些函数主要用来对一系列空格分割的文件名进行转换，这些函数的参数被作为若干个文件名来对待，函数对这样的一组文件名按照一定方式进行处理，并返回以空格分隔的多个文件名序列。他们是：

#### **2.1 `$(dir NAMES)`**

功能：
  取文件列表NAMES中每一个路径的目录部分。
返回：
  每一个路径的目录部分组成的新的字符串。
范例：

```makefile
A = /etc/init.d /home/gec/.bashrc /usr/bin/man
B = $(dir $(A))
```



处理后变量B的值是"`/etc/ /home/gec/ /usr/bin/`"

#### **2.2 `$(notdir NAMES)`**

功能：
  取文件列表NAMES中每一个路径的文件名部分。
返回：
  每一个路径的文件名部分组成的新的字符串。**注意：** 如果NAMES中存在不包含斜线的文件名，则不改变这个文件名，而以反斜线结尾的文件名，用空串代替。
范例：

```makefile
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(dir $(A))
```



处理后变量B的值是"`init.d .bashrc man`"

#### **2.3 `$(suffix NAMES)`**

功能：
  取文件列表NAMES中每一个路径的文件的后缀部分。后缀指的是最后一个.后面的子串。
返回：
  每一个路径的文件名的后缀部分组成的新的字符串。
范例：

```makefile
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(suffix $(A))
```



处理后变量B的值是"`.d .bashrc`"

#### **2.4 `$(basename NAMES)`**

功能：
  取文件列表NAMES中每一个路径的文件的前缀部分。前缀指的是最后一个.后面除了后缀的子串。
返回：
  每一个路径的文件名的前缀部分组成的新的字符串。
范例：

```makefile
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(basename $(A))
```



处理后变量B的值是"`/etc/init /home/vincent/ /usr/bin/man`"

#### **2.5 `$(addsuffix SUFFIX,NAMES)`**

功能：
  为文件列表NAMES中每一个路径的文件名添加后缀SUFFIX。
返回：
  添加了后缀SUFFIX的字符串。
范例：

```makefile
A = /etc/init.d /home/gec/.bashrc /usr/bin/man
B = $(addsuffix .bk,$(A))
```



处理后B为"`/etc/init.d.bk /home/gec/.bashrc.bk /usr/bin/man.bk`"

#### **2.6 `$(addprefix PREFIX,NAMES)`**

功能：
  为文件列表NAMES中每一个路径的文件名添加前缀PREFIX。
返回：
  添加了前缀PREFIX的字符串。
范例：

```makefile
A = /etc/init.d /usr/bin/man
B = $(addprefix host:,$(A))
```



处理后B的值为：
“`host:/etc/init.d host:/usr/bin/man`”

#### **2.7 `$(wildcard PATTERN)`**

功能：
  获取匹配模式为PATTERN的文件名。
返回：
  匹配模式为PATTERN的文件名。
范例：

```makefile
A = $(wildcard *.c)
```



假设当前路径下有两个.c文件a.c和b.c，则处理后A的值为：“`a.c b.c`”

#### **2.8 `$(foreach VAR,LIST,TEXT)`**

功能：
  首先展开变量“VAR”和“LIST”，而表达式“TEXT”中的变量引用不被展开。执行时把“LIST”中使用空格分割的单词依次取出赋值给变量“VAR”，然后执行“TEXT”表达式，重复直到“LIST”的最后一个单词（为空时结束）。
它是一个循环函数，类似于Linux的Shell中的循环。注意：由于“TEXT”中的变量或者函数引用在执行时才被展开，因此如果在“TEXT”中存在对“VAR”的引用，那么“VAR”的值在每一次展开式将会到的不同的值。
返回：
  以空格分隔的多次表达式“TEXT”的计算的结果。
范例：
假设当前目录下有两个子目录 `dir1/` 和 `dir2/`，先要将他们里面的所有文件赋值给变量FILES，可以这么写：

```shell
gec@ubuntu:~$ tree
.
├── dir1/
│   ├── file1
│   └── file2
├── dir2/
│   ├── a.c
│   └── b.c
└── Makefile
```



```makefile
# Makefile
DIR = dir1/ dir2/
FILES = $(foreach dir,$(DIR),$(wildcard $(dir)/*))

all:
    @echo $(FILES)
```



执行结果如下：

```shell
gec@ubuntu:~$ make
dir1/file1  dir1/file2  dir2/a.c  dir2/b.c
```



## 其他语法

### **1. 嵌套Makefile**

在多目录结构中，`Makefile`可以通过内置命令嵌套调用。例如有如下目录结构：

```shell
gec@ubuntu:~$ tree
.                   
├── dir/
│   └── Makefile   # 子Makefile
└── Makefile       # 顶层Makefile
```



要在顶层 `Makefile` 中调用子 `Makefile` ，只需执行如下语句：

```makefile
all:
    $(MAKE) -C dir/  # 调用指定目录下的子Makefile
```



### **2. 变量导出**

在嵌套调用子 `Makefile` 的过程中，如果需要将变量传递给子 `Makefile` ，可以使用如下语句：

```makefile
# 顶层Makefile
export A = apple    # 在顶层Makefile中，将变量A导出
B = banana          # 在顶层Makefile中，变量B未导出

all:
	@echo "rank 1: $(A)"
	@echo "rank 1: $(B)"
	@$(MAKE) -C dir/ # 调用位于dir/中的子Makefile
```



```
all:
	@echo "rank 2: $(A)" # 从顶层Makefile获得变量的值
	@echo "rank 2: $(B)" # 空值
```



执行结果是：

```shell
gec@ubuntu:~$ make
rank 1: apple
rank 1: banana
make[1]: Entering directory '/home/gec/dir'
rank 2: apple
rank 2:
make[1]: Leaving directory '/home/gec/dir'
```



### **3. 实用make选项**

#### **3.1 指定要执行的Makefile文件**

```makefile
make -f Altmake
make --file Altmake
make --makefile Altmake
```



以上三种方式都可以用来执行一个普通命令的文件作为Makefile文件。在缺省的情况下不指定任何Makefile文件，则make会在当前目录下依次查找命名为GNUmakefile和Makefile以及makefile的文件。

#### **3.2 指定终极目标**

```
make TARGET
```



所谓的终极目标指的是Makefile中第一个出现的规则中的第一个目标，是缺省的整个工程或者程序编译过程的总的规则和目的。如果想要执行除该目标之外的其他普通目标位编译的最终目的，则可以在执行make的同时指定。
在我们需要对程序的一部分进行编译，或者仅仅对某几个程序进行编译而不是完整地编译整个工程的时候，指定终极目标就很有用。

#### **3.3 强制重建所有规则中目标**

```
make -B
make --always-make
```



#### **3.4 指定Makefile的所在路径**

```
make -C dir/
make --directory=dir/
```



假如要执行的Makefile文件不在当前目录，可以使用该选项指定。这个选项一般用在一个Makefile内部调用另一个子Makefile的场景

Makefile的详细的语法非常多，本章只是一个引子，但对于认识Makefile以及做一些基本的应用足已，毕竟复杂的Makefile都不可能手工写，而是会用其他的软件自动生成的。

点击下载官方文档：[GNU make中文手册.pdf](http://vm.yueqian.com.cn:8886/group1/M00/00/09/rBJlJmKeBnaAFF4cABSX3jQpiOc925.pdf?token=null&ts=null&filename=GNU make中文手册.pdf)



## 其他



### 模板

```

```



### vscode插件

vscode-makefile-term

在每个target上方出现执行按钮
