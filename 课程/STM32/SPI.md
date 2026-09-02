# SPI

## 1 SPI

### 1.1 概述

  SPI（Serial Peripheral Interface）是由美国摩托罗拉公司最先推出的一种**同步串行传输**规范，也是一种单片机外设芯片串行外设扩展接口。该接口是一种**高速、全双工、同步**的通信总线，并且在芯片的管脚上只占用四根线，节约了芯片的管脚，大大的为PCB的布局上节省空间。**SPI通信总线的速度默认支持10Mbps，stm32f103最高可以支持18Mbps**。SPI接口主要应用在访问高速设备，如spi flash、2.4G无线传输、lcd设备显示、电阻屏触控IC等。
SPI接口主要应用在EEPROM、Flash、实时时钟、AD转换器，还有数字信号处理器和数字信号解码器之间。

  SPI由一个主设备和一个或多个从设备组成，主设备启动一个与从设备的同步通讯，从而完成数据的交换。

  SPI接口由MOSI（串行数据输出）、MISO（串行数据输入）、SCLK（串行移位时钟）、/SS（从设备使能信号，/SS亦可为NSS）四种信号构成。


![img](./img/rBJlJmJ15fCADYmEAABwsFM_4pM793.png)

  STM32F429有高达6个SPI（45 Mbits/s），其SPI接口提供两个主要功能：支持SPI协议和I2S音频协议。默认情况下，选择的是SPI功能。可通过软件将接口从SPI切换到I2S。

STM32F103中18Mbps
STM32F407中37.5Mbps

  串行外设接口SPI可与外部器件进行半双工/全双工的同步串行通信。该接口可配置为主模式，在这种情况下，它可为外部从器件提供通信时钟SCLK。该接口还能够在多主模式配置下工作。

  它可用于多种用途，包括基于双线的单工同步传输，其中一条可作为双向数据线，或使用CRC校验实现可靠通信。

### 1.2 接口

**1、引脚**

- MOSI – Master Output Slave Input主设备数据输出，从设备数据输入;
- MISO – Master Inpute Slave Output主设备数据输入，从设备数据输出; 
- SCLK – 时钟信号，由主设备产生;
- /SS – /CS(Chip Select)从设备使能信号，由主设备控制。当有多个从设备的时候，因为每个从设备上都有一个片选引脚接入到主设备机中，当我们的主设备和某个从设备通信时将需要将从设备对应的片选引脚电平拉低或者是拉高。

> SS:Slave Select
> CS:Chip Select
> NSS:Negative Slave Select
>
> / --> 表示低电平有效



软件SPI：可以使用任意IO引脚输出电平模拟SPI通信时序，实现SPI通信 -- 灵活，相对通信速率慢

硬件SPI：使用单片机内部的SPI外设的寄存器控制时序生成 -- 相对通信速率高，支持DMA与中断



**2、特点**

  SCLK信号线只由主设备控制，从设备不能控制信号线。同样，在一个基于SPI的设备中，至少有一个主控设备。

  这样传输的特点：这样的传输方式有一个优点，与普通的串行通讯不同，普通的串行通讯一次连续传送至少8位数据，而SPI允许数据一位一位的传送，甚至允许暂停，因为SCLK时钟线由主控设备控制，当没有时钟跳变时，从设备不采集或传送数据，也就是说，主设备通过对SCLK时钟线的控制可以完成对通讯的控制。

![img](./img/56740.png)

  SPI还是一个数据交换协议：因为SPI的数据输入和输出线独立，所以允许同时完成数据的输入和输出。不同的SPI设备的实现方式不尽相同，主要是数据改变和采集的时间不同，在时钟信号上沿或下沿采集有不同定义。


![img](./img/rBJlJmJ15fCAEv0ZAAC-nMAsRgY877.png)

  在SCLK的控制下，两个双向移位寄存器进行数据交换。


![img](./img/rBJlJmJ15fCADY5mAAAzGKLzaV8314.png)

  在点对点的通信中，SPI接口不需要进行寻址操作，且为全双工通信，显得简单高效。在多个从设备的系统中，每个从设备需要独立的使能信号，硬件上比I2C系统要稍微复杂一些。

  最后，SPI接口的一个缺点：没有指定的流控制，没有应答机制确认是否接收到数据。

在SCLK的控制下，两个双向移位寄存器进行数据交换。

![img](./img/56742.png)

初始状态

![img](./img/56743.png)

 

主机读取1bit过程

![img](./img/56744.gif)

 

当读取8次后，也就是读取8位后。

![img](./img/56745.png)

在点对点的通信中，SPI接口不需要进行寻址操作，且为全双工通信，显得简单高效。在多个从设备的系统中，每个从设备需要独立的使能信号，硬件上比I2C系统要稍微复杂一些。最后，SPI接口的一个缺点：没有指定的流控制，没有应答机制确认是否接收到数据。

### 1.3 工作模式

#### 1.3.1 Motorola SPI 通信（主流）

  SPI通信有4种不同的模式，不同的从设备可能在出厂是就是配置为某种模式，这是不能改变的；但我们的通信双方必须是工作在同一模式下，所以我们可以对我们的主设备的SPI模式进行配置，通过CPOL（时钟极性）和CPHA（时钟相位）来控制我们主设备的通信模式，具体如下：

> SPI的收发需要通过时钟信号，接收与发送一个bit数据，需要使用一个脉冲信号同步
>
> CPHA：时钟相位，告知从机什么时候接收数据，什么时候发送数据。
> 	0：主机在脉冲信号的第一边沿采集MISO的数据（接收数据），在第二边沿通过MISO引脚发送数据
> 	1：主机在脉冲信号的第二边沿采集MISO的数据（接收数据），在第二边沿通过MISO引脚发送数据
>
> CPOL：时钟极性，SPI总线在空闲时，时钟线处于什么电平状态，0-低电平 1-高电平
>
> 常用的模式：模式0与模式3，RFID模块，SD卡模块，有线网卡模块
>
> 非常用的模式：模式1与模式2，Lora模块，2.4G模块
>
> 具体使用模式几进行编程？需要参考模块的数据手册

```C
Mode0：CPHA=0，CPOL=0
Mode1：CPHA=0，CPOL=1
Mode2：CPHA=1，CPOL=0
Mode3：CPHA=1，CPOL=1
```

  时钟极性CPOL是用来配置时钟线处于空闲状态是哪种电平，时钟相位CPHA是用来配置数据采样是在第几个边沿：

- CPOL=0，表示时钟线在空闲状态为低电平
- CPOL=1，表示时钟线在空闲状态为高电平
- CPHA=0，表示数据采样是在第1个边沿，数据发送在第2个边沿
- CPHA=1，表示数据采样是在第2个边沿，数据发送在第1个边沿

| 模式 | CPHA | CPOL | 时钟空闲电平 | 数据采样时刻             | 数据变化时刻             |
| ---- | ---- | ---- | ------------ | ------------------------ | ------------------------ |
| 0    | 0    | 0    | 低电平       | 时钟上升沿（第一个边沿） | 时钟下降沿（第二个边沿） |
| 1    | 0    | 1    | 高电平       | 时钟下降沿（第一个边沿） | 时钟上升沿（第二个边沿） |
| 2    | 1    | 0    | 低电平       | 时钟下降沿（第二个边沿） | 时钟上升沿（第一个边沿） |
| 3    | 1    | 1    | 高电平       | 时钟上升沿（第二个边沿） | 时钟下降沿（第一个边沿） |

（1） CPOL=0，CPHA=0：此时空闲态时，SCLK处于低电平，数据采样是在第1个边沿，也就是 SCLK由低电平到高电平的跳变，所以数据采样是在上升沿，数据发送是在下降沿。


![img](./img/rBJlJmJ15fCAa6qdAAE6ffz-cz0048.png)

（2） CPOL=0，CPHA=1：此时空闲态时，SCLK处于低电平，数据发送是在第1个边沿，也就是 SCLK由低电平到高电平的跳变，所以数据采样是在下降沿，数据发送是在上升沿。


![img](./img/rBJlJmJ15fCAEv0ZAAC-nMAsRgY877.png)



#### 1.3.2 TI SPI 通信

  TI模式的SPI通信也称之为SSI(Synchronous Serial Interface)，由TI公司定义的接口协议标准。


![img](./img/rBJlJmJ15fCAFBKXAACc4-pXJGI984.png)

  SPI串行帧同步NSS引脚为低电平有效，在整个帧传输期间生效（拉低）。

  SSI串行帧同步NSS引脚在发送每个帧之前产生宽度为1个时钟周期的高脉冲。SSI 模块和片外从设备都在SCK的上升沿驱动输出数据，在SCK的下降沿锁存另一端的输入数据。

### 1.4 引脚映射

  STM32 芯片有多个 SPI 外设，它们的 SPI 通讯引脚（MOSI、MISO、SCLK 及 NSS）通过 GPIO引脚复用映射实现。


![img](./img/rBJlJmJ15fCAGFjWAABTpW-wQ9I743.png)

  6个SPI控制器中SPI1、SPI4、SPI5、SPI6 挂载在 APB2总线上，最高通信速率达45Mbtis/s，SPI2、SPI3挂载在 APB1 总线上，最高通信速率为 22.5Mbits/s。

## 2 SPI FLASH


![img](./img/rBJlJmJ15fCABy0hAAKtf8xyxCE118.png)

### 2.1 概述

1、内部结构

  W25Q128是容量为128Mbit的SPI接口NORFlash的器件，内部是按照Page、Sector、Block的结构来划分的，一个Page为256个Byte，一个Sector为16个Page也就是4KB，一个Block为16个Sector也就是64KB。相较于EEPROM而言，SPI Flash的存储空间更大，存取速度更快，广泛应用于嵌入式系统中数据、代码的固化。


![img](./img/rBJlJmJ15fCAQL-AAAIFAFwBa20840.png)

  对SPI Flash的操作主要有：写使能、擦除、数据写入、数据读出、读取ID、检测Flash忙状态等几种操作。对SPI Flash进行各种操作，需要先发送对应的控制命令。

2、写使能操作

  在对Flash进行擦除和写操作之前，必须先使能写操作，这是通过将Flash状态寄存器。

3、擦除操作

  Flash存储单元中是无法写入位1的，只能写入位0，所以要写入数据的话要先将原来的数据都擦出成0xFF然后写入数据的时候遇到bit 1时不做处理，遇到bit 0时写入0即可。因此， Flash进行写入之前需要先将目标区块擦除。

4、数据写操作

  数据写操作最多一次不能超过256个字节（一个页）。写入的时候可以不从页的开始地址写入，如果一次写入字节数溢出了一个页的空间，那么多出来的会从循环到页的开始地址处覆盖原来的数据（与EEPROM类似），页写的命令字为0x02，尾随24位的地址。

5、数据读操作

  读操作没有类似于写操作的显示，可以进行任意读。

6、读取ID操作

  为了识别芯片型号，需要读取芯片的ID号，W25Qxx系列Flash有多个ID号， Device ID（0xAB）、JEDEC ID（0x9F）、Unique ID（0x4B）、Manufacturer ID（0x90）等。W25Q128读取到的Manufacturer ID为0xEF，Device ID为0x17，JEDEC ID为0xEF4017。

7、检测Flash忙状态

  读取Flash状态寄存器的内容，并判断其中的WIP（Write In Progress）位状态（0：空闲，1：忙），检测Flash是否处于忙状态。读取Flash状态寄存器命令是0x05。

8、唤醒和掉电

  通过发送0xAB（区别于读取ID操作，在发送命令后不发送空闲字节）命令可以唤醒Flash。

  通过发送0xB9命令可以使得Flash进入掉电模式

### 2.2 引脚描述


![img](./img/rBJlJmJ15fCAaKHwAABVM7GromA531.png)

引脚说明：

- /CS：片选引脚
- DO:数据输出引脚
- /WP：写保护引脚
- DI:数据输入引脚
- CLK:时钟输入引脚
- /HOLD：“暂停引脚”，允许设备在被主动选择时暂停。当/HOLD被拉低时，此时/CS也是被拉低，DO引脚将处于高阻抗，DI和CLK引脚上的信号将被忽略。当/HOLD处于高电平时，设备操作可以恢复。保持功能可以是当多个设备共享相同的SPI信号时有用。

### 2.3 时序图

1、读ID


![img](./img/rBJlJmJ15fCASEURAAD4EvN-cBM935.png)

2、数据读


![img](./img/rBJlJmJ15fCAKmpiAAC0a3lUS3U928.png)

3、数据写


![img](./img/rBJlJmJ15fCAKX6BAAD4ontmWR8470.png)

4、打开写保护


![img](./img/rBJlJmJ15fCASom_AABllxuvZg4253.png)

5、关闭写保护


![img](./img/rBJlJmJ15fCAS-FIAABlo5JYaEg819.png)

6、扇区擦除


![img](./img/rBJlJmJ15fCAXsFqAACL-MmO9fA056.png)

### 2.4 硬件连接

**原理图**


![img](./img/rBJlJmJ15fCAW60iAACPWjEuDm4145.png)


![img](./img/rBJlJmJ15fCALIS6AAB2z8YjWtU489.png)

## 3 STM32CubeMX

1. 将PF6引脚配置为输出模式，PF7、PF8、PF9复用为SPI5功能。


![img](./img/rBJlJmJ15fCAPfEzAAAbSTFB-VA610.png)

1. 在“Categories”类别中选中SPI5。


![img](./img/rBJlJmJ15fCAbfSZAAAg3AF7J2k014.png)

1. Mode，选择“Full-Duplex Master”配置为全双工主机模式。Hardware NSS Signal选择为“Disable”，从机选择引脚不需要由硬件自动控制，也就是说通过软件代码控制。


![img](./img/rBJlJmJ15fCAdFzYAAAL8Nw-st0693.png)

1. SPI详细参数配置。


![img](./img/rBJlJmJ15fCAJOL-AABSjYoK0FM146.png)

1. PF6引脚配置输出电平为高电平，因为SPI主机和从机空闲状态的时候，从机选择引脚为高电平。


![img](./img/rBJlJmJ15fCAVj4EAAAcdlIiqeA905.png)

## 4 实例-读ID

1. SPI5初始化

```C
void MX_SPI5_Init(void)
{

  hspi5.Instance = SPI5;//spi实例为SPI5
  hspi5.Init.Mode = SPI_MODE_MASTER;//主器件角色，即通信的发起方
  hspi5.Init.Direction = SPI_DIRECTION_2LINES;//双线单向通信数据模式
  hspi5.Init.DataSize = SPI_DATASIZE_8BIT;//发送/接收选择 8 位数据帧格式
  hspi5.Init.CLKPolarity = SPI_POLARITY_HIGH;//空闲状态时，串行时钟线SCLK保持高电平
  hspi5.Init.CLKPhase = SPI_PHASE_2EDGE;//从第二个时钟边沿，MISO引脚开始采样数据
  hspi5.Init.NSS = SPI_NSS_SOFT;//使能软件从器件管理
  hspi5.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_16;//波特率控制,SPI硬件时钟=APB2硬件时钟/16=90MHz/16=5.625MHz
  hspi5.Init.FirstBit = SPI_FIRSTBIT_MSB;//帧格式：MSB，即优先传输最高有效位
  hspi5.Init.TIMode = SPI_TIMODE_DISABLE;//屏蔽发送中断
  hspi5.Init.CRCCalculation = SPI_CRCCALCULATION_DISABLE;//禁止 CRC 计算，若使能CRC，最后一个字节为CRC
  hspi5.Init.CRCPolynomial = 10;//无使能CRC时，该多项式值无效
  if (HAL_SPI_Init(&hspi5) != HAL_OK)
  {
    Error_Handler();
  }

}
```



2.SPI低级硬件初始化

```C
void HAL_SPI_MspInit(SPI_HandleTypeDef* spiHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(spiHandle->Instance==SPI5)
  {
  /* USER CODE BEGIN SPI5_MspInit 0 */

  /* USER CODE END SPI5_MspInit 0 */
    /* SPI5 clock enable */
    __HAL_RCC_SPI5_CLK_ENABLE();
  
    __HAL_RCC_GPIOF_CLK_ENABLE();
    /**SPI5 GPIO Configuration    
    PF7     ------> SPI5_SCK
    PF8     ------> SPI5_MISO
    PF9     ------> SPI5_MOSI 
    */
    GPIO_InitStruct.Pin = GPIO_PIN_7|GPIO_PIN_8|GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF5_SPI5;
    HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);

  }
}
```



1. GPIO初始化

```C
void MX_GPIO_Init(void)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOF_CLK_ENABLE();
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOF, GPIO_PIN_6, GPIO_PIN_SET);

  /*Configure GPIO pin : PF6 */
  GPIO_InitStruct.Pin = GPIO_PIN_6;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(GPIOF, &GPIO_InitStruct);
}
```



1. 读ID代码

```C
uint16_t w25qxx_read_id(void)
{
	uint16_t id=0;

	//片选引脚拉低
	HAL_GPIO_WritePin(GPIOF, GPIO_PIN_6, GPIO_PIN_RESET);
	
	//发送0x90
	SPI5_ReadWriteByte(0x90);

	//发送24bit的地址，全为0
	SPI5_ReadWriteByte(0x00);
	SPI5_ReadWriteByte(0x00);
	SPI5_ReadWriteByte(0x00);
	
	//读取厂商id，参数可以为任意参数
	id = SPI5_ReadWriteByte(0xFF)<<8;
	
	//读取设备id
	id|= SPI5_ReadWriteByte(0xFF);

	//片选引脚拉高	
	HAL_GPIO_WritePin(GPIOF, GPIO_PIN_6, GPIO_PIN_SET);
	
	return id;
}
```



1. 主函数

```C
int main(void)
{

	uint8_t buf[64]={0};
	uint32_t i=0;

	HAL_Init();

	SystemClock_Config();

	MX_GPIO_Init();
	MX_USART1_UART_Init();
	MX_SPI5_Init();

	//打印id信息
	printf("w25qxx spi flash id=%04X\r\n",w25qxx_read_id());

	while (1)
	{

	}
}
```



1. 下载演示


![img](./img/rBJlJmJ15fCAH_cwAAAf45hEbXA344.png)

## **应用领域**

1.无线传输

2.高速存储

3.读写器

**打开车门**

**启动汽车**

4.音频解码

5.TFT-显示屏

6.墨水屏

7.触摸屏

8.网络通信模块

## **拓展**

**Dual SPI（Dual serial peripheral interface）双线串行外设接口** 

​        我们发现标准SPI通信时发送和接收时主机和从机都只能使用自己的那根数据线进行数据传输，Dual SPI无论是接收还是发送都是使用两根数据线进行的，所以单向数据传输速度上是标准SPI的双倍。

​        另外需要注意Dual SPI一般情况下用于半双工通信。

![img](./img/56762.png)

 

 Quad SPI （Quad serial peripheral interface）四线SPI，即数据线最多可以使用4根。

 

![img](./img/56763.png)

#  LoRa

## **一、LoRa 技术概述**

LoRa (Long Range) 基于**Semtech**公司开发的一种基于扩频技术的低功耗广域网通信技术，专为长距离、低功耗的物联网应用设计。

![img](./img/56724.png)

**1. 核心特点**

- 远距离：在郊区可达 15km，城市环境可达 2-5km

- 低功耗：睡眠模式下电流仅几微安，电池寿命可达数年

- 抗干扰：采用扩频技术，具有很强的抗干扰能力

- 多节点：单网关支持数万节点

![img](./img/56725.png)

**2. 典型应用场景**

| **应用领域**                 | **具体场景**                | **核心价值**               |
| ---------------------------- | --------------------------- | -------------------------- |
| 智慧城市                     | 水 / 电 / 气 / 热智能抄表   | 远程自动采集，降人工成本   |
| 智慧路灯（调光 / 故障上报）  | 节能降耗，远程统一管理      |                            |
| 智慧停车（车位检测）         | 车位状态实时感知，优化调度  |                            |
| 智能井盖 / 垃圾桶监测        | 异常告警，提升市政运维效率  |                            |
| 智慧农业                     | 土壤温湿度 / 墒情监测       | 指导精准灌溉，节水增效     |
| 温室环境（温湿度 / CO₂）监测 | 自动化调控，提升作物产量    |                            |
| 畜牧定位与健康监测           | 防走失，提前预警疫病        |                            |
| 工业物联网                   | 设备状态（振动 / 温度）监测 | 预测性维护，减少停机故障   |
| 厂区能耗 / 管网监测          | 能耗可视化，降本增效        |                            |
| 危化品气体泄漏监测           | 实时告警，保障生产安全      |                            |
| 冷链物流                     | 冷藏车 / 冷库温湿度监测     | 全程温控追溯，保障品控     |
| 医药冷链环境监控             | 符合监管，防止药品失效      |                            |
| 智能建筑                     | 楼宇能耗 / 环境监测         | 节能管理，提升居住舒适度   |
| 安防传感（门磁 / 烟感）      | 盲区覆盖，及时告警          |                            |
| 医疗健康                     | 慢病 / 老人居家监测         | 远程监护，及时响应异常     |
| 医疗设备 / 药品定位追踪      | 资产高效管理，保障药品安全  |                            |
| 偏远 / 应急场景              | 山区气象 / 水文监测         | 无网区域数据回传，辅助预警 |
| 应急临时通信组网             | 快速部署，保障救援通信      |                            |

 

## **二、LoRa 关键参数（延伸阅读）**

![img](./img/56726.png)

**1. 载波频率**

- 中国常用频段：433MHz / 470MHz

- 欧洲：868MHz

- 北美：915MHz

- 选择依据：根据当地法规和天线设计

**2. 扩频因子(SF)**

 1个符号 = 1 个 chirp

![img](./img/56727.png)

**SF定义：**每个符号中包含的码片数，每个 LoRa 符号中包含的码片数 = 2^SF（码片：扩频通信中的最小传输单元）

**范围：**SF6 ~ SF12

**影响：**

- SF 越大：传输距离越远，数据速率越低，抗干扰能力越强（SF 增大直接导致单个符号的传输时长变长、每秒能传的符号数减少，即便单个符号携带的比特数略有增加）

- SF 越小：数据速率越高，传输距离越近

 

**3. 带宽(BW)**

**可选值：**7.8kHz ~ 500kHz

**常用值：**125kHz, 250kHz, 500kHz

**影响：**

- 带宽越大，数据速率越高，但抗干扰能力下降

- 带宽越小，灵敏度越高，传输距离越远

**（带宽扩大后，类似马路越宽，能同时跑的车越多，通行效率越高。系统会接收更多的噪声和干扰，且信号能量被分散，最终导致信噪比下降、抗干扰裕量减少。）**

**4. 编码率(CR)**

**编码率 = 信息比特数 / 发送的总比特数。**通常表示为分数形式，如 4/5、4/6、4/7、4/8（LoRa常用）：

- 4/5：每 4 个有效数据比特，编码后变成 5 个比特发送

- 4/8：每 4 个有效数据比特，编码后变成 8 个比特发送

**作用：**前向纠错编码，提高传输可靠性

**权衡：**CR 越小，纠错能力越强，但有效数据传输率越低

 

**数据速率计算：**

💡

R = SF × BW / (2^SF) × CR

- BW：带宽

- CR：编码率 (4/5, 4/6, 4/7, 4/8)

![img](./img/56728.png)

**5. 发射功率**

发射功率可调区间：-4dBm ~ +20dBm

- dBm 是射频功率常用单位，数值越大射频发射功率越高、信号传播能力越强，同时功耗、电磁辐射也会上涨

- 法规约束：各个国家、地区 Sub-GHz 频段的最大发射功率存在硬性上限，产品必须遵从属地规范，不可随意拉满 20dBm

- 优化思路：依据实际传输距离、环境遮挡程度动态匹配功率，近距离降功率省电，远距离提升功率保障链路连通

**示例 1：近距离室内场景（家居智慧电表，网关和终端相隔 15m，墙体少）**

选用功率：**-4dBm**效果分析：

1. 距离很短，最低一档功率就可以稳定完成通信；

1. 模块功耗降到低位，电池供电的终端续航能够大幅延长；

1. 发射信号强度低，不会对周边同频段 LoRa 设备造成干扰；

1. 合规层面：室内场景各国法规均认可该功率，不存在违规隐患。

**示例 2：城郊开阔户外场景（农田传感器，节点距离网关 1km，无密集建筑遮挡）**

选用功率：**14dBm**效果分析：

1. 中等功率足够覆盖千米级开阔传输距离；

1. 相比上限 20dBm，功耗下降明显，适配太阳能供电的野外终端；

1. 适配国内 Sub-GHz 常规法规限值，符合入网标准。

**示例 3：复杂遮挡场景（地下井盖监测终端，网关部署路面，存在混凝土土层遮挡，传输距离约 2.5km）**

选用功率：**20dBm（区间最大值）**效果分析：

1. 最大功率补偿墙体、泥土带来的信号衰减，保障穿透之后信号仍能正常被网关接收；

1. 使用前要核查本地法规：如果所在地区法定上限只有 14dBm，就不能开到 20dBm，需要改用调高 SF 扩频因子的方式增强链路余量。

**示例 4：跨境合规差异化选型（法规限制演示）**

1. 部署在欧盟部分区域：当地法规限定 ISM 频段最大功率仅 14dBm，哪怕硬件支持 20dBm，最高只能设置 14dBm；

1. 部署国内合规频段：合规上限可达 20dBm，偏远野外场景才可以启用满功率；

**动态调整策略实战案例（自适应功率方案）**

网关周期性检测终端上行信号的 RSSI 接收强度：

1. RSSI＞-70dBm（信号很强、距离近）：终端功率下调至 0~5dBm；

1. RSSI 处于 - 90~-70dBm（中等信号）：终端维持 10~15dBm；

1. RSSI＜-90dBm（信号偏弱、损耗大）：终端上调至法规允许的最大功率。

**实操避坑小贴士**

1. 不要无脑常驻 20dBm：电池供电设备满功率运行会缩减接近一半的续航时长；

1. 高密度部署园区（园区大量 LoRa 节点共存）：统一压低发射功率，规避大范围信号重叠引发的同频拥堵；

1. 冬季植被茂密、雨季空气湿度高会加大路径损耗，同等距离可以把功率上调 2~4dBm 预留余量。

**6. 参数配置示例**

| **应用场景** | **SF** | **BW** | **CR** | **发射功率** |
| ------------ | ------ | ------ | ------ | ------------ |
| 远程遥测     | SF12   | 125kHz | 4/8    | +20dBm       |
| 中速数据     | SF9    | 250kHz | 4/6    | +17dBm       |
| 高速传输     | SF7    | 500kHz | 4/5    | +14dBm       |
| 低功耗       | SF10   | 125kHz | 4/7    | +10dBm       |

 

## **三、LoRa 模块**

**1. 概述**

﻿[安信可 LoRa 系列模块Ra-01SC](https://docs.ai-thinker.com/Ra-01SC/#▫️概述)由深圳市安信可科技有限公司设计开发的。该模组 用于超长距离扩频通信，其射频芯片 **LLCC68** 主要采用 LoRa™远程调制解调器，用于超 长距离扩频通信，抗干扰性强，功耗低。

可广泛用于智能仪表，供应链和物流，家庭楼宇自动化，安防系统，远程灌溉系统等。

![img](./img/56729.png)

**特性**

- LoRa™ 调制解调器

- 支持 FSK、GFSK、MSK、GMSK、LoRa™及 OOK 调制方式

- 支持频段410MHz~525MHz

- 工作电压为3.3V,最大输出发射功率 +22dBm，最大工作电流为140mA

- 接收状态下具有低功耗特性，接收电流最低为4.2mA，待机电流为0.6mA

- 高灵敏度：低至-129dBm

- 支持扩频因子SF5/SF6/SF7/SF8/SF9/SF10/SF11

- 小体积双列邮票孔贴片封装

- 模块采用 **SPI** 接口，使用**半双工通信**，带CRC、高达 **256 字节**的数据包引擎

- 天线接口兼容邮票孔/圆孔和IPEX等多种接法，支持更多的方案选型

**2. 引脚说明**

| **Ra-01S 引脚** | **功能**   | **接线说明**                                      |
| --------------- | ---------- | ------------------------------------------------- |
| 3V3             | 电源输入   | 接 MCU 的 3.3V 电源（需保证电流）                 |
| GND             | 电源地     | 与 MCU 共地（建议多接 1 个 GND）                  |
| NSS             | SPI 片选   | MCU 输出，低电平选中模块                          |
| MOSI            | SPI 发送   | MCU→模块的数据传输                                |
| MISO            | SPI 接收   | 模块→MCU 的数据传输                               |
| SCK             | SPI 时钟   | MCU 提供时钟信号                                  |
| ANT             | 天线接口   | 接 50Ω 阻抗天线（如弹簧天线）                     |
| RST（建议）     | 复位       | MCU 输出，拉低 10ms 复位模块                      |
| DIO1 引脚       | 状态指示   | 可配置为事件中断输出，映射 TX/RX 完成、超时等事件 |
| BUSY（建议）    | 忙状态指示 | 模块输出，高电平表示忙                            |

你只需将 DIO1 接 MCU 的外部中断引脚，实现 “收发完成即时处理”。当 “发送完成（TX_DONE）” 或 “接收完成（RX_DONE）” 发生时，**DIO1引脚会自动拉高（产生上升沿）；**

**驱动代码下载**

﻿[GitHub - Lora-net/llcc68_driver: Driver for LLCC68 radio](https://github.com/lora-net/llcc68_driver/)﻿

﻿[Guistar/llcc68_driver - Gitee.com](https://gitee.com/IUuaena/llcc68_driver/tree/master/)﻿

## **四、MCU和 LoRa 硬件连接**

STM32 主要使用 **SPI** 和 LoRa 模块通信硬件连接如下：

![img](./img/56730.png)

 

## **五、移植LoRa驱动代码**

终端设备为例。

**5.1 STM32CubeMX配置**

![img](./img/56731.png)

![img](./img/56732.png)

 

![img](./img/56733.png)

 

**5.2 代码添加**

**5.2.1 将LoRa驱动代码拷贝到工程**

![img](./img/56734.png)

 

**5.2.2 添加源文件和头文件到工程中**

![img](./img/56735.png)

 

![img](./img/56736.png)

 

**5.3 移植文件清单**

移植时需要复制以下文件到目标工程 User/bsp/lora/ 目录：

| **文件**                                         | **来源**    | **移植时是否需要修改** |
| ------------------------------------------------ | ----------- | ---------------------- |
| llcc68.c/ llcc68.h                               | Semtech官方 | **不改**               |
| llcc68_driver_version.c/ llcc68_driver_version.h | Semtech官方 | **不改**               |
| llcc68_regs.h                                    | Semtech官方 | **不改**               |
| llcc68_status.h                                  | Semtech官方 | **不改**               |
| llcc68_hal.c/ llcc68_hal.h                       | 需用户实现  | **需要改**（适配平台） |
| llcc68_p2p.c/ llcc68_p2p.h                       | 需用户实现  | **需要改**（引脚定义） |

**5.4 五个关键移植步骤**

**步骤1：CubeMX 配置 SPI**

**Core/Src/spi.c**

```C
hspi1.Instance = SPI1;
hspi1.Init.Mode = SPI_MODE_MASTER;              // 主机模式
hspi1.Init.Direction = SPI_DIRECTION_2LINES;     // 全双工
hspi1.Init.DataSize = SPI_DATASIZE_8BIT;         // 8位数据帧
hspi1.Init.CLKPolarity = SPI_POLARITY_LOW;       // CPOL=0（空闲低电平）
hspi1.Init.CLKPhase = SPI_PHASE_1EDGE;           // CPHA=0（第一个边沿采样）
hspi1.Init.NSS = SPI_NSS_SOFT;                   // 软件控制NSS
hspi1.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_32;  // 分频32
hspi1.Init.FirstBit = SPI_FIRSTBIT_MSB;          // MSB先行
 
```

**技巧**：LLCC68 要求 SPI Mode 0（CPOL=0, CPHA=0）。波特率分频不能太小，72MHz/32 = 2.25MHz，在 LLCC68 的 16MHz 上限内。

**步骤2：CubeMX 配置 4 个 GPIO**

**Core/Src/gpio.c**

| **引脚**    | **模式**                   | **作用**       |
| ----------- | -------------------------- | -------------- |
| PA4 (NSS)   | OUTPUT_PP, SPEED_FREQ_HIGH | 片选，软件控制 |
| PB1 (RST)   | OUTPUT_PP, SPEED_FREQ_HIGH | 复位           |
| PB0 (BUSY)  | INPUT, NOPULL              | 忙信号（输入） |
| PB10 (DIO1) | GPIO_MODE_IT_RISING        | 上升沿外部中断 |

 

```C
/* DIO1 必须配置为上升沿外部中断 */
GPIO_InitStruct.Pin = LORA_DIO1_Pin;
GPIO_InitStruct.Mode = GPIO_MODE_IT_RISING;    // 上升沿触发
GPIO_InitStruct.Pull = GPIO_NOPULL;
HAL_GPIO_Init(LORA_DIO1_GPIO_Port, &GPIO_InitStruct);
```

**步骤3：使能 EXTI NVIC 中断 + 编写中断服务函数**

Core/Src/gpio.c末尾添加：

```C
/* EXTI interrupt init */
HAL_NVIC_SetPriority(EXTI15_10_IRQn, 10, 0);
HAL_NVIC_EnableIRQ(EXTI15_10_IRQn);    // 必须使能！否则DIO1中断不触发
```

Core/Src/stm32f1xx_it.c添加中断服务函数：

```C
void EXTI15_10_IRQHandler(void)
{
    HAL_GPIO_EXTI_IRQHandler(LORA_DIO1_Pin);
}
 
```

**步骤4：实现 HAL 抽象层（llcc68_hal.c）**

**这是移植的核心。Semtech 官方驱动只定义了接口，需要用户实现 4 个函数**：

User/bsp/lora/llcc68_hal.h定义上下文结构体：

```C
typedef struct {
    SPI_HandleTypeDef *hspi;    // SPI句柄
    GPIO_TypeDef *nss_port;     // NSS端口
    uint16_t nss_pin;           // NSS引脚
    GPIO_TypeDef *rst_port;     // RST端口
    uint16_t rst_pin;           // RST引脚
    GPIO_TypeDef *busy_port;    // BUSY端口
    uint16_t busy_pin;          // BUSY引脚
    GPIO_TypeDef *dio1_port;    // DIO1端口
    uint16_t dio1_pin;          // DIO1引脚
} llcc68_hal_context_t;
 
```

User/bsp/lora/llcc68_hal.c需实现 4 个函数：

| **函数**            | **作用** | **关键点**                                          |
| ------------------- | -------- | --------------------------------------------------- |
| llcc68_hal_write()  | SPI写    | 先等BUSY低 → 拉低NSS → 发command → 发data → 拉高NSS |
| llcc68_hal_read()   | SPI读    | 先等BUSY低 → 拉低NSS → 发command → 收data → 拉高NSS |
| llcc68_hal_reset()  | 硬件复位 | 拉低RST 10ms → 拉高RST → 等BUSY空闲                 |
| llcc68_hal_wakeup() | 唤醒     | 拉低NSS 1ms → 拉高NSS → 等BUSY空闲                  |

**技巧**：每次 SPI 操作前必须等 BUSY 引脚拉低，否则芯片会忽略指令。

**步骤5：配置引脚映射 + 中断回调**

User/bsp/lora/llcc68_p2p.h修改引脚定义与实际硬件一致：

```C
#define LLCC68_SPI_HANDLE &hspi1
#define LLCC68_NSS_PORT GPIOA
#define LLCC68_NSS_PIN  GPIO_PIN_4
#define LLCC68_RST_PORT GPIOB
#define LLCC68_RST_PIN  GPIO_PIN_1
#define LLCC68_BUSY_PORT GPIOB
#define LLCC68_BUSY_PIN  GPIO_PIN_0
#define LLCC68_DIO1_PORT GPIOB
#define LLCC68_DIO1_PIN  GPIO_PIN_10
```

User/bsp/isr_callback.c 中注册中断回调：

```C
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin)
{
    if (GPIO_Pin == LORA_DIO1_Pin) {
        DIO1_EXTI_Callback();    // 转发给LoRa驱动处理
    }
}
```

## **六、 测试验证**

![img](./img/56737.png)

 

# LoRaWAN（延伸阅读）

## **一、LoRa 点对点通信的本质与局限**

**LoRa 是一种低功耗、远距离的射频（RF）调制技术，点对点模式是它最基础的通信方式：**

**1. 通信形态：**终端节点（如传感器）直接与另一个节点（如网关或另一台终端）通过 LoRa RF 传输数据，是 “点到点” 或 “简单一对多” 的连接。

**2. 核心局限：**

- 覆盖范围有限：受环境、功率制约，无法支撑城市级、广域级的物联网部署。

- 无标准化网络架构：没有统一的接入管理、数据路由机制，无法应对海量设备并发连接。

- 应用孤立：终端数据直接发给接收端，不同应用系统难以兼容，也缺乏端到端的安全保障。

- 运维复杂度高：每个点对点链路都需要单独配置，大规模部署时成本和难度指数级上升。

## **二、LoRaWAN**

LoRaWAN 是基于 LoRa 技术的标准化广域物联网协议，它在 LoRa 射频技术之上，定义了一套完整的网络架构、通信规则和安全机制。结合下图，我们可以拆解它如何解决点对点的痛点：

![img](./img/56721.png)

**1. 分层架构：责任解耦，支撑规模化**

图中清晰展示了 4 层架构，实现了 “终端 - 网关 - 网络 - 应用” 的分层协作：

**终端层（End Nodes）**：各种物联网设备（如宠物追踪器、烟感、水表等），负责采集数据，通过 LoRa RF 与网关通信。

**网关层（Concentrator/Gateway）**：作为 “中转站”，接收多个终端的 LoRa 信号，再通过 3G/Ethernet 等回传链路（TCP/IP + SSL）将数据转发给网络服务器。

**网络服务器层（Network Server）**：网络的 “大脑”，负责设备接入认证、数据路由、频率规划、冲突避免（如自适应数据速率 ADR），并将终端数据转发给对应的应用服务器。

**应用服务器层（Application Server）**：处理具体业务逻辑（如数据分析、告警触发），通过安全通道接收加密数据，实现业务与网络的解耦。

**2. 核心能力升级：从 “零散连接” 到 “可运营网络”**

广域覆盖与海量接入：网关可多节点部署形成覆盖网络，单个网关理论上可连接上千个终端，解决了点对点的距离和容量瓶颈（图中多网关、多终端的场景就是典型体现）。

标准化与互操作性：LoRaWAN 是开源协议，不同厂商的终端、网关均可兼容，打破了点对点通信的设备孤岛问题。

端到端安全：图中 “AES Secured Payload” 和 “TCP/IP SSL” 标识显示，LoRaWAN 在物理层（AES-128 加密载荷）、网络层（SSL/TLS 传输加密）、应用层（安全通道）都有完整的安全机制，远胜点对点的简单加密。

网络管理与优化：网络服务器可动态调整终端传输功率、数据速率（ADR），优化网络容量与终端电池寿命，这是点对点通信完全不具备的运营能力。

**3. 价值总结**

- 点对点 LoRa 适合小范围、简单场景（如单个传感器到网关的临时数据传输）；

- LoRaWAN 则构建了一套可扩展、可运营的广域物联网架构，支撑智慧城市、工业物联网等大规模、跨场景的应用（如图中多类型终端接入、多应用服务器协同的复杂场景）。

 

## **三、总结**

在这篇入门梳理里，我先带大家快速过了 LoRa 和 LoRaWAN 的核心区别：LoRa 作为底层射频技术，它的点对点通信在覆盖、标准化和规模化上有明显局限；而 LoRaWAN 正是为了解决这些痛点而生的标准化协议，通过分层架构实现了广域覆盖、海量接入和可运营的网络管理。



# SPI常用函数接口

**STM32F103 HAL库 SPI 常用函数接口**

文件：stm32f1xx_hal_spi.c / stm32f1xx_hal_spi.h

句柄类型：SPI_HandleTypeDef hspix（CubeMX自动生成 hspi1 / hspi2）

统一返回值类型：HAL_StatusTypeDef

```C
typedef enum
{
  HAL_OK       = 0x00U,
  HAL_ERROR    = 0x01U,
  HAL_BUSY     = 0x02U,
  HAL_TIMEOUT  = 0x03U
} HAL_StatusTypeDef;
```

**一、初始化 / 反初始化**

**1. HAL_SPI_Init**

```C
HAL_StatusTypeDef HAL_SPI_Init(SPI_HandleTypeDef *hspi);
```

- 功能：根据句柄内结构体配置SPI模式、波特率、CPOL/CPHA、数据位、NSS管理等

- 参数：hspi：SPI外设句柄指针

- 返回值：HAL_OK 成功 / HAL_ERROR 参数错误

**2. HAL_SPI_DeInit**

```C
HAL_StatusTypeDef HAL_SPI_DeInit(SPI_HandleTypeDef *hspi);
```

- 功能：复位SPI外设寄存器，关闭外设时钟

- 参数：SPI句柄

- 返回值：HAL_OK / HAL_ERROR

**二、阻塞式收发（轮询模式，最简单常用）**

**3. HAL_SPI_Transmit 阻塞发送**

```C
HAL_StatusTypeDef HAL_SPI_Transmit(SPI_HandleTypeDef *hspi, const uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：阻塞发送一组数据，函数直到发完或超时才返回

- 参数

- hspi：SPI句柄

- pData：待发送数据缓冲区

- Size：发送字节数量

- Timeout：超时时间(ms)，HAL_MAX_DELAY无限等待

- 返回值：HAL_OK / HAL_BUSY / HAL_TIMEOUT / HAL_ERROR

**4. HAL_SPI_Receive 阻塞接收**

```C
HAL_StatusTypeDef HAL_SPI_Receive(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size, uint32_t Timeout);
```

- 功能：阻塞读取SPI数据，SPI收发同步，发送Dummy字节同时读取从机数据

- 参数同上，pData为接收缓存

- 返回值：同上

**5. HAL_SPI_TransmitReceive 收发同步（SPI最核心函数）**

常用：SPI Flash

```C
HAL_StatusTypeDef HAL_SPI_TransmitReceive(SPI_HandleTypeDef *hspi, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size, uint32_t Timeout);
```

- 功能：同步收发，发1字节同时收1字节，SPI读写寄存器必备

- 参数

- pTxData：发送缓冲区

- pRxData：接收缓冲区

- Size：传输字节数

- Timeout：超时ms

- 返回值：HAL_OK / HAL_TIMEOUT / HAL_BUSY / HAL_ERROR

**三、中断非阻塞收发（IT模式）**

**6. HAL_SPI_Transmit_IT**

```C
HAL_StatusTypeDef HAL_SPI_Transmit_IT(SPI_HandleTypeDef *hspi, const uint8_t *pData, uint16_t Size);
```

- 功能：开启SPI发送中断，非阻塞，数据在中断内搬运

- 参数：句柄、发送缓存、长度

- 返回值：HAL_OK / HAL_BUSY / HAL_ERROR

**7. HAL_SPI_Receive_IT**

```C
HAL_StatusTypeDef HAL_SPI_Receive_IT(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size);
```

- 功能：开启接收中断，等待从机数据

- 返回值：同上

**8. HAL_SPI_TransmitReceive_IT**

```C
HAL_StatusTypeDef HAL_SPI_TransmitReceive_IT(SPI_HandleTypeDef *hspi, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size);
 
```

- 功能：中断方式同步收发

**四、DMA高速收发**

**9. HAL_SPI_Transmit_DMA**

```C
HAL_StatusTypeDef HAL_SPI_Transmit_DMA(SPI_HandleTypeDef *hspi, const uint8_t *pData, uint16_t Size);
```

- 功能：DMA搬运发送，不占用CPU，大屏、Flash高速读写使用

**10. HAL_SPI_Receive_DMA**

```C
HAL_StatusTypeDef HAL_SPI_Receive_DMA(SPI_HandleTypeDef *hspi, uint8_t *pData, uint16_t Size);
```

**11. HAL_SPI_TransmitReceive_DMA**

```C
HAL_StatusTypeDef HAL_SPI_TransmitReceive_DMA(SPI_HandleTypeDef *hspi, const uint8_t *pTxData, uint8_t *pRxData, uint16_t Size);
```

**五、终止传输**

**12. HAL_SPI_Abort**

```C
HAL_StatusTypeDef HAL_SPI_Abort(SPI_HandleTypeDef *hspi);
```

- 功能：立即停止当前SPI传输（轮询模式）

- 返回值：HAL_OK / HAL_TIMEOUT

**13. HAL_SPI_Abort_IT**

```C
HAL_StatusTypeDef HAL_SPI_Abort_IT(SPI_HandleTypeDef *hspi);
```

- 功能：中断/DMA模式下终止传输，停止后触发完成回调

**六、中断服务函数与回调（弱函数，用户重写）**

**14. HAL_SPI_IRQHandler**

```C
void HAL_SPI_IRQHandler(SPI_HandleTypeDef *hspi);
```

- 功能：SPI中断入口，判断TX/RX/错误标志，调用对应回调；放在stm32f1xx_it.c对应SPI中断函数中

**15. 传输完成回调**

```C
__weak void HAL_SPI_TxCpltCallback(SPI_HandleTypeDef *hspi);
//发送完成回调
 
__weak void HAL_SPI_RxCpltCallback(SPI_HandleTypeDef *hspi);
//接收完成回调
 
__weak void HAL_SPI_TxRxCpltCallback(SPI_HandleTypeDef *hspi);
//同步收发完成回调
```

**16. DMA半传输回调（仅DMA模式）**

```C
__weak void HAL_SPI_TxHalfCpltCallback(SPI_HandleTypeDef *hspi);
__weak void HAL_SPI_RxHalfCpltCallback(SPI_HandleTypeDef *hspi);
__weak void HAL_SPI_TxRxHalfCpltCallback(SPI_HandleTypeDef *hspi);
```

**17. 错误回调**

```C
__weak void HAL_SPI_ErrorCallback(SPI_HandleTypeDef *hspi);
```

- 功能：溢出、模式错误、CRC校验错误时进入

**七、状态查询工具函数**

**18. HAL_SPI_GetState**

```C
HAL_SPI_StateTypeDef HAL_SPI_GetState(SPI_HandleTypeDef *hspi);
```

- 功能：获取SPI当前运行状态

- 返回枚举：

- HAL_SPI_STATE_RESET：未初始化

- HAL_SPI_STATE_READY：空闲就绪

- HAL_SPI_STATE_BUSY_TX：发送中

- HAL_SPI_STATE_BUSY_RX：接收中

- HAL_SPI_STATE_BUSY_TX_RX：同步收发中

- HAL_SPI_STATE_ERROR：出错

**19. HAL_SPI_GetError**

```C
uint32_t HAL_SPI_GetError(SPI_HandleTypeDef *hspi);
```

- 功能：读取SPI错误标志（溢出、模式故障、CRC错误）

**八、常用补充说明**

1. STM32F1硬件SPI NSS片选**无硬件自动管理**，项目中统一用GPIO手动拉低/拉高；

1. 读写W25Q、OLED、TFT优先使用 HAL_SPI_TransmitReceive；

1. 大数据刷屏/Flash批量读写使用SPI+DMA；

1. 短指令读写直接阻塞函数，代码最简单。

 





















