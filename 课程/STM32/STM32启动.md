# STM32启动

[toc]

`STM32`上电或者复位后，`CPU`首先执行的是一套固定的硬件启动规则：它会先从启动地址读取中断向量表，设置栈指针，然后跳转到复位处理函数`Reset_Handler`，最后才进入`C`语言的`main()`函数。

整个流程大致如下：

![image-20260823150105430](./img/image-20260823150105430.png)

## 启动程序

### **一、启动文件作用**

启动文件是用汇编语言编写的，是芯片上电后执行的第一段代码，奠定了整个程序运行的基石。

![image-20260814162827904](./img/image-20260814162827904.png)

**注意：**不同型号的STM32芯片，启动文件不全一样。

### **二、启动文件的核心作用**

这个文件主要完成以下关键任务：

💡

1. 初始化堆栈指针

2. 构建中断向量表

3. 执行系统初始化 

4. 跳转到主程序

5. 提供中断服务程序的默认入口

> 初始化堆栈指针 SP = _initial_sp 
>
> 初始化程序计数器指针 PC = Reset_Handler 
>
> 设置堆和栈的大小 
>
> 初始化中断向量表 
>
> 配置外部 SRAM 作为数据存储器（可选） 
>
> 配置系统时钟，通过调用 SystemInit函数（可选） 
>
> 调用 C 库中的 _main 函数初始化用户堆栈，最终调用 main 函数

### **三、详细代码分析**

#### **1. 堆栈配置**

```asm
Stack_Size		EQU     0x400    ; 定义栈大小为 1KB 0100 0000 0000

                AREA    STACK, NOINIT, READWRITE, ALIGN=3
Stack_Mem       SPACE   Stack_Size    ; 栈顶地址，初始化MSP的值
__initial_sp
```

- EQU： 用来定义一个常量，**类似**于C语言的 #define，定义常量。
- AREA： 声明一个段。STACK是段名，NOINIT表示不初始化为0，READWRITE可读可写，ALIGN(对齐方式)=3表示按8($2^3$​)字节对齐。

> ;这行代码是告诉编译器，让它开辟一个名为STACK的内存段，NOINIT表示这块内存不用清零，READWRITE表示可读可写，ALIGN表示对齐方式，这里是按照2的3次方，也就是8字节对齐。

- SPACE： 分配一段指定大小的内存空间。
- __initial_sp： 链接器会使用这个符号的值作为主堆栈指针的初始值。

> 表示预留一块大小为`Stack_Size`的内存空间，也就是预留`1KB`的`RAM`作为栈，`Stack_Mem`是这块栈空间的起始位置，`__initial_sp`位于这块空间的末尾。由于`ARM Cortex-M`的栈是向低地址增长的，所以初始栈指针要放在高地址位置，也就是`__initial_sp`。



在理解层面上来看，可以把`__initial_sp`看作是指向栈顶地址，也就是高地址的一个标志，因为它是预留栈空间后面的，同理，如果在预留栈空间这行代码之前设置一个标志，那么它就指向栈低，也就是低地址。

可以按照下面模型来理解：

![image-20260823151319676](./img/image-20260823151319676.png)

栈的作用很大，`C`程序没有栈是无法正常运行的，比如函数调用，局部变量的保存，中断现场的保护等都需要用到栈。



**同理，堆区配置：**

```asm
Heap_Size      EQU     0x200    ; 定义堆大小为 512字节
                AREA    HEAP, NOINIT, READWRITE, ALIGN=3 
__heap_base
Heap_Mem        SPACE   Heap_Size
__heap_limit
```

- 堆用于动态内存分配（如malloc、free）。

PRESERVE8、THUMB
都是给编译器看的配置指令，`PRESERVE8`会告诉链接器，这个文件里的所有代码，在调用函数时，堆栈指针都必须保证是`8`字节对齐的，`Thumb`告诉汇编器，后面所有的汇编指令都是`Thumb`格式的，要用`Thumb`指令集来翻译成机器码。

堆模型可以参照下图：

![image-20260823153156642](./img/image-20260823153156642.png)

需要知道的是，堆的有效范围通常可以理解为：`[__heap_base, __heap_limit)`，也就是左闭右开区间，`__heap_limit`不是最后一个可用字节，而是堆区域结束后的下一个地址。

堆主要服务于动态内存分配，比如：

```c
malloc();
free();
```

但在`STM32`裸机开发中，一般不推荐随便使用堆，因为`MCU`的`RAM`很小，动态内存可能带来内存碎片、申请失败、生命周期混乱等问题。所以裸机工程里更常用静态数组、全局缓冲区或者固定内存池。



#### **2. 中断向量表**

这是启动文件最核心的部分。

```asm
                AREA    RESET, DATA, READONLY
                EXPORT  __Vectors
                EXPORT  __Vectors_End
                EXPORT  __Vectors_Size
__Vectors       DCD     __initial_sp               ; 地址0: 初始栈顶地址
                DCD     Reset_Handler              ; 地址4: 复位中断服务程序
                DCD     NMI_Handler                ; 地址8: NMI Handler
                DCD     HardFault_Handler          ; 地址12: Hard Fault Handler
                ...                                 ; 更多系统异常
                DCD     WWDG_IRQHandler            ; 外部中断0 (Window Watchdog)
                DCD     PVD_IRQHandler             ; 外部中断1 (PVD)
                ...                                 ; 所有外部中断
__Vectors_End

__Vectors_Size  EQU  __Vectors_End - __Vectors

                AREA    |.text|, CODE, READONLY
```

- AREA RESET, DATA, READONLY： 定义一个名为RESET的只读数据段，存放向量表。

> 开辟一个名为`RESET`的内存段，我们之前看到的`STACK`和`HEAP`段，属性是`READWRITE`可读可写，最终会被放到`RAM`里面，而这里的属性是`READONLY`只读，这意味着这个段里面的所有数据（也就是中断向量表）最终会被放在`Flash`，也就是只读存储器里面。

- EXPORT __Vectors： 导出__Vectors符号，让链接器知道向量表的起始位置。

> 是导出向量表的起始地址，结束地址和大小，他们具体标记的位置

- DCD： 分配一个32位的字（4字节）内存，并初始化。

- 向量表结构：

- 第一个条目必须是**初始栈顶指针**。Cortex-M内核上电后，首先从地址0x00000000取出这个值赋给MSP。

- 第二个条目是**复位向量**，即Reset_Handler的地址。上电后，内核从地址0x00000004取出这个值，并跳转到该地址执行。

- 后续条目依次是各种异常和中断的入口地址。

其中`__Vectors`标记了向量表的起始地址，`__Vectors_End`标记了向量表的结束地址，`Vectors_Size`是二者之差。

`DCD`可以理解为定义一个`32`位常量，在这里，这些常量不是普通数字，而是`32`位地址。而这个中断向量表本质上就是一个入口地址表，从上面的图可以看到，中断向量表的第`0`项就是初始栈顶地址`__initial_sp`，第一项是复位处理函数`Reset_Handler`，以此类推。

当`STM32`上电时，`CPU`首先会读取中断向量表第`0`项，并把它作为初始`SP`栈指针，然后读取中断向量表第一项，跳转到`Reset_Handler`执行。

所以，中断向量表的前两项非常关键，`CPU`刚上电时，不知道栈在哪里，也不知道第一段程序应该从哪里执行，向量表就是用来告诉`CPU`这些入口地址的。



#### **3. 复位中断服务程序**

这是上电后执行的第一段**代码**。

```asm
Reset_Handler   PROC
                EXPORT  Reset_Handler             [WEAK]
        IMPORT  SystemInit
        IMPORT  __main
                 LDR     R0, =SystemInit
                 BLX     R0
                 LDR     R0, =__main
                 BX      R0
                 ENDP
```

- PROC/ENDP： 定义一个过程（函数）。

- [WEAK]： 弱定义。如果别处没有定义同名的强符号，则使用此定义。这里允许用户在C代码中自己实现一个Reset_Handler。

> 表示导出`Reset_Handler`这个符号，并且它是弱定义。弱定义的意思就是这个启动文件提供一个默认实现，如果用户或其他文件提供了同名强定义，链接器会优先使用强定义。
>
> 很多中断函数也是这种设计，启动文件先给默认入口，用户需要时可以自己重写。

- IMPORT： 声明外部符号，类似于C语言的extern。

- 执行流程：

> 表示`__main`和`SystemInit`在别的文件或库中定义，当前文件只是引用它们。`SystemInit`一般在系统文件中，用来做系统基础初始化，比如时钟配置、向量表相关配置等。`__main`不是我们自己写的`main()`，而是`Keil`运行库的入口函数。

2. LDR R0, =SystemInit： 将SystemInit函数的地址加载到寄存器R0。

3. BLX R0： **跳转并执行SystemInit()。这个函数通常由ST提供，在system_stm32f1xx.c中，它负责配置时钟、初始化等关键系统配置。不过用STM32CubeMX生成工程时，时钟配置已经在SystemClock_Config()函数中实现,SystemInit()函数不做配置了。**

> 这两句表示先把`SystemInit`的地址加载到`R0`，然后跳转过去执行，BLX表示有返回的跳转，也就是执行完之后还会回来。

2. LDR R0, =__main： 将__main的地址加载到R0。注意：这个__main不是你的C代码里的main函数，它是C库中的一个函数，由编译器提供。

3. BX R0： 跳转到__main。

- __main会完成以下工作：

- 复制初始化数据从Flash到SRAM（例如，初始化全局变量）。

- 将未初始化的内存区域清零（例如，.bss段）。

- 调用C库初始化（如果使用）。

- **最后，调用用户的main()函数。**

> 这两句表示把`__main`的地址加载到`R0`，然后跳转到`__main`。
>
> 这里用的是`BX`，不是`BLX`，因为跳到`__main`后，正常情况下不用再回到`Reset_Handler`。



##### **SystemInit、__main、main的区别**

`SystemInit()`偏向硬件系统初始化，常见工作包括系统时钟配置、时钟源设置、向量表偏移等。

`__main`是`C`运行库入口，它不是用户写的`main()`，它负责准备`C`语言运行环境，比如初始化全局变量。

例如：

```c
int a = 10;
int b;
```

`a = 10`是已初始化的全局变量，它的初值存放在`Flash`中，但程序运行时变量本体要在`RAM`中，所以启动时需要把`.data`段从`Flash`拷贝到`RAM`。而`b`是未初始化的全局变量，`C`语言规定它默认是`0`，所以启动时需要把`.bss`段清零。

这些工作通常由`__main`或`C`运行库启动过程完成。

最后才进入我们自己写的：

```c
int main(void)
{
    while (1)
    {
    }
}
```



#### **4. 默认中断服务程序**

```asm
NMI_Handler     PROC
                EXPORT  NMI_Handler                [WEAK]
                B       .  ; 无限循环
                ENDP
HardFault_Handler\
                PROC
                EXPORT  HardFault_Handler          [WEAK]
                B       .
                ENDP
...
```

- 对于所有异常和中断，这里都提供了一个默认实现：一个什么都不做的无限循环(B .)。

- 它们都被标记为**[WEAK]**。这意味着，如果你在C代码中自己实现了一个同名的函数（例如 void TIM2_IRQHandler(void) { ... }），**链接器会优先使用你的函数**，从而覆盖这个默认的空实现。这就是我们自定义中断服务函数的方式（函数名不能改，但是函数里面执行的代码我们可自定义）。



#### **5. 堆栈初始化（用于非微库）**

```asm
                 IF      :DEF:__MICROLIB
                 ... ; 如果使用微库，直接使用上面定义的符号
                 ELSE
                 IMPORT  __use_two_region_memory
                 EXPORT  __user_initial_stackheap
__user_initial_stackheap
                 LDR     R0, =  Heap_Mem    ; 返回堆起始地址
                 LDR     R1, =(Stack_Mem + Stack_Size) ; 返回栈结束地址
                 LDR     R2, = (Heap_Mem +  Heap_Size) ; 返回堆结束地址
                 LDR     R3, = Stack_Mem    ; 返回栈起始地址
                 BX      LR
                 ENDIF
```

- 这部分是为了支持标准的C库（而非微库Microlib）进行堆栈初始化。

- __user_initial_stackheap 函数会被C库调用，它需要返回堆和栈的边界地址。



## 自举模式

![image-20260814181215293](./img/image-20260814181215293.png)

**设置程序的自举模式**

**1. 什么是自举模式？**

**自举模式，也常被称为启动模式**，是 STM32 芯片在上电或复位时，决定从哪里开始执行程序的一种机制。芯片内部有一个专门的硬件电路，会在复位释放后的几个时钟周期内，采样特定的引脚电平，根据这些电平的组合来决定将哪个存储器地址映射到 0x0000 0000（初始堆栈指针和复位向量的地址），然后从那里开始执行代码。

**简单来说，自举模式就是告诉芯片：“请你从XXX地方开始启动”。**

**2. 如何配置自举模式？**

配置自举模式主要通过两个引脚的电平组合来实现：BOOT0 和 BOOT1。

**BOOT0：** 这是一个专用引脚，标记为 BOOT0。

**BOOT1：** 这个引脚在大部分型号中与某个 GPIO 引脚复用。在芯片复位时，它被采样为启动配置引脚；复位结束后，它就可以作为普通 GPIO 使用。

下面的表格清晰地展示了三种主要的启动模式：

| **BOOT0** | **BOOT1** | **启动模式**   | **描述**                                                     |
| --------- | --------- | -------------- | ------------------------------------------------------------ |
| 0         | X         | **主FLASH**    | 这是**最常用**的模式。芯片从内部 Flash 启动，执行用户程序。即:0x08000000 |
| 1         | 0         | **系统存储器** | 芯片从内部 ROM 启动，运行一段**内置的Bootloader** 程序。用于通过 USART、USB 等接口进行串口下载。即:0x1FFFF000 |
| 1         | 1         | **内置 SRAM**  | 芯片从内部的 RAM 启动。通常用于**调试**，因为代码掉电消失，不具备产品化条件。即:0x20000000 |

**注意：** 这里的 “X” 表示 “无关”，即无论 BOOT1 是高是低，只要 BOOT0 是 0，就从主闪存启动。

**3. 设置启动模式为** **主FLASH**

![img](./img/56492.png)

 **七、串口烧录**

**1.核心板正确跳线BOOT0引脚连接到高电平，BOOT1引脚连接到低电平，如下图。**

![img](./img/56493.png)

 **2.接上Type-C数据线，然后上电复位后进入系统存储器启动模式。**

![img](./img/56494.png)

 **3.打开FlyMcu选择串口（要提前安装好CH340驱动）、载入Hex文件，点击【开始编程】可烧录程序。**

![img](./img/56495.png)

**4.跳线帽恢复原有的主FLASH启动模式，上电复位后可运行刚烧录的程序。**

![img](./img/56496.png)

**八、一键清除临时文件**

![img](./img/56497.png)





## MAP

.map 文件是编译器链接时生成的一个文件，它主要包含了交叉链接信息。通过.map 文件，我们可以知道整个工程的函数调用关系、FLASH 和 RAM 占用情况及其详细汇总信息，能具体到单个源文件（.c/.s）的占用情况，根据这些信息，我们可以对代码进行优化。.map 文件可以分为以下 5 个组成部分： 

1. Archive member included to satisfy reference by file (symbol)
     调用的库函数信息：来自哪个.a中的哪个.o
2. Allocating common symbols
     未初始化的全局变量：大小 变量出处
3. Discarded input sections
     没有被调用的函数、变量
4. Memory Configuration
     根据.ld文件中MEMORY来划分的内存区域：名称、起始地址、长度
5. Linker script and memory map   链接器脚本和内存映射



![image-20260823162856765](./img/image-20260823162856765.png)



- 这张图的读法：一条地址轴，按"门牌号区间"分硬件

Cortex-M3 有 4GB 的统一地址空间（0x00000000 ~ 0xFFFFFFFF），ST 把它切成几大块，每块对应一类硬件：

| 门牌号区间      | 硬件               | 和启动文件的关系                              |
| :-------------- | :----------------- | :-------------------------------------------- |
| `0x00000000`    | 别名区（逻辑入口） | CPU 复位时**查这里**，实际被映射到 Flash      |
| `0x08000000`    | 片上 Flash         | 你的代码、向量表（RESET 段）、常量住这里      |
| `0x1FFFF000`    | 系统存储器         | ST 出厂 Bootloader（串口下载用），平时不碰    |
| `0x20000000`    | 片上 SRAM          | 栈、堆、全局变量住这里                        |
| `0x40000000` 起 | 外设寄存器         | GPIO/USART/TIM 等，写代码时通过寄存器地址访问 |
| `0xE0000000`    | 内核私有外设       | NVIC、SysTick、VTOR 等                        |







| 章节                               | 作用                                          | 当你什么场景用                                    |
| :--------------------------------- | :-------------------------------------------- | :------------------------------------------------ |
| **Component: armlink**             | 头部：用的哪版链接器（5.06 update 6）         | 排查工具版本问题                                  |
| **Section Cross References**       | 段交叉引用：谁的代码"引用了"谁的符号          | 追踪一个函数/变量被谁依赖                         |
| **Removing Unused input sections** | 链接器把没被引用的段删掉了（死代码剔除）      | 确认"为什么某个函数没编进去/占的空间被省了"       |
| **Image Symbol Table**             | 符号表：所有符号的地址/类型/大小/来自哪个文件 | **← 上一轮看 `__initial_sp`、`Stack_Mem` 就在这** |
| **Memory Map of the image**        | 地址→内容的完整"内存地图"，按地址从低到高     | 看某地址到底放的是什么数据                        |
| **Image component sizes**          | 就是你贴的底部统计表                          | 看 ROM/RAM 分配                                   |
| **Grand/ELF/ROM Totals**           | 汇总数据                                      |                                                   |



## RDP 读保护（Read‑out Protection）

RDP 是**选项字节 (Option Bytes) 里面的硬件安全机制**，不是软件，用来防止别人用 ST‑Link 读出你芯片 Flash 里的固件，防止代码被窃取。

### 三级 RDP

| 等级                         | 状态     | ST‑Link(SWD)                                                 | BOOT0=1 BOOT1=0（串口 ISP）                                  |
| :--------------------------- | :------- | :----------------------------------------------------------- | :----------------------------------------------------------- |
| **Level0（出厂默认）**       | 无锁     | ✅完全读写下载                                                | ✅可用，正常刷固件                                            |
| **Level1（用户开启读保护）** | 芯片锁住 | ❌ST‑Link 可以识别芯片 ID，但**不能读、不能写 Flash，Keil 下载报错** | ✅可用救砖；解锁时硬件强制整片擦除全部 Flash，旧代码全部清空，回到 Level0 开放状态 |
| **Level2**                   | 永久锁死 | ❌完全失效                                                    | ❌串口 ISP 也废掉，芯片报废，无法救回，千万不要碰STMicroele... |

> ⚠️关键点：**RDP1 降级回 Level0，芯片硬件自动 Mass‑Erase 整片 Flash，这是硬件强制，软件绕不开**，防止黑客临时解锁盗取代码意法半导体。



```
No target Connected
Error：Flash Download failed - Target DLL has been cancelled
```



### 关闭SWD、JTAG接口

```C
HAL_Init();
	|
HAL_MspInit();
	|
/** NOJTAG: JTAG-DP Disabled and SW-DP Enabled
  */
__HAL_AFIO_REMAP_SWJ_NOJTAG();
	|
#define __HAL_AFIO_REMAP_SWJ_NOJTAG()  AFIO_DBGAFR_CONFIG(AFIO_MAPR_SWJ_CFG_JTAGDISABLE)
	|
#define AFIO_DBGAFR_CONFIG(DBGAFR_SWJCFG)  do{ uint32_t tmpreg = AFIO->MAPR;     \
                                               tmpreg &= ~AFIO_MAPR_SWJ_CFG_Msk; \
                                               tmpreg |= DBGAFR_SWJCFG;          \
                                               AFIO->MAPR = tmpreg;              \
                                               }while(0u)
```



