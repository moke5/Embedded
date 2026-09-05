# 01-GPIO & LED

[toc]

## **一、GPIO 简介**

GPIO 是负责控制或采集外部器件信息的外设，主要负责输入输出功能。 ESP32-S3 芯片具有 45 个物理 GPIO 管脚，涵盖 GPIO0 至 GPIO21 以及 GPIO26 至GPIO28的广泛范围。然而，相较于 ESP32-S3芯片，模组引出的 GPIO管脚数量较少，仅有 36 个。尽管如此，这些管脚均具备通用 IO 功能，并且可以通过内部 IO MUX（复用矩阵）灵活复用为其他功能，这充分展现了 ESP32-S3 芯片的强大和灵活性。以下是模组的 GPIO 分布图。

![img](./img/58052.png)

从上面的图示中可见，黄色区域的管脚均可作为普通的 IO 端口使用。因此，在控制 LED灯时，我们可以自由选择任意一个管脚进行操作。但请注意，部分 IO 端口可能与 Flash 或PSRAM 等元件的管脚相关联，这就需要开发者在操作过程中参考相关技术手册，以避免潜在的问题。在ESP32S3 开发板中，模组的 IO10 被用来连接 LED 的负极，因此在本章的实验中，我们将主要对 IO10进行操作。

## **二、LED 简介**

LED 灯（发光二极管）是一种半导体光源，主要结构包括以下部分：

- 外壳：通常由塑料或玻璃制成，用于保护内部元件。

- 发光材料：LED 最核心的部分，由特殊半导体材料制成，例如：常见的 InGaN（氮化铟镓）或 AlInGaP（铝铟镓磷）。

- 芯片：用于产生光的发光二极管芯片。

- 引线：提供电连接的金属引线。

- 焊点：将LED 芯片与引线连接在一起的焊接点。

- 电极：负责连接半导体材料与外部电路，通常由金属制成。

- 反射腔：用于增强发光效果的一个结构，将发出的光反射到正面。

其发光原理基于半导体的特性。在半导体中，有两类重要的载流子：电子，主要存在于 n 型半导体中；而空穴，则主要存在于 p型半导体中。当 n 型半导体与 p型半导体材料接触时，它们的交界处会形成一个特殊的层结。当对这个层结施加适当的电压时，层结中的空穴与电子会发生重组，并释放出能量。这些能量会以光子的形式被释放出来，从而产生可见光。这就是 LED 发光的基本原理。

![img](./img/58062.png)

### **2.1 LED 灯驱动原理**

LED 驱动是指通过稳定的电源为 LED 提供适宜的电流和电压，确保其正常发光。LED 驱动方式主要有恒流和恒压两种，其中，恒流驱动因其能限定电流而备受青睐。由于 LED 灯对电流变化极为敏感，一旦电流超过其额定值，可能导致损坏。因此，恒流驱动通过确保电流的稳定性，进而保障 LED 的安全运行。

### **2.2 LED 灯驱动方式**

下面，我们来看一下 LED 两种驱动方式。

（1）灌入电流接法。指的是 LED 的供电电流是由外部提供电流，将电流灌入我们的 MCU；风险是当外部电源出现变化时，会导致 MCU 的引脚烧坏。其接法如下图所示。

![img](./img/58054.png)

（2）输出电流接法。指的是由 MCU 提供电压电流，将电流输出给 LED；如果使用 MCU的 GPIO 直接驱动 LED，则驱动能力较弱，可能无法提供足够的电流驱动 LED。其接法如下图所示。	

![img](./img/58056.png)

ESP32S3 开发板上的 LED 采用灌入电流接法，这种方式避免了 MCU 直接提供电压电流来驱动 LED，从而有效减轻了 MCU 的负载。这使得 MCU 能够更加专注于执行其他核心任务，进而提升了整体系统的性能和稳定性。

## **三、硬件设计**

### **3.1 例程功能**

**实验现象：** LED 灯以 500ms 的频率交替闪烁。

### **3.2 硬件资源**

1.LED：LED-D1-GPIO10

### **3.3 原理图**

本章用到的硬件有 LED 灯。电路在开发板上已经连接好，所以在硬件上不需要动任何东西，直接下载代码就可以测试使用。其连接原理图如下图所示。

![img](./img/58066.png)

从上图可知，若 IO10 输出低电平时，则 LED 亮起，反之，熄灭。LED灯在板子位置如下图。

![img](./img/58059.png)

## **四、GPIO初始化配置**

### **4.1** **方法1**

#### **4.1.1** **GPIO 函数介绍**

ESP-IDF 提供了丰富的 GPIO 操作函数，开发者可以在 esp-idf-v5.2.2\components\driver\gpio路径下找到相关的 gpio.c 和 gpio.h 文件。在 gpio.h 头文件中，你可以找到 ESP32-S3 的所有 GPIO 函数定义。接下来，作者将介绍一些常用的 GPIO 函数，这些函数的描述及其作用如下：

#### **4.1.2 GPIO 配置函数**

导入头文件“driver/gpio.h”，在此文件中包含GPIO配置函数用来配置 GPIO 的模式、上下拉等功能，其函数原型如下所示：

```C
esp_err_t gpio_config(const gpio_config_t *pGPIOConfig)
```

该函数的形参描述如下表所示：

| **参数**    | **描述**   |
| ----------- | ---------- |
| pGPIOConfig | GPIO结构体 |

**参数pGPIOConfig：** 为 GPIO 配置结构体指针，下面来看一下 gpio_config_t 结构体中的变量。

**返回值：**ESP_OK 表示配置成功，ESP_FAIL 表示配置失败。

**从函数参数分析可得：**通过设置一个结构体gpio_config_t，将IO48配置为输出模式，无上拉下拉且不支持中断。使用该方法的好处就是随心所欲，你可以按照自己的意向将对应的IO口配置为输入或输出，上拉或下拉，边沿中断或电平中断。

```C
/* GPIO 配置参数 */
typedef struct {
    uint64_t pin_bit_mask;        /* 配置引脚位 */
    gpio_mode_t mode;             /* 设置引脚模式 */
    gpio_pullup_t pull_up_en;     /* 设置上拉 */
    gpio_pulldown_t pull_down_en; /* 设置下拉 */
    gpio_int_type_t intr_type;    /* 中断配置 */
} gpio_config_t;
```

关于各个参数有哪一些看下表说明：

| **类型**                  | **类型说明**                | **可填参数**                        | **参数说明**                                            |
| ------------------------- | --------------------------- | ----------------------------------- | ------------------------------------------------------- |
| .pin_bit_mask             | 配置引脚位                  | (1 << x) 其中x为ESP32S3中可用的GPIO | 设置的引脚的位，例如要设置的是GPIO9引脚，则写为（1<<9） |
| .mode                     | 设置引脚模式                | GPIO_MODE_DISABLE                   | GPIO模式:关闭输入输出                                   |
| GPIO_MODE_INPUT           | GPIO模式:仅输入             |                                     |                                                         |
| GPIO_MODE_OUTPUT          | GPIO模式:仅输出模式         |                                     |                                                         |
| GPIO_MODE_OUTPUT_OD       | GPIO模式:只输出开漏模式     |                                     |                                                         |
| GPIO_MODE_INPUT_OUTPUT_OD | GPIO模式:输出输入为开漏模式 |                                     |                                                         |
| GPIO_MODE_INPUT_OUTPUT    | GPIO模式:输出和输入模式     |                                     |                                                         |
| .pull_up_en               | 设置上拉电阻                | GPIO_PULLUP_DISABLE                 | 禁用GPIO上拉电阻                                        |
| GPIO_PULLUP_ENABLE        | 使用GPIO上拉电阻            |                                     |                                                         |
| pull_down_en              | 设置下拉电阻                | GPIO_PULLDOWN_DISABLE               | 禁用GPIO下拉电阻                                        |
| GPIO_PULLDOWN_ENABLE      | 使用GPIO下拉电阻            |                                     |                                                         |
| .intr_type                | 中断配置                    | GPIO_INTR_DISABLE                   | 禁用GPIO中断                                            |
| GPIO_INTR_POSEDGE         | GPIO中断类型:上升沿         |                                     |                                                         |
| GPIO_INTR_NEGEDGE         | GPIO中断类型:下降沿         |                                     |                                                         |
| GPIO_INTR_ANYEDGE         | GPIO中断类型:上升沿和下降沿 |                                     |                                                         |
| GPIO_INTR_LOW_LEVEL       | GPIO中断类型:输入低电平触发 |                                     |                                                         |
| GPIO_INTR_HIGH_LEVEL      | GPIO中断类型:输入高电平触发 |                                     |                                                         |

在上表中，可填参数均可在 gpio_types.h 文件中找到。这些参数通常是通过枚举类型（enum）定义的，它们为特定的 GPIO 模式或配置提供了预定义的数值。当我们需要为结构体变量（如 gpio_mode_t）设置参数时，我们可以查阅 gpio_types.h 文件，找到对应的枚举类型，并从中选择适当的数值。这样，我们可以确保为GPIO接口设置的模式或配置是准确和有效的。

#### **4.1.3 什么是输入输出？**

输入是指将数据或信号从外部设备或其他源传递到目标设备或系统中（从外部设备传入到开发板的信号都可以叫输入）。在计算机系统中，输入通常是通过键盘、鼠标、触摸屏、传感器等外部设备向计算机发送数据或指令。

#### **4.1.4 什么是上下拉电阻？**

上下拉电阻（Pull-up and Pull-down resistors）是在电子电路中常用的元件，用于控制信号线的**默认状态。**

- 当信号线不连接到任何电源或地时，它处于开路状态，容易受到外界电磁干扰而产生不确定的电平。为了保证信号的稳定性，可以在信号线引脚上**加入上拉电阻或下拉电阻**。

- **上拉电阻**（Pull-up resistor）连接到信号线和高电平（通常为电源电压）之间。当信号线没有连接任何外部设备时，上拉电阻将该信号线拉为高电平。当外部设备连接到该信号线并输出低电平时，由于外部设备的电流较大，上拉电阻无法抵抗这种电流，信号线就会变为低电平。

- **下拉电阻**（Pull-down resistor）则连接到信号线和低电平（通常为地）之间。当信号线没有连接任何外部设备时，下拉电阻将该信号线拉为低电平。当外部设备连接到该信号线并输出高电平时，由于外部设备的电流较大，下拉电阻无法抵抗这种电流，信号线就会变为高电平。

**4.1.5 参考示例**

```C
include "driver/gpio.h"
 
#define     LED_PIN     GPIO_NUM_10
 
// 定义 GPIO 配置结构体，设置各配置项
gpio_config_t gpio = {
    .pin_bit_mask = 1 << LED_PIN,          // 位掩码：选中 GPIO10 引脚（bit10 置 1）
    .mode = GPIO_MODE_OUTPUT,              // 模式：推挽输出模式
    .pull_up_en = GPIO_PULLUP_DISABLE,     // 上拉：禁用内部上拉电阻
    .pull_down_en = GPIO_PULLDOWN_DISABLE, // 下拉：禁用内部下拉电阻
    .intr_type = GPIO_INTR_DISABLE,        // 中断：不使用中断（禁用 GPIO 中断）
};
 
// gpio的配置：将上述配置写入硬件寄存器，完成 GPIO 初始化
gpio_config(&gpio);
```

 

**gpio编号文件路径：\frameworks\esp-idf-v5.2.2\components\soc\esp32s3\include\soc\gpio_num.h**



```C
/*
 * SPDX-FileCopyrightText: 2015-2023 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: Apache-2.0
 */ 
 
#pragma once 
 
#ifdef __cplusplus 
extern "C" { 
#endif 
 
/**
 * @brief GPIO number
 */ 
typedef enum { 
    GPIO_NUM_NC = -1,    /*!< Use to signal not connected to S/W */ 
    GPIO_NUM_0 = 0,     /*!< GPIO0, input and output */ 
    GPIO_NUM_1 = 1,     /*!< GPIO1, input and output */ 
    GPIO_NUM_2 = 2,     /*!< GPIO2, input and output */ 
    GPIO_NUM_3 = 3,     /*!< GPIO3, input and output */ 
    GPIO_NUM_4 = 4,     /*!< GPIO4, input and output */ 
    GPIO_NUM_5 = 5,     /*!< GPIO5, input and output */ 
    GPIO_NUM_6 = 6,     /*!< GPIO6, input and output */ 
    GPIO_NUM_7 = 7,     /*!< GPIO7, input and output */ 
    GPIO_NUM_8 = 8,     /*!< GPIO8, input and output */ 
    GPIO_NUM_9 = 9,     /*!< GPIO9, input and output */ 
    GPIO_NUM_10 = 10,   /*!< GPIO10, input and output */ 
    GPIO_NUM_11 = 11,   /*!< GPIO11, input and output */ 
    GPIO_NUM_12 = 12,   /*!< GPIO12, input and output */ 
    GPIO_NUM_13 = 13,   /*!< GPIO13, input and output */ 
    GPIO_NUM_14 = 14,   /*!< GPIO14, input and output */ 
    GPIO_NUM_15 = 15,   /*!< GPIO15, input and output */ 
    GPIO_NUM_16 = 16,   /*!< GPIO16, input and output */ 
    GPIO_NUM_17 = 17,   /*!< GPIO17, input and output */ 
    GPIO_NUM_18 = 18,   /*!< GPIO18, input and output */ 
    GPIO_NUM_19 = 19,   /*!< GPIO19, input and output */ 
    GPIO_NUM_20 = 20,   /*!< GPIO20, input and output */ 
    GPIO_NUM_21 = 21,   /*!< GPIO21, input and output */ 
    GPIO_NUM_26 = 26,   /*!< GPIO26, input and output */ 
    GPIO_NUM_27 = 27,   /*!< GPIO27, input and output */ 
    GPIO_NUM_28 = 28,   /*!< GPIO28, input and output */ 
    GPIO_NUM_29 = 29,   /*!< GPIO29, input and output */ 
    GPIO_NUM_30 = 30,   /*!< GPIO30, input and output */ 
    GPIO_NUM_31 = 31,   /*!< GPIO31, input and output */ 
    GPIO_NUM_32 = 32,   /*!< GPIO32, input and output */ 
    GPIO_NUM_33 = 33,   /*!< GPIO33, input and output */ 
    GPIO_NUM_34 = 34,   /*!< GPIO34, input and output */ 
    GPIO_NUM_35 = 35,   /*!< GPIO35, input and output */ 
    GPIO_NUM_36 = 36,   /*!< GPIO36, input and output */ 
    GPIO_NUM_37 = 37,   /*!< GPIO37, input and output */ 
    GPIO_NUM_38 = 38,   /*!< GPIO38, input and output */ 
    GPIO_NUM_39 = 39,   /*!< GPIO39, input and output */ 
    GPIO_NUM_40 = 40,   /*!< GPIO40, input and output */ 
    GPIO_NUM_41 = 41,   /*!< GPIO41, input and output */ 
    GPIO_NUM_42 = 42,   /*!< GPIO42, input and output */ 
    GPIO_NUM_43 = 43,   /*!< GPIO43, input and output */ 
    GPIO_NUM_44 = 44,   /*!< GPIO44, input and output */ 
    GPIO_NUM_45 = 45,   /*!< GPIO45, input and output */ 
    GPIO_NUM_46 = 46,   /*!< GPIO46, input and output */ 
    GPIO_NUM_47 = 47,   /*!< GPIO47, input and output */ 
    GPIO_NUM_48 = 48,   /*!< GPIO48, input and output */ 
    GPIO_NUM_MAX, 
} gpio_num_t; 
 
#ifdef __cplusplus 
} 
#endif 
```

 

## **五、IO口操控**

### **5.1 GPIO电平控制函数**

配置完IO口后，让我们再来认识一个IO口控制函数。

```C
esp_err_t gpio_set_level(gpio_num_t gpio_num, uint32_t level)
```

该函数是ESP32在ESPIDF中用于设置GPIO口电平的函数，可以设置IO口的高低电平。

- gpio_num：要设置的GPIO口的编号。

- level：要设置的电平值，0表示低电平，1表示高电平。

函数的返回值是一个esp_err_t类型的枚举值，表示函数执行的结果。如果操作成功，返回ESP_OK；如果GPIO编号错误或该GPIO口未被设置为输出模式，返回相应的错误代码。

```C
int LED_PIN = GPIO_NUM_10;
gpio_set_level(LED_PIN, 0);//将led引脚配置为低电平
gpio_set_level(LED_PIN, 1);//将led引脚配置为高电平
```

### **5.2 什么是高低电平？**

高电平和低电平是指在数字电路中，电信号的电压电平高低状态。在数字电路中，信号的高电平和低电平通常对应于两个离散的电压电平值，例如在TTL（Transistor-Transistor Logic）电平标准中，低电平（L）通常被定义为在0伏到0.8伏的电压范围，而高电平（H）通常被定义为在2.4伏到5伏的电压范围。

在数字电路中，低电平和高电平通常用于代表逻辑“0”和“1”的两种状态。在逻辑电路中，当信号处于高电平时，通常表示逻辑“1“；而当信号处于低电平时，则表示逻辑”0“。这是因为数字电路中只有两种状态（1和0），而高电平和低电平恰好对应于逻辑“1”和“0”。

请注意，不同的电平标准可能会有不同的定义和规范。在不同的电路和系统中，高电平和低电平的定义可能会有所不同。

 

## **六、点灯验证**

**6.1 main.c**

```C
 
#include "driver/gpio.h"       // GPIO 驱动头文件，提供 gpio 的函数接口
#include "freertos/FreeRTOS.h" // FreeRTOS 内核头文件，提供任务、延时等接口
#include "freertos/task.h"     // FreeRTOS 任务头文件，提供 vTaskDelay 等任务函数
#include <stdio.h>             // 标准输入输出头文件，提供 printf 等函数
 
 
#define LED_PIN GPIO_NUM_10 // 宏定义：LED 所连接的 GPIO 引脚号（GPIO10）
 
/**
 * @brief LED 初始化函数：将 GPIO 配置为推挽输出模式，并设置初始状态为熄灭
 */
void led_init(void)
{
    // 定义 GPIO 配置结构体，设置各配置项
    gpio_config_t gpio = {
        .pin_bit_mask = 1 << LED_PIN,          // 位掩码：选中 GPIO10 引脚（bit10 置 1）
        .mode = GPIO_MODE_OUTPUT,              // 模式：推挽输出模式
        .pull_up_en = GPIO_PULLUP_DISABLE,     // 上拉：禁用内部上拉电阻
        .pull_down_en = GPIO_PULLDOWN_DISABLE, // 下拉：禁用内部下拉电阻
        .intr_type = GPIO_INTR_DISABLE,        // 中断：不使用中断（禁用 GPIO 中断）
    };
    // gpio的配置：将上述配置写入硬件寄存器，完成 GPIO 初始化
    gpio_config(&gpio);
    // 灯为熄灭状态：输出高电平（本工程中低电平点亮、高电平熄灭）
    gpio_set_level(LED_PIN, 1);
}
 
/**
 * @brief 应用主函数：程序入口，负责初始化外设并执行主循环逻辑
 */
void app_main(void)
{
    // led初始化：调用 LED 初始化函数
    led_init();
 
    // 串口打印测试信息（通过 UART0 输出到串口监视器）
    printf("This is led test\r\n");
 
    // 主循环：无限循环执行 LED 闪烁逻辑
    while (1)
    {
        // 亮灯：输出低电平，LED 点亮
        gpio_set_level(LED_PIN, 0);
 
        // 延时一会：阻塞延时 500ms（亮灯持续时间）
        vTaskDelay(pdMS_TO_TICKS(500));
 
        // 灭灯：输出高电平，LED 熄灭
        gpio_set_level(LED_PIN, 1);
        
        // 延时一会：阻塞延时 500ms（灭灯持续时间）
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}
```

**6.2** **CMakeLists.txt**

```C
idf_component_register(SRCS "main.c"
                    INCLUDE_DIRS ".")
```

**6.3 练习**

**练习1：**开发板上的标记着D1的LED灯，下载代码后将会周期性闪烁。

**练习2：**将led相关函数封装led.c。



# 项目结构

```plantext
| -- main
	|-main.c
	|-CMakeLists.txt
| -- components(第三方代码/BSP)
	| - bsp
		| - include
		| - C file
		| - CMakeLists.txt
	| - CMakeLists.txt
```



- 需要在项目级的`CMakeLists.txt`添加`set(COMPONETS main bsp xxx)` xxx---后续需要添加的文件夹
- 创建bsp文件夹，编写CMakeLists.txt

```
idf_component_register(
	SRCS bsp_board.c		# source file
	INCLUDE_DIRS include 	# head file
	PRIV_INCLUDE_DIRS .
	REQUIRES driver esp_timer xxx
	# 需要继续添加ESP系统组件
	# 使用ESP-IDF的系统组件 driver：驱动组件-GPIO/中断/IIC/SPI/定时器
	# esp-timer：软件定时器的组件
)
```

- 编写bsp文件
- 修改main中的CMameLists.txt 使用bsp库

```
idf_component_register(SRCS "led_main.c"
				REQUIRES bsp # bsp库的请求
				)
```

