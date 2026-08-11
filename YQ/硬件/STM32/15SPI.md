# 1 SPI

## 1.1 概述

  SPI（Serial Peripheral Interface）是由美国摩托罗拉公司最先推出的一种同步串行传输规范，也是一种单片机外设芯片串行外设扩展接口。该接口是一种高速、全双工、同步的通信总线，并且在芯片的管脚上只占用四根线，节约了芯片的管脚，大大的为PCB的布局上节省空间。
SPI接口主要应用在EEPROM、Flash、实时时钟、AD转换器，还有数字信号处理器和数字信号解码器之间。

  SPI由一个主设备和一个或多个从设备组成，主设备启动一个与从设备的同步通讯，从而完成数据的交换。

  SPI接口由MOSI（串行数据输出）、MISO（串行数据输入）、SCLK（串行移位时钟）、/SS（从设备使能信号，/SS亦可为NSS）四种信号构成。


![img](./img/rBJlJmJ15fCADYmEAABwsFM_4pM793.png)

  STM32F429有高达6个SPI（45 Mbits/s），其SPI接口提供两个主要功能：支持SPI协议和I2S音频协议。默认情况下，选择的是SPI功能。可通过软件将接口从SPI切换到I2S。

  串行外设接口SPI可与外部器件进行半双工/全双工的同步串行通信。该接口可配置为主模式，在这种情况下，它可为外部从器件提供通信时钟SCLK。该接口还能够在多主模式配置下工作。

  它可用于多种用途，包括基于双线的单工同步传输，其中一条可作为双向数据线，或使用CRC校验实现可靠通信。

## 1.2 接口

**1、引脚**

- MOSI – 主设备数据输出，从设备数据输入;
- MISO – 主设备数据输入，从设备数据输出;
- SCLK – 时钟信号，由主设备产生;
- /SS – 从设备使能信号，由主设备控制。当有多个从设备的时候，因为每个从设备上都有一个片选引脚接入到主设备机中，当我们的主设备和某个从设备通信时将需要将从设备对应的片选引脚电平拉低或者是拉高。

**2、特点**

  SCLK信号线只由主设备控制，从设备不能控制信号线。同样，在一个基于SPI的设备中，至少有一个主控设备。

  这样传输的特点：这样的传输方式有一个优点，与普通的串行通讯不同，普通的串行通讯一次连续传送至少8位数据，而SPI允许数据一位一位的传送，甚至允许暂停，因为SCLK时钟线由主控设备控制，当没有时钟跳变时，从设备不采集或传送数据，也就是说，主设备通过对SCLK时钟线的控制可以完成对通讯的控制。

  SPI还是一个数据交换协议：因为SPI的数据输入和输出线独立，所以允许同时完成数据的输入和输出。不同的SPI设备的实现方式不尽相同，主要是数据改变和采集的时间不同，在时钟信号上沿或下沿采集有不同定义。


![img](./img/rBJlJmJ15fCAEv0ZAAC-nMAsRgY877.png)

  在SCLK的控制下，两个双向移位寄存器进行数据交换。


![img](./img/rBJlJmJ15fCADY5mAAAzGKLzaV8314.png)

  在点对点的通信中，SPI接口不需要进行寻址操作，且为全双工通信，显得简单高效。在多个从设备的系统中，每个从设备需要独立的使能信号，硬件上比I2C系统要稍微复杂一些。

  最后，SPI接口的一个缺点：没有指定的流控制，没有应答机制确认是否接收到数据。

## 1.3 工作模式

### 1.3.1 Motorola SPI 通信（主流）

  SPI通信有4种不同的模式，不同的从设备可能在出厂是就是配置为某种模式，这是不能改变的；但我们的通信双方必须是工作在同一模式下，所以我们可以对我们的主设备的SPI模式进行配置，通过CPOL（时钟极性）和CPHA（时钟相位）来控制我们主设备的通信模式，具体如下：

```
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

（1） CPOL=0，CPHA=0：此时空闲态时，SCLK处于低电平，数据采样是在第1个边沿，也就是 SCLK由低电平到高电平的跳变，所以数据采样是在上升沿，数据发送是在下降沿。


![img](./img/rBJlJmJ15fCAa6qdAAE6ffz-cz0048.png)

（2） CPOL=0，CPHA=1：此时空闲态时，SCLK处于低电平，数据发送是在第1个边沿，也就是 SCLK由低电平到高电平的跳变，所以数据采样是在下降沿，数据发送是在上升沿。


![img](./img/rBJlJmJ15fCAEv0ZAAC-nMAsRgY877.png)

### 1.3.2 TI SPI 通信

  TI模式的SPI通信也称之为SSI(Synchronous Serial Interface)，由TI公司定义的接口协议标准。


![img](./img/rBJlJmJ15fCAFBKXAACc4-pXJGI984.png)

  SPI串行帧同步NSS引脚为低电平有效，在整个帧传输期间生效（拉低）。

  SSI串行帧同步NSS引脚在发送每个帧之前产生宽度为1个时钟周期的高脉冲。SSI 模块和片外从设备都在SCK的上升沿驱动输出数据，在SCK的下降沿锁存另一端的输入数据。

## 1.4 引脚映射

  STM32 芯片有多个 SPI 外设，它们的 SPI 通讯引脚（MOSI、MISO、SCLK 及 NSS）通过 GPIO引脚复用映射实现。


![img](./img/rBJlJmJ15fCAGFjWAABTpW-wQ9I743.png)

  6个SPI控制器中SPI1、SPI4、SPI5、SPI6 挂载在 APB2总线上，最高通信速率达45Mbtis/s，SPI2、SPI3挂载在 APB1 总线上，最高通信速率为 22.5Mbits/s。

# 2 SPI FLASH


![img](./img/rBJlJmJ15fCABy0hAAKtf8xyxCE118.png)

## 2.1 概述

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

## 2.2 引脚描述


![img](./img/rBJlJmJ15fCAaKHwAABVM7GromA531.png)

引脚说明：

- /CS：片选引脚
- DO:数据输出引脚
- /WP：写保护引脚
- DI:数据输入引脚
- CLK:时钟输入引脚
- /HOLD：“暂停引脚”，允许设备在被主动选择时暂停。当/HOLD被拉低时，此时/CS也是被拉低，DO引脚将处于高阻抗，DI和CLK引脚上的信号将被忽略。当/HOLD处于高电平时，设备操作可以恢复。保持功能可以是当多个设备共享相同的SPI信号时有用。

## 2.3 时序图

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

## 2.4 硬件连接

**原理图**


![img](./img/rBJlJmJ15fCAW60iAACPWjEuDm4145.png)


![img](./img/rBJlJmJ15fCALIS6AAB2z8YjWtU489.png)

# 3 STM32CubeMX

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

# 4 实例-读ID

1. SPI5初始化

```
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

```
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

```
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

```
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

```
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