# SPI液晶显示

[toc]



## **一、液晶显示**

液晶显示屏（LCD）用于数字型钟表和许多便携式计算机的一种显示器类型。

开发板上的液晶屏是 3.5 寸的 IPS 高清液晶屏，480x320分辨率为65K 色，显示色彩丰富。

特点描述：

- 升级采用 IPS 全视角面板，可视角度佳

- 板载电平转换电路，兼容 5V 和 3.3V MCU

- 采用 4 线制 SPI 串行总线，节约 I/O 引脚

- 模块可选 电容触摸/无触摸 功能

- 模块输入支持 2.54 排针接口和 FPC 外延接口

- 自带 micro TF 卡槽，方便扩展存储

- 提供底层驱动技术支持,WIKI 资料在线更新

- 模块老化测试多重检测可达军工级标准，支持长期稳定工作

液晶屏驱动芯片 ST7796U，采用 SPI 通信方式与 ESP32-S3 连接，本例实现了液晶屏的驱动、整屏显示一个颜色、以及显示图片。

![img](./img/58130.png)

**1.原理图**

![img](./img/58134.png)

![img](./img/58149.png)

 

**模块引脚列表与功能说明**

| **引脚编号** | **引脚名称** | **类型** | **连接说明**              | **功能描述**                                                 |
| ------------ | ------------ | -------- | ------------------------- | ------------------------------------------------------------ |
| 1            | VCC          | 电源     | VBUS                      | 模块主电源输入，当前为 5V                                    |
| 2            | GND          | 电源     | GND                       | 电源地                                                       |
| 3            | LCD_CS       | 输入     | 通过电阻（R53）上拉到 3V3 | LCD 片选信号（低电平有效），用于选择 LCD 控制器进行 SPI 通信 |
| 4            | LCD_RST      | 输入     | 外部复位源（RESET）       | LCD 硬件复位引脚（低电平复位）                               |
| 5            | LCD_RS       | 输入     | IO39_LCD_DC               | LCD 数据/命令选择引脚（DC），高电平为数据，低电平为命令      |
| 6            | SDI(MOSI)    | 输入     | IO40_LCD_MOSI             | SPI 主出从入数据线，用于向 LCD 发送数据或命令                |
| 7            | SCK          | 输入     | IO41_LCD_SCK              | SPI 时钟信号，由主控提供                                     |
| 8            | LED          | 输出控制 | IO42_LCD_BL               | 背光控制引脚                                                 |
| 9            | SDO(MISO)    | 输出     | LCD_MISO（接主控 MISO）   | SPI 主入从出数据线，用于从 LCD 读取状态或数据                |
| 10           | CTP_SCL      | 输入     | IO2_I2C_SCL               | 触摸屏 I2C 时钟线                                            |
| 11           | CTP_RST      | 输入     | RESET（共用系统复位）     | 触摸屏复位引脚（低电平复位）                                 |
| 12           | CTP_SDA      | 双向     | IO1_I2C_SDA               | 触摸屏 I2C 数据线                                            |
| 13           | CTP_INT      | 输入     | IO10                      | 触摸屏中断线                                                 |

 

**2.接口位置**

![img](./img/58104.png)

 

**3.实物图**

![img](./img/58108.png)

**1.1 使用例程**[](https://wiki.lckfb.com/zh-hans/szpi-esp32s3/beginner/lcd-display.html#_9-1-使用例程)

**1.示例工程如下：**

![img](./img/58142.png)

连接开发板到电脑，在 VSCode 上选择串口号，选择目标芯片为 esp32s3，串口下载成功后，开发板液晶屏上会轮流显示图片和不同的颜色

**1.2 例程讲解**

**1.2.1 app_main函数**[](https://wiki.lckfb.com/zh-hans/szpi-esp32s3/beginner/lcd-display.html#_9-2-例程讲解)

点击打开 main.c 文件，找到 app_main 函数，此函数是FreeRTOS任务的入口点，系统启动后自动调用，负责初始化所有硬件外设并启动主循环。

```C
void app_main(void)
{
    // 初始化I2C总线，用于与外部设备通信
    bsp_i2c_init(); 
 
    // 初始化PCA9557 I/O扩展芯片，扩展GPIO功能
    pca9557_init(); 
 
    // 初始化SPI接口LCD显示屏，配置通信参数
    bsp_lcd_init();   
    
    // 输出初始化完成日志信息
    ESP_LOGI(TAG, "LCD初始化完成");  
    
    // 设置LCD显示颜色为白色(RGB565格式: 0xFFFF)
    lcd_set_color(0xFFFF);          
    
    // 在屏幕指定位置绘制粤嵌Logo图片
    lcd_draw_pictrue(149, 112, 182, 96, g_image_logo_gec_182x96); 
 
    /**
     * @brief 主循环 - 持续运行的程序逻辑
     *
     * 循环执行以下操作:
     * 1. 设置颜色并显示Logo图片
     * 2. 延时2秒
     * 3. 切换颜色并延时
     * 4. 重复步骤1-3
     */
    while (1)
    {
        // 设置显示颜色为白色(RGB565: 0xFFFF)
        lcd_set_color(0xFFFF);   
        
        // 在坐标(149,112)处绘制182x96像素的Logo
        lcd_draw_pictrue(149, 112, 182, 96, g_image_logo_gec_182x96); 
 
        // 延时2000毫秒(2秒)，portTICK_PERIOD_MS为系统节拍周期
        vTaskDelay(2000 / portTICK_PERIOD_MS);                        
 
         // 设置显示颜色为绿色(RGB565: 0xFF00)
        lcd_set_color(0xFF00);   
        
        // 延时2000毫秒(2秒)
        vTaskDelay(2000 / portTICK_PERIOD_MS); 
 
        // 设置显示颜色为粉色(RGB565: 0x0FF0)
        lcd_set_color(0x0FF0);      
        
        // 延时2000毫秒(2秒)
        vTaskDelay(2000 / portTICK_PERIOD_MS); 
    }
}
```

液晶屏的 LCD_CS 引脚由 IO 扩展芯片 pca9557 控制，所以需要先初始化 pca9557，而 pca9557 是 i2c 通信芯片，所以又需要先初始化 i2c。

**1.2.2** **bsp_lcd_init****函数**[****](https://wiki.lckfb.com/zh-hans/szpi-esp32s3/beginner/lcd-display.html#_9-2-例程讲解)﻿

鼠标选中 bsp_lcd_init() 函数，位于 esp32_s3_gec.c 文件中。

```
// LCD显示初始化函数，用于完成液晶屏的完整初始化流程
esp_err_t bsp_lcd_init(void)
{
    // 定义返回值变量，初始化为ESP_OK表示成功
    esp_err_t ret = ESP_OK;
 
    // 调用液晶屏驱动初始化函数，初始化SPI总线和LCD驱动芯片
    ret = bsp_display_new();
    // 设置整屏背景颜色为白色，0xFFFF表示RGB565格式的白色
    lcd_set_color(0xFFFF);
    // 打开液晶屏显示，使能LCD显示功能
    ret = esp_lcd_panel_disp_on_off(panel_handle, true);
    // 打开背光显示，将背光亮度设置为100%
    ret = bsp_display_backlight_on();
 
    // 返回初始化结果
    return ret;
}
```

液晶屏显示的开关有两个，一个是 esp_lcd_panel_disp_on_off()，一个是 bsp_display_backlight_on()。

它们的区别是：

esp_lcd_panel_disp_on_off() 用来控制的是液晶屏的驱动芯片中的寄存器，控制液晶屏显示与否；

bsp_display_backlight_on() 用来控制液晶屏 LED 背光，通过调节 PWM 占空比调节亮度，使用的是 LEDC 外设产生的 PWM 信号。

这两个都打开，才能看到液晶屏显示的内容。

**1.2.3** **bsp_display_new函数**

bsp_display_new() 函数用于初始化液晶屏驱动，该函数也位于 esp32_s3_gec.c 文件中。

```
// 液晶屏初始化函数，用于初始化SPI总线和LCD驱动芯片
esp_err_t bsp_display_new(void)
{
    // 定义液晶屏面板IO句柄，用于SPI通信的IO操作
    esp_lcd_panel_io_handle_t io_handle = NULL;
    // 定义返回值变量，初始化为ESP_OK表示成功
    esp_err_t ret = ESP_OK;
    // 调用背光初始化函数，如果初始化失败则直接返回错误
    bsp_display_brightness_init();
   
    // 定义SPI总线配置结构体，用于配置SPI总线的各项参数
    const spi_bus_config_t buscfg = {
        // 设置SPI时钟引脚为BSP_LCD_SPI_CLK宏定义的GPIO引脚
        .sclk_io_num = BSP_LCD_SPI_CLK,
        // 设置SPI主输出从输入引脚为BSP_LCD_SPI_MOSI宏定义的GPIO引脚
        .mosi_io_num = BSP_LCD_SPI_MOSI,
        // 设置SPI主输入从输出引脚为未连接，因为LCD不需要MISO
        .miso_io_num = GPIO_NUM_NC,
        // 设置SPI写保护引脚为未连接，不使用四线SPI模式
        .quadwp_io_num = GPIO_NUM_NC,
        // 设置SPI保持引脚为未连接，不使用四线SPI模式
        .quadhd_io_num = GPIO_NUM_NC,
        // 设置最大传输大小为整个屏幕的像素数据大小，用于DMA传输
        .max_transfer_sz = BSP_LCD_H_RES * BSP_LCD_V_RES * sizeof(uint16_t),
    };
    // 初始化SPI总线，传入SPI总线号、配置结构体和DMA通道自动选择
    ESP_RETURN_ON_ERROR(spi_bus_initialize(BSP_LCD_SPI_NUM, &buscfg, SPI_DMA_CH_AUTO), TAG, "SPI init failed");
 
    // 定义液晶屏面板IO的SPI配置结构体，用于配置SPI通信参数
    const esp_lcd_panel_io_spi_config_t io_config = {
        // 设置数据命令选择引脚为BSP_LCD_DC宏定义的GPIO引脚
        .dc_gpio_num = BSP_LCD_DC,
        // 设置片选引脚为BSP_LCD_SPI_CS宏定义的GPIO引脚
        .cs_gpio_num = BSP_LCD_SPI_CS,
        // 设置SPI时钟频率为BSP_LCD_PIXEL_CLOCK_HZ宏定义的频率值
        .pclk_hz = BSP_LCD_PIXEL_CLOCK_HZ,
        // 设置LCD命令位宽为LCD_CMD_BITS宏定义的位宽
        .lcd_cmd_bits = LCD_CMD_BITS,
        // 设置LCD参数位宽为LCD_PARAM_BITS宏定义的位宽
        .lcd_param_bits = LCD_PARAM_BITS,
        // 设置SPI模式为3，即CPOL=1 CPHA=1
        .spi_mode = 3,
        // 设置传输队列深度为10，用于缓存SPI传输事务
        .trans_queue_depth = 10,
    };
    // 创建新的液晶屏面板IO，传入SPI总线句柄、IO配置和IO句柄指针
    esp_lcd_new_panel_io_spi((esp_lcd_spi_bus_handle_t)BSP_LCD_SPI_NUM, &io_config, &io_handle);
 
    // 定义液晶屏面板设备配置结构体，用于配置LCD驱动芯片参数
    const esp_lcd_panel_dev_config_t panel_config = {
        // 设置复位引脚为BSP_RST宏定义的GPIO引脚
        .reset_gpio_num = BSP_LCD_RST,
        // 设置RGB元素顺序为BGR，即蓝绿红顺序
        .rgb_ele_order = LCD_RGB_ELEMENT_ORDER_BGR,
        // 设置每个像素的位数为BSP_LCD_BITS_PER_PIXEL宏定义的位数
        .bits_per_pixel = BSP_LCD_BITS_PER_PIXEL,
    };
    // 如果定义了LCD_DRIVER_ST7789V2宏，则初始化ST7789驱动芯片
#ifdef LCD_DRIVER_ST7789V2
    // 创建新的ST7789液晶屏面板，传入IO句柄、面板配置和面板句柄指针
    ESP_GOTO_ON_ERROR(esp_lcd_new_panel_st7789(io_handle, &panel_config, &panel_handle), err, TAG, "New panel failed");
// 如果定义了LCD_DRIVER_ST7796宏，则初始化ST7796驱动芯片
#elifdef LCD_DRIVER_ST7796
    // 创建新的ST7796液晶屏面板，传入IO句柄、面板配置和面板句柄指针
    ESP_GOTO_ON_ERROR(esp_lcd_new_panel_st7796(io_handle, &panel_config, &panel_handle), err, TAG, "New panel failed");
#endif
 
    // 复位液晶屏，发送复位信号使LCD进入初始状态
    esp_lcd_panel_reset(panel_handle);
    // 拉低片选引脚，选中LCD设备进行通信
    lcd_cs(0);
    // 初始化液晶屏，配置LCD的内部寄存器
    esp_lcd_panel_init(panel_handle);
    // 反转颜色，使显示颜色与预期一致
    esp_lcd_panel_invert_color(panel_handle, true);
    // 交换XY轴，调整显示方向
    esp_lcd_panel_swap_xy(panel_handle, true);
    // 镜像显示，水平和垂直方向都进行镜像
    esp_lcd_panel_mirror(panel_handle, true, true);
 
    // 返回初始化结果
    return ret;
 
// 错误处理标签，当初始化失败时跳转到此处进行资源清理
err:
    // 如果面板句柄不为空，则删除面板句柄释放资源
    if (panel_handle)
    {
        // 删除液晶屏面板句柄
        esp_lcd_panel_del(panel_handle);
    }
    // 如果IO句柄不为空，则删除IO句柄释放资源
    if (io_handle)
    {
        // 删除液晶屏面板IO句柄
        esp_lcd_panel_io_del(io_handle);
    }
    // 释放SPI总线资源
    spi_bus_free(BSP_LCD_SPI_NUM);
    // 返回错误码
    return ret;
}
```

先是背光初始化，然后初始化 SPI 总线，液晶屏与 esp32 采用 SPI 通信，然后初始化其它控制引脚以及配置参数，最后控制液晶屏显示方式。

背光初始化 bsp_display_brightness_init() 函数，也位于 esp32_s3_gec.c 文件中，原理是把控制背光的引脚初始化成 PWM 引脚，通过控制 PWM 的占空比，控制液晶屏的亮度。

最后几个控制显示的函数，是根据我们开发板的显示调整了一下方向。

esp_lcd_panel_swap_xy() 函数控制 xy 坐标翻转，第 2 个参数，true 表示翻转，false 表示不翻转。

esp_lcd_panel_mirror() 函数控制 xy 方向是否镜像。第 2 个参数控制 x 方向，第 3 个参数控制 y 方向，true 表示镜像，false 表示不镜像。

**1.2.4 lcd_set_color函数**

显示背景色的函数 lcd_set_color，这个函数也位于 esp32_s3_gec.c 文件中，代码如下所示：

```
// 设置液晶屏颜色函数，用于将整个屏幕填充为指定的颜色
void lcd_set_color(uint16_t color)
{
    // 在外部SPIRAM中分配内存，分配液晶屏一行数据所需的大小
    uint16_t *buffer = (uint16_t *)heap_caps_malloc(BSP_LCD_H_RES * sizeof(uint16_t), MALLOC_CAP_8BIT | MALLOC_CAP_SPIRAM);
 
    // 检查内存分配是否成功
    if (NULL == buffer)
    {
        // 打印错误日志，提示内存不足
        ESP_LOGE(TAG, "Memory for bitmap is not enough");
        return;
    }
 
    // 循环遍历缓冲区的每个像素，将指定颜色填入缓冲区
    for (size_t i = 0; i < BSP_LCD_H_RES; i++)
    {
        // 将指定颜色值赋给缓冲区的当前位置
        buffer[i] = color;
    }
    // 循环遍历屏幕的每一行，将缓冲区的颜色数据绘制到屏幕上
    for (int y = 0; y < BSP_LCD_V_RES; y++)
    {
        // 在屏幕的指定行绘制缓冲区的颜色数据
        esp_lcd_panel_draw_bitmap(panel_handle, 0, y, BSP_LCD_H_RES, y + 1, buffer);
    }
    // 释放之前分配的内存，避免内存泄漏
    free(buffer);
 
}
```

这个函数，用来给整个液晶屏显示同一个颜色。

最开始分配了一块内存，BSP_LCD_H_RES 是液晶屏的宽度，即 320。RGB565 模式，每个像素点占用 2 个字节，所以 BSP_LCD_H_RES * sizeof(uint16_t)实际上就是液晶屏显示一行数据需要的内存大小。

MALLOC_CAP_8BIT 表示数据允许以 8 位或 16 位访问。MALLOC_CAP_SPIRAM 表示数据存储到 SPIRAM 中。

后面第 1 个 for 循环，给刚才开辟的内容都写上要显示的颜色数据。第 2 个 for 循环，显示整屏颜色。

esp_lcd_panel_draw_bitmap() 函数和刚才的 esp_lcd_panel_swap_xy() 等函数，都位于 esp-idf 的组件中，打开 esp-idf 整个工程，可以找到它们的源代码。

esp_lcd_panel_draw_bitmap() 函数，第 1 个参数指向液晶屏句柄，第 2 个参数表示 x 坐标的开始位置，第 3 个参数表示 y 坐标的开始位置，第 4 个参数表示 x 坐标的结束位置，第 5 个参数表示 y 坐标的结束位置，第 6 个参数表示要写入的颜色数据。分析这个 for 循环，每次调用一次这个函数，都会显示一行颜色，一共调用320 次，就显示了整屏颜色。

**1.2.5 lcd_draw_pictrue**

lcd_draw_pictrue() 函数用来显示一张图片，这个代码定义也位于 esp32_s3_gec.c 中。

```
// 显示图片函数，用于在LCD屏幕的指定位置显示图片
void lcd_draw_pictrue(int x_start, int y_start, int image_width, int image_height, const unsigned char *gImage)
{
    // 计算图片数据所需的字节数，每个像素占用2字节（RGB565格式）
    size_t pixels_byte_size = image_width * image_height * 2;
    // 在外部SPIRAM中分配内存，指定内存能力为8位可访问和SPIRAM
    uint16_t *pixels = (uint16_t *)heap_caps_malloc(pixels_byte_size, MALLOC_CAP_8BIT | MALLOC_CAP_SPIRAM);
    // 检查内存分配是否成功
    if (NULL == pixels)
    {
        // 打印错误日志，提示内存不足
        ESP_LOGE(TAG, "Memory for bitmap is not enough");
        // 内存分配失败，直接返回
        return;
    }
    // 将图片数据从源地址复制到分配的内存中
    memcpy(pixels, gImage, pixels_byte_size);
    // 计算图片显示的结束X坐标
    int x_end = x_start + image_width;
    // 计算图片显示的结束Y坐标
    int y_end = y_start + image_height;
    // 在LCD屏幕的指定区域绘制图片数据
    esp_lcd_panel_draw_bitmap(panel_handle, x_start, y_start, x_end, y_end, (uint16_t *)pixels);
    // 释放之前分配的内存，避免内存泄漏
    heap_caps_free(pixels);
}
```

函数的前 4 个参数，可以指定图片的起始位置和结束位置，第 5 个参数，传入图片数组名称。

这个显示图片的函数，和刚才显示整屏颜色的函数，有些类似。

首先，计算这张图片的像素大小，赋值给 pixels_byte_size，后面分配内存和拷贝内存的时候要用。

然后，分配整张图片所需字节大小的内存，使用 heap_caps_malloc。

接下来，memcpy()函数把图片数据拷贝到内存，第 1 个参数是目标内存地址，第 2 个参数是源数据地址，第 3 个参数是需要拷贝的字节数。

esp_lcd_panel_draw_bitmap() 函数在上面显示整屏颜色的函数里面也用过，每个参数的意义在前面讲解过，当时是每执行一次，显示一行的颜色，现在这里，是直接显示整屏的数据。

**1.3 注意事项**

编译之前，先设置目标芯片为 esp32s3，然后设置 menuconfig，把 flash 大小设置为 16MB，然后打开 PSRAM，因为程序中需要使用外部内存。

![img](./img/58112.png)

我们看上图中第 2 步这里，有两个选项，默认是 Quad，我们改成 Octal。Quad 是 4 线，Octal 是 8 线，因为我们的模组所使用的 ESP32-S3 芯片内部是 8 线 SPI，所以这里要选 Octal。第 3 步设置速度，默认 40M，我们改成 80M。

接下来就可以编译了，正常没有问题。如果你编译有错误，依据终端提示修改即可。

**1.4** **idf_component.yml**

idf_component.yml 是ESP-IDF组件管理系统的元数据配置文件 ，用于定义组件的依赖关系、版本信息、目标平台等关键信息。通过这个文件，ESP-IDF构建系统能够自动管理组件的下载、依赖解析和版本控制，大大简化了组件的使用和维护。

**1.4.1 文件作用机制**

**（一）组件注册流程**

```
idf_component.yml
         ↓
    组件管理器解析
         ↓
    检查依赖关系
         ↓
    验证目标芯片
         ↓
    下载/更新组件
         ↓
    集成到构建系统
```

 

**（二）依赖解析**

```
# 组件管理器自动处理依赖
idf.py reconfigure
# 1. 读取idf_component.yml
# 2. 解析dependencies字段
# 3. 检查ESP-IDF版本是否满足>=4.4
# 4. 下载cmake_utilities依赖
# 5. 验证targets是否匹配当前芯片
# 6. 生成构建配置
```

 

**（三）版本管理**

```
# 查看组件版本
idf.py component list
 
# 更新组件到最新版本
idf.py component update esp_lcd_st7796
 
# 指定版本安装
idf.py component install esp_lcd_st7796@1.4.0
```

 

**1.4.2 文件详细分析**

```
dependencies:
  cmake_utilities: 0.*
  idf: '>=4.4'
description: ESP LCD ST7796 driver (SPI && I80 && MIPI DSI)
repository: git://github.com/espressif/esp-bsp.git
repository_info:
  commit_sha: fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
  path: components/lcd/esp_lcd_st7796
targets:
- esp32
- esp32s2
- esp32s3
- esp32p4
- esp32c3
url: https://github.com/espressif/esp-bsp/tree/master/components/lcd/esp_lcd_st7796
version: 1.4.0
```

字段详细说明

**1. dependencies - 依赖关系配置**

```
dependencies:
  cmake_utilities: 0.*
  idf: '>=4.4'
```

功能说明 ：声明组件运行所需的依赖项及其版本要求。

| **依赖项**      | **版本要求** | **说明**                       |
| --------------- | ------------ | ------------------------------ |
| cmake_utilities | 0.*          | CMake工具库，任何0.x版本均可   |
| idf             | >=4.4        | ESP-IDF框架版本，要求4.4或更高 |

版本语法 ：

- 0.* ：匹配0.x.x的任何版本（如0.1.0、0.2.3）

- =4.4 ：匹配4.4.0及以上版本（如4.4.0、5.0.0、5.2.2）

- ^1.0.0 ：匹配1.x.x版本，但不包括2.0.0

- ~1.2.3 ：匹配1.2.x版本，但不包括1.3.0

实际应用 ：

```
# 示例：更严格的版本控制
dependencies:
  idf: '>=5.0,<6.0'        # 5.x版本，不包括6.0
  some_component: '^2.1.0'   # 2.1.0及以上，但不包括3.0.0
  another_lib: '1.2.3'      # 精确版本1.2.3
```

**2. description - 组件描述**

```
description: ESP LCD ST7796 driver (SPI && I80 && MIPI DSI)
```

功能说明 ：组件的简短描述，用于说明组件的功能和用途

内容解析 ：

- ESP LCD ：ESP-IDF LCD驱动框架的一部分

- ST7796 ：支持的LCD控制器型号（Sitronix ST7796）

- driver ：这是一个驱动程序组件

- SPI && I80 && MIPI DSI ：支持三种接口类型

-   SPI ：串行外设接口，低速但引脚少

-   I80 ：Intel 8080并行接口，速度较快

-   MIPI DSI ：移动行业处理器接口，高速串行接口

用途 ：

- 在组件管理器中显示组件简介

- 帮助开发者快速了解组件功能

- 用于文档生成和索引

**3. repository - 代码仓库地址**

```
repository: git://github.com/espressif/esp-bsp.git
```

功能说明 ：组件源代码的Git仓库地址

协议说明 ：

- git:// ：Git协议（仅读取，速度快，但可能被防火墙拦截）

- https:// ：HTTPS协议（需要认证，但兼容性好）

- ssh:// ：SSH协议（需要SSH密钥，安全性高）

实际应用 ：

```
# 示例：不同的仓库配置
repository: https://github.com/espressif/esp-bsp.git  # HTTPS协议
repository: ssh://git@github.com/espressif/esp-bsp.git  # SSH协议
repository: /local/path/to/component  # 本地路径
```

使用场景 ：

- 组件管理器自动下载源代码

- 版本更新和升级

- 源码追踪和调试

**4. repository_info - 仓库详细信息**

```
repository_info:
  commit_sha: fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
  path: components/lcd/esp_lcd_st7796
```

功能说明 ：指定组件在仓库中的精确位置和版本。

commit_sha - 提交哈希值

```
commit_sha: fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
```

功能说明 ：Git提交的SHA-1哈希值，标识组件的精确版本

特点 ：

- 唯一性 ：每个提交都有唯一的SHA-1哈希

- 不可变性 ：哈希值对应特定的代码状态

- 可追溯性 ：可以精确定位到某个提交

 

长度说明 ：

- 完整SHA-1：40个十六进制字符（如上所示）

- 短哈希：前7-8个字符（如 fd0098a ）

 

实际应用 ：

```
# 查看提交信息
git show fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
 
# 检出特定版本
git checkout fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
 
# 查看提交差异
git diff fd0098a HEAD
```

path - 组件路径

```
path: components/lcd/esp_lcd_st7796
```

功能说明 ：组件在仓库中的相对路径

路径解析 ：

```
esp-bsp/                          # 仓库根目录
└── components/                   # 组件目录
    └── lcd/                      # LCD相关组件
        └── esp_lcd_st7796/       # ST7796驱动组件
            ├── CMakeLists.txt
            ├── idf_component.yml
            ├── esp_lcd_st7796.c
            └── ...
```

使用场景 ：

- 组件管理器从仓库下载后，只提取指定路径的文件

- 支持一个仓库包含多个组件

- 减少下载的数据量

 

**5.targets - 支持的目标芯片**

```
targets:
- esp32
- esp32s2
- esp32s3
- esp32p4
- esp32c3
```

功能说明 ：声明组件支持的ESP32系列芯片型号。

实际应用 ：

```
# 示例：不同芯片的配置
targets:
  - esp32          # 支持ESP32
  - esp32s3        # 支持ESP32-S3
  - "!esp32c6"     # 不支持ESP32-C6（使用!排除）
  - "esp32*":      # 通配符，支持所有ESP32系列
```

编译时检查 ：

```
# CMakeLists.txt中的使用
if(TARGET esp32)
    # ESP32特定的配置
endif()
 
if(TARGET esp32s3)
    # ESP32-S3特定的配置（如MIPI-DSI支持）
endif()
```

**6. url - 项目主页**

```
url: https://github.com/espressif/esp-bsp/tree/master/components/lcd/esp_lcd_st7796
```

功能说明 ：组件的在线文档或源码浏览地址

用途 ：

- 提供文档链接

- 源码在线浏览

- 问题反馈和讨论

- 版本历史查看

 

**浏览器打开网址**

![img](./img/58126.png)

 

**7. version - 组件版本**

```
version: 1.4.0
```

功能说明 ：组件的版本号，遵循语义化版本规范（SemVer）

版本格式 ： 主版本号.次版本号.修订版本号

| **部分**       | **含义**                  | **变化规则**       |
| -------------- | ------------------------- | ------------------ |
| 主版本号 (1)   | 重大更新，不兼容的API修改 | 不兼容的API变更    |
| 次版本号 (4)   | 功能更新，向后兼容        | 新增功能，保持兼容 |
| 修订版本号 (0) | 错误修复，向后兼容        | Bug修复            |

 

**版本示例 ：**

```
version: 1.0.0    # 初始版本
version: 1.1.0    # 新增功能
version: 1.1.1    # 修复bug
version: 2.0.0    # 重大更新，API变更
```

**完整配置示例**

```
# 组件依赖
dependencies:
  idf: '>=5.0,<6.0'              # ESP-IDF 5.x版本
  esp_lcd: '^1.0.0'              # ESP LCD框架
  driver_gpio: '0.*'             # GPIO驱动
 
# 组件描述
description: ESP LCD ST7796 driver with multi-interface support
 
# 仓库地址
repository: https://github.com/espressif/esp-bsp.git
 
# 仓库详细信息
repository_info:
  commit_sha: fd0098aaa277c5b35cc54779ee7bfbda72e8db1e
  path: components/lcd/esp_lcd_st7796
  branch: master                  # 可选：指定分支
 
# 支持的芯片
targets:
  - esp32
  - esp32s3
  - esp32p4
 
# 项目主页
url: https://github.com/espressif/esp-bsp/tree/master/components/lcd/esp_lcd_st7796
 
# 组件版本
version: 1.4.0
 
# 可选字段
maintainer: "Espressif Systems"  # 维护者
license: Apache-2.0               # 许可证
tags:                             # 标签
  - lcd
  - display
  - driver
```

 

**二、调色板**

lcd_set_color() 函数设置背景色，背景色是一个 16 位数，格式为 RGB565。

在计算机的各种画图软件中，颜色一般用 RGB888 表示，用 3 个字节表示颜色，顺序为红绿蓝，每个字节的大小用十进制表示，就是 0~255。例如，白色的表示就是（255，255，255），黑色的表示就是（0，0，0），纯红色（255，0，0），纯绿色（0，255，0），纯蓝色（0，0，255），其它颜色，都是改变这些数字的合成，例如黄绿色（154 205 50）。

我们想在液晶屏上显示自己的颜色，可以把 RGB888 转成 RGB565，转换原理是，R 取字节的前 5 位，G 取字节的前 6 位，B 取字节的前 5 位。例如，黄绿色（154 205 50），转换过程如下：

红：154，写成二进制为 1001 1010，取前 5 位为 10011

绿：205，写成二进制为 1100 1101，取前 6 位为 110011

蓝：50，写成二进制为 0011 0010，取前 5 位为 00110

把 RGB565 合起来，即 10011 110011 00110，4 位对齐显示 1001 1110 0110 0110，正好是 2 个字节，写成十六进制就是 0x9E66。

使用 lcd_set_color 函数显示颜色，如果是BGR格式，需要将高低字节对调，即写成：

```
lcd_set_color(0x669E);
```

把 bsp_lcd_init() 函数中，lcd_set_color() 函数的参数，由原来的 0x0000 修改为 0x669E，再编译下载到开发板，可以看到它的颜色，黄绿色在电脑上的显示效果如下图所示，因为 RGB888 转换成 RGB565，所以肯定会有一些颜色损失，不过普通人基本上看不出来区别，大家可以对比一下。

更加简单的方法，可以直接通过PortHelper中的调色板，得到想要的16位色，如下图。

![img](./img/58116.png)

 

**三、图片取模**

如果想显示自己的图片，按照下面步骤实现。一共需要两步，先制作图片的数组文件，再修改程序让图片显示。制作图片数组文件，我们需要借助一款软件：PortHelper。

![img](./img/58089.png)

如上图所示，

- 输出数据类型：为“C 语言数组”；

- 扫描方式：“水平扫描”；

- 输出颜色深度：“16 位色[RGB565]”；

- 宽度和高度设置： 182 和 96；

- 输出字节序：“大端模式”；

转换后的文件复制到我们例程的 main 文件夹下面。

在 VSCode 中点击打开这个文件，我们可以看到它的数组名称和数组大小，如下。



```
// 文件名: logo_gec.png
// 原始图像大小: 182 x 96
// 自定义输出大小: 182 x 96
// 色深: 16 bpp (RGB565)
// 扫描方式:  水平扫描
// 扫描方向: 水平 从左到右, 垂直 从上到下
// 字节顺序: 大端模式
const unsigned char g_image_logo_gec_182x96[34944]={
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0x8D, 0xB9, 0x9D, 0xFB, 0xE7, 0xBF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 
..............        
    
};
```

最后编译下载，会看到液晶屏显示图片。

**四、ESP-LCD架构设计**

**4.1 函数**

**文件来源：esp-idf-v5.2.2\components\esp_lcd\src\esp_lcd_panel_ops.c**

**4.1.1 LCD面板初始化函数**

```
// LCD面板初始化函数，用于初始化LCD面板的内部寄存器和配置
// 功能说明：配置LCD面板的工作参数，设置显示模式、颜色格式等初始化参数
// 设计思路：调用面板驱动提供的init回调函数，完成LCD芯片的软件初始化
// 使用场景：在硬件复位后、首次使用LCD或需要重新配置显示参数时调用
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
// 返回值说明：
//   ESP_OK - 初始化操作成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的初始化失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的init函数指针执行初始化
// 注意事项：初始化前必须先完成硬件复位，初始化后才能进行显示操作
esp_err_t esp_lcd_panel_init(esp_lcd_panel_handle_t panel)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的init函数指针，执行LCD芯片的初始化配置
    // panel->init是函数指针，指向具体LCD驱动芯片的初始化实现
    return panel->init(panel);
}
```

**4.1.2 LCD面板删除函数**

```
// LCD面板删除函数，用于释放LCD面板占用的资源
// 功能说明：释放LCD面板相关的内存资源和硬件资源，清理驱动层的数据结构
// 设计思路：调用面板驱动提供的del回调函数，完成资源的释放和清理
// 使用场景：在不再使用LCD显示功能、程序退出或切换显示设备时调用
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
// 返回值说明：
//   ESP_OK - 资源释放成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的资源释放失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的del函数指针释放资源
// 注意事项：删除后不能再使用该面板句柄，需要重新创建才能使用LCD
esp_err_t esp_lcd_panel_del(esp_lcd_panel_handle_t panel)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的del函数指针，释放面板占用的所有资源
    // panel->del是函数指针，指向具体LCD驱动芯片的资源释放实现
    return panel->del(panel);
}
```

 

**4.1.3 LCD面板复位函数**

```
// LCD面板复位函数，用于对LCD面板进行硬件复位操作
// 功能说明：通过硬件复位信号将LCD面板恢复到初始状态，清除所有配置和显示内容
// 设计思路：调用面板驱动提供的reset回调函数，实现硬件层面的复位操作
// 使用场景：在LCD初始化失败、显示异常或需要重新配置时调用
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
// 返回值说明：
//   ESP_OK - 复位操作成功执行
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的硬件操作错误
// 实现原理：首先验证面板句柄的有效性，然后调用面板驱动层的reset函数指针执行复位
// 注意事项：复位操作会清除LCD的所有配置和显示内容，复位后需要重新初始化
esp_err_t esp_lcd_panel_reset(esp_lcd_panel_handle_t panel)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    // ESP_RETURN_ON_FALSE宏用于参数验证，第一个条件为false时执行错误返回
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的reset函数指针，执行实际的硬件复位操作
    // panel->reset是函数指针，指向具体LCD驱动芯片的复位实现
    return panel->reset(panel);
}
```

 

**4.1.4 LCD面板绘制位图函数**

```
// LCD面板绘制位图函数，用于在指定区域显示图像数据
// 功能说明：将RGB格式的图像数据绘制到LCD屏幕的指定矩形区域
// 设计思路：通过SPI或并口接口将图像数据传输到LCD的显存中
// 使用场景：显示图片、绘制图形、更新屏幕内容等需要显示图像数据的场景
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   x_start - 起始X坐标，类型为int，取值范围0到屏幕宽度-1，表示绘制区域的左边界
//   y_start - 起始Y坐标，类型为int，取值范围0到屏幕高度-1，表示绘制区域的上边界
//   x_end - 结束X坐标，类型为int，取值范围x_start到屏幕宽度，表示绘制区域的右边界
//   y_end - 结束Y坐标，类型为int，取值范围y_start到屏幕高度，表示绘制区域的下边界
//   color_data - 颜色数据指针，类型为const void*，指向RGB格式的图像数据，不能为NULL
// 返回值说明：
//   ESP_OK - 位图绘制成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄为NULL或坐标参数超出范围，参数无效
//   其他错误码 - 具体由底层驱动返回的数据传输失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的draw_bitmap函数指针传输图像数据
// 注意事项：坐标区域必须在屏幕范围内，数据格式必须与LCD配置的颜色格式匹配
esp_err_t esp_lcd_panel_draw_bitmap(esp_lcd_panel_handle_t panel, int x_start, int y_start, int x_end, int y_end, const void *color_data)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的draw_bitmap函数指针，执行图像数据的绘制操作
    // 传入起始坐标、结束坐标和颜色数据指针，完成指定区域的图像显示
    return panel->draw_bitmap(panel, x_start, y_start, x_end, y_end, color_data);
}
```

 

**4.1.5 LCD面板镜像设置函数**

```
// LCD面板镜像设置函数，用于设置屏幕显示的镜像模式
// 功能说明：控制LCD屏幕在水平或垂直方向进行镜像显示
// 设计思路：通过修改LCD驱动芯片的寄存器配置，实现显示内容的镜像翻转
// 使用场景：调整屏幕显示方向、适配不同安装角度、纠正显示倒置等问题
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   mirror_x - 水平镜像标志，类型为bool，true表示水平镜像，false表示不镜像
//   mirror_y - 垂直镜像标志，类型为bool，true表示垂直镜像，false表示不镜像
// 返回值说明：
//   ESP_OK - 镜像设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的mirror函数指针配置镜像模式
// 注意事项：镜像设置会影响整个屏幕的显示方向，需要根据实际安装情况配置
esp_err_t esp_lcd_panel_mirror(esp_lcd_panel_handle_t panel, bool mirror_x, bool mirror_y)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的mirror函数指针，设置水平和垂直方向的镜像模式
    // 传入水平镜像标志和垂直镜像标志，配置LCD芯片的显示方向
    return panel->mirror(panel, mirror_x, mirror_y);
}
```

 

**4.1.6 LCD面板坐标交换函数**

```
// LCD面板坐标交换函数，用于交换X轴和Y轴的显示方向
// 功能说明：将屏幕的X轴和Y轴进行交换，实现横屏和竖屏的切换
// 设计思路：通过修改LCD驱动芯片的寄存器配置，交换显示的坐标轴
// 使用场景：横竖屏切换、适配不同应用场景、调整显示方向等
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   swap_axes - 坐标轴交换标志，类型为bool，true表示交换X和Y轴，false表示不交换
// 返回值说明：
//   ESP_OK - 坐标轴交换设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的swap_xy函数指针交换坐标轴
// 注意事项：交换坐标轴后，屏幕的宽度和高度概念也会相应交换
esp_err_t esp_lcd_panel_swap_xy(esp_lcd_panel_handle_t panel, bool swap_axes)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的swap_xy函数指针，设置X轴和Y轴的交换模式
    // 传入交换标志，配置LCD芯片的坐标轴显示方式
    return panel->swap_xy(panel, swap_axes);
}
```

 

**4.1.7 LCD面板间隙设置函数**

```
// LCD面板间隙设置函数，用于设置屏幕显示区域之间的间隙
// 功能说明：配置LCD屏幕显示区域之间的水平和垂直间隙距离
// 设计思路：通过修改LCD驱动芯片的寄存器，设置显示区域的偏移量
// 使用场景：多屏拼接、调整显示位置、补偿物理安装偏差等场景
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   x_gap - 水平间隙距离，类型为int，取值范围通常为0到屏幕宽度，单位为像素
//   y_gap - 垂直间隙距离，类型为int，取值范围通常为0到屏幕高度，单位为像素
// 返回值说明：
//   ESP_OK - 间隙设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的set_gap函数指针配置间隙
// 注意事项：间隙设置会影响显示区域的起始位置，需要根据实际需求调整
esp_err_t esp_lcd_panel_set_gap(esp_lcd_panel_handle_t panel, int x_gap, int y_gap)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的set_gap函数指针，设置水平和垂直方向的间隙距离
    // 传入水平间隙值和垂直间隙值，配置LCD芯片的显示区域偏移
    return panel->set_gap(panel, x_gap, y_gap);
}
```

**4.1.8 LCD面板颜色反转函数**

```
// LCD面板颜色反转函数，用于反转显示颜色的极性
// 功能说明：将LCD显示的颜色进行反转，实现显示效果的翻转
// 设计思路：通过修改LCD驱动芯片的寄存器配置，反转RGB数据的显示逻辑
// 使用场景：调整显示效果、适配不同LCD面板、纠正颜色显示异常等
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   invert_color_data - 颜色反转标志，类型为bool，true表示反转颜色，false表示不反转
// 返回值说明：
//   ESP_OK - 颜色反转设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的invert_color函数指针配置颜色反转
// 注意事项：颜色反转会影响整个屏幕的显示效果，白色会变成黑色，黑色会变成白色
esp_err_t esp_lcd_panel_invert_color(esp_lcd_panel_handle_t panel, bool invert_color_data)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的invert_color函数指针，设置颜色数据的反转模式
    // 传入反转标志，配置LCD芯片的颜色显示逻辑
    return panel->invert_color(panel, invert_color_data);
}
```

 

**4.1.9 LCD面板显示开关函数**

```
// LCD面板显示开关函数，用于控制LCD屏幕的显示状态
// 功能说明：开启或关闭LCD屏幕的显示功能，控制屏幕是否输出图像
// 设计思路：通过修改LCD驱动芯片的显示控制寄存器，控制显示的开关状态
// 使用场景：省电模式、屏幕保护、临时关闭显示等需要控制显示状态的场景
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   on_off - 显示开关标志，类型为bool，true表示开启显示，false表示关闭显示
// 返回值说明：
//   ESP_OK - 显示开关设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性后，调用面板驱动层的disp_on_off函数指针控制显示状态
// 注意事项：关闭显示后屏幕会变黑，但背光可能仍然工作，需要单独控制背光
esp_err_t esp_lcd_panel_disp_on_off(esp_lcd_panel_handle_t panel, bool on_off)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 调用面板驱动层的disp_on_off函数指针，控制LCD屏幕的显示开关状态
    // 传入开关标志，配置LCD芯片的显示使能寄存器
    return panel->disp_on_off(panel, on_off);
}
```

 

**4.1.10 LCD面板显示关闭函数**

```
// LCD面板显示关闭函数，用于关闭LCD屏幕的显示功能
// 功能说明：关闭LCD屏幕的显示，使屏幕进入不显示状态
// 设计思路：通过调用显示开关函数，传入关闭标志来实现显示关闭
// 使用场景：省电模式、屏幕保护、需要关闭显示的场景
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   off - 关闭标志，类型为bool，true表示关闭显示，false表示不关闭显示
// 返回值说明：
//   ESP_OK - 显示关闭操作成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   其他错误码 - 由底层显示开关函数返回的错误码
// 实现原理：将off标志取反后调用显示开关函数，实现显示关闭功能
// 注意事项：该函数是显示开关函数的封装，参数逻辑与显示开关函数相反
esp_err_t esp_lcd_panel_disp_off(esp_lcd_panel_handle_t panel, bool off)
{
    // 调用显示开关函数，传入off参数的取反值
    // 当off为true时，传入false表示关闭显示；当off为false时，传入true表示开启显示
    return esp_lcd_panel_disp_on_off(panel, !off);
}
 
```

**4.1.11** **LCD面板睡眠模式函数**

```
// LCD面板睡眠模式函数，用于控制LCD屏幕的睡眠状态
// 功能说明：将LCD屏幕设置为睡眠模式或唤醒，实现低功耗或正常工作状态的切换
// 设计思路：通过修改LCD驱动芯片的睡眠控制寄存器，控制LCD的工作模式
// 使用场景：省电模式、长时间不使用屏幕、需要降低功耗的场景
// 参数说明：
//   panel - 面板句柄，类型为esp_lcd_panel_handle_t，指向LCD面板实例，不能为NULL
//   sleep - 睡眠标志，类型为bool，true表示进入睡眠模式，false表示唤醒屏幕
// 返回值说明：
//   ESP_OK - 睡眠模式设置成功完成
//   ESP_ERR_INVALID_ARG - 面板句柄参数为NULL，参数无效
//   ESP_ERR_NOT_SUPPORTED - 当前LCD面板不支持睡眠模式功能
//   其他错误码 - 具体由底层驱动返回的寄存器配置失败错误
// 实现原理：验证参数有效性和功能支持后，调用面板驱动层的disp_sleep函数指针
// 注意事项：进入睡眠模式后需要重新初始化才能正常显示，睡眠模式功耗极低
esp_err_t esp_lcd_panel_disp_sleep(esp_lcd_panel_handle_t panel, bool sleep)
{
    // 检查面板句柄是否为NULL，如果为NULL则返回参数无效错误
    ESP_RETURN_ON_FALSE(panel, ESP_ERR_INVALID_ARG, TAG, "invalid panel handle");
    // 检查面板驱动层是否支持睡眠模式功能，如果disp_sleep函数指针为NULL则不支持
    // ESP_RETURN_ON_FALSE宏用于功能支持检查，第一个条件为false时执行错误返回
    ESP_RETURN_ON_FALSE(panel->disp_sleep, ESP_ERR_NOT_SUPPORTED, TAG, "sleep is not supported by this panel");
    // 调用面板驱动层的disp_sleep函数指针，设置LCD屏幕的睡眠或唤醒状态
    // 传入睡眠标志，配置LCD芯片进入睡眠模式或从睡眠模式唤醒
    return panel->disp_sleep(panel, sleep);
}
```

 

**4.2 分层架构设计**

ESP-IDF 的 esp_lcd 框架分为三个层级:

- BUS 层（硬件接口）

- SPI / I2C / 8080 / RGB / MIPI DSI

- 负责 怎么把数据按该总线的规则发出去。

- IO 层（屏幕指令接口）

- st7789_spi、ili9341_spi、st7789_8080 等

- 负责 怎么向某个屏幕型号发送命令/数据。

- Panel 层

- st7789、ili9341

- 负责 分辨率、初始化序列、偏移、MADCTL、坐标翻转等逻辑。

 

**4.3 资源生命周期管理**

生命周期阶段 ：

```
创建 → 初始化 → 使用 → 清理 → 删除
  ↓       ↓       ↓      ↓      ↓
new()   init()  draw()  reset() del()
```

 

## **五、ST7796显示驱动IC库添加**

本项目使用 **ESP-IDF 组件管理器（Component Manager）** 通过 idf_component.yml 文件自动下载和管理 LVGL 依赖，无需手动克隆或复制源码。

```
# 组件依赖管理文件：声明本工程所依赖的 ESP-IDF 组件及其版本范围
dependencies:
  # ST7796 液晶屏驱动组件，由乐鑫官方维护
  # 版本要求：>= 1.3.0 且 < 2.0.0（^ 表示允许同主版本内的更新）
  espressif/esp_lcd_st7796: ^1.3.0
```

 

