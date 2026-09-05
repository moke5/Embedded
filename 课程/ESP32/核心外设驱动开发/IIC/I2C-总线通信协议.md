# I2C-总线通信协议

[toc]



## **一、什么是I2C**

IIC（Inter-Integrated Circuit）协议也称为I2C总线，是一种串行通信协议，通常用于连接低速外设。它由Philips（现在的NXP Semiconductors）公司于1980年代初开发，现在已经成为一个标准。IIC总线只需要两条数据线，分别是串行数据线（SDA）和串行时钟线（SCL），这使得它成为一种非常简单的接口。它适用基于芯片的通信，例如连接传感器、存储器或数字信号处理器等。

在IIC协议中，总线上有一个主设备和多个从设备。主设备掌控着总线上的通信过程，负责发起、控制、停止通信。而从设备则需要等待主设备的请求，接收或发送数据。主设备和从设备之间的数据交换采用帧格式，每个帧通常包含地址、数据和控制信息。主设备根据从设备的地址来选中要通信的设备，从设备则根据控制信息进行相应的操作。IIC协议可以支持多个从设备连接到同一个主设备，为系统设计提供了更大的灵活性。

![img](./img/58115.png)

 

## **二、I2C的硬件实现**

I2C总线通常使用两种电压电平，即高电平（VH）和低电平（VL）。高电平为2.5V至5.5V，低电平为0V至0.3V；这些电压电平范围是根据I2C规范确定的。

I2C总线有不同的传输速率可选，包括标准模式（100 kbps）、快速模式（400 kbps）以及高速模式。传输速率的选择取决于应用的需求和设备的支持能力。

为避免信号冲突，微处理器(MCU）必须只能驱动SDA和SCL在低电平，即开漏输出。设置为开漏模式主要是为了保护器件和防止干扰。

- **防止干扰：**多个器件共享同一条数据线（SDA）和同一条时钟线（SCL），如果采用推挽输出模式，多个器件的输出将会叠加在数据线上，造成信号干扰，严重时会损坏器件或导致通信错误。而采用开漏输出模式，则各个器件的输出只有拉低数据线的部分，不会干扰彼此，从而提高了总线的可靠性和抗干扰能力。

- 防止短路：在开漏输出模式下，由于器件的输出只有拉低数据线的部分，如果两个或多个器件同时输出，也不会造成短路。而如果采用推挽输出模式，两个或多个器件同时输出时，可能会形成短路。比如主设备输出高电平，从设备输出低电平。

因设置为开漏模式，需要连接一个外部的上拉电阻（例如:10k)将信号提拉至高电平。故I2C总线中的SDA（数据线）和SCL（时钟线）通常都连接了上拉电阻，以确保逻辑高电平的稳定性。上拉电阻的阻值通常在2.2kΩ至10kΩ之间，具体取决于总线的电容负载和通信距离。

I2C总线的最大线缆长度和传输容量受到一定限制。在标准模式下，最大线缆长度大约在1米左右，而在快速模式下，最大线缆长度约为0.3米。此外，线缆上的总线容量也会对传输速率产生影响。

![img](./img/58103.png)

 

## **三、I2C数据传输**

I2C协议使用总线抢占制进行数据传输。它只有两根通信线，因此它数据传输是基于时钟信号的。时钟由主设备产生，并控制数据的传输速率。数据由主设备发送并接收，但其交换是通过从设备的应答来实现的。

下面是IIC总线的几个重要的时序：

**起始信号：**SCL在高电平的状态下，SDA的电平由高转低，表示开始一次通信。

| ![img](./img/58107.png)**起始信号** | `void IIC_Start(void)``{``    SDA_OUT();//设置SDA为输出模式``    SDA(1);``    SCL(1);         ``    delay_us(5);``    SDA(0);``    delay_us(5);``    SCL(0);``    delay_us(5);         ``}` |
| ----------------------------------- | ------------------------------------------------------------ |
|                                     |                                                              |

**停止信号：**SCL在高电平的状态下，SDA的电平由低转高，表示结束这次通信。主设备在发送停止信号后不能再向从设备发送任何数据，除非再次发送起始信号。

| ![img](./img/58090.png)**发送接收时序**                      |                                                              |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `//发送一个字节``void IIC_Send_Byte(unsigned char dat)``{``    int i = 0;``    SDA_OUT();``    SCL(0);        ``    for( i = 0; i < 8; i++ )``    {``        SDA( (dat & 0x80) >> 7 );``        delay_us(1);``        SCL(1);``        delay_us(5);``        SCL(0);``        delay_us(5);``        dat<<=1;``    }        ``}` | `//接收一个字节``unsigned char IIC_Read_Byte(void)``{``    unsigned char i,receive=0;``    SDA_IN();//SDA设置为输入``    for(i=0;i<8;i++ )``    {``        SCL(0);``        delay_us(5);``        SCL(1);``        delay_us(5);``        receive<<=1;``        if( SDA_GET() == 1 )``        {        ``            receive |= 1;   ``        } ``    }``    SCL(0); ``    return receive;``}` |

I2C还提供了一种称为“ACK/NACK”（应答/非应答）的确认机制。如果一个设备接收到数据，它将通过在SDA线上拉低电平来发送一个应答信号以通知发送方数据已被接收。相反，如果数据被损坏或未接收，接收设备将发送非应答信号。（在SDA上保持高电平）。

| ![img](./img/58075.png)**应答信号**   | ` void IIC_Send_Ack(void)``{``    SDA_OUT();``    SCL(0);``    SDA(1);``    SDA(0);``    SCL(1);``    delay_us(5);``    SCL(0);``    SDA(1);``}` |
| ------------------------------------- | ------------------------------------------------------------ |
| ![img](./img/58087.png)**非应答信号** | `void IIC_Send_Nack(void)``{``    SDA_OUT();``    SCL(0);``    SDA(0);``    SDA(1);``    SCL(1);``    delay_us(5);``    SCL(0);``    SDA(0);``}` |

在IIC总线中，时钟线由主设备控制，每个数据位在时钟边沿更新，传输的最高速率取决于总线上最慢的设备。一般来讲，IIC总线的通信速率比较慢，通常在几百kbps的范围内。如果需要更高的传输速率，可以采用其他通信协议，如SPI协议、CAN协议等。

 

## **四、I2C通信流程**

I2C通信流程按照以下步骤进行：

- 主控向总线发送开始信号。

- 主控将要通信的**设备地址**和**读写位（R/W）**发送到总线上。

- 设备接收到地址后发送应答信号，主控接收到应答信号后发送数据或继续发送地址。

- 设备接收到数据后发送应答信号，主控接收到应答信号后可以继续发送数据或者停止通信。

- 主控向总线发送停止信号。

![img](./img/58099.png)

 

## **五、I2C基本参数**

- **速率：**I2C总线有标准模式（100 kbit/s）和快速模式（400 kbit/s）两种传输模式，还有更快的扩展模式和高速模式可供选择。

- **器件地址：**每个设备都有**唯一的7位**或10位地址，可以通过地址选择来确定与谁进行通信。

- **总线状态：**I2C总线有五种状态，分别是空闲状态、起始信号、结束信号、响应信号、数据传输。

- **数据格式：**I2C总线有两种数据格式，标准格式和快速格式。标准格式是8位数据字节加上1位ack/nack（应答/非应答）位，快速格式允许两个字节同时传输。

由于SCL和SDA线是双向的，它们也可能会由于外部原因（比如线路中的电容等）出现电平误差，而从而导致通信出错。因此，在IIC总线中，通常使用上拉电阻来保证信号线在空闲状态下的电平为高电平。

 

## **六、软件I2C与硬件I2C**

I2C协议可以通过软件实现或者硬件实现。这两种方式的区别在于实现的方法和所需的硬件资源。

### **6.1** **软件I2C**

软件I2C是指通过在程序中编写代码来实现I2C通信协议。它利用通用输入输出（GPIO）引脚来模拟I2C的数据线（SDA）和时钟线（SCL），通过软件控制引脚的电平变化来传输数据和生成时序信号。与硬件I2C相比，软件I2C的优势在于不需要特定的硬件支持，可以在任何支持GPIO功能的微控制器上实现。它利用了微控制器的通用IO引脚来实现I2C通信协议。

软件I2C的实现通过编程方式来模拟I2C的主机和从机设备。通过逐位地读取和写入GPIO引脚的状态，并根据I2C协议的时序要求进行相应的操作，实现数据的传输和通信。软件I2C的灵活性较高，可以根据应用需求进行定制和扩展。它可以处理多个从机设备，并支持多主机环境。因此，软件I2C广泛应用于资源受限的MCU系统，特别是那些需要与多个外部设备进行通信的应用。

尽管软件I2C的性能相对于硬件I2C较低，但在一些低速通信和简单通信需求的场景下，软件I2C是一种经济实用的解决方案。

### **6.2** **硬件I2C**

硬件I2C是指通过专门的硬件模块来处理I2C通信协议。大多数现代微控制器和一些外部设备已经集成了硬件I2C模块，这些硬件模块负责处理I2C通信的细节，包括生成正确的时序信号、自动处理信号冲突、数据传输和错误检测等。可以直接使用硬件引脚连接，无需编写时序的代码。

使用硬件I2C通常相对简单，开发者无需编写复杂的代码来处理通信协议的细节。硬件模块可以直接与外部设备连接，通过专用的引脚进行数据和时钟传输，从而实现高效且可靠的通信。

在选择软件I2C还是硬件I2C时，需要考虑应用需求和硬件资源。软件I2C适用于资源受限的系统，可以在任何支持GPIO的微控制器上实现，但相对性能较低。硬件I2C通常性能更好，但需要硬件支持，并且可能占据一些特定的引脚资源。

### **6.3** **I2C优缺点**

**优点：**

**双向传输：**I2C总线支持双向传输，可以通过SDA线同时传输主设备和从设备之间的数据，节约了总线的资源。

**系统集成：**I2C总线可以快速集成到芯片中，减少系统实现的逻辑复杂性，提高了设计效率。

**多设备共享：**I2C总线可以通过地址传输实现多个设备与主控器的通信，使得多个设备可以共享总线，并直接交互。

**高可靠性：**I2C总线使用逻辑层次的代替电气信号来表示数据传输，具有更高的传输可靠性。

**缺点：**

**带宽不高：**I2C总线的传输速度限制在400 kbps，相比较于SPI总线和CAN总线，带宽相对较低。

**时序要求严格：**I2C总线传输数据需要严格遵循时序要求，特别是在高速传输过程，时序容易受到干扰，造成通信失败。

**最长电缆长度有限：**虽然I2C总线可以通过中继器扩展总线长度，但是由于信号线受到干扰，信号衰减和时序要求等问题，电缆最长长度一般限制在1~2米之间。

总之，I2C总线具有双向传输、系统集成、多设备共享等优点，但传输速度相对较低，时序要求严格且最长电缆长度有限等缺点。

 

## **七、ESP32S3的I2C介绍**

ESP32S3有两个硬件I2C控制器（也称为端口），负责处理两条I2C总线上的通信。每个I2C控制器都可以作为主机或从机运行。ESP32的I2C接口可以配置为主模式或从模式，可以通过简单的API来控制I2C总线上的设备，主要特性如下：

- 支持主机模式和从机模式

- 支持多主机和从机通信

- 支持标准模式 (100 Kbit/s)

- 支持快速模式 (400 Kbit/s)

- 支持 7 位以及 10 位地址寻址

- 支持拉低 SCL 时钟实现连续数据传输

- 支持可编程数字噪声滤波功能

- 支持从机地址和从机内存或寄存器地址的双寻址模式

## **八、I2C的应用**

```C
/*
      使用IIC通信顺序分为 3 个部分【起始部分】【时序部分】【结束部分】
                
                
     【起始部分】相关函数：
                      void IIC_GPIO_Init(void);
                        
     【时序部分】相关函数：
                     i2c_cmd_handle_t i2c_cmd_link_create(void);
                     esp_err_t i2c_master_start(i2c_cmd_handle_t cmd_handle);
                     esp_err_t i2c_master_stop(i2c_cmd_handle_t cmd_handle);
                     esp_err_t i2c_master_write_byte(i2c_cmd_handle_t cmd_handle, uint8_t data, bool ack_en);
                     esp_err_t i2c_master_read_byte(i2c_cmd_handle_t cmd_handle, uint8_t *data, i2c_ack_type_t ack);
                                                                                
                                                                
     【结束部分】相关函数：
                    esp_err_t i2c_master_cmd_begin(i2c_port_t i2c_num, i2c_cmd_handle_t cmd_handle, TickType_t ticks_to_wait);
                    void i2c_cmd_link_delete(i2c_cmd_handle_t cmd_handle);
                                                                
*/
```

### **8.1 初始化 I2C 接口**

```C
/**
 * @brief 初始化 ESP32-S3 的 I2C 主模式总线
 *
 * 配置指定 I2C 外设为主机模式，设置 SDA/SCL 引脚号、上拉使能和通信速率。
 * 完成参数配置后安装 I2C 驱动程序，使能底层硬件。
 *
 * @return esp_err_t
 *         - ESP_OK: I2C 总线初始化成功
 *         - ESP_ERR_INVALID_ARG: 参数错误（如引脚号无效、时钟频率超限等）
 *         - ESP_FAIL: 驱动安装失败（如 I2C 外设已被占用）
 *
 * @note 默认使用 I2C_NUM_0（BSP_I2C_NUM），通信频率 100kHz（BSP_I2C_FREQ_HZ）
 * @note SDA/SCL 引脚使能内部上拉，外部可不再接上拉电阻
 * @note 安装驱动时接收/发送缓冲区和中断标志均设为 0（使用轮询方式通信）
 */
esp_err_t bsp_i2c_init(void)              // I2C总线初始化函数，返回操作结果
{
    i2c_config_t i2c_conf = {             // 创建I2C配置结构体，准备配置参数
        .mode = I2C_MODE_MASTER,          // 设置I2C工作模式：主机模式
        .sda_io_num = BSP_I2C_SDA,        // 设置SDA引脚号（GPIO1）
        .sda_pullup_en = GPIO_PULLUP_ENABLE, // 使能SDA内部上拉电阻
        .scl_io_num = BSP_I2C_SCL,        // 设置SCL引脚号（GPIO2）
        .scl_pullup_en = GPIO_PULLUP_ENABLE, // 使能SCL内部上拉电阻
        .master.clk_speed = BSP_I2C_FREQ_HZ // 设置I2C时钟频率：100kHz
    };
    i2c_param_config(BSP_I2C_NUM, &i2c_conf); // 将配置参数写入I2C_NUM_0控制器
 
    return i2c_driver_install(BSP_I2C_NUM, i2c_conf.mode, 0, 0, 0); // 安装I2C驱动并返回安装结果
}
```

### **8.2 安装 I2C 驱动**

```C
esp_err_t i2c_driver_install(i2c_port_t i2c_num, i2c_mode_t mode, size_t rx_buf_len, size_t tx_buf_len, int intr_flags)
```

调用 i2c_driver_install() 函数，为指定的 I2C 端口号安装 I2C 驱动程序。参数解析如下：

- **i2c_num**: I2C 总线端口号，类型为 i2c_port_t。可选参数有I2C_NUM_0、I2C_NUM_1；

- **mode**:I2C 工作模式，包括 I2C_MODE_MASTER（主模式）、I2C_MODE_SLAVE（从模式）和 I2C_MODE_MASTER_SLAVE（主从模式），类型为 i2c_mode_t。

- **rx_buf_le***: I2C 接收缓冲区长度，单位为字节，只有在从模式才用到，缓存大小必须大于 0，此处使用一个常量 I2C_MASTER_RX_BUF_DISABLE 表示禁用接收缓冲区。

- **tx_buf_len**: I2C 发送缓冲区长度，单位为字节，只有在从模式才用到，缓存大小必须大于 0，此处使用一个常量 I2C_MASTER_TX_BUF_DISABLE 表示禁用发送缓冲区。

- **intr_flags**: I2C 驱动中断标志，用于控制是否支持 I2C 中断处理程序。此处使用一个常量 0 表示不使用中断。

在调用该函数后，I2C 驱动程序会启动，从而可以读取或写入数据到 I2C 总线上的设备。**示例：**



```C
//注册I2C服务即使能
i2c_driver_install(IIC_NUM, conf.mode, I2C_MASTER_RX_BUF_DISABLE, I2C_MASTER_TX_BUF_DISABLE, 0); 
```

### **8.3 I2C 的读写操作**

**8.3.1 写函数**

```C
/**
 * @brief 向连接到特定 I2C 端口的设备执行写操作。
 *        此函数是对 `i2c_master_start()`、`i2c_master_write()`、`i2c_master_read()` 等函数的封装。
 *        仅可在 I2C 主机模式下调用。
 *
 * @param i2c_num          要执行传输的 I2C 端口号
 * @param device_address   I2C 设备的 7 位地址
 * @param write_buffer     要在总线上发送的字节数据
 * @param write_size       写入缓冲区的大小，单位为字节
 * @param ticks_to_wait    在超时之前等待的最大时钟节拍数
 *
 * @return
 *     - ESP_OK           操作成功
 *     - ESP_ERR_INVALID_ARG     参数错误
 *     - ESP_FAIL         发送命令错误，从机未对传输进行 ACK 响应
 *     - ESP_ERR_INVALID_STATE  I2C 驱动程序未安装或未处于主机模式
 *     - ESP_ERR_TIMEOUT  操作超时，因为总线忙
 */
esp_err_t i2c_master_write_to_device(i2c_port_t i2c_num, uint8_t device_address,
                                     const uint8_t* write_buffer, size_t write_size,
                                     TickType_t ticks_to_wait);
```

 

```C
/**
 * @brief 向 QMI8658 指定寄存器写入单字节数据
 *
 * 将寄存器地址和待写入数据组合成 2 字节包，通过 I2C 总线发送给传感器。
 *
 * @param[in] reg_addr  目标寄存器地址（8 位）
 * @param[in] data      要写入寄存器的 8 位数据值
 *
 * @return esp_err_t
 *         - ESP_OK: 写入成功
 *         - ESP_ERR_TIMEOUT: I2C 总线通信超时
 *         - ESP_FAIL: 从设备无应答
 *
 * @note 如需连续写入多个寄存器，可多次调用此函数，或使能地址自动递增功能后
 *       使用 qmi8658_register_read() 的写入部分来实现块写入
 */
esp_err_t qmi8658_register_write_byte(uint8_t reg_addr, uint8_t data) // 写单字节寄存器函数
{
    uint8_t write_buf[2] = {reg_addr, data}; // 构造发送缓冲区：第1字节为寄存器地址，第2字节为写入数据
 
    return i2c_master_write_to_device(       // 通过I2C向器件发送数据
        BSP_I2C_NUM,                         // I2C外设编号：I2C_NUM_0
        QMI8658_SENSOR_ADDR,                 // QMI8658器件I2C地址：0x6A
        write_buf, sizeof(write_buf),        // 发送2字节数据（地址+数据）
        1000 / portTICK_PERIOD_MS            // 通信超时时间（1000个系统Tick）
    );
}
```

 

**8.3.2 写读函数**

```C
/**
 * @brief 对 I2C 总线上的设备执行先写后读操作。
 *        在“写”和“读”之间使用重复起始信号（repeated start），因此总线在两次事务完成之前不会被释放。
 *        此函数是对 `i2c_master_start()`、`i2c_master_write()`、`i2c_master_read()` 等函数的封装。
 *        仅可在 I2C 主机模式下调用。
 *
 * @param i2c_num          要执行传输的 I2C 端口号
 * @param device_address   I2C 设备的 7 位地址
 * @param write_buffer     要在总线上发送的字节数据
 * @param write_size       写入缓冲区的大小，单位为字节
 * @param read_buffer      用于存储总线上接收到的字节数据的缓冲区
 * @param read_size        读取缓冲区的大小，单位为字节
 * @param ticks_to_wait    在超时之前等待的最大时钟节拍数
 *
 * @return
 *     - ESP_OK                 操作成功
 *     - ESP_ERR_INVALID_ARG    参数错误
 *     - ESP_FAIL               发送命令错误，从机未对传输进行 ACK 响应
 *     - ESP_ERR_INVALID_STATE  I2C 驱动程序未安装或未处于主机模式
 *     - ESP_ERR_TIMEOUT        操作超时，因为总线忙
 */
esp_err_t i2c_master_write_read_device(i2c_port_t i2c_num, uint8_t device_address,
                                       const uint8_t* write_buffer, size_t write_size,
                                       uint8_t* read_buffer, size_t read_size,
                                       TickType_t ticks_to_wait);
```

**8.3.3 读函数**

```C
/**
 * @brief 向连接到特定 I2C 端口的设备执行读操作。
 *        此函数是对 `i2c_master_start()`、`i2c_master_write()`、`i2c_master_read()` 等函数的封装。
 *        仅可在 I2C 主机模式下调用。
 *
 * @param i2c_num          要执行传输的 I2C 端口号
 * @param device_address   I2C 设备的 7 位地址
 * @param read_buffer      用于存储总线上接收到的字节数据的缓冲区
 * @param read_size        读取缓冲区的大小，单位为字节
 * @param ticks_to_wait    在超时之前等待的最大时钟节拍数
 *
 * @return
 *     - ESP_OK           操作成功
 *     - ESP_ERR_INVALID_ARG     参数错误
 *     - ESP_FAIL         发送命令错误，从机未对传输进行 ACK 响应
 *     - ESP_ERR_INVALID_STATE  I2C 驱动程序未安装或未处于主机模式
 *     - ESP_ERR_TIMEOUT  操作超时，因为总线忙
 */
esp_err_t i2c_master_read_from_device(i2c_port_t i2c_num, uint8_t device_address,
                                      uint8_t* read_buffer, size_t read_size,
                                      TickType_t ticks_to_wait);
```

  

```C
/**
 * @brief 读取 QMI8658 指定寄存器的值（连续读取）
 *
 * 通过 I2C 总线向 QMI8658 发送寄存器地址，然后读取返回的多字节数据。
 * 利用 I2C 组合帧（写地址 + 读数据）在单次总线事务中完成操作。
 *
 * @param[in]  reg_addr  目标寄存器地址（8 位）
 * @param[out] data      指向数据缓冲区的指针，用于存放读取到的数据
 * @param[in]  len       要读取的字节数（缓冲区大小必须 >= len）
 *
 * @return esp_err_t
 *         - ESP_OK: 读取成功
 *         - ESP_ERR_TIMEOUT: I2C 总线通信超时（当前超时设为 1000 ticks）
 *         - ESP_FAIL: 从设备无应答（NACK）
 *
 * @note QMI8658 的寄存器地址为单字节，寄存器地址自动递增功能由 CTRL1 寄存器控制
 * @note 当 len > 1 且地址自动递增已使能时，可连续读取相邻寄存器
 */
esp_err_t qmi8658_register_read(uint8_t reg_addr, uint8_t *data, size_t len) // 读寄存器函数
{
    return i2c_master_write_read_device(   // I2C组合事务：先写寄存器地址，再读取数据
        BSP_I2C_NUM,                       // I2C外设编号：I2C_NUM_0
        QMI8658_SENSOR_ADDR,               // QMI8658器件I2C地址：0x6A
        &reg_addr, 1,                      // 发送1字节寄存器地址
        data, len,                         // 读取len字节数据存入缓冲区
        1000 / portTICK_PERIOD_MS          // 通信超时时间（1000个系统Tick）
    );
}
```

**文件路径：frameworks\esp-idf-v5.2.2\components\driver\i2c\include\driver\i2c.h**



## **九、新版的I2C函数接口**

### **9.1 数据结构**

**1.I2C 主总线配置结构体**

```C
/**
 * @brief I2C 主总线配置结构体
 * 
 * 用于配置 I2C 主总线的各项参数，创建总线前需填充该结构体。
 */
typedef struct {
    i2c_port_num_t i2c_port;             /**< I2C 端口号，设置为 -1 时由驱动自动分配 */
    gpio_num_t sda_io_num;               /**< SDA 数据线 GPIO 引脚号 */
    gpio_num_t scl_io_num;               /**< SCL 时钟线 GPIO 引脚号 */
    i2c_clock_source_t clk_source;       /**< I2C 总线时钟源，同一组通道必须使用相同时钟源 */
    uint8_t glitch_ignore_cnt;           /**< 毛刺过滤阈值，典型值为 7（单位：I2C 模块时钟周期） */
    int intr_priority;                   /**< 中断优先级，设为 0 时驱动选择默认优先级（1/2/3） */
    size_t trans_queue_depth;            /**< 内部传输队列深度，增大可支持更多异步挂起事务 */
    struct {
        uint32_t enable_internal_pullup: 1; /**< 是否使能内部上拉电阻（高频下建议使用外部上拉） */
    } flags;
} i2c_master_bus_config_t;
```

**2.I2C 从设备配置结构体**

```C
/**
 * @brief I2C 从设备配置结构体
 * 
 * 用于配置挂载在 I2C 总线上的具体从设备参数，添加设备前需填充该结构体。
 */
typedef struct {
    i2c_addr_bit_len_t dev_addr_length;  /**< 设备地址长度，如 I2C_ADDR_BIT_LEN_7 或 I2C_ADDR_BIT_LEN_10 */
    uint16_t device_address;             /**< 从设备原始地址（7 位或 10 位，不含读/写位） */
    uint32_t scl_speed_hz;               /**< 该设备的 SCL 时钟频率（Hz） */
    uint32_t scl_wait_us;                /**< SCL 等待时间（微秒），0 表示不等待 */
    struct {
        uint32_t disable_ack_check: 1;   /**< 是否禁用 ACK 检查，0 表示启用检查 */
    } flags;
} i2c_device_config_t;
 
```

### **9.2 接口函数**

**1.创建 I2C 主总线实例**

```C
/**
 * @brief 创建 I2C 主总线实例
 * 
 * 分配并初始化一个新的 I2C 主总线，返回总线句柄供后续操作使用。
 *
 * @param bus_config        指向 I2C 主总线配置结构体的指针
 * @param ret_bus_handle    返回的 I2C 总线句柄指针
 *
 * @return
 *     - ESP_OK             操作成功
 *     - ESP_ERR_INVALID_ARG    参数无效
 *     - ESP_ERR_NO_MEM     内存不足，创建失败
 *     - ESP_ERR_NOT_FOUND  无可用的空闲总线
 */
esp_err_t i2c_new_master_bus(const i2c_master_bus_config_t *bus_config,
                             i2c_master_bus_handle_t *ret_bus_handle);
```

 

**2.将 I2C 从设备添加到已创建的主总线上**

```C
/**
 * @brief 将 I2C 从设备添加到已创建的主总线上
 * 
 * 为指定的从设备分配设备句柄，后续对该设备的读写操作均需使用此句柄。
 *
 * @param bus_handle        已创建的 I2C 主总线句柄
 * @param dev_config        指向从设备配置结构体的指针
 * @param ret_dev_handle    返回的从设备句柄指针
 *
 * @return
 *     - ESP_OK             操作成功
 *     - ESP_ERR_INVALID_ARG    参数无效
 *     - ESP_ERR_NO_MEM     内存不足，添加失败
 */
esp_err_t i2c_master_bus_add_device(i2c_master_bus_handle_t bus_handle,
                                    const i2c_device_config_t *dev_config,
                                    i2c_master_dev_handle_t *ret_dev_handle);
 
```

 

**3.执行 I2C 写-读组合传输（先写后读）**

```C
/**
 * @brief 执行 I2C 写-读组合传输（先写后读）
 * 
 * 该函数用于典型的寄存器读操作：先向从设备写入寄存器地址，然后从该寄存器读取数据。
 * 若通过回调注册了异步模式，则该函数非阻塞，完成信息通过回调获取。
 *
 * @param dev_handle        从设备句柄（由 i2c_master_bus_add_device 获得）
 * @param write_buffer      待发送的写数据缓冲区指针（通常为寄存器地址）
 * @param write_size        写数据长度（字节数）
 * @param read_buffer       用于存储读取数据的缓冲区指针
 * @param read_size         需读取的数据长度（字节数）
 * @param xfer_timeout_ms   传输超时时间（毫秒），-1 表示一直等待
 *
 * @return
 *     - ESP_OK             操作成功
 *     - ESP_ERR_INVALID_ARG    参数无效
 *     - ESP_ERR_TIMEOUT    操作超时（总线忙或硬件故障）
 */
esp_err_t i2c_master_transmit_receive(i2c_master_dev_handle_t dev_handle,
                                      const uint8_t *write_buffer,
                                      size_t write_size,
                                      uint8_t *read_buffer,
                                      size_t read_size,
                                      int xfer_timeout_ms);
 
```

 

**文件路径：frameworks\esp-idf-v5.5\components\esp_driver_i2c\include\driver\i2c_master.h**

**迁移提示**：在 ESP-IDF v5.5 中，旧版 i2c_master_write_read_device 已更名为 i2c_master_transmit_receive，且不再使用命令链表（i2c_cmd_link_xxx）方式，直接调用上述接口即可完成 I2C 通信。

 

### **9.3 新版I2C的设计思路**

新版 I2C 驱动的设计思路发生了根本性变化：**从“先安装驱动，再配置总线”转变为“先创建总线实例，再挂载设备”**。这种“总线-设备”分层模型让驱动管理更清晰，也解决了旧版驱动的一些痛点。

**9.3.1 新版 I2C 添加设备的思路：先总线，后设备**

这个思路将操作流程分为清晰的“两步走”，整个过程围绕 i2c_master_bus_handle_t（总线句柄）和 i2c_master_dev_handle_t（设备句柄）展开。

- **第一步：初始化 I2C 总线**，获得总线句柄 bus_handle。这就像给 I2C 通信“修路”，配置好引脚、时钟和速度等核心参数。

```C
i2c_master_bus_handle_t bus_handle;
i2c_master_bus_config_t bus_cfg = {
    .i2c_port = I2C_NUM_0,
    .sda_io_num = GPIO_NUM_21,
    .scl_io_num = GPIO_NUM_22,
    .clk_source = I2C_CLK_SRC_DEFAULT,
    .glitch_ignore_cnt = 7,
    .flags.enable_internal_pullup = true,
};
ESP_ERROR_CHECK(i2c_new_master_bus(&bus_cfg, &bus_handle));
```

- **第二步：在已创建的总线上添加 I2C 设备**，得到设备句柄 dev_handle。这就像在修好的“路”上为具体设备“设站”，只关注该设备的地址和通信速率。

```C
i2c_master_dev_handle_t dev_handle;
i2c_device_config_t dev_cfg = {
    .dev_addr_length = I2C_ADDR_BIT_LEN_7,
    .device_address = 0x3C, // 设备地址
    .scl_speed_hz = 400000, // 该设备速率
};
ESP_ERROR_CHECK(i2c_master_bus_add_device(bus_handle, &dev_cfg, &dev_handle));
 
```

- **后续读写**：获得设备句柄后，使用 i2c_master_transmit()、i2c_master_receive() 等进行通信。

这个流程更加直观，并且当总线上有多个设备时，可以分别为每个设备调用 i2c_master_bus_add_device，共享同一个 bus_handle。

**9.3.2 新版 I2C 驱动的主要优点**

1. **API 更简洁，编程更高效**：最大的变化是**彻底取消了旧版复杂的命令链表（i2c_cmd_link_xxx）操作方式**。在新版中，读写等操作只需调用单一函数即可完成，极大地简化了代码，降低了编程门槛。

1. **架构更清晰，易于理解**：将“总线”和“设备”的概念在 API 层面分离，更符合 I2C 通信的物理拓扑结构。这种分层模型使得代码结构更清晰，也便于管理多设备场景。

1. **性能更优，资源利用率高**：这是新版驱动的一个核心改进。

- **通信速度更快**：根据社区测试数据，新版驱动在同等条件下（如ESP32-S3 @ 240MHz，1MHz I2C时钟），执行同样任务的速度相比旧版提升了约 **30%**。

- **代码体积更小**：由于内部实现更精简，新版驱动编译后的固件体积也有所减小。

1. **线程安全，更适合RTOS**：新版驱动在设计上考虑了多任务环境，接口是线程安全的（Thread-safe），可以直接在FreeRTOS的不同任务中调用，无需额外加锁。

**9.3.3 功能变更速查**

为了方便从旧版迁移，这里也整理了一些核心 API 的名称变更：

| **旧版 API (driver/i2c.h)**    | **新版 API (driver/i2c_master.h)** |
| ------------------------------ | ---------------------------------- |
| i2c_driver_install()           | **i2c_new_master_bus()**(概念变更) |
| i2c_param_config()             | 合并到 i2c_master_bus_config_t     |
| i2c_master_write_to_device()   | **i2c_master_transmit()**          |
| i2c_master_read_from_device()  | **i2c_master_receive()**           |
| i2c_master_write_read_device() | **i2c_master_transmit_receive()**  |
| i2c_cmd_link_create()          | 已移除，无需手动创建               |
| i2c_master_cmd_begin()         | 已移除，由新读写函数内部完成       |

总的来说，新版 I2C 驱动通过更先进的架构设计，在易用性、性能和资源占用上都带来了显著的提升。

 

## **十、旧驱动提示**

 

**程序运行打印信息1：i2c: This driver is an old driver, please migrate your application code to adapt `driver/i2c_master.h`**

**程序运行打印信息2：i2c: CONFLICT! driver_ng is not allowed to be used with this old driver**

 

这个警告信息的意思是，你的项目（或它所依赖的某个组件）正在使用 ESP-IDF 中的旧版 I2C 驱动 (driver/i2c.h)，而 ESP-IDF 从 v5.2 版本开始就推荐使用功能更强、设计更现代的新版 I2C 驱动 (driver/i2c_master.h)。

 

**警告产生的原因和影响**

- **为什么会发生？**

- **你或你使用的组件**（如第三方传感器、摄像头、音频Codec驱动等）的代码，调用的是旧版 I2C 驱动的 API。

- 你使用的 **ESP-IDF 版本较新** (v5.2及以上)，框架开始提醒开发者进行迁移。

- **潜在风险：新旧驱动冲突 (可能导致崩溃)**

新旧驱动在 ESP-IDF v5.3+ 中**不能共存**。如果你的工程中，一部分代码用了新驱动，另一部分用了旧驱动，可能会在运行时触发 E (1050) i2c: CONFLICT! driver_ng is not allowed to be used with this old driver 这样的**严重错误并导致程序崩溃 (abort)** 。因此，整个工程必须统一使用同一版本的 I2C 驱动 。

- **未来的必然性：旧驱动将被彻底移除**

旧版 I2C 驱动 (driver/i2c.h) 已在 ESP-IDF v6.0 中标记为**生命周期终止 (End-of-Life, EOL)**，并计划在 v7.0 中彻底移除 。这意味着现在不迁移，未来将无法编译。

**解决方案**

解决这个问题有三种主要途径，你可以根据情况选择。

### **方案一：迁移你的应用代码到新驱动 (推荐，一劳永逸)**

这是最根本的解决办法。如果你的项目代码直接调用了 I2C 驱动，你应该主动进行迁移。

1. **修改包含的头文件**：将 #include "driver/i2c.h" 替换为 #include "driver/i2c_master.h"。

1. **更新 CMakeLists.txt**：在 CMakeLists.txt 中，将 REQUIRES driver 替换为 REQUIRES esp_driver_i2c 。

1. **重写代码逻辑**：新版驱动的 API 发生了很大变化，你需要重写 I2C 初始化、读写等流程。

- **核心变化**：不再需要创建命令链表 (i2c_cmd_link_xxx)，直接调用新的函数即可 。

- **初始化流程**：

1. 用 i2c_new_master_bus() 初始化总线。

1. 用 i2c_master_bus_add_device() 添加设备并获取设备句柄。

- **主要函数名变更**：

- i2c_master_write_read_device() → i2c_master_transmit_receive()

- i2c_master_write_to_device() → i2c_master_transmit()

- i2c_master_read_from_device() → i2c_master_receive()

**有些模块还需要进入SDK配置编辑器进行设置新老版本的I2C驱动，如下图。**

![img](./img/58095.png)

 

### **方案二：暂时忽略警告并强制使用旧驱动 (临时方案，有风险)**

如果项目依赖的第三方库（如 esp-idf-lib 等）暂时无法更新，你可能需要一个临时过渡方案。

1. **检查并统一驱动类型**：确保整个工程的所有组件，包括ESP-IDF组件和你的代码，都配置为使用**旧驱动**。

1. **通过** **menuconfig** **强制旧驱动**：在配置中，可能有选项可以强制旧驱动或禁用新驱动，例如：

- Component config → Audio Code Device Configuration 中若有类似 "Enable backward compatibility for the I2c driver" 的选项，可以启用它（此为旧驱动兼容模式）。

1. **抑制编译警告**：如果你只想在编译时消除这个警告，可以在 menuconfig 中启用：

- Component config → Legacy Driver Configurations → Legacy I2C Driver Configurations → Suppress legacy driver deprecated warning 。

**注意**：此方法仅隐藏警告，不解决新旧驱动共存时的冲突问题，冲突依然会导致运行时崩溃。

### **方案三：降级 ESP-IDF 版本 (不推荐)**

如果迁移工作量巨大且时间紧迫，可以暂时退回到旧版驱动仍被视为主流且没有警告的版本（例如 v5.1.x）。但这会让你错过新版本的功能和修复，从长远来看不可取。

**总结与建议**

- **首选方案**是**方案一**。尽早将代码迁移到新版 I2C 驱动，是面向未来的最佳实践。

- **如果遇到第三方库问题**，可以检查该库是否已提供新驱动支持（例如 esp32-camera 库在 v5.4+ 已提供新版驱动），或主动为它们贡献代码进行迁移 。

- **避免混合使用**新旧驱动。在彻底完成迁移前，请确保整个工程**统一**使用旧驱动，以规避 CONFLICT 错误导致的崩溃 。 