# PWM 脉冲宽带调制

[toc]

## **一、PWM介绍**

PWM（Pulse Width Modulation 脉宽调制）是利用微处理器的数字输出来对模拟电路进行控制的一种非常有效的技术。它是一种对模拟信号电平进行数字编码的方法。是指在一定时间内波形的高电平（即 1 状态）所占用的时间比例。通过高分辨率计数器的使用，方波占空比被调制用来对一个模拟信号的电平进行编码。PWM 信号任然是数字的，因为在给定的任何时刻，满幅值的直流供电要么完全有，要么完全无。比如我们的电压输出是 5V的，那么经过改变 PWM 的占空比，可以达到在一定时间内输出 3.3V 或者 1.3V 的效果。

**举个例子**

想象你有一个LED和一个开关，你以肉眼看不清的速度，快速反复地开关一次，这样LED灯就会亮一半时间，暗一半时间。如果你快速地进行这个操作，对于观察者来说，LED就像是以半亮度持续亮着。这就是PWM的基本原理。如果你把大部分时间保持开关为关闭状态，那么LED会显得更暗；相反，如果你把开关大部分时间保持为打开状态，LED会显得更亮。这就是PWM调节占空比来控制亮度的过程。

## **二、PWM的基本参数**

PWM 是脉冲宽度调制，具有两个非常重要的参数：频率和占空比。 

**频率：**PWM 信号的周期长度，通常使用赫兹 (Hz) 表示，表示每秒钟有多少个脉冲。PWM 的频率是整个周期的倒数。指 1 秒钟内信号从高电平到低电平再回到高电平的次数（一个周期）。

**占空比：**占空比是指一个周期内高电平所占的比例。

**分辨率：**ESP32 支持的 PWM 信号分辨率是指设备可输出的不同占空比级别的数量。例如，8 位分辨率就表示设备可以输出 2^8 个不同占空比级别，即 0%、1/256、2/256 … 直到 100%。

## **三、ESP32S3上的PWM**

在ESP32-S3中有两个硬件外设可以输出PWM信号，分别是LED PWM **控制器** (LEDC) 和 **电机控制脉宽调制器** (MCPWM)。它们各有其特点和用途：

1、**LED PWM 控制器 (LEDC)**：这个模块的主要设计目标是产生高精度的 PWM 波形，用以控制 LED 灯的亮度或者产生声音。LEDC 的分辨率可以达到 16 位，能够产生准确且平滑的变化，适用于控制 LED 灯的亮度和产生声音。并且，**LEDC 支持多达 8 个通道的 PWM 输出**，且**支持任意的GPIO引脚**。用户可以配置每个通道的频率和占空比。

2、电机控制脉宽调制器 (MCPWM)：这个模块主要用于马达控制，包括伺服马达、步进马达和普通电机。MCPWM 支持更加复杂的控制模式，如电机的向前/向后驱动、断电刹车等，并且支持闭环控制模式，能满足更复杂的电机控制需求。MCPWM 支持高达 6 个通道的独立 PWM 输出，并且支持死区控制和外部信号捕获。

总的来说，它们两者在处理 PWM 方面有所不同，并被应用于不同的场景。LEDC 更加适合控制灯光、声音等线性设备，而 MCPWM 包含更高级的功能，适合电机控制。本章我们以LED PWM 控制器作为案例输出PWM，后面简称LEDC。

 

## **四、PWM的操作流程**

**定时器配置：**指定 PWM 信号的频率和占空比分辨率。

**通道配置：**绑定定时器和输出 PWM 信号的 GPIO。

**改变 PWM 信号：**[﻿](https://docs.espressif.com/projects/esp-idf/zh_CN/stable/esp32s3/api-reference/peripherals/ledc.html#ledc-api-change-pwm-signal)输出 PWM 信号来驱动 LED。可通过软件控制或使用硬件渐变功能来改变 LED 的亮度。

### **4.1 定时器配置**

要设置定时器，可调用函数 **ledc_timer_config()**，并将包括如下配置参数的数据结构**ledc_timer_config_t** 传递给该函数。关于**ledc_timer_config_t** 的相关参数说明：

- **speed_mode**：速度模式。注意，与 ESP32 不同，ESP32-S3 仅支持设置通道为低速模式，即LEDC_LOW_SPEED_MODE。

- **timer_num**： 通道的定时器源。定时器索引 **ledc_timer_t。可选参数如下：**

- LEDC_TIMER_0

- LEDC_TIMER_1

- LEDC_TIMER_2

- LEDC_TIMER_3

- LEDC_TIMER_MAX

- **freq_hz**： PWM 信号频率，表示LEDC模块的定时器时钟频率设置，单位为Hz。

- **duty_resolution**： PWM 占空比分辨率。占空比分辨率通常用**ledc_timer_bit_t**设置，范围是 10 至 15 位。如需较低的占空比分辨率（上至 10，下至 1），可直接输入相应数值。相关参数请参考 **ledc_timer_bit_t**。

- **clk_cfg**：LEDPWM的时钟来源。可选以下参数：

LEDC_AUTO_CLK：启动定时器时，将根据给定的分辨率和占空率参数自动选择ledc源时钟;

LEDC_USE_APB_CLK：选择APB作为源时钟;

LEDC_USE_RC_FAST_CLK：选择“RC_FAST”作为源时钟;

LEDC_USE_XTAL_CLK：选择XTAL作为源时钟;

LEDC_USE_RTC8M_CLK：”LEDC_USE_RC_FAST_CLK” 的别名;

频率和占空比分辨率相互关联。PWM 频率越高，占空比分辨率越低，反之亦然。如果 API 不是用来改变 LED 亮度，而是用于其它目的，这种相互关系可能会很重要。

时钟源同样可以限制PWM频率。选择的时钟源频率越高，可以配置的PWM频率上限就越高。

| **时钟名称**    | **时钟频率** | **时钟功能**                                 |
| --------------- | ------------ | -------------------------------------------- |
| **APB_CLK**     | **80 MHz**   | /                                            |
| **RC_FAST_CLK** | **~20 MHz**  | 支持动态调频（DFS）功能，支持Light-sleep模式 |
| **XTAL_CLK**    | **40 MHz**   | 支持动态调频（DFS）功能                      |

**备注：**

- 如果 ESP32-S3 的定时器选用了RC_FAST_CLK作为其时钟源，驱动会通过内部校准来得知这个时钟源的实际频率。这样确保了输出PWM信号频率的精准性。

- ESP32-S3 的所有定时器共用一个时钟源。因此 ESP32-S3 不支持给不同的定时器配置不同的时钟源。

### **4.2 通道配置**

定时器设置好后，需要配置所需的通道（**ledc_channel_t** 之一）。配置通道需调用函数 **ledc_channel_config()。**通道的配置与定时器设置类似，需向通道配置函数传递包括通道配置参数的结构体。

```C
ledc_channel_config_t 
```

此时，通道会按照 **ledc_channel_config_t** 的配置开始运作，并在选定的 GPIO 上生成由定时器设置指定的频率和占空比的 PWM 信号。在通道运作过程中，可以随时通过调用函数 **ledc_stop()** 将其暂停。**ledc_channel_config_t** 的参数说明如下：

**gpio_num**：配置输出引脚；例如使用GPIO6引脚，则gpio_num = 6；

**speed_mode**：LEDC速度模式选择，可选参数有高速模式（LEDC_HIGH_SPEED_MODE）或低速模式（LEDC_LOW_SPEED_MODE）

**channel**：LEDC的输出通道（PWM的输出通道），可选参数有0~7；

**intr_type**： 配置中断。可选参数有使能中断（LEDC_INTR_FADE_END）和失能中断（LEDC_INTR_DISABLE）

**timer_sel**：**选择通道的定时器源。定时器索引 ledc_timer_t。可选参数如下：**

- LEDC_TIMER_0

- LEDC_TIMER_1

- LEDC_TIMER_2

- LEDC_TIMER_3

- LEDC_TIMER_MAX

**duty**：LEDC通道的占空比设置。占空比设定范围为 0 到 2的duty_resolution次方。

**hpoint**： led通道 hpoint 值。hpoint 叫做占空比作用点。它表示占空比对应的时钟计数值。所谓占空比作用点，表示LEDC模块在输出PWM信号的过程中，会根据计数器和占空比值比较得出一个结果，将其与hpoint进行比较，然后输出PWM信号。

hpoint = 0（**常规使用**）

- duty = 高电平计数值；PWM 从计数 0 开始输出高电平。适合 LED 调光、电机驱动。

hpoint > 0（相位偏移模式）

- hpoint：计数器到该值才开始输出高电平；

- duty：依旧控制高电平持续多长；波形向后偏移；适合多路相位错开。

| **配置**            | **行为描述**                                                 |
| ------------------- | ------------------------------------------------------------ |
| hpoint=0,duty=512   | 0‑512 高；512‑1023 低；标准 50% 占空比 PWM                   |
| hpoint=200,duty=512 | 0‑199 低；200‑712 高；712‑1023 低；占空比依旧约 50%，波形整体后移 |

 

**output_invert**：启用(1)或禁用(0)gpio输出反相。

```C
// 准备并应用LEDC PWM通道配置
ledc_channel_config_t ledc_channel = {
    .speed_mode     = LEDC_LOW_SPEED_MODE,  //LED模式 低速模式
    .channel        = LEDC_CHANNEL_0,       //通道0
    .timer_sel      = LEDC_TIMER_0,         //定时器源 定时器0
    .intr_type      = LEDC_INTR_DISABLE,    //关闭中断
    .gpio_num       = 5,                    //输出引脚  GPIO5
    .duty           = 0,                    //设置占空比为0
    .hpoint         = 0                     //比较值
};
 
ledc_channel_config(&ledc_channel);
```

### **4.3 改变 PWM 信号**

通道开始运行、生成具有恒定占空比和频率的 PWM 信号之后，有几种方式可以改变该信号。驱动 LED 时，主要通过改变占空比来变化光线亮度。

#### **4.3.1 改变 PWM 占空比**

调用函数 **ledc_set_duty()** 可以设置新的占空比。之后，调用函数 **ledc_update_duty()** 使新配置生效。要查看当前设置的占空比，可使用 *get* 函数 **ledc_get_duty()**。

**（一）设置占空比**

```C
esp_err_t ledc_set_duty(ledc_mode_t speed_mode, ledc_channel_t channel, uint32_t duty);
```

**speed_mode** **:** LEDC速度模式选择，可选参数有高速模式（LEDC_HIGH_SPEED_MODE）或低速模式（LEDC_LOW_SPEED_MODE）

**channel**：- LEDC通道(0 - LEDC_CHANNEL_MAX-1)，从 ledc_channel_t 中选择；

**duty**：设置led的负载，负载设置范围为0 到 (2 的 duty_resolution 次方) - 1；

**（二）更新占空比**

```C
esp_err_t ledc_update_duty(ledc_mode_t speed_mode, ledc_channel_t channel)
```

- **speed_mode**：LEDC速度模式选择，可选参数有高速模式（LEDC_HIGH_SPEED_MODE）或低速模式（LEDC_LOW_SPEED_MODE）

- **channel**：LEDC通道(0 - LEDC_CHANNEL_MAX-1)，从 ledc_channel_t 中选择；

**示例：**假设分辨率设置为 13位。 则50%的占空比= ((2的13次方) - 1) * 50% = （8,192-1）* 0.5 = 4095.5；

```C
    // 设置占空比为50%
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 4095);
    // 更新通道占空比
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
```

另外一种设置占空比和其他通道参数的方式是调用 **通道配置** 一节提到的函数 **ledc_channel_config()**。

传递给函数的占空比数值范围取决于选定的 duty_resolution，应为 0 至 (2 的 duty_resolution 次方) - 1。例如，如选定的占空比分辨率为 10，则占空比的数值范围为 0 至 1023。此时分辨率为 ~0.1%。

#### **4.3.2 改变 PWM 频率**

LED PWM 控制器 API 有多种方式即时改变 PWM 频率：

**（一）设置频率**

通过调用函数 **ledc_set_freq()** 设置频率，可用函数 **ledc_get_freq()** 查看当前频率。

```C
esp_err_t ledc_set_freq(ledc_mode_t speed_mode, ledc_timer_t timer_num, uint32_t freq_hz);
```

- **speed_mode**：LEDC速度模式选择，可选参数有高速模式（LEDC_HIGH_SPEED_MODE）或低速模式（LEDC_LOW_SPEED_MODE）

- **timer_num**： LEDC定时器(0-3)，从ledc_timer_t中选择;

- **freq_hz**：设置led频率;

**（二）绑定通道**

通过调用函数 **ledc_bind_channel_timer()** 将其他定时器绑定到该通道来改变频率和占空比分辨率。

```C
esp_err_t ledc_bind_channel_timer(ledc_mode_t speed_mode, ledc_channel_t channel, ledc_timer_t timer_sel);
```

- **speed_mode** **-**  LEDC速度模式选择，可选参数有高速模式（LEDC_HIGH_SPEED_MODE）或低速模式（LEDC_LOW_SPEED_MODE）

- **channel** **-** LEDC通道(0 - LEDC_CHANNEL_MAX-1)，从 ledc_channel_t 中选择；

- **timer_sel** – LEDC定时器(0-3)，从ledc_timer_t中选择;

**（三）改变通道定时器**

通过调用函数 **ledc_channel_config()** 改变通道的定时器。

 

## **五、硬件连接与准备**

本案例使用板载的LED进行呼吸灯测试。一般人眼睛对于 80HZ 以上刷新频率则完全没有闪烁感，由于频率很高时看不到闪烁，占空比越大 LED 越亮，占空比越小 LED 越暗。所以在频率一定时，可以用不同占空比改变 LED 灯的亮度，使其达到一个呼吸灯的效果（逐渐亮在逐渐灭，如此反复）。

板载的LED接到的引脚是GPIO10，所以我们在初始化时，需要将LEDC功能绑定到GPIO10。

**亮度高**

![img](./img/58072.png)

**亮度低**

![img](./img/58076.png)

## **六、PWM呼吸灯验证**

**6.1 main.c**

```C
/**
 * @brief 应用主函数：程序入口，负责初始化外设并执行主循环逻辑
 */
void app_main(void)
{
    int32_t duty = 0;
    
    // 初始化 LEDC PWM 定时器与输出通道（GPIO10 输出 100Hz PWM 信号）
    pwm_led_init();
 
    // 通过 UART0 输出调试信息，提示 LED 测试开始
    printf("This is pwm led test\n");
 
    // 设置目标占空比：100%，灯为熄灭状态
    ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, 1023);
 
    // 更新占空比：使 ledc_set_duty 设置的值立即生效
    ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
 
    // 主循环：无限循环维持程序运行，LED 保持点亮状态
    while (1)
    {
        //帮忙实现呼吸灯效果，占空比从0%~100%循环变化
        for (duty = 0; duty <= 1023; duty+=10)
        {
            ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty);
            ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(10));
        }
        for (duty = 1023; duty >= 0; duty-=10)
        {
            ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty);
            ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(10));
        }
        // 阻塞延时 50ms：避免空转占用 CPU
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}
```

 

**6.2 pwm.c**

```C
/**
 * ============================================================
 *  文件名称 : pwm.c —— LEDC（PWM）驱动模块（ESP32-S3 / ESP-IDF）
 *  功能描述 : 提供 LEDC 定时器与通道初始化接口 pwm_led_init()，
 *             将 GPIO10 配置为 PWM 输出，用于驱动 LED 亮度。
 *
 *  【引脚与参数定义】
 *    LED_PIN     = GPIO_NUM_10
 *    PWM 频率    = 100Hz
 *    分辨率      = 10 位（占空比范围 0 ~ 1023）
 *    速度模式    = LEDC_LOW_SPEED_MODE
 *    定时器编号  = LEDC_TIMER_0
 *    通道编号    = LEDC_CHANNEL_0
 *
 *  【代码逻辑说明】
 *    1. ledc_timer_config():   配置 LEDC 定时器（频率、分辨率、时钟源等）；
 *    2. ledc_channel_config(): 配置输出通道并关联定时器，映射到 GPIO10，
 *                              同时设置初始占空比与初始输出电平。
 * ============================================================
 */
 
#include "driver/gpio.h"       // GPIO 驱动头文件，提供 gpio 的函数接口
#include "freertos/FreeRTOS.h" // FreeRTOS 内核头文件，提供任务、延时等接口
#include "freertos/task.h"     // FreeRTOS 任务头文件，提供 vTaskDelay 等任务函数
#include <stdio.h>             // 标准输入输出头文件，提供 printf 等函数
 
// 包含 ESP32 LEDC（LED Control）驱动库
// LEDC 是 ESP32 专用的 PWM 控制器，用于生成 PWM 信号
#include "driver/ledc.h"
 
/**
 * @brief LEDC PWM 初始化函数：配置 PWM 定时器与输出通道，使 GPIO10 输出 PWM 信号
 *
 * 注意：本函数使用 LEDC 硬件 PWM 控制器生成波形，而非普通的 GPIO 推挽输出。
 */
void pwm_led_init(void)
{
    // 定义 LEDC 定时器配置结构体，PWM 输出频率 100Hz
    ledc_timer_config_t ledc_timer = {
        // 设置定时器速度模式：低速模式
        .speed_mode = LEDC_LOW_SPEED_MODE,
 
        // 设置定时器编号：定时器0
        .timer_num = LEDC_TIMER_0,
 
        // 设置PWM分辨率：10位（0-1023）
        // 分辨率越高，占空比调节越精细
        .duty_resolution = LEDC_TIMER_10_BIT,
 
        // 设置PWM频率：100Hz
        // 频率越高，PWM周期越短
        .freq_hz = 100,
 
        // 设置定时器分频器：自动计算
        // ESP32会根据频率和分辨率自动计算分频器值
        .clk_cfg = LEDC_AUTO_CLK,
    };
    // 将定时器配置应用到 LEDC 硬件，使定时器生效
    ledc_timer_config(&ledc_timer);
 
    // 定义 LEDC 通道配置结构体
    ledc_channel_config_t ledc_channel = {
        // 设置通道速度模式：低速模式
        .speed_mode = LEDC_LOW_SPEED_MODE,
 
        // 设置通道编号：通道0
        .channel = LEDC_CHANNEL_0,
 
        // 设置定时器编号：定时器0
        // 通道必须关联到一个定时器
        .timer_sel = LEDC_TIMER_0,
 
        // 设置GPIO引脚：GPIO10
        // PWM信号将从该引脚输出
        .gpio_num = GPIO_NUM_10,
 
        // 设置初始占空比：0
        // 占空比范围：0-1023（基于10位分辨率，对应0-100%亮度）
        // 计算公式：占空比值 = (亮度百分比 / 100) * 1023
        .duty = 0,
 
        // 设置初始输出电平：低电平
        .hpoint = 0,
    };
 
    // 将通道配置应用到 LEDC 硬件，PWM 信号从 GPIO10 输出
    ledc_channel_config(&ledc_channel);
}
```

**6.3 CMakeLists.txt**

```C
file(GLOB_RECURSE ALL_SRCS  "./*.c"  )
idf_component_register(SRCS ${ALL_SRCS} 
                       INCLUDE_DIRS ".")
```

 

 