# Makefile+cmake

[toc]

## Makefile

#### **1.问题的引入**

当我们要编译成千上万个源程序文件的时候，光靠手工使用GCC工具来达到目的也许就会很没有效率，我们亟需一款能够帮助我们自动检查文件的更新情况，自动进行编译的软件，GNUmake就是这样的一款软件。

在 Linux（unix）环境下使用 GNU 的 make工具能够比较容易的构建一个属于你自己的工程，整个工程的编译只需要一个命令就可以完成编译、连接以至于最后的执行。不过这需要我们投入一些时间去完成一个或者多个称之为 Makefile 文件的编写。

#### **2.make与Makefile的概念**

##### **2.1工程管理器make的概念**

协助我们有序地、正确地自动编译整个工程的所有该编译的文件，这样的软件被称为 **工程管理器**，make 就是一款工程管理器软件。

##### **2.2** **Makefile的概念**

make 正常工作时，会读取一个称为 Makefile 的配置文件，该配置文件可以为 make 指明细致的工作规则，比如所使用的工具链、要编译的目标文件名称、要递归编译的子文件夹路径等等。对工程管理器软件的学习，主要就是对其配置文件 Makefile 的语法的学习。

Makefile 文件描述了整个工程的编译、连接等规则。其中包括：工程中的哪些源文件需要编译以及如何编译、需要创建那些库文件以及如何创建这些库文件、如何最后产生我们想要得可执行文件。尽管看起来可能是很复杂的事情，但是为工程编写 Makefile 的好处是能够使用一行命令来完成“自动化编译”，一旦提供一个（通常对于一个工程来说会是多个）正确的 Makefile。编译整个工程你所要做的唯一的一件事就是在 shell 提示符下输入 make 命令。整个工程完全自动编译，极大提高了效率。

make 是一个命令工具，它解释 Makefile 中的指令（应该说是规则）。在 Makefile 文件中描述了整个工程所有文件的编译顺序、编译规则。

##### **2.3Makefile文件的位置**

Makefile 是用来指导make对源代码进行编译的，因此在一个多目录结构的工程项目中，凡是有源码出现的目录，都会有一个 Makefile 去管理，而所有的 Makefile，都通过工程项目顶层目录下的 Makefile 去直接或间接调用。

 

#### **3.目标与依赖**

目标和依赖是 Makefile 语法中最基本的概念，假设有一个源文件 a.c，编译生成 a.o ，那么前者是依赖，后者 a.o 是目标，但进一步将 a.o 编译成可执行文件 a，那么 a.o 此时就变成依赖，最终的文件 a 是目标，因此目标和依赖是相对的概念。

![image-20260714091146390](./img/image-20260714091146390.png)

在 Makefile 中，使用冒号来区隔它们：

```makefile
# 目标:依赖
a.o:a.c
 
# 目标:依赖列表
image:a.o b.o c.o d.o
```

目标：通常是最后需要生成的文件名或者为了实现这个目的而必需的中间过程文件名。可以是.o 文件、也可以是最后的可执行程序的文件名等。另外，目标也可以是一个 make执行的动作的名称，如目标“clean”，我们称这样的目标是“伪目标”。

依赖：生成规则目标所需要的文件名列表。通常一个目标依赖于一个或者多个文件。

 

#### **4.规则**

在目标与依赖下面，使用一种特殊的语法 "<tab>语句" 来构成一个规则，比如：

```makefile
# 一套规则：
a.o:a.c 
    gcc a.c -o a.o -c -fPIC  # 行首必须是制表符tab
```

请注意：在上述语句中，目标与依赖、命令共同构成了一个规则，命令的行首必须是制表符 tab 键，不能是空格，否则会报错。另外，命令可以是多行：

```makefile
image:a.o b.o c.o d.o 
    gcc a.c -o a.o -c -fPIC
    gcc b.c -o b.o -c -fPIC
    gcc c.c -o c.o -c -fPIC
    gcc d.c -o d.o -c -fPIC
    gcc a.o b.o c.o d.o -o image
```

重点：规则中的各个命令什么时候被执行？

当目标文件不存在时。

当目标文件存在，但时间戳比依赖列表中的某一文件旧时。

因此，当目标文件已经被编译且其依赖文件没有修改，那么再次执行make就不会触发任何动作，这就是make和 Makefile 的最基本的逻辑：只在有需要的时候编译，尽量提高编译效率。

练习：编写一个最简单的 Makefile，管理一个单一源码文件。

 

#### **5.** **终极目标和多目标编译**

在一个 Makefile 中，可以有多套规则，也就说可以有多个目标，在这多个目标中，最先出现的被称为终极目标，它是执行make时默认的目标，比如：

```makefile
a:a.c
    gcc a.c -o a
b:b.c
    gcc b.c -o b
```

以上 Makefile 中，a是终极目标，b不是，因此直接执行make时，只会针对第一套规则进行推导：

```bash
gec@ubuntu:~$ ls
a.c b.c Makefile
gec@ubuntu:~$ make
gcc a.c -o a
```

 

要执行第二套规则，则需要在执行make命令时特意指定，比如：

```bash
gec@ubuntu:~$ make b
gcc b.c -o b
```

 

对于这种多目标编译，更传统的做法是，虚构一个被大家共同依赖的**伪目标**，利用 Makefile 编译链自动编译所有的目标，比如：

```makefile
all:a b
 
a:a.c
    gcc a.c -o a
 
b:b.c
    gcc b.c -o b
```

 

执行结果是：

```bash
gec@ubuntu:~$ make
gcc a.c -o a
gcc b.c -o b
```

 

#### **6.** **隐式规则**

Makefile 会根据目标和依赖简单地自动推导出编译语句，这种情况叫隐式规则，比如：

```makefile
all:a b
```

在上述 Makefile 中，没有任何编译语句，甚至连a和b的依赖文件都没写，但这个 Makefile 可以正常执行：

```bash
gec@ubuntu:~$ make
cc a.c -o a
cc b.c -o b
```

此时，Makefile 的执行逻辑是：监测到终极目标的依赖文件a和b不存在，就会自动寻找以a和b为目标的规则，在本文件中没有，然后就会尝试在本目录中寻找 a.c 和 b.c ，如果找到了就以它们为依赖文件，自动编译它们，这个过程就是隐式规则。

注意到，隐式规则可以帮忙处理一些比较简单地编译，它要求目标文件和依赖文件同名（除了后缀不同），不支持多文件编译，也不支持个性化编译选项。

 

#### **7. 伪目标**

Makefile 中把那些没有任何依赖只有执行动作的目标称为“伪目标”（phony targets）。由于有隐式规则的存在，因此伪目标在某些极端情况下可能会被**误编译**，比如上述例子中，all 是伪目标，不是真正要编译生成的目标，但如果源码目录中恰巧有一个文件叫 all.c ，那么根据 Makefile 的隐式规则，将会触发 all.c 的编译动作。

如何规避隐式规则这种误操作呢？很简单，明确告诉 Makefile ，all是伪目标，不要编译他：

```makefile
all:a b
 
.PHONY:all
```

 

上述语句中，.PHONY 是 Makefile 的一个关键字，用来声明伪目标，防止隐式规则滥用。

在 Makefile 中，常见的伪目标除了all之外，还有clean、distclean等，用来清除生成的中间文件，例如：

```makefile
all:a b
 
clean:  # 清除所有目标文件、可重定位文件
    rm a b *.o
 
distclean:clean  # 先执行clean，然后清除所有交换文件、核心转储文件
    rm .*.sw? core
 
.PHONY:all clean
```

目标“clean”不是一个文件，它仅仅代表执行一个动作的标识。正常情况下，不需要执行这个规则默认的推导动作（比如发现这个规则的依赖不存在，自动推导该依赖生成的规则），因此目标“clean”没有出现在其它任何规则的依赖列表中。因此在执行 make时，它所指定的动作不会被执行。除非在执行 make 时明确地指定它。而且目标“clean”没有任何依赖文件，它只有一个目的，就是通过这个目标名来执行它所定义的命令。

 

#### **8.变量**

#####  **8.1自定义变量**

类似于shell脚本，可以在 Makefile 定义变量和引用变量：

```makefile
BIN=a b
 
all:$(BIN)

clean:
    rm $(BIN)
```

##### **8.2变量的定义引用**

所谓定义引用，指的是在定义一个变量的时候引用了另一个变量的值。比如下面定义变量B的时候，其值引用了变量A：

```makefile
A = China
B = I love $(A)
 
all:
    echo $(B)
```

执行结果：

```bash
gec@ubuntu:~$ make
echo I love China
I love China
```

##### **8.3内置变量**

Makefile有许多跟编译相关的内置变量，比如：

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

##### **8.4 静态规则与自动化变量**

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

![image-20260714091222135](./img/image-20260714091222135.png)

#### **9.赋值符号与续行符**

1. =

：这是简单的赋值操作符。使用等号赋值的变量在Makefile中只会被赋予一次值，即使在Makefile中有多个赋值语句，也只有最后一个赋值语句的值会被使用

2. := 像鼻运算符

：这个操作符用于定义一个变量，并立即展开其值。这意味着在Makefile的解析过程中，使用赋值的变量会在定义时立即计算其值，而不是在变量使用时。

3. ?=

：条件赋值操作符。如果变量之前没有被赋值，那么使用可以给它赋一个默认值。如果变量已经有值了，那么即使后面有赋值，也不会改变其值。

4. +=

：这个操作符用于向已经定义的变量追加值。如果变量已经存在，会将右侧的值添加到变量现有的值后面。如果变量不存在，的行为就像简单的赋值操作符。

#### **10.Makefile函数**

Makefile 中的函数可以实现一些特性的功能，其基本语法是：

```makefile
VAR = $(函数 参数1[,参数2,参数3,...])
```

 语法要点有：

- 函数及其参数用 $() 

- 函数与参数之间用空格隔开

- 若函数需要多个参数，则参数之间用逗号隔开

- 若函数有返回值，其值可以直接赋值给变量

##### **1. 内置文本处理函数**

**1.1** **$(subst FROM,TO,TEXT)**

功能：

  将字符串TEXT中的字符FROM替换为TO。

返回：

  替换之后的新字符串。

范例：

```makefile
A = $(subst pp,PP,apple tree)
 
```

 

替换之后变量A的值是"aPPle tree"

**1.2** **$(patsubst PATTERN,REPLACEMENT,TEXT)**

功能：

  按照PATTERN搜索TEXT中所有以空格隔开的单词，并将它们替换为REPLACEMENT。**注意：** 参数PATTERN可以使用模式通配符%来代表一个单词中的若干字符，如果此时REPLACEMENT中也出现%，那么REPLACEMENT中的%跟PATTERN中的%是一样的。

返回：

  替换之后的新字符串。

范例：

```
A = $(patsubst %.c,%.o,a.c b.c)
 
```

 

替换之后变量A的值是 a.o b.o

 

**1.3** **$(strip STRING)**

功能：

  去掉字符串中开头和结尾的多余的空白符（掐头去尾），并将其中连续的多个空白符合并为一个。**注意：** 所谓的空白符指的是空格、制表符。

返回：

  去掉多余空白符之后的新字符串。

范例：

```
A = $(strip "  apple     tree  ")
 
```

 

处理之后，变量A的值是 apple tree

 

**1.4** **$(findstring NEEDLE, HAYSTACK)**

功能：

  在给定的字符串HAYSTACK中查找子串NEEDLE。

返回：

  找到则返回NEEDLE，否额返回空。

范例：

```
A = $(findstring pp, apple tree)
B = $(findstring xx, apple tree)
 
```

 

变量A的值是pp，变量B的值是空。

 

**1.5** **$(filter PATTERN,TEXT)**

功能：

  过滤掉TEXT中所有不符合给定模式PATTERN的单词。其中PATTERN可以是多个模式的组合。

返回：

  TEXT中所有符合模式组合PATTERN的单词组成的子串。

范例：

```
A = a.c b.o c.s d.txt
B = $(filter %.c %.o,$(A))
 
```

 

过滤后变量B的值是 a.c b.o

 

**1.6** **$(filter-out PATTERN,TEXT)**

功能：

  过滤掉TEXT中所有符合给定模式PATTERN的单词，与函数filter功能相反。

返回：

  TEXT中所有不符合模式组合PATTERN的单词组成的子串。

范例：

```
A = a.c b.o c.s d.txt
B = $(filter %.c %.o,$(A))
 
```

 

过滤后变量B的值是 c.s d.txt

 

**1.7** **$(sort LIST)**

功能：

  将字符串LIST中的单词按字母升序的顺序排序，并且去掉重复的单词。

返回：

  排完序且没有重复单词的新字符串。

范例：

```
A = foo bar lose foo ugh
B = $(sort $(A))
 
```

 

处理后变量B的值是 bar foo lose ugh

**1.8** **$(word N,TEXT)**

功能：

  取字符串TEXT中的第N个单词。注意，N必须为正整数。

返回：

  第N个单词（如果N大于TEXT中单词的总数则返回空）。

范例：

```
A = an apple tree
B = $(word 2 $(A))
 
```

 

处理后变量B的值是 apple

 

**1.9** **$(wordlist START,END,TEXT)**

功能：

  取字符串TEXT中介于START和END之间的子串。

返回：

  介于START和END之间的子串（如果START大于TEXT中单词的总数或者START大于END时返回空，否则如果END大于TEXT中单词的总数则返回从START开始到TEXT的最后一个单词的子串）。

范例：

```
A = the apple tree is over 5 meters tall
B = $(wordlist 4,100,$(A))
 
```

 

处理后变量B的值是 is over 5 meters tall

以上9个函数是make内嵌的的文本处理函数。在书写Makefile时可搭配使用，来实现复杂功能。

 

##### **2. 文件名处理函数**

GNU make除了这些内嵌的文本处理函数之外，还存在一些针对于文件名的处理函数。这些函数主要用来对一系列空格分割的文件名进行转换，这些函数的参数被作为若干个文件名来对待，函数对这样的一组文件名按照一定方式进行处理，并返回以空格分隔的多个文件名序列。他们是：

**2.1** **$(dir NAMES)**

功能：

  取文件列表NAMES中每一个路径的目录部分。

返回：

  每一个路径的目录部分组成的新的字符串。

范例：

```
A = /etc/init.d /home/gec/.bashrc /usr/bin/man
B = $(dir $(A))
 
```

处理后变量B的值是"/etc/ /home/gec/ /usr/bin/"

 

**2.2** **$(notdir NAMES)**

功能：

  取文件列表NAMES中每一个路径的文件名部分。

返回：

  每一个路径的文件名部分组成的新的字符串。**注意：** 如果NAMES中存在不包含斜线的文件名，则不改变这个文件名，而以反斜线结尾的文件名，用空串代替。

范例：

```
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(dir $(A))
 
```

 

处理后变量B的值是"init.d .bashrc man"

 

**2.3** **$(suffix NAMES)**

功能：

  取文件列表NAMES中每一个路径的文件的后缀部分。后缀指的是最后一个.后面的子串。

返回：

  每一个路径的文件名的后缀部分组成的新的字符串。

范例：

```
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(suffix $(A))
 
```

 

处理后变量B的值是".d .bashrc"

 

**2.4** **$(basename NAMES)**

功能：

  取文件列表NAMES中每一个路径的文件的前缀部分。前缀指的是最后一个.后面除了后缀的子串。

返回：

  每一个路径的文件名的前缀部分组成的新的字符串。

范例：

```
A = /etc/init.d /home/vincent/.bashrc /usr/bin/man
B = $(basename $(A))
 
```

 

处理后变量B的值是"/etc/init /home/vincent/ /usr/bin/man"

 

**2.5** **$(addsuffix SUFFIX,NAMES)**

功能：

  为文件列表NAMES中每一个路径的文件名添加后缀SUFFIX。

返回：

  添加了后缀SUFFIX的字符串。

范例：



```
A = /etc/init.d /home/gec/.bashrc /usr/bin/man
B = $(addsuffix .bk,$(A))
 
```

 

处理后B为"/etc/init.d.bk /home/gec/.bashrc.bk /usr/bin/man.bk"

 

**2.6** **$(addprefix PREFIX,NAMES)**

功能：

  为文件列表NAMES中每一个路径的文件名添加前缀PREFIX。

返回：

  添加了前缀PREFIX的字符串。

范例：

```
A = /etc/init.d /usr/bin/man
B = $(addprefix host:,$(A))
 
```

 

处理后B的值为：

“host:/etc/init.d host:/usr/bin/man”

 

**2.7** **$(wildcard PATTERN)**

功能：

  获取匹配模式为PATTERN的文件名。

返回：

  匹配模式为PATTERN的文件名。

范例：

```
A = $(wildcard *.c)
 
```

 

假设当前路径下有两个.c文件a.c和b.c，则处理后A的值为：“a.c b.c”

 

**2.8** **$(foreach VAR,LIST,TEXT)**

功能：

  首先展开变量“VAR”和“LIST”，而表达式“TEXT”中的变量引用不被展开。执行时把“LIST”中使用空格分割的单词依次取出赋值给变量“VAR”，然后执行“TEXT”表达式，重复直到“LIST”的最后一个单词（为空时结束）。

它是一个循环函数，类似于Linux的Shell中的循环。注意：由于“TEXT”中的变量或者函数引用在执行时才被展开，因此如果在“TEXT”中存在对“VAR”的引用，那么“VAR”的值在每一次展开式将会到的不同的值。

返回：

  以空格分隔的多次表达式“TEXT”的计算的结果。

范例：

假设当前目录下有两个子目录 dir1/ 和 dir2/，先要将他们里面的所有文件赋值给变量FILES，可以这么写：

```bash
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

 

```Makefile
# Makefile
DIR = dir1/ dir2/
FILES = $(foreach dir,$(DIR),$(wildcard $(dir)/*))
 
all:
    @echo $(FILES)
 
```

 

执行结果如下：

```
gec@ubuntu:~$ make
dir1/file1  dir1/file2  dir2/a.c  dir2/b.c
```

 

**10.****Makefile其他语法**

**1. 嵌套Makefile**

在多目录结构中，Makefile可以通过内置命令嵌套调用。例如有如下目录结构：

```
gec@ubuntu:~$ tree
.                   
├── dir/
│   └── Makefile   # 子Makefile
└── Makefile       # 顶层Makefile
 
```

要在顶层 Makefile 中调用子 Makefile ，只需执行如下语句：

```
all:
    $(MAKE) -C dir/  # 调用指定目录下的子Makefile
 
```

 

**2. 变量导出**

在嵌套调用子 Makefile 的过程中，如果需要将变量传递给子 Makefile ，可以使用如下语句：

```
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

```
gec@ubuntu:~$ make
rank 1: apple
rank 1: banana
make[1]: Entering directory '/home/gec/dir'
rank 2: apple
rank 2:
make[1]: Leaving directory '/home/gec/dir'
 
```

 

##### **3. 实用make选项**

**3.1 指定要执行的Makefile文件**

```
make -f Altmake
make --file Altmake
make --makefile Altmake
 
```

 

以上三种方式都可以用来执行一个普通命令的文件作为Makefile文件。在缺省的情况下不指定任何Makefile文件，则make会在当前目录下依次查找命名为GNUmakefile和Makefile以及makefile的文件。

 

**3.2 指定终极目标**

```
make TARGET
 
```

所谓的终极目标指的是Makefile中第一个出现的规则中的第一个目标，是缺省的整个工程或者程序编译过程的总的规则和目的。如果想要执行除该目标之外的其他普通目标位编译的最终目的，则可以在执行make的同时指定。

在我们需要对程序的一部分进行编译，或者仅仅对某几个程序进行编译而不是完整地编译整个工程的时候，指定终极目标就很有用。

 

**3.3 强制重建所有规则中目标**

```
make -B
make --always-make
 
```

 

**3.4 指定Makefile的所在路径**

```
make -C dir/
make --directory=dir/
 
```

假如要执行的Makefile文件不在当前目录，可以使用该选项指定。这个选项一般用在一个Makefile内部调用另一个子Makefile的场景

Makefile的详细的语法非常多，本章只是一个引子，但对于认识Makefile以及做一些基本的应用足已，毕竟复杂的Makefile都不可能手工写，而是会用其他的软件自动生成的。



### 常见编译选项

C/C++编译过程中，编译器提供了多种选项来控制编译行为和优化代码。以下是一些常见的编译选项：

-o ：指定输出的文件名。

-c：只编译和汇编，但不进行链接，生成目标文件（.o 或 .obj 文件）。

-O0, -O1, -O2, -O3：设置不同的优化级别。-O0 表示没有优化，-O1 表示启用基本优化，-O2 表示进一步优化，-O3 表示启用更多的优化选项，包括更激进的优化策略。

-g：生成调试信息。-g1, -g2, -g3 分别设置不同的调试信息级别。

-Wall：打开几乎所有的警告信息。

-w：关闭所有警告信息。

-I：添加头文件搜索路径。

-L：添加库文件搜索路径。

-l：链接时搜索并使用指定的库。

-D：定义宏。

-U：取消宏定义。

-fPIC 或 -fpic：生成位置无关代码，对于生成共享库是必要的。

-static：禁止使用动态链接库，生成的可执行文件较大，但不需要动态库支持。

-shared：生成共享库。

-std=：指定使用的C或C++标准，例如 -std=c99 或 -std=gnu++11。

-Wextra：打开额外的警告信息。

-Werror：将所有警告当作错误处理。

-Wno-error：将特定警告不当作错误处理。

-fexceptions：启用异常处理。

-fno-exceptions：禁用异常处理。

 

这些选项可以根据项目需求和编译环境的特点进行选择和组合，以达到预期的编译效果。



## cmake

#### **1.问题的引入**

在早期和当今的Linux工程管理中，make工程管理器占据了半壁江山，但make的配置文件Makefile的语法晦涩难懂，接触过的人都清楚，Makefile写起来非常困难。解决这个问题的办法无法有两个：

- 使用 automake 工具生成configure脚本，让其自动生成Makefile。

- 使用 cmake 工具直接生成Makefile。

#### **2.cmake概述**

cmake 是一款跨平台的免费开源软件工具，用于使用与编译器无关的方法来管理软件的构建过程。比如，在 Android Studio 上进行 NDK 开发默认就是使用 cmake 管理 C/C++ 代码，在 Linux 环境下有大量项目都使用 cmake 来管理，因此最好对 cmake 有一定的了解。

![image-20260714110025455](./img/image-20260714110025455.png)

cmake最重要的作用就是协助我们自动生成项目所需要的Makefile，以便于工程管理器make可以指导编译器的工作，他们的关系大概如下：

![image-20260714110039906](./img/image-20260714110039906.png)

1. 开发者编写CMakeLists.txt，指导cmake自动生成Makefile
2. 自动生成的Makefile，指导make和gcc，将源代码编译成可执行程序

这样一来，我们就摆脱了晦涩难写的Makeifle，转而编写简单可爱的 CMakeLists.txt ，利用cmake即可管理整个项目



#### **3.安装cmake** 

##### **3.1 在** **ubuntu** **中安装** **cmake**

ubuntu安装 cmake 只需一条指令：

```
gec@ubuntu:~$ sudo apt install cmake
```

可以通过以下指令来查看当前已安装的 cmake 的版本，若需要升级版本，可直接使用 apt 指令来升级：

```
# 查看cmake版本
gec@ubuntu:~$ cmake --version
 
# 升级cmake
gec@ubuntu:~$ sudo apt upgrade cmake
```

##### **3.2 在** **windows** **中安装** **cmake**

可以在 cmake 的 [官网](https://cmake.org/download/) 下载其源码，或挑选符合用户操作系统的二进制安装包即可

####  **4.简单示例**

#####  **4.1 入门操作**

假设有一C语言源程序 main.c ，其内容如下：

```C
#include <stdio.h>
 
int main(int argc, char const *argv[])
{
    printf("一起学习cmake\n");
    return 0;
}
```

 现使用 cmake 来管理该项目的构建工作，在 main.c 同一目录下，编写一个 CMakeLists.txt：

```bash
gec@ubuntu:~/cmake$ tree
.
├── CMakeLists.txt
└── main.c
gec@ubuntu:~/cmake$ 
 
```

文件 CMakeLists.txt 是 cmake 的配置文件，用来告诉 cmake 如何生成最终的 Makefile。此处的 CMakeLists.txt 非常简单，仅包含一句话：

```cmake
# CMakeLists.txt
add_executable(main main.c)
 
```

 **注意：**

- 配置文件的名称 CMakeLists.txt 是固定的，不可改成别的名字

- 配置文件的名称 CMakeList.txt 不区分大小写，但一般的写法如此所示。

- add_executable 用来指明最终要生成一个可执行文件的名称，及其所依赖的源文件列表。

在源码目录中，直接执行命令 “cmake .”（其中 . 表示 CMakeLists.txt 所在的位置在当前目录） 来读取 CMakeLists.txt 并生成 Makefile：

![image-20260714110159209](./img/image-20260714110159209.png)

此时会发现，目录中自动生成了Makefile了：

![image-20260714110225406](./img/image-20260714110225406.png)

有了Makefile，就可以直接make编译项目程序了:

![image-20260714110314486](./img/image-20260714110314486.png)

此时，程序main已经编译完毕。

##### **4.2 源码隔离**

一般而言，为了项目工程观感更干净、利落，我们不希望源码跟编译工具文档像上面的例子那样混在一起，因此对于cmake而言，通常的操作是：在源码中创建一个专门用于存储编译输出文件的存储区域，不妨命名为 build/ ，使自动生成的文件与开发者编写的源码隔离：

```bash
# 创建一个构建目录，专门用来存放构建过程中产生的非源码文件
gec@ubuntu:~/cmake$ mkdir build/
 
# 进入该构建目录
gec@ubuntu:~/cmake$ cd build
gec@ubuntu:~/cmake/build$
 
# 在构建目录中执行 `cmake`
gec@ubuntu:~/cmake/build$ cmake ..
 
```

这样，项目构建过程中产生的所有非源码文件就都被保存在 build 目录下了：

```cmake
.
├── build/
│   ├── CMakeCache.txt
│   ├── CMakeFiles/
│   ├── cmake_install.cmake
│   └── Makefile
├── main.c
└── CMakeLists.txt
 
```

有了 Makefile 就可以直接编译了：

```bash
# 编译
gec@ubuntu:~/cmake/build$ make
Scanning dependencies of target main
[ 50%] Building C object CMakeFiles/main.dir/main.o
[100%] Linking C executable main
[100%] Built target main
 
# 查看编译结果
gec@ubuntu:~/cmake/build$ ls -lp
total 39
-rwxrwxrwx 1 root root 12281 May 31 20:30 CMakeCache.txt
drwxrwxrwx 1 root root  4096 May 31 20:30 CMakeFiles/
-rwxrwxrwx 1 root root  1441 May 31 20:30 cmake_install.cmake
-rwxrwxrwx 1 root root 16736 May 31 20:30 main
-rwxrwxrwx 1 root root  4868 May 31 20:30 Makefile
 
# 执行程序
gec@ubuntu:~/cmake/build$ ./main
一起学习cmake
```



## CMakeLists基础语法

#### **1. 多文件编译**

**语法：**  **add_executable(可执行文件 源文件1 源文件2 ... ...)**

假设某可执行文件 main 由多个源码文件编译而成：

```
add_executable(main main.c a.c b.c)
 
```

 

#### **2. 指定头文件路径**

**语法：**  **include_directories(头文件所在路径)**

假设文件结构如下：

```
.
├── build/
├── inc/
│   └── head.h
└── main.c
├── CMakeLists.txt
 
 
```

其中，主程序 main.c 依赖于头文件 head.h，那么在与之同目录的 CMakeLists.txt 中，需要以其所在路径为基准添加头文件相对路径或绝对路径：

```
# CMakeLists.txt
include_directories(./inc)  # 相对路径，基于CMakeLists.txt所在路径
add_executable(main main.c)
 
```

 或者

```cmake
# CMakeLists.txt
include_directories(/home/gec/cmake/inc)  # 绝对路径
add_executable(main main.c)
```

#### **3. 设定变量和调用shell命令**

**语法：**  **set(变量名称 变量值)**

在指定头文件路径的例子中，当使用绝对路径时，若采用上述方式则在不同电脑间执行会很容易出现错误，更好的方式是让 CMakeLists.txt 在被解析的时候自动获取其所在路径，这可以在 CMakeLists.txt 中嵌套 shell 命令来达到：

```cmake
# 定义一个变量 SRCDIR，使其值等于当前路径
set(SRCDIR $(pwd))
 
# 引用变量 SRCDIR 的值来设定头文件所在路径 
include_directories($(SRCDIR)/inc)
 
```

#### **4. 添加工程子目录和编译库文件**

**语法：**  **add_subdirectory(子目录名称)**  **add_library(库名 [库类型] 源文件1 源文件2 ... ...)**  **库类型：** **SHARED** **、** **STATIC**

假设在工程目录中有一个 lib 子目录，里面包含若干源码，需要将其编译成动态库或静态库，目录文件结构如下：

```bash
gec@ubuntu:~/cmake$ tree
.
├── build/
├── inc
│   └── head.h
├── lib
│   ├── a.c   # 假设要编译成动态库
│   ├── b.c   # 假设要编译成静态库
│   └── CMakeLists.txt
├── main.c
└── CMakeLists.txt
 
```

其中， a.c 和 b.c 是两个简单模块，分别实现两个整数相加和相减：

```C
// a.c
int sumup(int a, int b) {
    return a+b;
}
 
```



```C
// b.c
int minus(int a, int b) {
    return a-b;
}
 
```

 

此时，只需要在 lib/ 下增加一个 CMakeLists.txt 文件即可，其内容如下：

```cmake
# cmake/lib/CMakeLists.txt
add_library(a SHARED a.c)
add_library(b STATIC b.c) # 静态库是默认的，此处 STATIC 可以不写
 
```

 注意，上述关键字 SHARED 和 STATIC 必须是大写。然后在顶层 CMakeLists.txt 增加该子目录的包含语句：

```cmake
# cmake/CMakeLists.txt
add_subdirectory(lib/)
 
```

这样，就可以通过顶层的 CMakeLists.txt 来间接执行子目录工程配置信息，最终在 build/ 中生成动态库和静态库。

```shell
gec@ubuntu:~/cmake/build$ tree -L 2
.
├── CMakeCache.txt
├── CMakeFiles/
├── cmake_install.cmake
├── lib/          # 此处自动生成的 lib/ 是要与源码目录的 cmake/lib 保持一致
│   ├── CMakeFiles
│   ├── cmake_install.cmake
│   ├── liba.so   # 生成的动态库
│   ├── libb.a    # 生成的静态库
│   └── Makefile  # 可由此 Makefile 重新编译生成库文件
├── main
└── Makefile
 
```

值得注意的是：cmake 为了更好地自适应工程文件的结构，其所生成的文件的相对位置均与源码目录中的相对位置保持一致，因此在此处会发现，库文件 liba.so 和 libb.a 均位于 lib/ 下，这与源码的目录结构保持一致。

#### **5. 指明库路径和链接指定的库文件**

**语法：**  **link_directories(库所在路径)**  **target_link_libraries(目标文件 库名1 库名2 ... ...)**

假设主程序 main.c 引用了 lib/ 下各个库文件的接口，则编译时就必须链接相关的库文件。在顶层 CMakeLists.txt 中添加两行 target_link_libraries() 语句：

```cmake
# CMakeLists.txt
set(SRCDIR $(pwd))
include_directories($(SRCDIR)/inc/)
 
add_executable(main main.c)
target_link_libraries(main a)  # 指明可执行文件main依赖于库a
target_link_libraries(main b)  # 指明可执行文件main依赖于库b
 
add_subdirectory(lib/)
 
```

 或者

```cmake
# CMakeLists.txt
set(SRCDIR $(pwd))
include_directories($(SRCDIR)/inc/)
 
add_executable(main main.c)
target_link_libraries(main a b)  # 指明可执行文件main依赖于库a和b
 
add_subdirectory(lib/)
 
```

注意，在以上示例中，并没有指定库文件a和b所在的路径，这是因为这两个库文件所在的路径 lib/ 已经作为子目录被顶层 CMakeLists.txt 添加了，如果主程序所依赖的库文件在别处，比如依赖于 /tmp/libx.so，那么顶层 CMakeLists.txt 要这么写：

```cmake
# CMakeLists.txt
set(SRCDIR $(pwd))
include_directories($(SRCDIR)/inc/)
 
link_directories(/tmp)
add_executable(main main.c)
target_link_libraries(main a b)
target_link_libraries(main x)  # 指明可执行文件main依赖于库x及其所在路径
 
add_subdirectory(lib/)
 
```

注意：语句 link_directories() 要写在 add_executable() 之前。

#### **6. 指定工具链**

**语法：**  **set(CMAKE_C_COMPILER "aarch64-linux-gnu-gcc")**  **set(CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++")**

假设程序要放到 RockX 平台上去运行，那么需要指定对应平台的交叉工具链：

```cmake
# CMakeLists.txt
 
set(CMAKE_C_COMPILER "aarch64-linux-gnu-gcc")   # 指定C编译器
set(CMAKE_CXX_COMPILER "aarch64-linux-gnu-g++") # 指定C++编译器
 
set(SRCDIR $(pwd))
include_directories($(SRCDIR)/inc/)
 
add_executable(main main.c)
target_link_libraries(main a b)
 
add_subdirectory(lib/)
```

#### **7. 指定编译选项**

**语法：**  **set(CMAKE_C_FLAGS "具体编译选项")**

编译程序的时候，经常需要增加一些特别的选项，比如增加优化等级、指定运行时链接路径等：

```cmake
# CMakeLists.txt
 
set(CMAKE_C_FLAGS "-O2 -Wl,-rpath=./lib")  # 设定优化等级和运行库所在路径
 
set(SRCDIR $(pwd))
include_directories($(SRCDIR)/inc/)
 
add_executable(main main.c)
target_link_libraries(main a b)
 
add_subdirectory(lib/)
```

#### **8. 设定cmake的最低版本**

**语法：**  **cmake_minimum_required(VERSION x.x)**

由于 cmake 的特性会随着版本的更新而发生变化，因此手头写的 CMakeLists.txt 可能在别的电脑不适用，为了检测并提前报告版本兼容性的问题，一般都需要在 CMakeLists.txt 判定 cmake 的版本：

```
cmake_minimum_required(VERSION 3.8)
 
```

 

需要注意的是，版本检查机制至少在 2.8 之后才被支持，因此上述语句中版本号至少应为 2.8 。

#### **9. 指定工具链文件**

**语法：**  **cmake -DCMAKE_TOOLCHAIN_FILE=xxx**

我们可以直接在 CMakeLists.txt 中设置跟工具链相关的所有细节，但有时候工具的设置项比较多，而且同一项目可能要部署到不同的平台中去，不同平台可能对工具链的配置信息不尽相同且都需要保留，那么如果能将跟平台相关的工具链的配置信息单独放在一个文件中，然后在执行 cmake 指令的时候临时指定，将会很大地提升工作效率。

例如，在A平台中，需要设定如下编译配置信息：

```cmake
# A.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(TOOLCHAIN_DIR /usr/local/arm/)
set(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/bin/arm-linux-gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_DIR}/bin/arm-linux-g++)
 
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_FIND_ROOT_PATH ${TOOLCHAIN_DIR}
	${TOOLCHAIN_DIR}/arm-none-linux-gnueabi/include
	${TOOLCHAIN_DIR}/arm-none-linux-gnueabi/lib)
 
```

 在B平台中，需要设定如下编译配置信息：

```cmake
# B.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(TOOLCHAIN_DIR /home/gec/RockX/3568)
set(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/bin/aarch64-linux-gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_DIR}/bin/aaarch64-linux-g++)
 
```

那么，可以将这些信息从 CMakeLists.txt 抽离出来，单独形成两个文件：A.cmake 和 B.cmake ，然后在源码编译时通过上述内置命令来灵活指定：

```
# 选择A
gec@ubuntu:~/cmake/build$ cmake .. -DCMAKE_TOOLCHAIN_FILE=A.make
 
# 选择B
gec@ubuntu:~/cmake/build$ cmake .. -DCMAKE_TOOLCHAIN_FILE=B.make
 
```

####  **10. 设定项目名称**

**语法：**  **project(PRO_NAME VERSION x.x.x LANGUAGES X)**

一般而言，项目需要设置一个版本号，方便进行版本的发布，也可以根据版本对问题或者特性进行追溯和记录。可以通过如下语句来设定项目的版本信息：

```
project(cmake_demo VERSION 1.0.0 LANGUAGES C CXX)
 
```

#### **11. 常见内置变量**

```cmake
PROJECT_SOURCE_DIR：工程的根目录
PROJECT_BINARY_DIR：运行cmake命令的目录，通常为${PROJECT_SOURCE_DIR}/build
PROJECT_NAME：返回通过 project 命令定义的项目名称
CMAKE_CURRENT_SOURCE_DIR：当前处理的 CMakeLists.txt 所在的路径
CMAKE_CURRENT_BINARY_DIR：target 编译目录
CMAKE_CURRENT_LIST_DIR：CMakeLists.txt 的完整路径
EXECUTABLE_OUTPUT_PATH：重新定义目标二进制可执行文件的存放位置
```



```cmake
#指定cmake的版本
cmake_minimum_required(VERSION 3.8)
#指定项目名称和版本号
project(main VERSION 1.0.0 LANGUAGES C CXX)
 
#指定编译器
set(CMAKE_C_COMPILER "gcc")
set(CMAKE_CXX_COMPILER "g++")
 
#指定可执行程序 以及 源文件
add_executable(main ./src/main.c ./src/add.c ./src/b.c)
#指定头文件的路径
include_directories(./inc)
include_directories(./lib)
 
#在顶层的CmakeLists.txt中指定 子CmakeLists的路径
add_subdirectory(./lib)
 
#工程中使用了库文件 ，要指定库文件的路径
link_directories(./lib)
#可执行文件main 使用了 库文件 liblcd.so
target_link_libraries(main lcd)
```



## jpeg库

#### **一、移植第三方库（** **jpeg库** **的使用）**

库：是一堆函数的集合。看不到源码

1、源文件：jpegsrc.v9a.tar.gz

1.下载源码

﻿https://github.com/mozilla/mozjpeg/tree/jpeg-9d﻿

2、将源文件放到我们的共享目录下

3、将共享目录下的源文件移动到家目录下

```bash
gec@ubuntu:/mnt/hgfs/linux$ mv jpegsrc.v9a.tar.gz  ~
gec@ubuntu:/mnt/hgfs/linux$ cd
```

4、在家目录下解压我们的源文件

```bash
gec@ubuntu:~$ tar xzvf jpegsrc.v9a.tar.gz -C  ~
```

tar：压缩或者解压

xzvf：   x     表示解压    z:表示以.gz结尾的压缩包	  vf：以可见的方式解压

-C：指定解压的路径

~ ：解压到家目录下

解压之后的目录：jpeg-9a

5、进入解压之后的目录jpeg-9a

```C
gec@ubuntu:~$ cd jpeg-9a/
```

 6、执行配置文件            ---------------》帮助我们自动生成Makefile

开发板使用：

```bash
gec@ubuntu:~/jpeg-9a$ ./configure  --host=arm-linux  --prefix=/home/gec/jpeg
```

如果是在虚拟机Ubuntu上使用,则执行下面一行

```bash
./configure --prefix=/home/gec/jpeg --enable-shared --enable-static
```

--host：指定交叉编译工具链

--prefix：指定安装的路径

--enable-shared :生成动态库

--enable-static:生成静态库

7、编译工程

```
make
```

8、安装

```bash
make install
```

9、进去我们编译完成之后安装好的路径下   jpeg

```bash
gec@ubuntu:~$ cd jpeg
gec@ubuntu:~/jpeg$ ls
bin  include  lib  share
```

注意：查看库的文件属性

```shell
gec@ubuntu:~/jpeg/lib$ file libjpeg.so.9.1.0
libjpeg.so.9.1.0: ELF 32-bit LSB shared object, ARM, version 1 (SYSV), dynamically linked, not stripped
gec@ubuntu:~/jpeg/lib$
```

10、进入/jpeg/lib

将libjpeg.so.9.1.0 复制到我们的共享目录下

```bash
cp  libjpeg.so.9.1.0  /mnt/hgfs/linux
```

libjpeg.so.9.1.0

lib：库的前缀

jpeg：库的名字	

so：库的后缀

9：库的版本号

1.0：库的修正号 

11、将libjpeg.so.9.1.0的后缀去掉（在window中重命名即可）------》libjpeg.so.9

12、将libjpeg.so.9库下载到开发板中的/lib目录下

#### **二、jpeg格式图片的编解码**

1.使用jpeg库提供接口函数来帮助我们实现jpeg格式图片的显示

jpg图片是用特定的算法压缩过

2.流程:

1)定义跟jpeg图片解压缩操作有关的结构体变量

```
struct jpeg_decompress_struct cinfo;//解压结构
struct jpeg_error_mgr jerr;//错误结构
```

2)初始化解压缩结构体和错误结构体

```
jpeg_create_decompress(cinfo);
 
jpeg_std_error((struct jpeg_error_mgr * err));
```

参数:cinfo --->struct jpeg_decompress_struct结构体指针

 3)指定解压缩数据源--->打开你要显示jpg图片 fopen--FILE *

```
FILE *fp = fopen();
 
jpeg_stdio_src((j_decompress_ptr cinfo, FILE * infile));
```

参数: infile --->你使用fopen打开jpg图片的返回值

4)读取jpg的头信息

```
jpeg_read_header((j_decompress_ptr cinfo,boolean require_image));
```

5)开始解压缩

```
jpeg_start_decompress((j_decompress_ptr cinfo));
```

6)获取jpg图片的RGB数值

```
jpeg_read_scanlines((j_decompress_ptr cinfo,
JSAMPARRAY scanlines,
JDIMENSION max_lines));
```

参数: scanlines --->用来存放每一次读取到一行jpeg图片的rgb数值

max_lines --->你打算读取多少行

​    显示jpeg图片读取一行数据的时候，那个buf不要定义成数组，因为buf取地址之后类型就不是二级指针了

7)解压缩完毕

```
jpeg_finish_decompress((j_decompress_ptr cinfo));
```

8)释放资源

```
jpeg_destroy_decompress JPP((j_decompress_ptr cinfo));
```

3.使用jpeg的动态库编译程序

方法一:  arm-linux-gcc showjpeg.c  libjpeg.so  -o showjpg

方法二:  arm-linux-gcc showjpeg.c  -o  showjpg  -L.  -ljpeg

#### **三、jpeg图片的显示**

1、编译命令：

```
arm-linux-gcc jpeg_show.c  -o jpeg_show  -I /home/gec/jpeg/include -L /home/gec/jpeg/lib -ljpeg
```

-I   ：指定头文件的路径

-L   ：指定库文件的路径

-l   ：指定库的名字

2、将编译生成之后的jpeg_show下载到开发板

3、在开发板中执行jpeg_show

```
chmod 777 jpeg_show
./jpeg_show  4.jpg
 
 
---->注意：执行的时候要加上你要显示的图片名字
 
```

 

```C
#include <stdio.h> 
#include <unistd.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <fcntl.h> 
#include <string.h> 
#include <strings.h> 
#include <stdlib.h> 
#include <stdbool.h> 
#include <sys/mman.h> 
 
#include "jpeglib.h"  //jpg库的头文件 
 
/*
使用jpg库提供的接口函数实现jpg的显示
先显示800*480大小全屏的jpg
任意位置显示任意大小的jpg
*/ 
//封装任意大小jpg显示  提高代码的健壮性(鲁棒性)
 
int show_anyjpg(int x,int y,char *jpgpath) 
{ 
    int i,j; 
    int lcdfd; 
    int *lcdmem; 
    //打开开发板液晶屏的驱动 
    lcdfd=open("/dev/fb0",O_RDWR); //fb-->frame buffer 
    if(lcdfd==-1) { 
        perror("打开lcd失败！\n"); 
        return -1; 
    }    
    //通过内存映射得到液晶屏的首地址 
    lcdmem=mmap(NULL,800*480*4,PROT_READ|PROT_WRITE,MAP_SHARED,lcdfd,0); 
    if(lcdmem==NULL) { 
        perror("映射lcd失败!\n"); 
        return -1; 
    } 
    //定义解压缩结构体变量和处理错误的结构体变量 
    struct jpeg_decompress_struct mydem; 
    struct jpeg_error_mgr myerr;
    //初始化 
    mydem.err=jpeg_std_error(&myerr); 
    jpeg_create_decompress(&mydem); 
    FILE *jpgp; 
    //打开你要显示的jpg 
    jpgp=fopen(jpgpath,"r+"); 
    if(jpgp==NULL) { 
        perror("打开jpg失败！\n"); 
        return -1; 
    } 
    //获取数据源 
    jpeg_stdio_src(&mydem,jpgp); 
    //读取jpg的头信息 
    jpeg_read_header(&mydem,1); 
    printf("图片的宽是：%d\n",mydem.image_width); 
    printf("图片的高是：%d\n",mydem.image_height); 
    //开始解压缩 
    jpeg_start_decompress(&mydem); 
    //定义一个指针存放一行RGB数值 
    char *rgbbuf=calloc(1,mydem.image_width*3); 
    //定义一个指针存放转换得到的一行ARGB 
    int *lcdbuf=calloc(1,mydem.image_width*4); 
    //解压缩成功后得到的就是jpg图片的原始RGB数值--》读取并填充到lcd上 
    for(i=0; i<mydem.image_height; i++) //比如：图片是800*480大小 
    { 
        //每次循环读取一行RGB 
        jpeg_read_scanlines(&mydem,(JSAMPARRAY)&rgbbuf,1); 
        //填充(写入)到开发板的液晶屏中 
        //将一行RGB--》转化成ARGB 
        for(j=0; j<mydem.image_width; j++) { 
        	lcdbuf[j]=0x00<<24|rgbbuf[3*j]<<16|rgbbuf[3*j+1]<<8|rgbbuf[3*j+2]; 
                  //00[0][1][2] 
        } 

        //在指定的位置(x,y)显示该图片 
        memcpy(lcdmem+(y+i)*800+x,lcdbuf,mydem.image_width*4); 
    } 
    //收尾工作 
    jpeg_finish_decompress(&mydem); 
    jpeg_destroy_decompress(&mydem); 
    close(lcdfd); 
    fclose(jpgp); 
    munmap(lcdmem,800*480*4); 
    free(rgbbuf); 
    free(lcdbuf); 
    return 0; 
} 
 
//在任意位置显示一张800*480缩小4倍后的jpg图片 
int show_anyjpg_solv(int x,int y,char *jpgpath) 
{ 
    int i,j; 
    int lcdfd; 
    int *lcdmem; 
    int jpgbuf[800*480]; 
    //打开开发板液晶屏的驱动 
    lcdfd=open("/dev/fb0",O_RDWR); //fb-->frame buffer 
    if(lcdfd == -1) { 
        perror("打开lcd失败！\n"); 
        return -1; 
    } 
    //通过内存映射得到液晶屏的首地址 
    lcdmem = mmap(NULL,800*480*4,PROT_READ|PROT_WRITE,MAP_SHARED,lcdfd,0); 
    if(lcdmem==NULL) { 
        perror("映射lcd失败!\n"); 
        return -1; 
    } 
    //定义解压缩结构体变量和处理错误的结构体变量 
    struct jpeg_decompress_struct mydem; 
    struct jpeg_error_mgr myerr; 
    mydem.err=jpeg_std_error(&myerr); 
    jpeg_create_decompress(&mydem); 
    FILE *jpgp; 
    //打开你要显示的jpg 
    jpgp=fopen(jpgpath,"r+"); 
    if(jpgp==NULL) { 
        perror("打开jpg失败！\n"); 
        return -1; 
    } 
    //获取数据源 
    jpeg_stdio_src(&mydem,jpgp); 
    //读取jpg的头信息 
    jpeg_read_header(&mydem,1); 
    printf("图片的宽是：%d\n",mydem.image_width); 
    printf("图片的高是：%d\n",mydem.image_height); 
    //开始解压缩 
    jpeg_start_decompress(&mydem); 
    //定义一个指针存放一行RGB数值 
    char *rgbbuf=calloc(1,mydem.image_width*3); 
    //定义一个指针存放转换得到的一行ARGB 
    int *lcdbuf=calloc(1,mydem.image_width*4); 
    //解压缩成功后得到的就是jpg图片的原始RGB数值--》读取并填充到lcd上 
    for(i=0; i<mydem.image_height; i++) //比如：图片是800*480大小 
    { 
        //每次循环读取一行RGB 
        jpeg_read_scanlines(&mydem,(JSAMPARRAY)&rgbbuf,1); 
        //填充(写入)到开发板的液晶屏中 
        //将一行RGB--》转化成ARGB 
        for(j=0; j<mydem.image_width; j++) { 
            lcdbuf[j]=0x00<<24|rgbbuf[3*j]<<16|rgbbuf[3*j+1]<<8|rgbbuf[3*j+2]; 
                      //00[0][1][2] 
            jpgbuf[i*mydem.image_width+j] = lcdbuf[j]; 
        } 
        
        //在指定的位置(x,y)显示该图片 
        //memcpy(lcdmem+(y+i)*800+x,lcdbuf,mydem.image_width*4); 
    } 
    //切割缩小4倍图片	 
    int minbuf[200*120]={0}; 
    
    for(j=0; j<mydem.image_height; j++) { 
        for(i=0; i<mydem.image_width; i++) { 
            if(mydem.image_height%4==0 && mydem.image_width%4==0) 
            minbuf[j/4*200+i/4] = jpgbuf[j*mydem.image_width+i]; 
        } 
    } 
    //显示 
    for(j=0; j<120; j++) { 
        for(i=0; i<200; i++) { 
            lcdmem[(j+y)*800+i+x] = minbuf[j*200+i]; 
        } 
    } 
    //收尾工作 
    jpeg_finish_decompress(&mydem); 
    jpeg_destroy_decompress(&mydem); 
    close(lcdfd); 
    fclose(jpgp); 
    munmap(lcdmem,800*480*4); 
    free(rgbbuf); 
    free(lcdbuf); 
    return 0; 
} 
 
 
int main(int argc,char **argv) 
{ 
    if(argc!=4) { 
        printf("sorry，你传参失败，格式如下：./程序名  图片路径  x y坐标！\n"); 
        return -1; // ./showjpg  test.jpg  0  0 
    } 
    show_anyjpg(atoi(argv[2]),atoi(argv[3]),argv[1]); 
    //show_anyjpg_solv(atoi(argv[2]),atoi(argv[3]),argv[1]); 
    return 0; 
}
```







