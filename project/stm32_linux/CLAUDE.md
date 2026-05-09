# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个基于 STM32F103C8T6 和 Linux 网关的物联网数据采集与汇聚系统。

### 硬件架构
- **终端节点**：STM32F103C8T6 + FreeRTOS + LVGL + ESP8266 (Wi-Fi)
- **传感器**：SHT30 (I2C) 温湿度传感器
- **显示**：1.8寸 TFT LCD (ST7735, SPI)
- **网关**：Ubuntu 虚拟机作为嵌入式 Linux 网关

### 数据流
```
传感器 → I2C/SPI → STM32 → UART → ESP8266 → TCP → Linux网关 → MQTT → 云端
```

### 引脚分配 (STM32F103C8T6)

| 外设 | 引脚 | 备注 |
|------|------|------|
| USART1 TX/RX | PA9/PA10 | 调试串口 |
| USART2 TX/RX | PA2/PA3 | 连接 ESP8266 |
| I2C2 SCL/SDA | PB10/PB11 | 连接 SHT30 |
| SPI1 SCK/MOSI | PA5/PA7 | LCD 接口 |
| SPI1 NSS (CS) | PA4 | LCD 片选 (软件控制) |
| SWDIO/SWCLK | PA13/PA14 | 调试接口 (勿占用) |
| LCD 背光 PWM | PA8 | TIM1_CH1 |

## 软件架构

### STM32 端 (FreeRTOS)
四个任务并发运行：

| 任务 | 优先级 | 功能 | 栈深 |
|------|--------|------|------|
| SensorTask | 高 | 周期读取 SHT30，打包 JSON | 512B |
| WiFiTask | 中 | ESP8266 初始化、AT 指令、TCP 发送 | 1024B |
| LVGLTask | 中 | 驱动 LCD，显示数据 | 2048B |
| DebugTask | 低 | 串口输出日志 | 256B |

**任务通信**：使用 FreeRTOS 队列传递 JSON 字符串指针

### Linux 网关
- TCP Server (epoll 多路复用，端口 5000)
- 多线程工作者线程池处理文件 I/O 和 MQTT
- JSON 解析验证
- CSV 文件存储 (`/var/iotdata/sensor_log.csv`)
- MQTT 发布到云端 (Eclipse Paho)

## 开发环境

### STM32 开发
- IDE：STM32CubeIDE 或 Keil MDK
- 工具：STM32CubeMX (生成初始化代码)
- 调试：ST-Link V2
- 库：
  - FreeRTOS (CMSIS-RTOS v2)
  - LVGL v8.3
  - cJSON (JSON 生成)

### Linux 网关开发
- 虚拟机：VMware Workstation 或 VirtualBox
- 系统：Ubuntu 20.04 LTS
- 网络模式：桥接模式 (与 STM32 同一局域网)
- 库：
  - cJSON (JSON 解析)
  - Eclipse Paho MQTT C

## 通信协议

### STM32 → Linux (TCP)
- 端口：5000
- 格式：JSON 字符串，UTF-8，以 `\n` 结尾
- 示例：`{"temp":25.6,"humi":60.2}\n`
- 心跳：每 10 秒 `{"ping":1}\n`，回复 `{"pong":1}\n`

### MQTT 发布
- Broker：`broker.emqx.io:1883` (或 test.mosquitto.org)
- Topic：`/student/project/sensor`
- QoS：1
- 消息：`{"id":"stm32_01","ts":"2025-07-20T14:30:02","temp":25.6,"humi":60.2}`

## 开发顺序

### 第一阶段：STM32 底层驱动
1. 点亮 LED，USART1 调试打印
2. 移植 FreeRTOS，测试任务切换
3. 调试 I2C 读取 SHT30
4. 调试 SPI 驱动 LCD (ST7735)
5. 调试 UART2 与 ESP8266 AT 指令通信

### 第二阶段：STM32 集成
1. 将外设驱动封装成任务
2. 实现队列通信机制
3. 移植 LVGL，显示传感器数据
4. ESP8266 TCP 透传与网络调试助手联调

### 第三阶段：Linux 网关
1. 搭建 Ubuntu 环境，编写 TCP Server/Client
2. 引入 epoll 实现多连接管理
3. 集成 cJSON 解析
4. 添加文件存储功能
5. 集成 MQTT 发布

### 第四阶段：系统联调
1. 确保全链路数据完整
2. 演示和文档

## 调试工具

| 工具 | 用途 |
|------|------|
| PuTTY / MobaXterm | 串口调试 |
| NetAssist | TCP 网络调试 |
| MQTTX | MQTT 订阅测试 |
| Git | 版本管理 |

## 关键技术点

### FreeRTOS 配置
- `configUSE_PREEMPTION=1` (抢占式调度)
- `configTOTAL_HEAP_SIZE=12KB`
- 使用 CMSIS-RTOS v2 API

### ESP8266 AT 指令流程
```
AT+CWMODE=1           // Station 模式
AT+CWJAP="SSID","PASS" // 连接路由器
AT+CIPSTART="TCP","192.168.1.xxx",5000 // 连接网关
AT+CIPSEND=len        // 发送数据
```

### Linux epoll 模式
- 边缘触发 (ET) + 非阻塞 fd
- 主线程 epoll 事件循环
- 工作者线程池处理耗时操作

## 文件结构约定

```
stm32_linux/
├── stm32/              # STM32 项目代码 (STM32CubeIDE 项目)
│   ├── Core/
│   ├── Drivers/
│   ├── Middlewares/    # FreeRTOS, LVGL, cJSON
│   └── MDK-ARM/        # Keil 工程 (可选)
└── linux_gateway/      # Linux 网关代码
    ├── src/            # 源文件
    ├── include/        # 头文件
    ├── build/          # 编译输出
    └── data/           # 存储的传感器数据
```

## 常见问题

### ESP8266 连接失败
- 确保 CH_PD 接 3.3V
- 波特率 115200
- 检查路由器 SSID/密码

### LCD 花屏
- SPI 时钟不要太高 (9MHz 以内)
- 检查初始化序列 (ST7735 有不同版本)

### Linux 端口占用
```bash
sudo lsof -i:5000      # 查看端口占用
sudo kill -9 <PID>     # 杀死进程
```
