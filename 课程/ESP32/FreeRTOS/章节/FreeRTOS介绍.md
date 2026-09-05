# FreeRTOS介绍

[toc]

## **一、FreeRTOS是什么**

![https://share.note.youdao.com/yws/public/resource/f17d7df84e9ce036d04d9c597fdc8125/xmlnote/F3884373DF0B4A6C8EA9C562869E6EB0/WEBRESOURCE764dc4e2a41f4c8fbfe471e4020d0231/57835](./img/57835.png)

FreeRTOS（Free Real-Time Operating System）是一个开源的实时操作系统，专门设计用于嵌入式系统和实时应用程序。它提供了一套简单、可移植、可扩展的内核功能，帮助开发者管理任务调度、内存管理、中断处理、通信和同步等操作，以便在资源受限的嵌入式环境下实现可靠的实时任务调度和协作。

FreeRTOS是RTOS系统的一种，FreeRTOS十分的小巧，可以在资源有限的微控制器中运行，当然，FreeRTOS 不仅局限于在微控制器中使用。但从文件数量上来看 FreeRTOS 要比μC/OS-II和μC/OS-III少的多。	

FreeRTOS 最大的优势就是开源免费，商业使用的话不需要用户公开源代码，也不存在任何版权问题，是当前小型嵌入式操作系统市场使用率最高的。

 

**官网**

﻿https://www.freertos.org/﻿

 

**api函数**

﻿https://www.freertos.org/a00106.html﻿

 

![https://share.note.youdao.com/yws/public/resource/f17d7df84e9ce036d04d9c597fdc8125/xmlnote/F3884373DF0B4A6C8EA9C562869E6EB0/WEBRESOURCE7b2b6b678ee84c5398361e3c83a698d3/57838](./img/57838.png)

**文档下载**

﻿https://www.freertos.org/Documentation/RTOS_book.html﻿

 

以下是官网文档的下载地址页面。

![https://share.note.youdao.com/yws/public/resource/f17d7df84e9ce036d04d9c597fdc8125/xmlnote/F3884373DF0B4A6C8EA9C562869E6EB0/WEBRESOURCE256e0666f4b146918f6d7172fdc0e452/57827](./img/57827.png)

 

约定：为了方便简读该系统，统一称呼为“开源实时操作系统”。

 

## **二、FreeRTOS的特点**

FreeRTOS被广泛使用的原因是它为嵌入式系统和实时应用程序提供了一系列重要的优势和功能，使得开发者更容易构建可靠、高效的实时应用。以下是为什么需要FreeRTOS的几个关键原因：

1. 实时性能：FreeRTOS是一个实时操作系统，具有响应快、精确的任务调度和中断处理能力。它能够满足实时应用的时间约束，确保关键任务按时执行，保持系统的可靠性和稳定性。

1. 可移植性：FreeRTOS的内核是高度可移植的，可以方便地移植到不同的处理器架构和硬件平台上。这使得开发者可以在各种嵌入式系统上使用FreeRTOS，无论是单片机还是高性能处理器。

1. 简单易用：FreeRTOS具有简单和直观的API，易于学习和使用。它提供了一套清晰的任务管理、同步机制和内存管理功能，开发者可以快速上手并开发应用程序。

1. 资源效率：FreeRTOS是一个轻量级的操作系统，具有较小的内存占用和低的处理器负载。它被设计为高效利用有限的资源，适用于资源受限的嵌入式环境。

1. 可扩展性：FreeRTOS提供了可扩展的特性和组件，如信号量、队列、定时器等，可以根据应用需求进行定制和扩展。开发者可以根据实际情况选择所需的功能，提高系统的灵活性和可定制性。

1. 开源和活跃的社区支持：FreeRTOS是一个开源项目，拥有庞大而活跃的开发者社区。这意味着开发者可以获得免费的支持、文档、示例代码和社区贡献的扩展功能，从而更好地理解和使用FreeRTOS。

综上所述，FreeRTOS作为一款成熟且广泛应用的实时操作系统，具备实时性能、可移植性、简单易用、资源效率、可扩展性等优势。这些特点使得FreeRTOS成为嵌入式系统开发中的首选，特别适用于对实时性要求较高的应用领域，如工业自动化、医疗设备、消费电子、物联网等。

 

## **三、FreeRTOS代码规范**

FreeRTOS 核心源码文件的编写遵循 MISRA 代码规则，同时支持各种编译器。但考虑到有些编译器的性能还比较弱，不支持 C 语言的新标准 C99 和 C11 的一些特性和语法，所以 FreeRTOS 的源码中就没有引入 C99 和 C11 的新特性，但是有一个例外，源码中有用到头文件 stdint.h（这个文件是C99标准才引入的）。

 

### **3.1 FreeRTOS代码结构**

![https://share.note.youdao.com/yws/public/resource/f17d7df84e9ce036d04d9c597fdc8125/xmlnote/F3884373DF0B4A6C8EA9C562869E6EB0/WEBRESOURCEb299b6150c2b4fb88019af514a93d680/57831](./img/57831.png)

 

其内核代码文件就这几个，非常简洁:

- croutine.c/croutine.h: 协程，在8位/16位平台下效率比较高，在32位平台建议使用任务task。

- event_groups.c / event_groups.h:顾名思义，这个是事件组的实现。

- heap_x.c：内核堆实现，FreeRTOS提供了heap_1.c ～ heap_5.c 5种堆管理器，各有优缺点，需要根据应用进行选择，常用**heap_4.c**：堆空间可以分配也可以释放。

- list.c/list.h：链表实现，主要为调度器提供数据结构算法支持服务。比如任务链表。

- port.c/portmacro.h：硬件相关层级可移植抽象，主要包括SysTick中断，上下文切换，中断管理，具体实现很大程度上取决于平台（单片机体系硬件内核和编译器工具集）。通常以汇编语言实现，常由芯片厂商完成。

- queue.c/queue.h/semphr.h：信号量、互斥锁、消息队列实现。

- tasks.c/task.h:任务管理器实现。

- timers.c/timers.h：软件定时器实现。

- FreeRTOS.h：选编译配置文件，用于汇总所有源文件的编译选择控制。

- FreeRTOSConfig.h：FreeRTOS内核配置，Tick时钟和irq中断配置。

 

### **3.2 FreeRTOS代码规范**

#### **3.2.1 变量**

变量有**严格的前缀标识**变量类型属性：

- c – char 字符型变量

- s – short 短整型变量

- l – long  长整型变量

- x – portBASE_TYPE 在 portmacro.h 中定义，便于移植的数据类型转定义（esp32：int32_t）

- u – unsigned 无符号整型

- p -  pointer 指针

举例：

```C
//x表示portBASE_TYPE, u 表示无符号型
PRIVILEGED_DATA static volatile TickType_t xTickCount = ( TickType_t ) configINITIAL_TICK_COUNT;
PRIVILEGED_DATA static volatile UBaseType_t uxTopReadyPriority = tskIDLE_PRIORITY;
 
//比如在list.h 中
struct xLIST_ITEM
{
    configLIST_VOLATILE TickType_t xItemValue;
    //指针以p打头
    struct xLIST_ITEM * configLIST_VOLATILE pxNext; 
    struct xLIST_ITEM * configLIST_VOLATILE pxPrevious; 
    void * pvOwner; 
    struct xLIST * configLIST_VOLATILE pxContainer; 
};
```

 

对于C语言的基本数据类型，做了可移植转定义：

```C
#define portCHAR          char
#define portFLOAT         float
#define portDOUBLE        double
#define portLONG          long
#define portSHORT         short
#define portSTACK_TYPE    uint32_t
#define portBASE_TYPE     long
```

 

#### **3.2.2 函数**

前缀：

- v ：void 无返回类型

- x ：返回portBASE_TYPE

- prv ：私有函数，模块内使用

```C
//ux 表示无符号portBASE_TYPE 返回值
//List表示该函数所属文件
//Remove函数名
UBaseType_t uxListRemove( ListItem_t * const pxItemToRemove ) PRIVILEGED_FUNCTION;
 
//又比如prv 表示模块内函数
static TickType_t prvGetNextExpireTime( BaseType_t * const pxListWasEmpty ) PRIVILEGED_FUNCTION;
```

 

#### **3.2.3 宏**

定义宏所属文件，也即在哪个文件内定义的：

- port：比如portable.h中portMAX_DELAY

- task：比如task.h中task_ENTER_CRITICAL

- pd ：例如projdefs.h中定义的pdTRUE

- config：例如 FreeRTOSConfig.h中定义的configUSE_PREEMPTION

- err：例如 projdefs.h中定义的errQUEUE_FULL

至于这么严格的代码规范是否值得推崇，提高阅读性。但是在实际开发中这个见仁见智，有些企业比较喜欢Linux代码风格，对于过于复杂的代码规范，会继续原有的代码风格。

