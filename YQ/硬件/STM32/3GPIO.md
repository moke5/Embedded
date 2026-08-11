# 1 概述

  GPIO,即通用I/O(输入/输出)端口，是STM32可控制的引脚。STM32芯片的GPIO引脚与外部设备连接起来，可实现与外部通讯、控制外部硬件或者采集外部硬件数据的功能。

GPIO的复用：


![img](./img/rBJlJmJidzyAB24_AAAfLYFwhr8831.png)

  STM32F4 有很多的内置外设，这些外设的外部引脚都是与 GPIO 共用的。也就是说，一个引脚可以有很多作用，但是默认为IO口，如果想使用一个 GPIO内置外设的功能引脚，就需要GPIO的复用。比如说串口就是GPIO复用为串口。

# 2 GPIO的工作模式

## 2.1 简述

### 4种输入模式

- 浮空输入（即不连接内部上下拉电阻）
- 上拉输入
- 下拉输入
- 模拟输入

### 4种输出模式

- 开漏输出（带上拉或者下拉）
- 复用开漏输出（带上拉或者下拉）
- 推挽输出（带上拉或者下拉）
- 复用推挽输出（带上拉或者下拉）

### 4种最大输出速度

- 低速，2MHz
- 中速，25MHz
- 高速，50MHz
- 超高速，100MHz

**速度的配置，就是决定IO口驱动电路的响应速度**

我们需要结合实际情况配置速度，不同速度会有不同的影响。

功耗与干扰：

- 配置高速：输出频率高，噪音大，功耗高，电磁干扰强；
- 配置低速：输出频率低，噪音小，功耗低，电磁干扰弱；提高系统EMI（电磁干扰）性能；

  实际情况中，比如：低功耗的产品，你会考虑功耗。环境不好的场合，通信不稳定，你会考虑电磁干扰（电磁干扰（Electromagnetic Interference，EMI）是干扰电缆信号并降低信号完好性的电子噪音）等。

速度配置实例：

  (1) 对于串口来说，加入最大波特率为115200bps，这样只需要用2MHz的GPIO的引脚速度就可以了，省电噪音又小；


  (2) 对于I2C接口，假如使用400KHz波特率，若想把余量留大一些，2MHz的GPIO引脚速度或许是不够，这时可以选用10MHz的GPIO引脚速度；


  (3) 对于SPI接口，假如使用18MHz或9MHz的波特率，用10MHz的GPIO口也不够用了，需要选择呢50MHz的GPIO引脚速度;


  (4) GPIO口设置为输入时，输出驱动电路与端口是断开的，所以这时配置输出速度是无意义的。

## 2.2 详细分析

### 1、输出配置

  当某引脚配置为输出模式时，内部结构如下图。


![img](./img/rBJlJmJidzyABg8qAAGi5YAujro513.png)

对 I/O 端口进行编程作为输出时，内部电路关键工作如下：

- 输出缓冲器被打开：
    - 开漏模式：输出寄存器中的“0”可激活 N-MOS，而输出寄存器中的“1”会使端口保持高阻态 (Hi-Z)（P-MOS 始终不激活）。
    - 推挽模式：输出寄存器中的“0”可激活 N-MOS，而输出寄存器中的“1”可激活P-MOS。
- 施密特触发器输入被打开。
- 根据 GPIOx_PUPDR 寄存器中的值决定是否打开弱上拉电阻和下拉电阻对输出数据寄存器的读访问可获取最后的写入值。

*说明：*

高阻态（英语：High impedance）表示电路中的某个节点具有相对电路中其他点相对更高的阻抗。通俗的讲，可以看作输出（输入）电阻非常大。它的极限状态可以认为悬空（开路）。也就是说理论上高阻态不是悬空，它是对地或对电源电阻极大的状态。

施密特触发器（英语：Schmitt trigger）是包含正反馈的比较器电路。

- 当输入电压高于正向阈值电压，输出为高；
- 当输入电压低于负向阈值电压，输出为低；
- 当输入在正负向阈值电压之间，输出不改变，也就是说输出由高电准位翻转为低电准位，或是由低电准位翻转为高电准位时所对应的阈值电压是不同的。只有当输入电压发生足够的变化时，输出才会变化，因此将这种元件命名为触发器。
    施密特触发器可作为波形整形电路，能将模拟信号波形整形为数字电路能够处理的方波波形。

保护二极管：引脚内部加上这两个保护二极管可以防止引脚外部过高或过低的电压输入。

保护二极管功能的实现原理：当引脚电压高于VDD时，上方的二极管导通吸收这个电压，当引脚电压低于VSS时，下方的二极管导通，防止不正常电压引入芯片导致芯片烧毁

**推挽电路**

  推挽电路（push-pull）就是两个不同极性晶体管间连接的输出电路。推挽电路采用两个参数相同的功率BJT管（双极结型晶体管（Bipolar Junction Transistor—BJT）常见的NPN或PNP三极管）或MOSFET管（场效应管），以推挽方式存在于电路中，各负责正负半周的波形放大任务，电路工作时，两只对称的功率开关管每次只有一个导通，所以导通损耗小效率高。推挽输出既可以向负载灌电流，也可以从负载抽取电流。

  在电路设计中，推挽输出是一种很常用的输出模式。推挽输出有很多优点，比如更低的损耗，更安全的输出等。推挽”之意，即为当一个管子推出去时，另一个管子拉回来。输入不同，交替导通。

举个例子

- 当输入信号为高电平的时候，上面的管子导通，下面的管子截止，输出信号为高电平。
- 当输入信号为低电平的时候，上面的管子截止，下面的管子导通，输出信号为低电平。

### 2、输入配置

  当某引脚配置为输入模式时，内部结构如下图。


![img](./img/rBJlJmJidzyAbnYbAAFWBuWa0TE929.png)

对 I/O 端口进行编程作为输入模式时，内部电路关键工作如下：

- 输出缓冲器被关闭
- 施密特触发器输入被打开
- 根据 GPIOx_PUPDR 寄存器中的值决定是否打开上拉和下拉电阻
- 输入数据寄存器每隔 1 个 AHB1 时钟周期对 I/O 引脚上的数据进行一次采样
- 对输入数据寄存器的读访问可获取 I/O 状态

**施密特触发器**

  在电子学中，施密特触发器（英语：Schmitt trigger）是包含正反馈的比较器电路。

  对于标准施密特触发器，当输入电压高于正向阈值电压，输出为高；当输入电压低于负向阈值电压，输出为低；当输入在正负向阈值电压之间，输出不改变，也就是说输出由高电准位翻转为低电准位，或是由低电准位翻转为高电准位时所对应的阈值电压是不同的。只有当输入电压发生足够的变化时，输出才会变化，因此将这种元件命名为触发器。

  施密特触发器可作为波形整形电路，能将模拟信号波形整形为数字电路能够处理的方波波形，而且由于施密特触发器具有滞回特性，所以可用于抗干扰，其应用包括在开回路配置中用于抗扰，以及在闭回路正回授/负回授配置中用于实现多谐振荡器。

### 3、复用功能配置

  当某引脚配置为复用功能模式时，内部结构如下图。


![img](./img/rBJlJmJidzyAEAnXAAFmBGwR0X0904.png)

对 I/O 端口进行编程作为复用功能时：

- 可将输出缓冲器配置为开漏或推挽
- 输出缓冲器由来自外设的信号驱动（发送器使能和数据）
- 施密特触发器输入被打开
- 根据 GPIOx_PUPDR 寄存器中的值决定是否打开弱上拉电阻和下拉电阻
- 输入数据寄存器每隔 1 个 AHB1 时钟周期对 I/O 引脚上的数据进行一次采样
- 对输入数据寄存器的读访问可获取 I/O 状态

### 4、模拟配置

  当某引脚配置为模拟配置模式时，内部结构如下图。


![img](./img/rBJlJmJidzyAE5hJAAEDDZ_9yvY180.png)

对 I/O 端口进行编程作为模拟配置时：

- 输出缓冲器被禁止。
- 施密特触发器输入停用，I/O 引脚的每个模拟输入的功耗变为零。施密特触发器的输出被强制处理为恒定值 (0)。
- 弱上拉和下拉电阻被关闭。
- 对输入数据寄存器的读访问值为“0”。
- 在模拟配置中，I/O 引脚不能为 5 V 容忍。

# 3 原理图

**1、LED硬件设计**


![img](./img/rBJlJmJidzyAXriBAABWrRT2zBQ493.png)

![img](./img/rBJlJmJidzyAf97pAACEIQwTQko885.png)

**2、按键硬件设计**


![img](./img/rBJlJmJidzyAeljSAABnUEq_peI220.png)
![img](./img/rBJlJmJidzyACRtbAAEdtRqN-Q4918.png)

# 4 寄存器编程

实现步骤

- 使能端口H硬件时钟，可以理解为启动了汽车发动机，汽车才有动力控制行走方向；
- 设置PH10引脚为输出模式，可以理解为汽车为前进模式；
- 设置PH10引脚电平状态
    - 高电平，可以理解为汽车前进
    - 低电平，可以理解为汽车停止

## 4.1 寄存器边界地址


![img](./img/rBJlJmJidzyAYlvOAAE6yGX9iAA924.png)

## 4.2 寄存器描述

**1、RCC AHB1 外设时钟使能寄存器 (RCC_AHB1ENR)**

*RCC AHB1 peripheral clock enable register*

偏移地址：0x30

复位值：0x0010 0000

访问：无等待周期，按字、半字和字节访问。


![img](./img/rBJlJmJidzyAG9hqAACH2z32jgo983.png)

**2、GPIO 端口模式寄存器 (GPIOx_MODER) (x = A…I)**

*GPIO port mode register*

偏移地址：0x00

复位值：

- 0xA800 0000（端口 A）
- 0x0000 0280（端口 B）
- 0x0000 0000（其它端口）


![img](./img/rBJlJmJidzyAEbHZAABk-pvWaQg743.png)

**3、GPIO 端口输出类型寄存器 (GPIOx_OTYPER) (x = A…I)**

*GPIO port output type register*

偏移地址：0x04

复位值：0x0000 0000


![img](./img/rBJlJmJidzyAbparAABDxSWNqV4505.png)

**4、GPIO 端口输出速度寄存器 (GPIOx_OSPEEDR) (x = A…I/)**

*GPIO port output speed register*

偏移地址：0x08

复位值：

- 0x0000 00C0（端口 B）
- 0x0000 0000（其它端口）


![img](./img/rBJlJmJidzyAJmTlAABeSgiTqZ8015.png)

**5、GPIO 端口上拉/下拉寄存器 (GPIOx_PUPDR) (x = A…I/)**

*GPIO port pull-up/pull-down register*

偏移地址：0x0C

复位值：

- 0x6400 0000（端口 A）
- 0x0000 0100（端口 B）
- 0x0000 0000（其它端口）


![img](./img/rBJlJmJidzyAaUCLAABdzf3nwHM514.png)

**6、GPIO 端口输出数据寄存器 (GPIOx_ODR) (x = A…I)**

*GPIO port output data register*

偏移地址：0x14

复位值：0x0000 0000


![img](./img/rBJlJmJidzyAbGILAABDvWHpFrA988.png)

**7、GPIO 端口输入数据寄存器 (GPIOx_IDR) (x = A…I)**

*GPIO port input data register*

偏移地址：0x10

复位值：0x0000 XXXX（其中 X 表示未定义）


![img](./img/rBJlJmJidzyASFGkAABEFdcas38744.png)

**8、GPIO 端口置位/复位寄存器 (GPIOx_BSRR) (x = A…I)**

*GPIO port bit set/reset register*

偏移地址：0x18

复位值：0x0000 0000


![img](./img/rBJlJmJidzyAfetiAAGptnq-Fbw649.png)

## 4.3 参考代码

```
#include "stm32f4xx.h"

#define RCC_AHB1ENR	        (*(volatile uint32_t *)(0x40023800+0x30))
#define GPIOH_MODER	        (*(volatile uint32_t *)(0x40020000+0x00))
#define GPIOH_BSRR		    (*(volatile uint32_t *)(0x40020000+0x18))

void led_init(void)
{
	RCC_AHB1ENR|=1<<7;
	GPIOH_MODER|=1<<20;
}

void led_off(void)
{
	GPIOH_BSRR=1<<10;
}

void led_on(void)
{
	GPIOH_BSRR=1<<(10+16);
}

void delay(void)
{
	uint32_t i=0x200000;
	while(i--);
}

int main(void)
{
	led_init();
	while (1)
	{
		led_on();
		delay();
	
		led_off();
		delay();	  
	}
}
```







## 4.4 演示

  当上述程序成功烧录到粤嵌STM32F429开发板后，则看到D3灯持续闪烁，演示效果如下。


![img](./img/rBJlJmJidzyAOlo3AAJ3lE2IdJU055.gif)

# 「课堂练习1」

  利用寄存器编程，实现D4灯闪烁。

# 5 函数接口及使用

## 5.1 函数接口说明

### 1、端口时钟使能

  当芯片复位后，端口硬件时钟是默认关闭状态，需要调用__HAL_RCC_GPIOx_CLK_ENABLE函数来打开，例如打开端口A、端口B、端口C硬件时钟示例代码如下：

```
端口A硬件时钟使能
__HAL_RCC_GPIOA_CLK_ENABLE()

端口B硬件时钟使能
__HAL_RCC_GPIOB_CLK_ENABLE()

端口C硬件时钟使能
__HAL_RCC_GPIOC_CLK_ENABLE()
```







### 2、 引脚配置

```
void HAL_GPIO_Init(GPIO_TypeDef  *GPIOx, GPIO_InitTypeDef *GPIO_Init)
```







参数：

- GPIOx,指定哪个端口，x为端口号。如当前为端口A，则写GPIOA；当前为端口B，则写GPIOB。
- GPIO_Init，GPIO的配置。

返回值：无。

示例1：将GPIOH10配置为输出模式，引脚内部接上拉电阻。

```
GPIO_InitTypeDef GPIO_Initure;

GPIO_Initure.Pin=GPIO_PIN_10; 		    //第10根引脚
GPIO_Initure.Mode=GPIO_MODE_OUTPUT_PP;	//推挽输出
GPIO_Initure.Pull=GPIO_PULLUP;		    //上拉电阻
GPIO_Initure.Speed=GPIO_SPEED_HIGH;	    //高速
HAL_GPIO_Init(GPIOH,&GPIO_Initure);	    //初始化端口H
```







示例2：将GPIOA0配置为输入模式，引脚内部接上拉电阻。

```
GPIO_InitTypeDef GPIO_Initure;
 
GPIO_Initure.Pin=GPIO_PIN_0;              //第0根引脚
GPIO_Initure.Mode= GPIO_MODE_INPUT;       //输入模式
GPIO_Initure.Pull=GPIO_PULLUP;		      //上拉电阻
GPIO_Initure.Speed=GPIO_SPEED_HIGH;       //高速
HAL_GPIO_Init(GPIOA,&GPIO_Initure);       //初始化端口A
```







### 3、 引脚电平输出

```
void HAL_GPIO_WritePin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)
```







参数：

- GPIOx,指定哪个端口，x为端口号。例如当前为端口A，则写GPIOA；当前为端口B，则写GPIOB。
- GPIO_Pin，指定哪个引脚。例如引脚为第9根引脚，则写GPIO_Pin_9。
    PinState，引脚电平状态。高电平为GPIO_PIN_SET，低电平为GPIO_PIN_RESET。

返回值：无。

示例1：将GPIOF9配置为输出高电平。

```
HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,GPIO_PIN_SET);
```







示例2：将GPIOF9配置为输出低电平。

```
HAL_GPIO_WritePin(GPIOH,GPIO_PIN_10,GPIO_PIN_RESET);
```







### 4、引脚电平反转

```
void HAL_GPIO_TogglePin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin)
```







参数：

- GPIOx,指定哪个端口，x为端口号。例如当前为端口A，则写GPIOA；当前为端口B，则写GPIOB。
- GPIO_Pin，指定哪个引脚。例如引脚为第9根引脚，则写GPIO_Pin_9。

返回值：无。

示例1：将GPIOH10配置为输出电平反转。

```
HAL_GPIO_TogglePin (GPIOH,GPIO_PIN_10);
```







### 5、读取引脚电平

```
GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef* GPIOx, uint16_t GPIO_Pin)
```







参数：

- GPIOx,指定哪个端口，x为端口号。例如当前为端口A，则写GPIOA；当前为端口B，则写GPIOB。
- GPIO_Pin，指定哪个引脚。例如引脚为第9根引脚，则写GPIO_Pin_9。

返回值：引脚电平状态。

- 高电平，GPIO_PIN_SET；
- 低电平，GPIO_PIN_RESET。

## 5.2 使用

### 1、参考代码

**gpio.c**

```
void MX_GPIO_Init(void)
{
	GPIO_InitTypeDef GPIO_InitStruct = {0};

	__HAL_RCC_GPIOH_CLK_ENABLE();


	HAL_GPIO_WritePin(GPIOH, GPIO_PIN_10, GPIO_PIN_SET);

	GPIO_InitStruct.Pin = GPIO_PIN_10;
	GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
	GPIO_InitStruct.Pull = GPIO_NOPULL;
	GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
	HAL_GPIO_Init(GPIOH, &GPIO_InitStruct);
}
```







**main.c**

```
int main(void)
{
	HAL_Init();
	SystemClock_Config();
	MX_GPIO_Init();

	while (1)
	{

		HAL_GPIO_TogglePin(GPIOH, GPIO_PIN_10);
		HAL_Delay(500);	 
	}
}
```







### 2、演示

  当上述程序成功烧录到粤嵌STM32F429开发板后，则看到D3灯持续闪烁，演示效果如下。

![img](./img/rBJlJmJidzyAOlo3AAJ3lE2IdJU055.gif)

# 「课堂练习2」

  利用HAL库编程，实现D4灯闪烁。

# 6 STM32CubeMX

## 6.1 配置引脚为输出模式

1.选中PH10引脚。


![img](./img/rBJlJmJidzyAZ4G7AAAgj-j3P68056.gif)

2.配置PH10引脚为输出模式。


![img](./img/rBJlJmJidzyAB24_AAAfLYFwhr8831.png)

3.再次详细配置PH10引脚。


![img](./img/rBJlJmJidzyAGzQ5AABLEiGV7Fs665.png)

4.导出代码。


![img](./img/rBJlJmJidzyAb3yOAAAFZWAIeSI210.png)

## 6.2 配置引脚为输入模式

1.选中PA0引脚。


![img](./img/rBJlJmJidzyAM597AAAvtDoyfbI712.gif)

2.配置PA0为输入模式。


![img](./img/rBJlJmJidzyAB24_AAAfLYFwhr8831.png)

3.再次详细配置PA0引脚。


![img](./img/rBJlJmJidzyABbcOAAATGRfOrt4371.png)

4.导出代码。


![img](./img/rBJlJmJidzyAb3yOAAAFZWAIeSI210.png)

# 「课堂练习3」

  基于STM32CubeMX代码向导软件，为D3、D4、D5灯连接到的引脚配置为输出推挽模式，为K2、K3按键连接到的引脚配置为输入浮空模式。

# 7 应用领域

1.常见密码锁，矩阵键盘。


![img](./img/rBJlJmJidzyAL9DBAFbCwiEecUs172.gif)

2.数显时间继电器