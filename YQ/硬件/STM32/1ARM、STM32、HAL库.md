# ARM

[toc]

# 1 ARM概述

## 1.1 历史

  1978年，物理学家赫尔曼·豪泽（Hermann Hauser）和工程师Chris Curry，在英国剑桥创办了CPU公司（Cambridge Processing Unit），主要业务是为当地市场供应电子设备。1979年，CPU公司改名为Acorn公司。1985年，Roger Wilson和Steve Furber设计了他们自己的第一代32位、6MHz的处理器，用它做出了一台RISC指令集的计算机，简称ARM（Acorn RISC Machine）。这就是ARM这个名字的由来。

- 经典指令集
    - CISC
        复杂指令集计算机（Complex Instruction Set Computer）
        在CISC指令集的各种指令中，大约有20%的指令会被反复使用，占整个程序代码的80%。而余下的指令却不经常使用，在程序设计中只占20%，目前，桌面计算机流行的x86体系结构即使用CISC。
    - RISC
        精简指令集计算机（reduced instruction set computer）
        支持的指令比较简单，所以功耗小、价格便宜，特别适合移动设备。早期使用ARM芯片的典型设备，就是苹果公司的牛顿PDA。

特点区别各方面如下：

1. 指令系统
    　　CISC：计算机的指令系统比较丰富，有专用指令来完成特定的功能。因此，处理特殊任务效率较高。
    　　RISC：设计者把主要精力放在那些经常使用的指令上，尽量使它们具有简单高效的特色。对不常用的功能，常通过组合指令来完成。因此，在RISC 机器上实现特殊功能时，效率可能较低。但可以利用流水技术和超标量技术加以改进和弥补。

1. 存储器操作
    　　CISC：机器的存储器操作指令多，操作直接。
    　　RISC：对存储器操作有限制，使控制简单化。

1. 程序
    　　CISC：汇编语言程序编程相对简单，科学计算及复杂操作的程序社设计相对容易，效率较高。
    　　RISC：汇编语言程序一般需要较大的内存空间，实现特殊功能时程序复杂，不易设计。

1. 中断
    　　CISC：机器是在一条指令执行结束后响应中断。
    　　RISC：机器在一条指令执行的适当地方可以响应中断。

1. CPU
    　　CISC：CPU包含有丰富的电路单元，因而功能强、面积大、功耗大。
    　　RISC：CPU包含有较少的单元电路，因而面积小、功耗低。

1. 设计周期
    　　CISC：微处理器结构复杂，设计周期长。
    　　RISC：微处理器结构简单，布局紧凑，设计周期短，且易于采用最新技术。

1. 用户使用
    　　CISC：微处理器结构复杂，功能强大，实现特殊功能容易。
    　　RISC：微处理器结构简单，指令规整，性能容易把握，易学易用。

1. 应用范围
    　　CISC：机器则更适合于通用机。
    　　RISC：由于RISC指令系统的确定与特定的应用领域有关，故RISC 机器更适合于专用机。

## 1.2 ARM的应用

  20世纪90年代开始，ARM 32位嵌入式RISC处理器扩展到世界范围，占据了低功耗、低成本和高性能的嵌入式系统应用领域的领先地位。ARM公司既不生产芯片也不销售芯片，它只出售芯片技术授权。

  搭载ARM芯片架构的设备数量是英特尔的25倍。全世界99%的智能手机和平板电脑都采用ARM架构。约有43亿人每天都会触摸一台搭载ARM芯片的设备，占全球总人口的60%。


![img](./img/rBJlJmKm03qAeAEpAAEBlXUvppo142.png)

# 2 ARM处理器

## 2.1 ARM的处理器类型

目前ARM架构常见类型：


![img](./img/rBJlJmKm03qAdzT7AACG29su4I4428.jpg)

- Cortex-A：针对高性能计算。如我们目前手机SoC中常出现的Cortex-A76等。
- Cortex-R：针对实时操作处理。主要是面向嵌入式实时处理器。在汽车的电子制动系统，工业控制领域等领域比较常见。
- Cortex-M：专为低功耗、低成本系统设计。目前火热的IoT领域常常见到采用Cortex-M架构的处理器。


![img](./img/rBJlJmKm03qAQrCwAA6Z1avIoPQ281.png)

ARM：经典系列、Cortex-M系列、Cortex-R系列、Cortex-A系列。

**经典系列（ARM7、ARM9、ARM11）**


![img](./img/rBJlJmKm03qAMovNAAPWL94En3M077.png)

**Cortex-A系列**


![img](./img/rBJlJmKm03qAMRlOAAYQWQK5OUU854.png)

  Application Processors（应用处理器）–面向移动计算、智能手机、服务器等市场的的高端处理器。这类处理器运行在很高的时钟频率（超过1GHz），支持像Linux，Android，MS Windows和移动操作系统等完整操作系统需要的内存管理单元（MMU）。

  如果规划开发的产品需要运行上述其中的一个操作系统，你需要选择ARM应用处理器(Cortex-A53、Cortex-A73、Cortex-A76、Cortex-A77)。



**Cortex-R系列**

![img](./img/rBJlJmKm03qAVwAhAAGOI-bUUl0901.png)

  Real-time Processors（实时处理器）–面向实时应用的高性能处理器系列，例如硬盘控制器，汽车传动系统和无线通讯的基带控制。

  多数实时处理器不支持MMU，不过通常具有MPU、Cache和其他针对工业应用设计的存储器功能。实时处理器运行在比较高的时钟频率（例如200MHz 到 >1GHz ），响应延迟非常低。

  然实时处理器不能运行完整版本的Linux和Windows操作系统，但是支持大量的实时操作系统（RTOS）。

  其相比Cortex-A系列，少了对页表的支持，也就是说软件看到的地址都是物理地址，相对来说软件运行时间和中断响应速度都更加快速稳定，容易预测。

**Cortex-M系列**

![img](./img/rBJlJmKm03qAVLs5AAHo04fpMSE320.png)

  Microcontroller Processors（微控制器处理器）–微控制器处理器通常设计成面积很小和能效比很高。

  通常这些处理器的流水线很短，最高时钟频率很低（虽然市场上有此类的处理器可以运行在200Mhz之上）。 并且，新的Cortex-M处理器家族设计的非常容易使用。因此，ARM微控制器处理器在单片机和深度嵌入式系统市场非常成功和受欢迎。

  其相比Cortex-R就更加精简了，更短的流水线，更简单的指令集，更少的运算单元，调试单元，总线性能要求不高，以低功耗为主。

## 2.2 ARM RISC的特点

  ARM处理器则是ARM架构下的RISC（精简指令集）处理器。ARM处理器广泛的使用在许多嵌入式系统。ARM处理器的特点有指令长度固定，执行效率高，低成本等，主要特点如下：

- 指令集——RISC减少了指令集的种类，通常一个周期一条指令，采用固定长度的指令格式，编译器或程序员通过几条指令完成一个复杂的操作。而CISC指令集的指令长度通常不固定；
- 流水线——RISC采用单周期指令，且指令长度固定，便于流水线操作执行；
- 寄存器——RISC的处理器拥有更多的通用寄存器，寄存器操作较多。例如ARM处理器具有37个寄存器；
- Load/Store结构——使用加载/存储指令批量从内存中读写数据，提高数据的传输效率；
- 寻址方式简化，指令长度固定，指令格式和寻址方式种类减少。

# 「课堂练习1」

简述ARM的定义与种类。

## 2.3 ARM指令架构

  Thumb是16位指令；Thumb-2是16和32位混合指令集。ARM指令集则起始32位，在ARMv8开始，支持64位。

| 指令架构 |      特性       |            说明             |
| :------: | :-------------: | :-------------------------: |
|  Thumb   |      16位       |        最早的指令集         |
| Thumb-2  | 16位和32位混合  |     在Cortex系列中引入      |
|   A32    | ARM 32 位指令集 |   即以前称之为ARM的指令集   |
|   A64    | ARM 64 位指令集 | 在ARMv8-A中引入的，支持64位 |

### Thumb与Thumb-2

  ARM32指令集：代码全部是 32位的，每条指令能承载更多的信息，因此使用最少的指令完成功能， 所以在相同频率下运行速度也是最快的， 但也因为每条指令是32位的而占用了最多的程序空间。

  Thumb指令集：代码全部是16位的，每条指令所能承载的信息少，因此它需要使用更多的指令才能完成功能， 因此运行速度慢， 但它也占用了最少的程序空间

  Thumb-2指令集：在前面两者之间取了一个平衡，兼有二者的优势，当一个操作可以使用一条32位指令完成时就使用32位的指令，加快运行速度，而当一次操作只需要一条16位指令完成时就使用位的指令，节约存储空间。


![img](./img/rBJlJmKm03qAJNpwAAG-x-a8LrQ063.png)

  MCU使用什么指令集主要由内核决定的，比如Cortex-M4使用的是Thumb-2指令集。

# 「课堂练习2」

简述ARM、Thumb、Thumb-2指令集。







## 2.4 ARM CPU 的架构

| 架构版本  |                             说明                             |                           chipsets                           |
| :-------: | :----------------------------------------------------------: | :----------------------------------------------------------: |
|   ARMv1   |                             原型                             |                             原型                             |
|   ARMv2   |             原型，增强v1，添加乘法指令和协处理器             |                             原型                             |
|   ARMv3   |                 添加了MMU、Cache、WriteCache                 |                         第一个处理器                         |
|   ARMv4   |         32位，3级整数流水线； 商业化大量的Arm7处理器         |        ARM7TDMI、ARM720T、ARM9TDMI、ARM940T、ARM920T         |
|   ARMv5   | 32位，5-6级整数流水线。包括ARMv5TE、ARMv5EJ；[E：增强型DSP指令集。包括全部算法和16位乘法操作。J：支持新的Java] | ARM9E-S、ARM966E-S、ARM1020E、ARM 1022E以及XScale是ARMv5TE的。ARM9EJ-S、ARM926EJ-S、ARM7EJ-S、ARM1026EJ-S是基于ARMv5EJ的。 |
|   ARMv6   | 32位 ARMv6 包括了（ SIMD、Thumb、Jazelle、DBX、(VFP)、MMU）, ARMv6T2包括了（SIMD、Thumb-2、(VFP)、MPU）, ARMv6KZ包括了（ARMv6基础上增加MMU、TrustZone）,ARMv6K包括了（1-4 核SMP、MMU） |                     ARM1176JZ、ARM1136EJ                     |
| ARMv7-A/R |   32位，Cortex-A系列芯片的指令集。其加入的特性都引入到v8-A   |                  Cortex-A5,A7,A8,A9,A15,A17                  |
|  ARMv8-A  |                         引入64位支持                         |         Cortex-A32,A35,A53,A55,A57;A73,A75,A76,A76AE         |

**新的ARMv7，ARMv8指令集**

![img](./img/rBJlJmKm03qAYlK5AACwe_qeKPY264.png)

![img](./img/rBJlJmKm03qADCLOAAKFrScSs78983.jpg)

**截止目前ARM处理器的最新系列**

![img](./img/rBJlJmKm03qAQbenABg8NkGnC0g046.png)

## 2.5 Cortex-M 系列

### Cortex-M 选型

  Cortex-M家族兄弟众多，且性能各异，满足了不同客户的需求，使得ARM公司拥有 40 个以上的 合作伙伴，包括 NXP Semiconductors、STMicroelectronics、Texas Instruments 和 Toshiba 等领先供应商。

- 选择Cortex –M0
    能耗最低的最小ARM处理器，在不到 12 K 门的面积内能耗仅有 85 µW/MHz（0.085 毫瓦），同时保留与功能丰富的 Cortex-M3 处理器的工具和二进制向上兼容性。
    M0指令只有 56 个，这样便可以快速掌握整个 Cortex-M0 指令集（如果需要）；M0优化的连接性，设计为支持低能耗连接，如 Bluetooth Low Energy (BLE)、IEEE 802.15 和 Z-wave。

    

- 选择Cortex-M3
    在 90nmG基础上为12.5DMIPS/mW。将集成的睡眠模式与可选的状态保留功能相结合，全功能性让M3处理器执行Thumb®-2 指令集以获得最佳性能和代码大小，包括硬件除法、单周期乘法和位字段操作。Cortex-M3 NVIC 在设计时是高度可配置的，最多可提供240 个具有单独优先级、动态重设优先级功能和集成系统时钟的系统中断。

    

- 选择Cortex-M4
    在M3的基础上强化了运算能力，新加了浮点、DSP、并行计算等，用以满足需要有效且易于使用的控制和信号处理功能混合的数字信号控制市场。满足面向电动机控制、汽车、电源管理、嵌入式音频和工业自动化市场的新兴类别的灵活解决方案。

    

**主流的Cortex-M3与Cortex-M4差异**

- 架构

![img](./img/rBJlJmKm03qAJLcfABOcLMlPUGc669.png)

- 性能


![img](./img/rBJlJmKm03qABd2vAAPGpik3Ftg589.png)

  以上是M4与M3的性能对比，官方提供的测试数据如图。

  对于图表，Y轴代表执行给出的计算用的相对的周期数。 因此，循环数越小，性能越好。以Cortex-M3作为参考，Cortex-M4的性能计算，性能比大概为其周期计数的倒数。举例说明，PID功能，Cortex-M4的周期数是与Cortex-M3的约0.7倍，因此相对性能是1/0.7，即1.4倍。

### Cortex-M4体系结构


![img](./img/rBJlJmKm03qATOUaAACEZ5e4OVc058.gif)

1. Cortex-M4架构

ARM Cortex采用的是哈佛架构，为系统提供了三套总线。

- ICode总线
- DCode总线
- System总线

(1) Cortex-M4的工作状态



- ARM指令集

- Thumb指令集

    

(2) Cortex-M4工作模式

- Thread Mode：线程模式即正常模式
- Hander Mode：处理模式即异常（中断）模式

1. Cortex-M4寄存器

  寄存器：在cpu内部暂存数据内容的，但是所有的指令的运算数，最终需要放到寄存器中才能运算。

  寄存器分为：通用寄存器和专用寄存器：

- 通用寄存器： R0~R7 thumb-2所有的指令都可以访问它，R8 ~ R12 只有少量的thumb指令可以访问，thumb - 2都可以访问它。
- 专用寄存器 ：R13、R14、R15、xPSR

R13（SP）：Stack Pointer 堆栈指针，保存堆栈的栈顶地址的一个寄存器
R14（LR）：Linked Register 链接寄存器。在执行指令的过程的时候，需要保存该指令的下一条指令的地址（返回地址）
R15（PC）：Program Counter 程序计数器。PC保存的是下一条指令的地址
xPSR：Program Status Register 程序状态寄存器。保存程序运行过程中的一些状态标记，这些要保存的状态分为：
应用状态寄存器：APSR N Z C V Q
中断状态寄存器：IPSR Interrupt
执行状态寄存器：EPSR Excute



---



# 1 历史背景

  8051单片机是嵌入式学习中一款入门级的经典 MCU，因其结构简单，易于教学，且可以通过串口编程而不需要额外的仿真器，所以在教学时被大量采用，至今很多大学在嵌入式教学中用的还是8051。

  8051单片机诞生于 70 年代，属于传统的 8 位单片机，现在的市场产品竞争越来越激烈，对成本极其敏感，相应地对 MCU 的性能要求也更苛刻：更多功能，更低功耗，易用界面和多任务。面对这些要求，8051单片机现有的资源就显得得抓襟见肘。所以无论是高校教学还是市场需求，都急需一款新的 MCU 来为这个领域注入新的活力。

  基于这样的市场需求， ARM 公司推出了其全新的基于 ARMv7 架构的 32 位 Cortex- M3 微控制器内核。紧随其后，ST（意法半导体）公司就推出了基于 Cortex-M3 内核的STM32。STM32凭借其产品线的多样化、极高的性价比、简单易用的库开发方式，迅速在众多 Cortex-M3 MCU中脱颖而出，成为最闪亮的一颗新星。STM32一上市就迅速占领了中低端 MCU 市场，受到了市场和工程师的无比青睐，颇有星火燎原之势。

  作为一名合格的嵌入式工程师，面对新出现的技术，我们不是充耳不闻，而是要尽快吻合市场的需要，跟上技术的潮流。如今 STM32 的出现就是一种趋势，一种潮流，我们要做的就是搭上这趟快车，让自己的技术更有竞争力。

  除了桌面PC之外，所有的控制类设备，都称之嵌入式。


![img](./img/wKgP3GI-jRiAYJywAAMO9lsb8ZA698.png)

# 2 STM32

**介绍**

  STM32系列专为要求高性能、低成本、低功耗的嵌入式应用设计的ARM Cortex®-M0，M0+，M3, M4和M7内核 。按内核架构分为不同产品：

  主流产品（STM32F0、STM32F1、STM32F3）、超低功耗产品（STM32L0、STM32L1、STM32L4、STM32L4+）、高性能产品（STM32F2、STM32F4、STM32F7、STM32H7）

> ST,就是一间公司，意法半导体。
> M，微电子/微控制器
> 32,单片机是32位

**ST公司**

![img](./img/wKgP3GI-jRiAFlLWAASbaydWetE069.png)
![img](./img/wKgP3GI-jRiAMHnyAApNx0Qb668959.png)

**产品系列**

- 为智能驾驶和物联网提供半导体解决方案
    今天，意法半导体的产品无处不在，致力于与客户共同努力实现智能驾驶、智能工厂、智能城市和智能家居，以及下一代移动和物联网产品。
- 智能驾驶：更安全、更环保、联网能力更强
    据业内估计，当今80%的汽车工业创新应用都是由电子技术直接或间接实现的，这意味整车半导体占比在逐年稳定增长。通过整合多项技术，意法半导体的智能驾驶产品和解决方案让汽车变得更安全、更环保、联网能力更强。
- 从视觉、雷达、影像、传感器、GNSS卫星定位技术，到随动转向照明系统和用户显示技术，我们的先进驾驶辅助系统(ADAS)产品技术让汽车驾驶变得更安全；我们的能源管理处理器(EMU, ECU)，被所有汽车子系统用作核心部件的功率管理芯片、电动汽车宽能带隙技术(SiC和GaN)、传感器等等，让汽车驾驶变得更环保；我们的车间通信和车路通信(V2X)解决方案、信息娱乐系统和车载信息服务处理器、收音机调谐器、功率放大器、传感器，让汽车联网通信能力更强。
- 物联网: 智能个人设备、智能家居、智能城市和智能工厂
    由于物联网市场高度分散，我们的目标市场横跨整个客户群，从最大的客户，到超过十万家同样重要的中小客户，我们通过经销商网络和大众市场营销计划为客户提供服务。

**其他**

  意法半导体通过提供工业自动化和机器人技术，让制造业和其它工业领域提高能效、灵活性和安全性。我们称这些技术为智能工业技术，其在工业领域引发的变化经常被人称为第四次工业革命。工业智能综合应用各种产品，包括微控制器、传感器、致动器、电机控制、信号调理、工业通信解决方案、电源、保护器件、无线模块、显示器和LED控制器，使工业系统变更加智能。

  ST通过其核心：能源消耗和管理系统来解决智能家居、建筑和城市的问题。这些解决方案解决了一些关键功能：智能电表内部的安全、多功能芯片，帮助消费者和公用事业公司跟踪和平衡电力、水和天然气的消耗和计费；更智能的街道照明，感知周围环境，调暗或关闭，以适应照明条件和市政需求；测量交通流量的传感器，可以在障碍物周围改变车辆和行人的路线；以及允许这些环境连接到物联网(IoT)的连接性解决方案。

  我们个人日常生活受益于我们每天携带的经常使用的“智能产品”。意法半导体是一家全球领先的半导体厂商，拥有下一代消费设备所需的全部关键技术：低功耗和超低功耗微控制器、安全解决方案、传感器和制动器、连通性、调节和保护、电机控制、功率和电源管理。

  意法半导体用一系列可兼容性的开发生态环境，使开发原型便捷而实惠，包括硬件和软件开发工具，评估组件和为垂直应用和云兼容性配备的带有预嵌入软件的模块，并有ST伙伴计划提供机会去扩展可信的设计和工程公司，帮助客户加快产品上市时间。意法半导体通过提供能源管理的核心技术产品，满足高速发展的智能家居和智能城市系统的市场需求。从双片智能表计解决方案，到智能水平更高的路灯系统，意法半导体解决方案瞄准智能城市的关键功能。智能表计帮助消费者和公用事业记录水电燃气的使用情况和费用；智能路灯可以监测环境，根据环境光线条件和市政需求开关灯或调节亮度，监测交通流量，提供潜在拥堵路况信息。

# 3 选型

## 3.1 背景

  并非所有基于ARM架构的MCU都能提供相同水平的性能和能效，因此选择合适的方案是非常重要的。

  许多MCU供应商组合包括主题上的数百种变体。虽然看起来基于ARM Cortex-M的MCU的出现可能是这一广泛选择的核心，但实际上总有很多32位选项可供选择。

  在过去，对任何给定指令集的支持只是选择过程中的一个重要元素，但是由于ARM，指令集的相关性可能已经变得没有实际意义。围绕Cortex-M内核的生态系统意味着工程师可以在一个架构上合理地标准化。但这仍然有许多功能需要比较。在今天的嵌入式应用程序中，这将重点放在一个简短的参数列表中，这些参数仍然可以根据需求进行测量。那么让我们来看看需要考虑的八个最重要的MCU功能。

**有功功率**

  与使用CMOS技术制造的所有集成器件一样，MCU仅在其逻辑门改变状态时消耗功率。现代MCU中CMOS门的数量意味着功耗可能会变得很大，特别是在高时钟速率下。因此，有源功耗是近年来大多数设备制造商关注的关键数字和面积。
  大多数MCU将努力在有功功耗和处理性能之间取得平衡。即使相同的内核位于器件的核心，该参数也可能因MCU供应商的设计专业知识而有很大差异。

**性能**

  了解性能指标非常重要，特别是在查阅数据表时，因为规格经常在“理想”（或更不适合）的操作条件下报告。要提供高性能和低有功功率是困难的，同样，一个领域MCU供应商可以区分他们的产品。仔细比较数据表性能规格，并向MCU供应商询问结果背后的实际运行条件。

**响应**

  保持有功功率低的一种方法是降低工作频率，这不可避免地并且很自然地导致睡眠模式。任何MCU都可以进入消耗最少有功和静态功耗的模式，但总是通过时钟和功率门控来实现，即将时钟或功率移到MCU的特定区域。在不适当考虑目标应用的要求的情况下使用该技术的惩罚可能导致MCU在需要时恢复其职责的速度很慢。从深度睡眠模式快速唤醒是MCU供应商中一个激烈争议的参数。

**能源效率**

  如果降低响应性是使用睡眠模式的惩罚，则益处是较低的能量消耗。在这里，趋势是已经有一段时间并且实施一系列睡眠模式，为正确的操作条件提供适当的效率水平。降低功耗和快速唤醒的休眠模式应该补充深度睡眠模式，在应用需要时，即使以更长的唤醒时间为代价，也能将功耗降至最低。超低功耗有源和睡眠模式的组合以及非常快的唤醒时间定义了MCU的能效。
  能源效率由功耗随时间变化定义，即最低有效和睡眠模式能量加上最快的唤醒时间。

**外设**

  MCU设计的最新发展是在外围子系统中实现更高的智能，允许各种外设自动运行。除了为应用程序开发带来新的维度之外，自主外设的最重要的好处是它们允许内核更长时间保持（深度）睡眠模式。自动外围设备无需定期从深度节能睡眠模式中出现以检查事件，而是能够注册事件并决定是否需要核心干预。如果您的应用需要出色的能效，请务必选择具有支持自主外设操作的架构的MCU。

**接口**

  一些供应商提供的MCU能够直接和智能地连接到更广泛的信号。MCU本质上是数字的，但通常具有高水平的混合信号能力，例如集成模拟到数字和数字到模拟转换器。然而，由于我们生活的世界本质上仍然是模拟的，因此越来越需要为模拟信号提供更大的支持，特别是那些来自传感器的模拟信号。物联网（IoT）将由先进的传感器启用，这些传感器将包含很小的模拟信号。能够直接连接到小型电容式，电感式或电阻式传感器，并在唤醒CPU之前智能地解析信号，这无疑将成为面向物联网设计的常见用例。

**软件**

  虽然如前所述，ARM Cortex系列拥有强大且不断发展的软件提供商生态系统，但终端应用程序仍需要专用的应用程序代码。软件开发现在被认为是工程资源的最大单一消费者，因此在选择合适的MCU时，考虑生态系统和MCU供应商提供的软件支持水平和工具质量非常重要。MCU供应商仍然必须提供强大且用户友好的软件开发工具。即使IDE由首选合作伙伴提供，也必然会有特定差异化功能所需的支持元素。寻找能够提供非常全面的开发生态系统的MCU供应商，旨在简化设计过程。

## 3.2 STM32的分类与型号

**分类**

  STM32 有很多系列，可以满足市场的各种需求，从内核上分有 Cortex-M0、M3、M4和 M7 这几种，每个内核又大概分为主流、高性能和低功耗。


![img](./img/wKgP3GI-jRiATnllAAFPId-qP_k536.png)

Cortex-M分为：M0，M0+，M3，M4，M7。

- M0，M0+：基础版本，从图中可以看出来，有过于基础，所以生产不出来高性能的STM32的单片机；
- M3：目前最主流的设计内核选型，应用范围广；
- M4：比较着M3的内核来说，M4处理器添加了DSP的数据（这里可以认为是浮点数）处理的指令；重点解释一下：对于CPU（不是SOC）来说，运算浮点类型的数据是很麻烦的一件事，在选型的时候，如若用应用的领域需要大量浮点数据的运算的时候，那么就要选择M4的内核，M4会大大提高处理器性能和运算速度，而如果要要处理的浮点数据不多，则可以直接选择M3内核处理器；比如项目是平衡车或者平衡器的时候选择M4比较好；
- M7：性能好和功耗高兼具，适合追求极致性能项目；

可以认为：数字越大，性能越高；

**命名方法**


![img](./img/wKgP3GI-jRiAVmruAASSipACnM8580.png)

  STM32型号的说明：以**STM32F407ZET6**这个型号的芯片为例，该型号的组成为7个部分，其命名规则如下：

（1）STM32：STM32代表ARM Cortex-M4内核的32位微控制器。
（2）F：F代表芯片子系列。
（3）407：高性能，带DSP和FPU。
（4）Z：Z这一项代表引脚数，其中T代表36脚，C代表48脚，R代表64脚，V代表100脚，Z代表144脚。
（5）E：E这一项代表内嵌Flash容量，其中6代表32K字节Flash，8代表64K字节Flash，B代表128K字节Flash，C代表256K字节Flash，D代表384K字节Flash，E代表512K字节Flash。
（6）T：T这一项代表封装，其中H代表BGA封装，T代表LQFP封装，U代表VFQFPN封装。
（7）6：6这一项代表工作温度范围，其中6代表-40——85℃，7代表-40——105℃



# HAL库

# 1 背景

  ST为开发者提供了非常方便的开发库。到目前为止，有标准外设库(SPL库)、HAL库、LL库三种。前两者都是常用的库，后面的LL库是ST最近才添加，随HAL源码包一起提供。


![img](./img/wKgP3GI-jTeAeuBBAAGByXlmfY4758.png)

**标准外设库（Standard Peripheral Libraries）**



  标准外设库（Standard Peripherals Library）是对 STM32 芯片的一个完整的封装，包括所有标准器件外设的器件驱动器。这应该是目前使用最多的 ST 库。几乎全部使用 C 语言实现。但是，标准外设库也是针对某一系列芯片而言的，可移植性不强。例如，STM32F1x 的库和 STM32F3x 的库在文件结构上就有些不同，此外，在内部的实现上也稍微有些区别，这个在具体使用（移植）时，需要注意。

  相对于 HAL 库，标准外设库仍然接近于寄存器操作，主要就是将一些基本的寄存器操作封装成了 C 函数。开发者需要关注所使用的外设是在哪个总线之上，具体寄存器的配置等底层信息。

**硬件抽象库（Hardware Abstract Layer）**

  HAL 库是 ST 为 STM32 最新推出的抽象层嵌入式软件，可以更好的确保跨 STM32 产品的最大可移植性。该库提供了一整套一致的中间件组件，如 RTOS，USB，TCP/IP 和 图形 等。

  HAL 库是基于一个非限制性的 BSD 许可协议（Berkeley Software Distribution）而发布的开源代码。 ST 制作的中间件堆栈（USB 主机和设备库，STemWin）带有允许轻松重用的许可模式，只要是在 ST 公司的 MCU 芯片上使用，库中的中间件(USB 主机/设备库,STemWin)协议栈即被允许随便修改，并可以反复使用。至于基于其它著名的开源解决方案商的中间件（FreeRTOS，FatFs，LwIP和PolarSSL）也都具有友好的用户许可条款。

  作为目前 ST 主推的外设库，HAL库相关的文档还是非常详细的。
可以说HAL 库就是用来取代之前的标准外设库的。相比标准外设库，STM32Cube HAL 库表现出更高的抽象整合水平，HAL API 集中关注各外设的公共函数功能，这样便于定义一套通用的用户友好的API函数接口，从而可以轻松实现从一个STM32产品移植到另一个不同的STM32系列产品。HAL库是ST未来主推的库，从前年开始ST新出的芯片已经没有STD库了，比如 F7 系列。目前，HAL库已经支持STM32全线产品。

  使用HAL库编程，最好尽量符合HAL库编程的整体架构。

**LL 库（Low Layer）**

  LL库（Low Layer）是 ST 最近新增的库，与 HAL 库捆绑发布，文档也是和 HAL 库文档在一起的，比如：在STM32F3x 的 HAL 库说明文档中，ST 新增了LL库这一章节，但是在 F2x 的HAL文档中就没有。

  LL 库更接近硬件层，对需要复杂上层协议栈的外设不适用，直接操作寄存器。其支持所有外设。使用方法：
独立使用，该库完全独立实现，可以完全抛开 HAL 库，只用LL库编程完成。在使用STM32CubeMX生成项目时，直接选LL库即可。如果使用了复杂的外设，例如 USB，则会调用 HAL 库混合使用，和 HAL 库结合使用。

  目前，CubeMX 在生成项目时，可以选择采用 LL 库。

# 2 HAL库

  HAL全称Hardware Abstract Layer，意为硬件抽象层，HAL库是STM32开发生态中极为重要的组成部分，不过它不单独提供，而是以STM32CubeMX拓展包的形式提供。拓展包中除HAL库之外，也有Fatfs、FreeRTOS、STemWin等组件，可以在STM32CubeMX中选择性的使用，开发者可以直接使用该软件进行可视化配置，大大节省开发时间。

![img](./img/wKgP3GI-jTeAPSisAAK2xujsCKo764.png)

![img](./img/wKgP3GI-jTeAKHAvAAD1gyaweC4378.png)

  与标准外设库相比，HAL库封装得显得更加紧凑，并且源代码通过对外设的对象化，使“层”的特点非常明显，大部分外设也都通过句柄操作，极难见到寄存器的影子。

  但是近几年来，ST正在逐渐停止对标准外设库的更新，并主推HAL库（不过H7没有标准外设库，只有HAL库，所以无所谓）。

  先从标准外设库说起。C语言本身无法操作STM32的外设，程序对外设的操作，是通过外设的寄存器实现的。STM32外设的寄存器数量十分庞大，分别挂接在APB、AHB等总线上，在开发中如果直接操作外设寄存器，工作量是难以想象的。所以在早期，ST提供了一套封装了外设寄存器的代码模板，也就是标准外设库。由于经过了封装，在开发时不必直接操作外设寄存器，而是通过标准外设库间接操作，避免了直接操作外设寄存器的过程中因计算失误和工作疲劳等原因造成的错误。不过随着需求逐渐提高，越来越多的开发者在工程中加入了中间件(即 RTOS、GUI、FS等)。

  标准外设库只是对寄存器的简单封装，并不能完全将硬件封锁在底层代码中，所以很容易造成中间件不兼容的情况。


  相比之下，HAL库的封装十分到位，它以外设为单位封装，将功能有关联的外设进行交叉或者合并，并能向上层的用户程序或者中间件提供标准且统一的功能级接口而不是外设接口。其中最容易理解的，就是把EXTI合并到GPIO中，将多个可由GPIO产生的EXTI中断封装成了一个回调函数void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)，即把GPIO的外部中断功能封装成了一个中断回调接口。


官方给出的 HAL 库的包含结构：

![img](./img/wKgP3GI-jTeAZTYCAAKhHJNRZY0555.png)

  stm32f4xx.h 主要包含STM32同系列芯片的不同具体型号的定义，是否使用HAL库等的定义，接着，其会根据定义的芯片信号包含具体的芯片型号的头文件：

```
#if defined(STM32F405xx)
  #include "stm32f405xx.h"
#elif defined(STM32F415xx)
  #include "stm32f415xx.h"
#elif defined(STM32F407xx)
  #include "stm32f407xx.h"
#elif defined(STM32F417xx)
  #include "stm32f417xx.h"
#elif defined(STM32F427xx)
  #include "stm32f427xx.h"
#elif defined(STM32F437xx)
  #include "stm32f437xx.h"
#elif defined(STM32F429xx)
  #include "stm32f429xx.h"
#elif defined(STM32F439xx)
  #include "stm32f439xx.h"
#elif defined(STM32F401xC)
  #include "stm32f401xc.h"
#elif defined(STM32F401xE)
  #include "stm32f401xe.h"
#elif defined(STM32F410Tx)
  #include "stm32f410tx.h"
#elif defined(STM32F410Cx)
  #include "stm32f410cx.h"
#elif defined(STM32F410Rx)
  #include "stm32f410rx.h"
#elif defined(STM32F411xE)
  #include "stm32f411xe.h"
#elif defined(STM32F446xx)
  #include "stm32f446xx.h"
#elif defined(STM32F469xx)
  #include "stm32f469xx.h"
#elif defined(STM32F479xx)
  #include "stm32f479xx.h"
#elif defined(STM32F412Cx)
  #include "stm32f412cx.h"
#elif defined(STM32F412Zx)
  #include "stm32f412zx.h"
#elif defined(STM32F412Rx)
  #include "stm32f412rx.h"
#elif defined(STM32F412Vx)
  #include "stm32f412vx.h"
#elif defined(STM32F413xx)
  #include "stm32f413xx.h"
#elif defined(STM32F423xx)
  #include "stm32f423xx.h"
#else
 #error "Please select first the target STM32F4xx device used in your application (in stm32f4xx.h file)"
#endif
```

# 2 HAL库文件结构


HAL：Hardware Abstraction[æbˈstrækʃn] Layer，硬件抽象层


![img](./img/wKgP3GI-jTeAWITnAAFSlD0IT5Q611.png)

  从上图不难看出，LL 库和 HAL 库两者相互独立，只不过 LL 库更底层。而且，部分 HAL 库会调用LL库（例如：USB驱动）。同样，LL 库也会调用 HAL 库用户可以使用 STMCubeMX 直接生成对应芯片的整个项目（目前主流开发工具的项目基本全支持），STMCubeMX 负责给整理各种需要的源码文件。

## 2.1 HAL驱动文件

  外设驱动API文件和头文件：包含了常见主要的通用API，其中ppp表示外设名称，如adc、usart、gpio、irda等；

- *stm32f4xx_hal_ppp.c*
- *stm32f4xx_hal_ppp.h*

  外设驱动扩展API文件和头文件：包含指定的API和内部不同实现以覆盖通用API的新定义API接口函数，其中ppp表示外设名称；

- *stm32xx_hal_ppp_ex.c*
- *stm32xx_hal_ppp_ex.h*

  初始化HAL库文件、包含DBGMCU（调试接口）、Remap（重映射）和SysTick的TimeDelay；

- *stm32xx_hal.c*
- *stm32xx_hal.h*

自带的相应库函数例子：包含相应外设的初始化和去初始化；

- *stm32xx_hal_msp_template.c*
- *stm32xx_hal_conf_template.h*

通用HAL资源定义：包含通用定义声明、枚举、结构和宏定义；

- *stm32xx_hal_def.h*

## 2.2 用户应用文件

用于在main函数前初始化系统时钟，包含SystermInit（）函数，但不会在StartUp时配置相同时钟（与标准库不同的地方）；

- *system_stm32f4xx.c*

包含reset handler处理函数、中断向量、并允许调整堆栈大小：

- *startup_stm32f4xx.s*

    

EWARM工具链文件，用以调整堆栈大小以适应应用程序的要求；

- *stm32f4xx_flash.icf*

    

用户自定义外设初始化文件：包括初始化和去初始化，包含主例程和回调；

- *stm32f4xx_hal_msp.c*

用户自定义驱动文件：允许用户自定义HAL驱动，可以使用默认配置而无需修改；

- *stm32f4xx_hal_conf.h*

    

异常处理和外设中断服务文件：会在SysTick_Handler（）函数中反复调用HAL_IncTick（）以实现延时；

- *stm32f4xx_it.c/.h*

    

主函数：调用HAL_Init（）函数、在Debug模式下使用的assert_failed（）时间检测函数、系统时钟配置函数、外设HAL初始化和应用代码；

- *main.c/.h*

    

通过STM32CubeMX配置的工程，已经默认做好如下的配置：

- HAL初始化完成；
- SysTick中断服务实现HAL_Delay（）延时功能；
    = 系统时钟配置为器件最大频率的时钟。

# 3 HAL数据结构

每一个HAL驱动都遵循以下数据结构：

- 外设句柄结构 Peripheral handle structures
- 初始化和配置结构 Initialization and configuration structures
- 特殊的过程结构 Specific process structures

## 3.1 外设句柄结构-Peripheral handle structures

  PPP_HandlerTypeDef *handler是HAL驱动程序中实现的主要结构；它处理外设模块配置、注册、嵌入外围设备所需要的所有结构和变量；
该句柄结构主要用于：

- 可以初始化多个实例（可以使用相同的结构定义和配置多个相同外设，如USART1、USART2、USART3），使每个初始化的外设都有相同的完整的结构；
- 外围进程互通，管理进程之间的共享数据资源，如全局变量、DMA句柄结构、状态机；
- 存储，用于管理对应的初始化HAL外设驱动程序中的全局变量；

外设句柄结构举例：

```
typedef struct
{
	USART_TypeDef *Instance; 	/* USART registers base address */
	USART_InitTypeDef Init; 	/* Usart communication parameters */
	uint8_t *pTxBuffPtr;		/* Pointer to Usart Tx transfer Buffer */
	uint16_t TxXferSize; 		/* Usart Tx Transfer size */
	__IO uint16_t TxXferCount;	/* Usart Tx Transfer Counter */
	uint8_t *pRxBuffPtr;		/* Pointer to Usart Rx transfer Buffer */
	uint16_t RxXferSize; 		/* Usart Rx Transfer size */
	__IO uint16_t RxXferCount;	/* Usart Rx Transfer Counter */
	DMA_HandleTypeDef *hdmatx;	/* Usart Tx DMA Handle parameters */
	DMA_HandleTypeDef *hdmarx;	/* Usart Rx DMA Handle parameters */
	HAL_LockTypeDef Lock; 		/* Locking object */
	__IO HAL_USART_StateTypeDef State; /* Usart communication state */
	__IO HAL_USART_ErrorTypeDef ErrorCode;/* USART Error code */
}USART_HandleTypeDef;
```

  外设句柄结构的定义：在外设驱动头文件stm32f4xx_hal_ppp.h中定义；其名称通常都是PPP_HandleTypeDef；这些结构通常都是用来初始化子模块和子实例；

  特定的进程结构：具体的流程结构使用特定的流程（通用API），通常也是定义在外设驱动头文件中；

```
  void (* TxHalfCpltCallback)(struct __UART_HandleTypeDef *huart);        /*!< UART Tx Half Complete Callback        */
  void (* TxCpltCallback)(struct __UART_HandleTypeDef *huart);            /*!< UART Tx Complete Callback             */
  void (* RxHalfCpltCallback)(struct __UART_HandleTypeDef *huart);        /*!< UART Rx Half Complete Callback        */
  void (* RxCpltCallback)(struct __UART_HandleTypeDef *huart);            /*!< UART Rx Complete Callback             */
  void (* ErrorCallback)(struct __UART_HandleTypeDef *huart);             /*!< UART Error Callback                   */
  void (* AbortCpltCallback)(struct __UART_HandleTypeDef *huart);         /*!< UART Abort Complete Callback          */
  void (* AbortTransmitCpltCallback)(struct __UART_HandleTypeDef *huart); /*!< UART Abort Transmit Complete Callback */
  void (* AbortReceiveCpltCallback)(struct __UART_HandleTypeDef *huart);  /*!< UART Abort Receive Complete Callback  */
  void (* WakeupCallback)(struct __UART_HandleTypeDef *huart);            /*!< UART Wakeup Callback                  */
  void (* MspInitCallback)(struct __UART_HandleTypeDef *huart);           /*!< UART Msp Init callback                */
  void (* MspDeInitCallback)(struct __UART_HandleTypeDef *huart);         /*!< UART Msp DeInit callback              */
```

# 4 HAL驱动规则

## 4.1 HAL API命名规则

HAL_API命名规则见下表。
HAL：Hardware Abstraction[æbˈstrækʃn] Layer，硬件抽象层


![img](./img/wKgP3GI-jTeASp49AAFZlEel3YE179.png)

其中PPP是外设模式，而不是指外设本身；
MODE指的是过程模式，是轮循、中断或DMA模式；
FEATURE指的是实现功能，如Start、Stop；

NA，Not Available，不可用。

示例如下：

```
HAL_StatusTypeDef HAL_TIM_PWM_Start(TIM_HandleTypeDef *htim, uint32_t Channel)
HAL_StatusTypeDef HAL_TIM_PWM_Start_IT(TIM_HandleTypeDef *htim, uint32_t Channel)
HAL_StatusTypeDef HAL_TIM_PWM_Start_DMA(TIM_HandleTypeDef *htim, uint32_t Channel, uint32_t *pData, uint16_t Length)
```

  以下外围设备其初始化不需要提供句柄handler和实例对象instance object；GPIO、SYSTICK、NVIC、RCC、FLASH处理中断和特定时钟配置的宏在每个外设/模块驱动头文件中定义:


![img](./img/wKgP3GI-jTeAdRBDAAGsgA7Nidg400.png)

- NVIC和SYSTICK是ARM Cortex的两个核心功能，与这些功能相关的API位于stm32f4xx_hal_cortex.c中；
- 从寄存器中读取状态位或标志时，它由位移值构成，且通常返回的宽度为32位；
- 在初始化HAL_PPP_Init() 的API中，Init函数在修改句柄字段之前会检查句柄PPP_HandleTypeDef内容是否为空；

```
HAL_PPP_Init(PPP_HandleTypeDef)
if(hppp == NULL)
{
	return HAL_ERROR;
}
```

宏定义分为两类：
宏定义可以帮助我们防止出错，提高代码的可移植性和可读性等。

- 条件宏定义

```
  #define ABS(x) (((x) > 0) ? (x) : -(x))
```

- 伪代码宏（多指令宏）

```
  #define __HAL_LINKDMA(__HANDLE__, __PPP_DMA_FIELD_, __DMA_HANDLE_) \
	do{ \
		(__HANDLE__)->__PPP_DMA_FIELD_ = &(__DMA_HANDLE_); \
		(__DMA_HANDLE_).Parent = (__HANDLE__); \
	} while(0)
```

## 4.2 HAL中断处理程序和回调函数

  除了API，HAL外设驱动还包含：

- HAL_PPP_IRQHandler()外设中断处理函数；
- 用户定义回调函数，系统默认的回调函数定义为weak属性，一旦用户- 自己定义了回调函数会覆盖系统默认的回调函数；

  有三种类型的回调函数：

- 外围系统初始化/去初始化回调：HAL_PPP_MspInit()、HAL_PPP_MspDeInit()；
- 处理完整进程的回调函数：HAL_PPP_ProcessCpltCallback；
- 错误处理回调函数：HAL_PPP_ErrorCallback；


![img](./img/wKgP3GI-jTeAJQ8oAAEBedX0SNs399.png)

# 5 API分类

## 5.1 HAL通用API

通用的API由四个方面组成：



- 初始化和去初始化：
    HAL_PPP_Init(), HAL_PPP_DeInit()
- IO操作来对外围设备进行有效的数据访问：
    HAL_PPP_Read(), HAL_PPP_Write(),HAL_PPP_Transmit(), HAL_PPP_Receive()
- 控制操作来动态更改外设配置和其他操作模式：
    HAL_PPP_Set (), HAL_PPP_Get ()
- 状态和错误处理来检索外围和数据流状态，并识别发生的错误：
    HAL_PPP_GetState (), HAL_PPP_GetError ()


![img](./img/wKgP3GI-jTeAAeY1AAQDo7vDK-E687.png)

## 5.2 HAL拓展API

  扩展API提供了特定的函数，或者为特定的应用程序覆盖修改过的API系列（系列）或同一系列中的特定型号。

  扩展模型包含一个附加文件stm32f4xx_hal_ppp_ex.c，其中包括给定部分的所有特定函数和define语句（stm32f4xx_hal_ppp_ex.h）。

下面是一个基于ADC外围设备的示例：



![img](./img/wKgP3GI-jTeAS10rAAGFMYi5Bjk744.png)

# 6 浅谈句柄、MSP函数、Callback函数

## 6.1 句柄

  在STM32的标准库中，假设我们要初始化一个外设（这里以USART为例），我们首先要初始化他们的各个寄存器。在标准库中，这些操作都是利用固件库结构体变量+固件库Init函数实现的：

```
USART_InitTypeDef USART_InitStructure;

USART_InitStructure.USART_BaudRate = bound;//串口波特率
USART_InitStructure.USART_WordLength = USART_WordLength_8b;//字长为8位数据格式
USART_InitStructure.USART_StopBits = USART_StopBits_1;//一个停止位
USART_InitStructure.USART_Parity = USART_Parity_No;//无奇偶校验位
USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//无硬件数据流控制
USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//收发模式

USART_Init(USART3, &USART_InitStructure); //初始化串口1
```

  可以看到，要初始化一个串口，需要对六个位置进行赋值，然后引用Init函数，并且USART_InitStructure并不是一个全局结构体变量，而是只在函数内部的局部变量，初始化完成之后，USART_InitStructure就失去了作用。
  而在HAL库中，同样是USART初始化结构体变量，我们要定义为全局变量。

```
UART_HandleTypeDef UART1_Handler;
```

右键查看结构体成员

```
typedef struct
{
	  USART_TypeDef                 *Instance;        /*!< UART registers base address        */
	  UART_InitTypeDef              Init;             /*!< UART communication parameters      */
	  uint8_t                       *pTxBuffPtr;      /*!< Pointer to UART Tx transfer Buffer */
	  uint16_t                      TxXferSize;       /*!< UART Tx Transfer size              */
	  uint16_t                      TxXferCount;      /*!< UART Tx Transfer Counter           */
	  uint8_t                       *pRxBuffPtr;      /*!< Pointer to UART Rx transfer Buffer */
	  uint16_t                      RxXferSize;       /*!< UART Rx Transfer size              */
	  uint16_t                      RxXferCount;      /*!< UART Rx Transfer Counter           */  
	  DMA_HandleTypeDef             *hdmatx;          /*!< UART Tx DMA Handle parameters      */ 
	  DMA_HandleTypeDef             *hdmarx;          /*!< UART Rx DMA Handle parameters      */
	  HAL_LockTypeDef               Lock;             /*!< Locking object                     */
	  __IO HAL_UART_StateTypeDef    State;            /*!< UART communication state           */
	  __IO uint32_t                 ErrorCode;        /*!< UART Error code                    */
}UART_HandleTypeDef;
```

  我们发现，与标准库不同的是，该成员不仅包含了之前标准库就有的六个成员（波特率，数据格式等），还包含过采样、（发送或接收的）数据缓存、数据指针、串口 DMA 相关的变量、各种标志位等等要在整个项目流程中都要设置的各个成员。


  该 `UART1_Handler` 就被称为串口的句柄它被贯穿整个USART收发的流程，比如开启中断：

```
HAL_UART_Receive_IT(&UART1_Handler, (u8 *)aRxBuffer, RXBUFFERSIZE);
```

比如后面要讲到的MSP与Callback回调函数：

```
void HAL_UART_MspInit(UART_HandleTypeDef *huart);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
```

  在这些函数中，只需要调用初始化时定义的句柄UART1_Handler就好。

## 6.2 MSP函数

  MCU Specific Package `[spəˈsɪfɪk ˈpækɪdʒ] `，为单片机的具体方案。

**MSP是指和MCU相关的初始化。**

  初始化一个串口，首先要设置和 MCU 无关的东西，例如波特率，奇偶校验，停止位等，这些参数设置和 MCU 没有任何关系，可以使用 STM32F1，也可以是 STM32F2/F3/F4/F7上的串口。而一个串口设备它需要一个 MCU 来承载，例如用 STM32F4 来做承载，PA9 做为发送，PA10 做为接收，MSP 就是要初始化 STM32F4 的 PA9,PA10，配置这两个引脚。所以 HAL驱动方式的初始化流程就是：HAL_USART_Init()—>HAL_USART_MspInit() ，先初始化与 MCU无关的串口协议，再初始化与 MCU 相关的串口引脚。在 STM32 的 HAL 驱动中HAL_PPP_MspInit()作为回调，被 HAL_PPP_Init()函数所调用。当我们需要移植程序到 STM32F1平台的时候，我们只需要修改 HAL_PPP_MspInit 函数内容而不需要修改 HAL_PPP_Init 入口参数内容。

  在HAL库中，几乎每初始化一个外设就需要设置该外设与单片机之间的联系，比如IO口，是否复用等等，可见，HAL库相对于标准库多了MSP函数之后，移植性非常强，但与此同时却增加了代码量和代码的嵌套层级。可以说各有利弊。

  同样，MSP函数又可以配合句柄，达到非常强的移植性：

```
void HAL_UART_MspInit(UART_HandleTypeDef *huart);
```

入口参数仅仅需要一个串口句柄，这样有能看出句柄的方便。

## 6.3 Callback函数

  类似于MSP函数，个人认为Callback函数主要帮助用户应用层的代码编写。
  还是以USART为例，在标准库中，串口中断了以后，我们要先在中断中判断是否是接收中断，然后读出数据，顺便清除中断标志位，然后再是对数据的处理，这样如果我们在一个中断函数中写这么多代码，就会显得很混乱：

```
//串口3中断服务程序
void USART3_IRQHandler(void)                	
{
	u8 Res;
	if(USART_GetITStatus(USART3, USART_IT_RXNE) != RESET)  
	{
		Res =USART_ReceiveData(USART3);	//读取接收到的数据
		/*数据处理区*/
	}   		 
} 
```

  而在HAL库中，进入串口中断后，直接由HAL库中断函数进行托管：

```
void USART1_IRQHandler(void)                	
{ 
	HAL_UART_IRQHandler(&UART1_Handler);	//调用HAL库中断处理公用函数
	/***************省略无关代码****************/	
}
```

  HAL_UART_IRQHandler这个函数完成了判断是哪个中断（接收？发送？或者其他？），然后读出数据，保存至缓存区，顺便清除中断标志位等等操作。

  比如提前设置了，串口每接收五个字节，就要对这五个字节进行处理。

  在开始定义了一个串口接收缓存区：

```
/*HAL库使用的串口接收缓冲,处理逻辑由HAL库控制，接收完这个数组就会调用HAL_UART_RxCpltCallback进行处理这个数组*/
/*RXBUFFERSIZE=5*/
u8 aRxBuffer[RXBUFFERSIZE];
```

  在初始化中，在句柄里设置好了缓存区的地址，缓存大小（五个字节）。

```
/*该代码在HAL_UART_Receive_IT函数中，初始化时会引用*/
huart->pRxBuffPtr = pData;//aRxBuffer
huart->RxXferSize = Size;//RXBUFFERSIZE
huart->RxXferCount = Size;//RXBUFFERSIZE
```



  则在接收数据中，每接收完五个字节，HAL_UART_IRQHandler才会执行一次Callback函数：

```
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);
```



  在这个Callback回调函数中，我们只需要对这接收到的五个字节（保存在aRxBuffer[]中）进行处理就好了，完全不用再去手动清除标志位等操作。所以说Callback函数是一个应用层代码的函数，我们在一开始只设置句柄里面的各个参数，然后就等着HAL库把自己安排好的代码送到手中就可以了。

  综上，就是HAL库的三个与标准库不同的地方。

  从这三个小点就可以看出HAL库的可移植性之强大，并且用户可以完全不去理会底层各个寄存器的操作，代码也更有逻辑性。但与此带来的是复杂的代码量，极慢的编译速度，略微低下的效率。