# IIC

[toc]

## IIC

### 1 I2C

#### 1.1 概述

  I2C(IIC,Inter－Integrated Circuit，集成电路总线）总线是由Philips公司开发的一种简单、双向二线制**同步串行总线**。它只需要两根线即可在连接于总线上的器件之间传送信息。

  主器件用于启动总线传送数据，并产生时钟以开放传送的器件，此时任何被寻址的器件均被认为是从器件。


![img](./img/rBJlJmJ8ytCAPL9VAAISbkkMWUE31.jpeg)

#### 1.2 I2C总线特点

I2C总线特点可以概括如下：

(1)在硬件上，I2C总线只需要一根数据线和一根时钟线两根线，总线接口已经集成在芯片内部，不需要特殊的接口电路，而且片上接口电路的滤波器可以滤去总线数据上的毛刺。因此，I2C总线**简化**了硬件电路PCB布线，**降低**了系统成本，提高了系统可靠性。因为I2C芯片（如mpu6050、ft5x06、gslx680等）除了这两根线和少量中断线，与系统再没有连接的线，用户常用IC可以很容易形成标准化和模块化，便于重复利用。

(2)I2C总线是一个真正的多主机总线，如果两个或多个主机同时初始化数据传输，可以通过冲突检测和仲裁防止数据破坏，每个连接到总线上的器件都有唯一的地址，任何器件既可以作为主机也可以作为从机，但同一时刻只允许有一个主机。数据传输和地址设定由软件设定，非常灵活。总线上的器件增加和删除不影响其他器件正常工作。

(3)I2C总线可以通过外部连线进行在线检测，便于系统故障诊断和调试，故障可以立即被寻址，软件也利于标准化和模块化，缩短开发时间。

(4)连接到相同总线上的IC数量只受总线最大电容的限制，串行的8位双向数据传输位速率在标准模式下可达100Kbit/s，快速模式下可达400Kbit/s，高速模式下可达3.4Mbit/s。

总线具有极低的电流消耗．抗高噪声干扰，增加总线驱动器可以使总线电容扩大10倍，传输距离达到15m；兼容不同电压等级的器件，工作温度范围宽。

![img](./img/56428.png)

(5)总线具有极低的电流消耗．抗高噪声干扰，增加总线驱动器可以使总线电容扩大10倍，传输距离达到15m；兼容不同电压等级的器件，工作温度范围宽。



**信号概念**

I2C通信，存在几种信号

1）起始信号（起始条件）：通知从机做好通信的准备。

2）应答信号：有应答（ACK）和无应答（NACK）。有应答是SDA为低电平，无应答是SDA为高电平。

3）停止信号（停止条件）：告诉从机通信已经结束。



#### 1.3 I2C总线协议

**1、起始和停止条件**

  I2C协议规定，总线上数据的传输必须以一个起始信号作为开始条件，以一个结束信号作为传输的停止条件。起始和结束信号总是由主设备产生。

  起始和结束信号产生条件：总线在空闲状态时，SCL和SDA都保持着高电平，当SCL为高电平而SDA由高到低的跳变，表示产生一个起始条件；当SCL为高而SDA由低到高的跳变，表示产生一个停止条件。

  在起始条件产生后，总线处于忙状态，由本次数据传输的主从设备独占，其他I2C器件无法访问总线；而在停止条件产生后，本次数据传输的主从设备将释放总线，总线再次处于空闲状态。


![img](./img/rBJlJmJ8ytCAQ0uBAABspLm9gTI122.png)

**2、响应应答和非响应应答**

1）响应应答信号

  主设备在SCL线上产生每个时钟脉冲的过程中将在SDA线上传输一个数据位，当一个字节按数据位从高位到低位的顺序传输完后，紧接着从设备将拉低SDA线，回传给主设备一个应答位，此时才认为一个字节真正的被传输完成。当然，并不是所有的字节传输都必须有一个应答位，比如当从设备不能再接收主设备发送的数据时，从设备将回传一个非响应应答位。


![img](./img/rBJlJmJ8ytCAJ75jAAH2DPh6Scs089.png)

2）非响应应答信号


![img](./img/rBJlJmJ8ytCAYqaRAAGmugElVsQ642.png)

**3、地址**

  I2C总线上的每一个设备都对应一个唯一的地址，主从设备之间的数据传输是建立在地址的基础上，也就是说，主设备在传输有效数据之前要先指定从设备的地址，地址指定的过程和上面数据传输的过程一样，只不过大多数从设备的地址是7位的，然后协议规定再给地址添加一个最低位用来表示接下来数据传输的方向，0表示主设备向从设备写数据，1表示主设备向从设备读数据。


![img](./img/rBJlJmJ8ytCAZa44AADDt7QiHJA662.png)

#### 1.4 I2C总线操作

1、特征

I2C总线的操作实际就是主从设备之间的读写操作。大致可分为以下三种操作情况：

- 主设备往从设备中写数据。
- 主设备在从设备中读数据。
- 主设备往从设备中写数据，然后重启起始条件，紧接着在从设备中读取数据；或者是主设备在从设备中读数据，然后重启起始条件，紧接着主设备往从设备中写数据。

**主设备往从设备中写入数据**


![img](./img/rBJlJmJ8ytCAQD2lAAEtGu776vk124.png)

**主设备从从设备中读取数据**


![img](./img/rBJlJmJ8ytCAPnMXAABthM8iZ6Y194.png)

**重启起始条件**


![img](./img/rBJlJmJ8ytCANT7cAADVWAX6Hw0834.png)

**一次完整的数据传输**



![img](./img/rBJlJmJ8ytCATlIqAAIATS-t36w809.png)

**数据有效性**


![img](./img/rBJlJmJ8ytCAM9KeAABxlDfbDr8932.png)

#### 1.5 I2C总线时钟同步与仲裁

**1、概述**

  如果两个master都想在同一条空闲总线上传输，此时必须能够使用某种机制来选择将总线控制权交给哪个master，这是通过时钟同步和仲裁来完成的，而被迫让出控制权的master则需要等待总线空闲后再继续传输。在单一master的系统上无需实现时钟同步和仲裁。

**2、时钟同步（Clock synchronization ）**

  时钟同步是通过I2C总线上的SCL之间的线“与”（wired-AND）来完成的，即如果有多个主机同时产生时钟，那么只有所有master都发送高电平时，SCL上才表现为高电平，否则SCL都表现为低电平。


![img](./img/rBJlJmJ8ytCAFBsiAACr4HYlixQ963.png)

**3、总线仲裁**

  总线仲裁和时钟同步类似，当所有主机在SDA上都写1时，SDA的数据才是1，只要有一个主机写0，那此时SDA上的数据就是0。

  一个主机每发送一个bit数据，在SCL处于高电平时，就检查看SDA的电平是否和发送的数据一致，如果不一致，这个主机便知道自己输掉仲裁，然后停止向SDA写数据。也就是说，如果主机一直检查到总线上数据和自己发送的数据一致，则继续传输，这样在仲裁过程中就保证了赢得仲裁的master不会丢失数据。

  输掉仲裁的主机在检测到自己输了之后也不再产生时钟脉冲，并且要在总线空闲时才能重新传输。

  仲裁的过程可能要经过多个bit的发送和检查，实际上两个主机如果发送的时序和数据完全一样，则两个主机都能正常完成整个的数据传输。


![img](./img/rBJlJmJ8ytCAErADAADnzxF4V0Y829.png)

**I2C总线清零**

  SCL：一般情况下SCL不会卡在低电平，出现这种情况的话，如果设备包含硬件复位引脚，推荐使用硬件复位。如果设备没有硬件复位引脚，可以通过重新上电方式触发设备内部上电复位电路。

  SDA：如果SDA卡在低电平，主机应发送9个时钟脉冲，那些将SDA拉低的设备在这9个时钟周期内应释放总线。如果没有的话，则需要通过硬件复位或重新上电的方式清除拥堵。



### **硬件I2C**

> 软件IIC：使用GPIO+延时，模拟通信协议的时序，可以使用任意的GPIO引脚实现IIC通信
>
> 硬件IIC：使用芯片自带IIC时序生成寄存器（硬件电路）生成时序，GPIO引脚固定(复用功能)，通信速率比软件更快，时序生成更简单

STM32F103的I2C（Inter-Integrated Circuit）模块是一种灵活的双线串行通信接口，支持多主机/从机模式、标准模式（100 kHz）、快速模式（400 kHz）及高速模式（3.4 MHz）。以下是其核心特性、功能配置及实际应用的详细解析

**4.1 I2C 硬件结构**

**1. 主要特性**

- **协议支持**：

- 兼容 **I2C 总线规范 2.1 版本**。

- 支持 **7位和10位设备地址**。

- 支持 **多主机（Multi-Master）** 和 **仲裁（Arbitration）**。

- **通信速率**：

- **标准模式**（Sm）：100 kHz。

- **快速模式**（Fm）：400 kHz。

- **高速模式**（Fm+）：最高 3.4 MHz（需主设备支持）。

- **功能模式**：

- **主模式（Master）**、从模式（Slave）。

- 支持 **DMA 传输**。

- 支持 **中断/事件触发**。

 

**4.2 I2C 工作模式**

**1. 主模式（Master Mode），常用**

- **功能**：

- 发起通信，控制SCL时钟。

- 支持单次传输或连续传输（带重复起始条件）。

- **典型流程**：

a.发送 **起始条件（START）**。

b.发送 **从设备地址 + R/W位**。

c.发送/接收数据字节。

d.发送 **停止条件（STOP）**。

 

![img](./img/56435.png)

 

![img](./img/56436.png)

 

**2. 从模式（Slave Mode）**

- **功能**：

- 监听总线，响应主机地址。

- 支持双地址（OAR1和OAR2）。

- **典型流程**：

a.配置自身地址（7位或10位）。

b.等待主机发起通信。

c.接收地址匹配后发送ACK，进入数据传输。

**3. 通信失败常见原因**

- **硬件问题**：

- SCL/SDA线未正确上拉（需外部4.7kΩ上拉电阻）。

- 总线短路或接触不良。

- **软件问题**：

- 未启用I2C或GPIO时钟。

- 时序配置错误（如ClockSpeed与实际设备不兼容）。

- 未正确处理事件标志（如未清除ADDR标志）。



### 2 AT24C02


![img](./img/rBJlJmJ8ytCAGyKMAAPQInqX4Bg352.png)

  AT24C02是一个2K位串行CMOS EEPROM， 内部含有256个8位字节。AT24C02有一个8字节页写缓冲器。该器件通过I2C总线接口进行操作，有一个专门的写保护功能。

#### 2.1 概述

- Standard-voltage Operation
- 2.7 (VCC = 2.7V to 5.5V)
- Automotive Temperature Range –40°C to 125°C
- Internally Organized 128 x 8 (1K), 256 x 8 (2K), 512 x 8 (4K),
    1024 x 8 (8K) or 2048 x 8 (16K)
- Two-wire Serial Interface
- Schmitt Trigger, Filtered Inputs for Noise Suppression
- Bidirectional Data Transfer Protocol
- 400 kHz Compatibility
- Write Protect Pin for Hardware Data Protection
- 8-byte Page (1K, 2K), 16-byte Page (4K, 8K, 16K) Write Modes
- Partial Page Writes are Allowed
- Self-timed Write Cycle (5 ms max)
- High-reliability
- Endurance: 1 Million Write Cycles
- Data Retention: 100 Years
- 8-lead JEDEC SOIC and 8-lead TSSOP Packages

#### 2.2 引脚功能


![img](./img/rBJlJmJ8ytCAQ6CTAAEfC2lNBWo920.png)

#### 2.3 设备地址


![img](./img/rBJlJmJ8ytCAHqREAADJllBVVuk679.png)

#### 2.4 页编程


![img](./img/rBJlJmJ8ytCABkNFAABipfjVefY820.png)

#### 2.5 连续读


![img](./img/rBJlJmJ8ytCAS6NUAADpGWQYv6I179.png)

### 3 STM32CubeMX

（1）PB6与PB7引脚复用I2C1_SCL与I2C1_SDA。



![img](./img/rBJlJmJ8ytCAIbhAAAANCHRgb0E183.png)

（2）I2C1详细参数配置。


![img](./img/rBJlJmJ8ytCAGuuNAABr-2Fnxmk722.png)

### 4 实例-读写数据

1. I2C1实例初始化

```C
I2C_HandleTypeDef hi2c1;

void MX_I2C1_Init(void)
{
  hi2c1.Instance = I2C1;//I2C1实例
  hi2c1.Init.ClockSpeed = 100000;//时钟线频率为100KHz
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;//在快速模式(400KHz))下，占空比为： t_Low/t_High = 2，这个需要根据连接的从设备可以查询到tLow与tHigh
  hi2c1.Init.OwnAddress1 = 0;//只在从机模式下生效，自有地址1-7位寻址模式
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;//7位从地址
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;//关闭双地址模式
  hi2c1.Init.OwnAddress2 = 0;//只在从机模式下生效，自有地址1-7位寻址模式
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;//禁止广播呼叫。不对地址0（通用的广播地址）应答。
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;//只在从机模式下生效，禁止时钟延长。
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)  {
    Error_Handler();
  }
  /** Configure Analogue filter 
  */
  //可编程噪声滤波器仅适用于 STM32F42xxx 和 STM32F43xxx 器件。在快速模式下， I2C 标准要求将 SDA 和 SCL 线上尖峰脉宽在 50 ns 以内的噪声都抑止掉。
  
  
  //模拟滤波器使能
  if (HAL_I2CEx_ConfigAnalogFilter(&hi2c1, I2C_ANALOGFILTER_ENABLE) != HAL_OK)  {
    Error_Handler();
  }

  //如果模拟滤波器也已使能，则需将数字滤波器添加到模拟滤波器中。数字滤波器可抑制脉宽达 DNF[3:0] *TPCLK1 以下的尖峰。
  if (HAL_I2CEx_ConfigDigitalFilter(&hi2c1, 0) != HAL_OK)  {
    Error_Handler();
  }
}
```



1. I2C低级硬件初始化

```C
void HAL_I2C_MspInit(I2C_HandleTypeDef* i2cHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  if(i2cHandle->Instance==I2C1)  {
    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**I2C1 GPIO Configuration    
    PB6     ------> I2C1_SCL
    PB7     ------> I2C1_SDA 
    */
    GPIO_InitStruct.Pin = GPIO_PIN_6|GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF4_I2C1;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    __HAL_RCC_I2C1_CLK_ENABLE();
 
  }
}
```



1. 主程序

```C
int main(void)
{
	uint32_t i=0;
	uint8_t buf_wr[8]={1,2,3,4,5,6,7,8};
	uint8_t buf_rd[8]={0};	

	HAL_Init();

	SystemClock_Config();
	MX_GPIO_Init();
	MX_I2C1_Init();
	MX_USART1_UART_Init();

	printf("This is eeprom test\r\n");

	if(HAL_I2C_Mem_Write(&hi2c1, 0xA0, 0, I2C_MEMADD_SIZE_8BIT,buf_wr,8,1000) == HAL_OK) {
		printf("HAL_I2C_Mem_Write success \r\n");
	} else {
		printf("HAL_I2C_Mem_Write fail \r\n");
	}

	printf("HAL_I2C_Mem_Read data is:");
	
	HAL_I2C_Mem_Read(&hi2c1, 0xA1, 0, I2C_MEMADD_SIZE_8BIT,buf_rd,8,1000);

	for(i=0; i<8; i++) printf("%02X ",buf_rd[i]);
	
	printf("\r\n");

	while (1)
	{
	}
}
```



1. 演示


![img](./img/rBJlJmJ8ytCAL4zHAAAh8gIPSTU713.png)

### 4 应用领域

1. 触摸屏


![img](./img/rBJlJmJ8ytCARkB2AAjoJU4_fA493.jpeg)

1. 无人机


![img](./img/rBJlJmJ8ytCAcoImAAY58cZqguY77.jpeg)

重要器件：加速度/角速度/陀螺仪传感器、气压传感器、摄像头。

1. 智能手表与手环


![img](./img/rBJlJmJ8ytCAYO2hAAOpLPF6oUY94.jpeg)

重要器件：加速度/角速度/陀螺仪传感器


![img](./img/rBJlJmJ8ytCATjl6AAJEXAKy2eA55.jpeg)

重要器件：心率传感器



## OLED屏代码移植

### **一、OLED屏**

OLED屏使用到SSD1306驱动器，它是一款带控制器的用于OLED点阵图形显示系统的单片CMOS OLED/PLED驱动器。

SSD1306内置对比度控制器、显示RAM（GDDRAM）和振荡器，以此减少了外部元件的数量和功耗。该芯片有256级亮度控制。数据或命令由通用微控制器通过硬件选择的6800/8000系通用并行接口、I2C接口或SPI（串行外围接口）发送。该芯片适用于许多小型便携式低功耗应用，如指纹锁显示屏、手机副显示屏、MP3播放器和计算器等。

本屏幕模块分辨率为128x64，SSD1306显存一共分为8页，每页大小为128字节。

**OLED屏幕显示文字的原理实际上是将文字转换成像素点矩阵**，再将像素点矩阵存储在单片机中，在程序运行时调用对应的数组成员即可控制OLED屏幕上的像素点，同样，使用OLED屏幕显示图像也是同样的原理，本次设计中选用了单片机多功能调试助手中的“点阵生成”功能，该软件可将文字或BMP单色位图转换为16位进制数据。

 

![img](./img/56404.png)

OLED显示

 

### **二、I2C接口的0.96 寸OLED屏**

![img](./img/56405.png)

1. GND 电源地
2. VCC 电源正（3～5.5V）
3. SCL OLED 的 D0 脚，在 IIC 通信中为时钟管脚
4. SDA OLED 的 D1 脚，在 IIC 通信中为数据管脚
5. 分辨率：128  * 64

 

### **三、移植OLED屏代码**

**核心思想**

**定义**

将某平台的源码运行到新的平台，该过程称之为移植。移植过程会存在逐步修改、逐步编译的过程，直到编译通过为止。

 

**技巧**

关键**修改**跟**硬件**平台(当前修改为M3)相关的代码(只要修改接近最底层的代码)，该代码特征一般为如下：

 

![img](./img/56406.png)

![img](./img/56407.png)

 

 

**1. 将OLED屏代码文件夹拷贝到你的工程**

![img](./img/56408.png)

 

**2. keil5打开你的工程，添加OLED代码**

![img](./img/56409.png)

![img](./img/56410.png)

**3. STM32CubeMX配置**

![img](./img/56411.png)

 

**4. 编写测试代码**

```C
#include "app_main.h" 
#include "main.h" 
#include "tim.h" // 包含STM32CubeMX生成的TIM头文件 
#include "debug.h" 
#include "oled_demo.h"
 
...省略中间代码显示
 
// 替代main函数中的while循环 
void app_main(void) 
{ 
    oled_demo(); 
    while (1)      // 你可以在这里处理其它事情的代码 
    { 
        HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin); 
        HAL_Delay(1000); 
    } 
} 
 
```

**注意：如果编译时，提示使用OLED中文的代码函数调用有问题。可以尝试更换V6版本编译器。**

 

**5. 现象**

显示温湿度传感器图片

![img](./img/56412.png)

 

**6. oled代码使用**

使用说明可以看readme.txt，以及源码。

![img](./img/56413.png)

 

 

**四、关于GDDRAM**

SSD1306内置的GDDRAM是一个位映射的静态RAM，用于保存要显示的位模式。RAM的大小为128 x 64位，RAM分为八页，从第0页到第7页，用于单色128x64点阵显示器。

《SSD1315.pdf》P21页

![img](./img/56414.png)

 

当一个数据字节被写入GDDRAM时，所有行都是当前页面的同一页的图像数据列被填充（即，由列地址指针指向的整列（8位）被填充）。数据位D0写入最上面一行，而数据位D7写入最下面一行，如下图所示。

![img](./img/56415.png)

﻿

每个格表示一位图像数据

 

 

因此在使用取模软件的时候，要正确设置取模方式、取模走向。

- 取模方式选中列行扫描，即从第一列开始向下取8个点作为一个字节，然后从第二列开始向下取8个点作为第二个字节…依此类推。如果最后不足8个点就补满8位。取模顺序是从低到高，即第一个点作为最低位。

- 取模走向选中低位在前。

**取模中的“你”点阵分析。**

![img](./img/56416.png)



```C
 /* "你", 0 */ 
{ 
  0x00, 0x80, 0x60, 0xF8, 0x07, 0x40, 0x20, 0x18, 0x0F, 0x08, 0xC8, 0x08, 0x08, 0x28, 0x18, 0x00, 
  0x01, 0x00, 0x00, 0xFF, 0x00, 0x10, 0x0C, 0x03, 0x40, 0x80, 0x7F, 0x00, 0x01, 0x06, 0x18, 0x00, 
},
```

 

**五、写时序**

往OLED写入数据时，I2C写入时序如下所示：

![img](./img/56417.png)

（1）主机先发起开始（START）信号，然后发送1byte首字节，包括从机地址(7位，默认0x78) 和读写数据位(1位，最低位，0为写模式)，驱动器识别从机地址为本机地址之后，将会发出应答信号(ACK) 。

（2）主机收到从机（驱动器）的应答信号之后，随后传输1byte控制字节。一个控制字节主要由Co 和 D/C# 位后面再加上六个0组成的。

- **如果Co为0，后面传输的信息就只包含数据字节。Co = 1，后续传输数据包含控制字节+数据字节。**

- **D/C# 位决定了下个数据字节是作为命令还是数据。D/C# 为0时，下一个数据被视为命令；D/C# 为1时，下一个数据被视为显示数据，存储到GDDRAM中。**

```C
/***这里的 0x40 就是控制字节（0x40 = 0100 0000）
Co = 0(位7=0)
D/C# = 1(位6=1，表示数据位5-0 = 0
这意味着：发送的Count字节都是数据，没有额外的控制字节插入。
***/
static void OLED_WR_Data(uint8_t *Data, uint8_t Count)
{
    HAL_I2C_Mem_Write(&hi2c1, 0x78, 0x40, I2C_MEMADD_SIZE_8BIT, Data, Count, HAL_MAX_DELAY);
}
```

（3）收到控制字节ACK信号之后，传输要写入的数据字节。

（4）传输完毕之后主机发出结束（STOP）信号。

 

**六、关键命令**

🔔*官方原文：《驱动芯片手册.pdf》P34**

In normal display data RAM read or write and page addressing mode, the following steps are required to 

define the starting RAM access pointer location: 

• Set the page start address of the target display location by command B0h to B7h. 

• Set the lower start column address of pointer by command 00h~0Fh. 

• Set the upper start column address of pointer by command 10h~1Fh.

 

**1. 设置起始列地址低位/高位**

单字节指令：00H / 10H （低/高）+ A[3:0]

A为需要设置页的坐标的低/高四位。

 

**2. 设置页地址**

单字节指令： B0H + A[3:0]

A为需要设置的页，最高为7。

使用上述的设置列地址与页地址命令设置显示的位置，参考代码如下：

```C
static void OLED_Set_Pos(uint8_t x, uint8_t y)
{
    OLED_WR_Byte(0xb0 + y, OLED_CMD);                 // 设置页地址（0xb0 + y）
    OLED_WR_Byte(((x & 0xf0) >> 4) | 0x10, OLED_CMD); // 设置列地址高4位
    OLED_WR_Byte((x & 0x0f), OLED_CMD);               // 设置列地址低4位
}
```

 

## OLED项目中的应用

**一、智能屏锁**

![img](./img/56420.png)

链接：https://oshwhub.com/course-examples/eda-lock﻿

 

**二、收音机Pro**

![img](./img/56421.png)

链接：https://oshwhub.com/twist_66/edcminipro-radio-strikes-based-o﻿

 

 

**三、环境监测**

![img](./img/56422.png)

 

![img](./img/56423.png)

链接：https://oshwhub.com/asdgcgjh/second-generation-multi-paramete﻿

 

 

**四、智能桌面宠物**

![img](./img/56424.png)

链接：https://oshwhub.com/sngelswyh/stm32-smart-desktop-pet﻿

 

**五、OLED小电视**

![img](./img/56425.png)

链接：https://oshwhub.com/czjz/0-96-xiao-dian-shi﻿

 

## I2C常用函数接口

**一、I2C 通信（hal_i2c.c/h，标准I2C主机模式，硬件I2C）**

句柄：I2C_HandleTypeDef hi2cx，支持7位/10位从机地址

**1. HAL_I2C_Master_Transmit 主机阻塞发送**

```C
HAL_StatusTypeDef HAL_I2C_Master_Transmit(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, const uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：主机发送数据给从机，带起始、停止信

- 参数：

a.hi2c：I2C句柄

b.DevAddress：从机7位地址（左移1位，最低位0=写）

c.pData：发送缓存

d.Size：字节数

e.Timeout：超时ms

- 返回值：HAL_OK / HAL_TIMEOUT / HAL_ERROR / HAL_BUSY

**2. HAL_I2C_Master_Receive 主机阻塞读取**

```C
HAL_StatusTypeDef HAL_I2C_Master_Receive(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：主机读取从机数据

- 参数：DevAddress最低位1=读，其余同上

- 返回值：状态码

**3. HAL_I2C_Mem_Write 寄存器写（传感器/EEPROM最常用）**

```C
// 将命令码(寄存器)与实际写入的数据分开
HAL_StatusTypeDef HAL_I2C_Mem_Write(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint16_t MemAddress, uint16_t MemAddSize, const uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：向I2C从机指定寄存器写入数据

- 参数：MemAddress：从机内部寄存器地址 MemAddSize：寄存器地址宽度 I2C_MEMADD_SIZE_8BIT/I2C_MEMADD_SIZE_16BIT

- 返回值：状态码

**4. HAL_I2C_Mem_Read 寄存器读取**

```C
HAL_StatusTypeDef HAL_I2C_Mem_Read(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint16_t MemAddress, uint16_t MemAddSize, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：读取从机指定寄存器数据

- 参数同上

- 返回值：状态码

**5. 中断非阻塞收发（IT）**

```C
HAL_StatusTypeDef HAL_I2C_Master_Transmit_IT(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, const uint8_t *pData, uint16_t Size);
HAL_StatusTypeDef HAL_I2C_Master_Receive_IT(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint8_t *pData, uint16_t Size);
HAL_StatusTypeDef HAL_I2C_Mem_Write_IT / HAL_I2C_Mem_Read_IT
```

- 功能：中断方式I2C读写，释放CPU

- 参数：无超时参数

- 返回值：状态码

**6. DMA方式I2C收发**

```C
HAL_I2C_Master_Transmit_DMA / HAL_I2C_Master_Receive_DMA
HAL_I2C_Mem_Write_DMA / HAL_I2C_Mem_Read_DMA
```

- 功能：DMA搬运，大数据量读写EEPROM优选

**7. I2C通信完成回调（弱函数）**

```C
__weak void HAL_I2C_MasterTxCpltCallback(I2C_HandleTypeDef *hi2c); //主机发送完成
__weak void HAL_I2C_MasterRxCpltCallback(I2C_HandleTypeDef *hi2c); //主机接收完成
__weak void HAL_I2C_MemTxCpltCallback(I2C_HandleTypeDef *hi2c); //寄存器写完成
__weak void HAL_I2C_MemRxCpltCallback(I2C_HandleTypeDef *hi2c); //寄存器读完成
```

- 参数：I2C句柄

- 返回值：无

**8. HAL_I2C_Init / HAL_I2C_DeInit**

```C
HAL_StatusTypeDef HAL_I2C_Init(I2C_HandleTypeDef *hi2c);
HAL_StatusTypeDef HAL_I2C_DeInit(I2C_HandleTypeDef *hi2c);
```

- 功能：初始化I2C时钟速度、模式、地址；复位外设

- 参数：I2C句柄

- 返回值：HAL_OK/ERROR

**9. HAL_I2C_IsDeviceReady 检测从机是否在线**

```C
HAL_StatusTypeDef HAL_I2C_IsDeviceReady(I2C_HandleTypeDef *hi2c, uint16_t DevAddress, uint32_t Trials, uint32_t Timeout);
```

- 功能：多次发送地址ACK探测，判断I2C从机是否存在

- 参数：Trials：重试次数；Timeout单次超时

- 返回值：HAL_OK设备就绪，否则超时/错误

**补充通用返回值枚举 HAL_StatusTypeDef**

```C
typedef enum
{
  HAL_OK       = 0x00U,  //操作成功
  HAL_ERROR    = 0x01U,  //参数错误/硬件故障
  HAL_BUSY     = 0x02U,  //外设正在占用
  HAL_TIMEOUT  = 0x03U   //操作超时未完成
} HAL_StatusTypeDef;
```

 

## 取模教程

### **一、文字取模**

假如我想在屏幕上显示16像素高的文字：“您好，广州”，字库是没有这些字的，我们需要取模。

**1. 准备好你取模的文字**

如，“您好，广州”。（注意：也可以是字符）



**2. Porthelper取模**

![img](./img/56395.png)

 

**3. 将取模的代码移植到oledfont.h**

![img](./img/56396.png)

 

**4. 使用**

```C
OLED_ShowString(0, 0, "您好广州", 16);    // 直接调用该函数显示文字即可
```

### **二、图片取模**

如果你想显示你指定的图片，你也需要图片取模。

**1. 使用Porthelper将图片转换成bmp格式图片**

推荐图标网站：👍[iconfont-阿里巴巴矢量图标库](https://www.iconfont.cn/)﻿

![img](./img/56397.png)

![img](./img/56398.png)

 

**2. 取模**

![img](./img/56399.png)

 

**3.** **将取模的代码移植到bmp.h**

![img](./img/56400.png)

 

**4. 使用**

```C
OLED_DrawBMP(0, 0, 32, 32, g_image_dot_1_24bit_32x32);
```

 

### **三、gif 图片显示**

![img](./img/56401.gif)

gif 图片本质就是很多张图片连续显示。我们只需要把这些图片数据取模显示即可。可以使用 Porthelper 将 gif 图片导出连续的BMP后再批量图片取模。

![img](./img/56402.png)



# 变参

```C
#include <stdio.h>
#include <stdarg.h>
char oled_show_buff[16] = {0}; // 128/8=16
void OLED_ShowText_Fmt(u8 x, u8 y, char *fmt, ...)
{
    va_list ap;
    va_start(ap, fmt);
    vsprintf(oled_show_buff, fmt, ap);
    va_end(ap);
    
    OLED_Show_Text(x,y,oled_show_buff);
}
```



