# DMA

[toc]



## DMA原理与应用

### **一、引入**

此前我们采集光敏、土壤湿度等多路电压时，采用了 “一个 ADC 外设仅使用 1 个通道、对应检测一路电压” 的方式，这种方式在面对大量电压采样需求时，会因 STM32 片上 ADC 外设数量有限而难以满足。而回忆 ADC 功能框图可知，单个 ADC 外设本身就支持多路通道的电压检测，若再搭配 DMA 技术，还能实现多路电压的高效采集。

### **二、DMA简介**

DMA（Direct Memory Access，直接存储器存取）是 STM32 等单片机的重要外设，其核心功能是**独立完成数据的高速搬运**，全程无需 CPU 参与干预。**在数据传输过程中，DMA 会自主实现 **“外设与内存” 或 “内存与内存” 之间的数据迁移，此时 CPU 无需暂停当前任务去查询、搬运数据，可同时并行执行其他核心逻辑（如阻值换算、查表获取光强 / 土壤湿度等），实现类似 “多线程” 的并行工作效果，大幅提升单片机的整体运行效率。

**举例：**

DMA将串口接收到的数据转移到SRAM，CPU可以控制I/O或响应中断，提高了效率。

- **串口数据转移到SRAM**

![img](./img/56449.png)

串口数据转移到SRAM

 

- **SRAM数据转移到串口**

 

![img](./img/56450.gif)

SRAM数据转移到串口

 

当串口数据的转移由CPU交给DMA负责后，CPU就可以执行其他事情如下图的点灯，实现并发，提高了效率。

 

![img](./img/56451.gif)

DMA负责转移数据，CPU执行其他事情

### **三、DMA 核心传输特性**

#### **1. 传输方向（3 种）**

传输方向指的是数据从哪里来，搬到那里去。主要有三种：

- 外设到存储器（Peripheral to Memory，P2M）：最常用（如 USART1 接收数据到内存数组、**ADC 采样结果存入内存**）。

- 存储器到外设（Memory to Peripheral，M2P）：最常用（如**内存数组**数据通过 **USART1** 发送、SPI 批量写数据到外设）。

- 存储器到存储器（Memory to Memory，M2M）：仅 DMA1 支持（将一块内存数据拷贝到另一块内存，如大容量数组复制，效率远高于 CPU 循环拷贝）。

#### **2. 数据宽度（可选 8/16/32 位）**

**数据宽度指的是 DMA 单次传输操作中，从源地址到目标地址所搬运的数据单位大小（即单次传输的数据位数）。**

- 外设数据宽度：与外设数据寄存器位宽匹配（如 USART 数据寄存器为 8 位，ADC 结果为 12 位（通常配置为 16 位存储））。

- 存储器数据宽度：可根据需求配置（如数组为uint8_t则选 8 位，uint16_t则选 16 位）。

- 注意：外设与存储器数据宽度可不一致，DMA 会自动完成数据位宽转换。（但是会有数据错乱风险，实际项目推荐宽度一致）

#### **3. 地址增量模式**

**地址增量模式，指的是每完成一次 DMA 数据传输后，对应的源地址或目标地址是否会自动向上递增**

- 使能增量：传输完成后，对应地址自动递增（如内存数组传输，需使能存储器地址增量，逐个填充 / 读取数组元素）。

- 禁止增量：传输完成后，地址保持不变（如外设固定寄存器（USART_DR）、内存单个寄存器，需禁止增量）。

- 常规配置：M2P/P2M 模式下，外设地址禁止增量，存储器地址使能增量；M2M 模式下，源地址和目标地址均使能增量。

#### **4. 传输模式（2 种）**

传输模式，特指当 DMA 传输任务完成后，是单次工作即停止还是持续重复工作（循环重复刚才的工作）。

- 正常模式：一次传输完成后（传输计数器减至 0），DMA 停止工作，不再进行新的传输，需重新配置或手动触发才能再次传输。

- 循环模式（Circular Mode）：传输完成后，传输计数器自动重装初始值，DMA 持续重复传输（如 ADC 连续采样、串口循环收发固定长度数据）。

#### **5. 优先级配置**

**4 个优先级等级：非常高（Very High）、高（High）、中（Medium）、低（Low），用于解决多个 DMA 通道同时请求传输时的仲裁顺序：**

- 通道优先级高于通道号（如高优先级通道 1 > 低优先级通道 2）。

- 同优先级下，通道号越小，优先级越高（如中优先级通道 1 > 中优先级通道 2）。

 

### **四、DMA功能框图**

下面图描述了ADC 采集多路通道的电压时，通过DMA搬运数据到数据的过程。

![img](./img/56452.png)

 

**关于DMA外设通道：**

不同DMA控制器的通道对应着不同的外设请求。每个通道拥有独立的配置参数（传输方向、数据宽度、地址增量、传输模式、优先级等），可独立初始化、使能、禁用，一个通道的配置和工作状态不会影响其他通道。例如，DMA1的通道1，就可以用来复杂ADC1数据的搬运。

![img](./img/56453.png)

 

### **五、代码示例**

接下来，我们使用 ADC1 采集通道0的光敏电阻电压、通道1的土壤湿度传感器电压，并且使用DMA帮忙搬数据，实现数据的高效采集。

**1. STM32CubeMX配置**

![img](./img/56454.png)

 

![img](./img/56455.png)

 

![img](./img/56456.png)

 

![img](./img/56457.png)

 

**2. 关键代码**

![img](./img/56458.png)

 

![img](./img/56459.png)

 

![img](./img/56460.png)

 

![img](./img/56461.png)



## DMA常用函数接口

**STM32F103 HAL库 DMA 常用函数接口**

基于 stm32f1xx_hal_dma.c/h，包含初始化、启停、中断回调、状态查询，统一说明：函数原型、功能、参数、返回值。

通用句柄：DMA_HandleTypeDef hdma_x，CubeMX自动生成（如 hdma_usart1_tx、hdma_adc1）

统一返回类型：HAL_StatusTypeDef（HAL_OK / HAL_ERROR / HAL_BUSY / HAL_TIMEOUT）

### **一、DMA初始化/反初始化**

**1. HAL_DMA_Init**

```C
HAL_StatusTypeDef HAL_DMA_Init(DMA_HandleTypeDef *hdma);
```

- 功能：初始化DMA通道参数（传输方向、数据宽度、循环模式、存储器/外设增量、传输长度等）

- 参数：hdma：DMA通道句柄指针

- 返回值：HAL_OK 初始化成功；HAL_ERROR 参数非法

**2. HAL_DMA_DeInit**

```C
HAL_StatusTypeDef HAL_DMA_DeInit(DMA_HandleTypeDef *hdma);
```

- 功能：复位指定DMA通道寄存器，关闭时钟，恢复默认状态

- 参数：DMA句柄指针

- 返回值：HAL_OK / HAL_ERROR

### **二、DMA启动/停止传输**

**（外设联动不单独调用，配套外设XX_DMA函数；纯内存搬运专用）**

**3. HAL_DMA_Start**

```C
HAL_StatusTypeDef HAL_DMA_Start(DMA_HandleTypeDef *hdma, uint32_t SrcAddress, uint32_t DstAddress, uint32_t DataLength);
```

- 功能：阻塞式启动DMA传输（无中断，纯轮询），内存→内存/内存→外设/外设→内存通用

- 参数：

a.hdma：DMA句柄

b.SrcAddress：源地址（外设DR寄存器/内存数组首地址）

c.DstAddress：目标地址

d.DataLength：传输数据长度（单位：DMA设置的数据宽度，字节/半字/字）

- 返回值：HAL_OK 启动成功；HAL_BUSY DMA正在工作；HAL_ERROR 参数错误

**4. HAL_DMA_Start_IT**

```C
HAL_StatusTypeDef HAL_DMA_Start_IT(DMA_HandleTypeDef *hdma, uint32_t SrcAddress, uint32_t DstAddress, uint32_t DataLength);
```

- 功能：中断模式启动DMA，传输完成/半传输/出错触发中断回调

- 参数：同 HAL_DMA_Start

- 返回值：HAL_OK / HAL_BUSY / HAL_ERROR

**5. HAL_DMA_Abort**

```C
HAL_StatusTypeDef HAL_DMA_Abort(DMA_HandleTypeDef *hdma);
```

- 功能：立即终止当前DMA传输，清除传输标志

- 参数：DMA句柄

- 返回值：HAL_OK 停止成功；HAL_TIMEOUT 停止超时；HAL_ERROR

**6. HAL_DMA_Abort_IT**

```C
HAL_StatusTypeDef HAL_DMA_Abort_IT(DMA_HandleTypeDef *hdma);
```

- 功能：中断方式停止DMA，停止后触发传输完成回调

- 参数：DMA句柄

- 返回值：HAL_OK / HAL_BUSY

### **三、传输完成轮询等待**

**7. HAL_DMA_PollForTransfer**

```C
HAL_StatusTypeDef HAL_DMA_PollForTransfer(DMA_HandleTypeDef *hdma, uint32_t CompleteLevel, uint32_t Timeout);
```

- 功能：轮询等待DMA达到指定传输状态

- 参数：

a.hdma：DMA句柄

b.CompleteLevel：等待等级

- HAL_DMA_FULL_TRANSFER：等待全部数据传输完成

- HAL_DMA_HALF_TRANSFER：等待半传输完成

c.Timeout：超时时间(ms)，HAL_MAX_DELAY永久等待

- 返回值：HAL_OK：达到指定传输状态HAL_TIMEOUT：等待超时HAL_ERROR：DMA传输出错

### **四、中断服务与回调函数**

**8. HAL_DMA_IRQHandler**

```C
void HAL_DMA_IRQHandler(DMA_HandleTypeDef *hdma);
```

- 功能：DMA中断入口函数，判断中断标志（半传、全传、传输错误），调用对应回调；在stm32f1xx_it.c中DMA中断服务函数内调用

- 参数：触发中断的DMA通道句柄

- 返回值：无

**9. 三大弱回调函数（用户重写实现业务逻辑）**

```C
__weak void HAL_DMA_TransferCompleteCallback(DMA_HandleTypeDef *hdma);
```

- 功能：DMA**全部数据传输完成**回调

- 参数：DMA句柄

- 返回值：无

```C
__weak void HAL_DMA_HalfTransferCallback(DMA_HandleTypeDef *hdma);
```

- 功能：DMA**半缓冲区传输完成**回调（循环采集、音频数据流常用）

- 参数：DMA句柄

- 返回值：无

```C
__weak void HAL_DMA_ErrorCallback(DMA_HandleTypeDef *hdma);
```

- 功能：DMA传输错误回调（总线错误、模式配置错误时触发）

- 参数：DMA句柄

- 返回值：无

### **五、状态查询工具函数**

**10. HAL_DMA_GetState**

```C
HAL_DMA_StateTypeDef HAL_DMA_GetState(DMA_HandleTypeDef *hdma);
```

- 功能：获取DMA通道当前运行状态

- 参数：DMA句柄

- 返回值（DMA状态枚举）：

- HAL_DMA_STATE_RESET：未初始化

- HAL_DMA_STATE_READY：空闲就绪

- HAL_DMA_STATE_BUSY：正在传输

- HAL_DMA_STATE_TIMEOUT：传输超时

- HAL_DMA_STATE_ERROR：传输异常

**11. HAL_DMA_GetError**

```C
uint32_t HAL_DMA_GetError(DMA_HandleTypeDef *hdma);
```

- 功能：读取DMA错误标志位，定位故障类型

- 参数：DMA句柄

- 返回值：错误掩码（DMA_ERROR_TE 传输错误等）

### **六、补充：外设配套DMA函数**

*（日常开发最常用，不单独操作DMA句柄）**

DMA极少单独调用HAL_DMA_Start，都是通过外设封装接口启动，前面章节已提及，汇总对照：

1. USART DMA收发

```C
HAL_UART_Transmit_DMA();
HAL_UART_Receive_DMA();
```

1. ADC DMA采集

```C
HAL_ADC_Start_DMA();
HAL_ADC_Stop_DMA();
```

1. I2C DMA读写

```C
HAL_I2C_Mem_Write_DMA();
HAL_I2C_Mem_Read_DMA();
HAL_I2C_Master_Transmit_DMA();
HAL_I2C_Master_Receive_DMA();
```

**补充通用返回枚举**

```C
typedef enum
{
  HAL_OK       = 0x00U,
  HAL_ERROR    = 0x01U,
  HAL_BUSY     = 0x02U,
  HAL_TIMEOUT  = 0x03U
} HAL_StatusTypeDef;
```

 

