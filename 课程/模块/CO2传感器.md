[toc]



## **一、CO2传感器**

JW01-CO2 是一款基于 NDIR 非分散红外技术、支持 UART接口、具备温湿度补偿与自动校准功能、量程 350–2000ppm 的 CO₂ 传感器，适配室内空气质量监测、新风系统等低功耗嵌入式场景。

![img](./img/56892.png)

 

![img](./img/56893.png)

 

![img](./img/56894.png)

 

## **二、CO2传感器终端硬件连接**

![img](./img/56895.png)

 

![img](./img/56896.png)

 

![img](./img/56897.png)

## **三、CO2数据帧解析**

CO2传感器采集数据前，需要预热60 秒。预热后，CO2模块会每间隔1秒，通过UART发送一次二氧化碳浓度数据。**数据帧格式如下：**

![img](./img/56898.png)

 

**固定参数解读（B1/B4/B5）**

- B1=0x2C：模块地址固定，代表当前这条数据是本 CO₂模块发出；

- B4=0x03、B5=0xFF：满量程数值 = 0x03 * 256 + 0xFF = 1023 PPM，说明这款传感器测量量程 0~1023ppm。

```C
例如，使用单片机接收数据为：2Ch  01h   90h  03h  0FFh  BFh，使用uint8_t co2_buffer[6];接收该数据，
那么:
    co2_buffer[0] = 0x2C, 
    co2_buffer[1] = 0x01, 
    co2_buffer[2] = 0x90, 
    co2_buffer[3] = 0x30, 
    co2_buffer[4] = 0xFF, 
    co2_buffer[5] = 0xBF, 
    
先计算校验和 = co2_buffer[0] + co2_buffer[1] + co2_buffer[2] + co2_buffer[3] + co2_buffer[4]
            = 取低8位数据=0xBF
            = co2_buffer[5]（校验通过，证明接收的数据是准确的，没有在传输中收到影响）
                    
再计算CO2浓度 = co2_buffer[1] * 256 + co2_buffer[2]
             = 0x01 * 256 + 0x90
             = 400ppm
```

 

## **四、代码示例**

**1. STM32CubeMX配置UART2**

![img](./img/56899.png)

![img](./img/56900.png)

 

![img](./img/56901.png)

**2. 用户代码**

**2.1 添加代码文件**

![img](./img/56902.png)

 

**2.2 co2.c**

```C
#include "co2.h"
#include <string.h>
 
uint8_t co2_buffer[CO2_RX_BUF_SIZE]; // CO2接收缓冲
volatile uint8_t co2_rx_len;         // CO2接收长度
 
// 接收中断回调函数,在HAL_UARTEx_RxEventCallback中调用
void CO2_UART_Callback(uint16_t Size)
{
    co2_rx_len = Size;                                                    // 串口接收中断
    HAL_UARTEx_ReceiveToIdle_IT(&huart2, co2_buffer, sizeof(co2_buffer)); // 开启接收数据
    // printf("co2_rx_len = %d, uart1_buf = %s\n", co2_rx_len, co2_buffer);
}
// 启动接收中断
void CO2_UART_Receive_Start(void)
{
    co2_rx_len = 0;
    memset(co2_buffer, 0, sizeof(co2_buffer));
    HAL_UARTEx_ReceiveToIdle_IT(&huart2, co2_buffer, sizeof(co2_buffer));
}

/**
 * @brief 获取CO2浓度值
 *
 * @param co2_value CO2浓度值
 * @param timeout 超时时间(ms)
 * @return uint8_t 0: 成功;  1:超时;  2:模块地址错误;  3:校验和错误
 */
uint8_t CO2_get_data(uint16_t *co2_value, uint32_t timeout)
{
    uint32_t start_time = HAL_GetTick();
    while (1)
    {
        if (co2_rx_len == CO2_RX_BUF_SIZE) {
            break;
        }
        if (HAL_GetTick() - start_time > timeout)
        {
            return 1;
        }
    }
    
 
    co2_rx_len = 0; // 重新接收
 
    // 1. 校验模块地址（第1字节为0x2C）
    if (co2_buffer[0] != 0x2C)
    {
        return 2;
    }
 
    // 2. 计算和校验
    uint8_t check_sum = 0;
    for (uint8_t i = 0; i < CO2_RX_BUF_SIZE - 1; i++)
    {
        check_sum += co2_buffer[i];
    }
 
    if (check_sum != co2_buffer[CO2_RX_BUF_SIZE - 1]) // 校验和不匹配
    {
        return 3;
    }
 
    // 3. 解析CO2浓度值
    *co2_value = (co2_buffer[1] << 8) | co2_buffer[2];
 
    return 0;
}
 
```

 

**2.3 co2.h**

```C
#ifndef CO2_H
#define CO2_H
 
#include "main.h"
#include "usart.h"
 
#define CO2_RX_BUF_SIZE 6 // 调试接收缓冲区大小
 
extern uint8_t co2_buffer[CO2_RX_BUF_SIZE]; // CO2接收缓冲
extern volatile uint8_t co2_rx_len;         // CO2接收长度
 
void CO2_UART_Callback(uint16_t Size);
void CO2_UART_Receive_Start(void);
uint8_t CO2_get_data(uint16_t *co2_value, uint32_t timeout);
#endif
 
```

 

**2.4** **ISR_callback.c**

![img](./img/56903.png)

 

**2.5 app_main.c**

```C
#include "app_main.h" 
#include "main.h" 
#include "tim.h" // 包含STM32CubeMX生成的TIM头文件 
#include "debug.h" 
#include "co2.h"
 
...省略中间代码显示
 
// 替代main函数中的while循环
void app_main(void)
{
    uint32_t tick_1S = HAL_GetTick();
    uint16_t co2_value = 0; // CO2浓度值
    uint8_t ret = 0;
 
    Debug_UART_Receive_Start(); // 启动调试串口接收
    CO2_UART_Receive_Start();   // 启动CO2传感器串口接收
 
    while (1) // 你可以在这里处理其它事情的代码
    {
        if (HAL_GetTick() - tick_1S >= 1000)
        {
            tick_1S = HAL_GetTick();
            HAL_GPIO_TogglePin(LED_GPIO_Port, LED_Pin);
            ret = CO2_get_data(&co2_value, 1000);
            if (ret)
            {
                printf("CO2传感器通信失败,ret = %d\n", ret);
            }
            else
            {
                printf("CO2浓度：%hhu ppm\n", co2_value);
            }
        }
    }
}
```

 

**3. 现象**

![img](./img/56904.png)

 