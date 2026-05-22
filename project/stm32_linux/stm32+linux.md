# **基于 FreeRTOS 的物联网终端 + Linux 网关数据汇聚系统**

好的，这是一份按你的要求，以“论文形式”撰写的完整项目方案。你可以把它当作一本详细的开发手册，边学边做。

---

# 基于STM32与Linux虚拟网关的物联网数据采集系统设计

## 摘要
本项目旨在设计一套**物联网数据采集与汇聚系统**，充分利用手头现有的 STM32F103C8T6 开发板和普通 PC 机。系统采用**双处理器架构**：STM32 作为**物联网终端节点**，负责传感器数据采集、本地显示与无线发送；PC 端 Ubuntu 虚拟机作为**嵌入式 Linux 网关**，负责数据接收、持久化存储与云端转发。项目完整覆盖嵌入式开发核心技术栈，包括 FreeRTOS 实时操作系统、LVGL 图形界面、串口 Wi-Fi 透传、Linux 网络编程（Socket/Epoll）、多线程并发、JSON 数据交换与 MQTT 协议上云，适用于嵌入式 Linux 应用开发方向的求职作品展示。

**关键词**：STM32；FreeRTOS；LVGL；嵌入式 Linux；Epoll；MQTT；物联网网关

---

## 1. 引言
随着物联网技术的普及，大量设备需要接入网络，但单个设备往往资源受限。典型的解决方案是**“终端节点 + 网关”**架构。本设计模拟这一架构，以低成本、高可复现性为原则，采用 STM32F103C8T6 作为弱终端，借助 ESP-01S Wi-Fi 模块实现无线通信；利用个人电脑 Ubuntu 虚拟机搭建功能完备的嵌入式 Linux 网关，实现对终端数据的汇聚、处理和上云。

本项目完整覆盖从底层硬件驱动到上层应用协议的全链路，可作为嵌入式 Linux 应用开发工程师的能力证明。

## 2. 系统总体架构

### 2.1 物理拓扑
```
传感器 ──┬── I2C/SPI ── STM32F103C8T6 (FreeRTOS + LVGL) ── UART ── ESP8266 (Wi-Fi)
          │                                          │
          └── 按键/蜂鸣器等                           └── LCD/OLED (SPI)
          
                                            ↓ (TCP/Wi-Fi)

                         PC Ubuntu 虚拟机 (Linux 网关)
                         ├── TCP Server (Socket + Epoll)
                         ├── 数据解析 (JSON)
                         ├── 本地存储 (文件 I/O)
                         └── MQTT Client → 公共云平台
```

### 2.2 数据流
1.  STM32 通过 I2C 读取温湿度传感器 SHT30，通过 SPI 读取 LCD 触摸坐标。
2.  采集到的数据打包成 JSON 字符串，经 FreeRTOS 消息队列传递到 UART 发送任务。
3.  串口通过 ESP8266 模块以 STA 模式连接路由器，使用 TCP 协议将 JSON 数据发送给 Linux 网关。
4.  Linux 网关开启高并发 TCP Server，接收多个客户端连接（模拟多终端），解析 JSON 后存入本地文件，同时通过 MQTT 发布到云端。

## 3. 硬件选型与 STM32F103C8T6 引脚全分配

### 3.1 硬件清单
| 模块         | 型号                                 | 用途                     |
| :----------- | :----------------------------------- | :----------------------- |
| 主控芯片     | STM32F103C8T6 (Blue Pill/最小系统板) | 终端主控                 |
| Wi-Fi 模块   | ESP-01S (ESP8266)                    | 无线通信                 |
| 温湿度传感器 | SHT30 (I2C)                          | 环境数据采集             |
| 显示屏       | 1.8寸 TFT LCD (ST7735, SPI)          | 本地数据显示与 LVGL 界面 |
| 调试器       | ST-Link V2                           | 程序下载与调试           |

### 3.2 STM32F103C8T6 引脚分配总表

下表列出 STM32F103C8T6 所有引脚的默认功能、可复用功能，以及**在本项目中的具体用途**。未用到引脚标记为“预留”，后续可扩展其他外设。

| 引脚编号 | 引脚名称 | 默认功能       | 复用功能(部分)   | 本项目用途              | 备注                       |
| :------: | :------- | :------------- | :--------------- | :---------------------- | :------------------------- |
|    1     | VBAT     | 备份电源       | -                | 接3.3V                  | 电池备份域供电             |
|    2     | PC13     | GPIO/ 侵入检测 | TAMPER-RTC       | 预留                    | 可用作输出，注意驱动能力弱 |
|    3     | PC14     | GPIO           | OSC32_IN         | 预留                    | 外部低速晶振输入脚         |
|    4     | PC15     | GPIO           | OSC32_OUT        | 预留                    | 外部低速晶振输出脚         |
|    5     | OSC_IN   | 主晶振输入     | -                | 接8MHz晶振              | 系统时钟源                 |
|    6     | OSC_OUT  | 主晶振输出     | -                | 接8MHz晶振              | 系统时钟源                 |
|    7     | NRST     | 复位           | -                | 接复位按键              | 低电平复位                 |
|    8     | VSSA     | 模拟地         | -                | GND                     | 模拟部分地                 |
|    9     | VDDA     | 模拟电源       | -                | 3.3V                    | 模拟部分供电               |
|    10    | PA0      | GPIO           | TIM2_CH1/ADC_IN0 | **ADC 通道0**           | 备用电池电压检测（可选）   |
|    11    | PA1      | GPIO           | TIM2_CH2/ADC_IN1 | 预留                    | 可做通用IO                 |
|    12    | PA2      | GPIO           | USART2_TX        | **USART2 TX**           | 连接 ESP8266 的 RXD        |
|    13    | PA3      | GPIO           | USART2_RX        | **USART2 RX**           | 连接 ESP8266 的 TXD        |
|    14    | PA4      | GPIO           | SPI1_NSS/ADC_IN4 | **SPI1 NSS (软件控制)** | LCD 片选信号               |
|    15    | PA5      | GPIO           | SPI1_SCK         | **SPI1 SCK**            | LCD 时钟线                 |
|    16    | PA6      | GPIO           | SPI1_MISO        | **SPI1 MISO**           | LCD 主入从出 (可不用)      |
|    17    | PA7      | GPIO           | SPI1_MOSI        | **SPI1 MOSI**           | LCD 主出从入               |
|    18    | PB0      | GPIO           | ADC_IN8          | 预留                    | 可做按键输入               |
|    19    | PB1      | GPIO           | ADC_IN9          | 预留                    | 可做LED输出                |
|    20    | PB2      | GPIO           | BOOT1            | 预留                    | 注意启动配置               |
|    21    | PB10     | GPIO           | I2C2_SCL         | **I2C2 SCL**            | SHT30 时钟线 (复用)        |
|    22    | PB11     | GPIO           | I2C2_SDA         | **I2C2 SDA**            | SHT30 数据线 (复用)        |
|    23    | VSS      | 地             | -                | GND                     | 数字地                     |
|    24    | VDD      | 电源           | -                | 3.3V                    | 数字电源                   |
|    25    | PB12     | GPIO           | SPI2_NSS         | 预留                    | 可接SD卡片选               |
|    26    | PB13     | GPIO           | SPI2_SCK         | 预留                    | 可接SD卡时钟               |
|    27    | PB14     | GPIO           | SPI2_MISO        | 预留                    | 可接SD卡数据               |
|    28    | PB15     | GPIO           | SPI2_MOSI        | 预留                    | 可接SD卡数据               |
|    29    | PA8      | GPIO           | MCO/ TIM1_CH1    | **LCD 背光 PWM**        | TIM1_CH1 输出PWM调光       |
|    30    | PA9      | GPIO           | USART1_TX        | **调试串口 TX**         | 连接 ST-Link 虚拟串口或 PC |
|    31    | PA10     | GPIO           | USART1_RX        | **调试串口 RX**         | 连接 ST-Link 虚拟串口或 PC |
|    32    | PA11     | GPIO           | USB D-           | 预留                    | USB 接口                   |
|    33    | PA12     | GPIO           | USB D+           | 预留                    | USB 接口                   |
|    34    | PA13     | GPIO           | SWDIO            | **SWDIO**               | 调试接口数据线             |
|    35    | VSS      | 地             | -                | GND                     | 数字地                     |
|    36    | VDD      | 电源           | -                | 3.3V                    | 数字电源                   |
|    37    | PA14     | GPIO           | SWCLK            | **SWCLK**               | 调试接口时钟线             |
|    38    | PA15     | GPIO           | JTDI             | 预留                    | 可做GPIO，注意调试占用     |
|    39    | PB3      | GPIO           | JTDO             | 预留                    | 可做GPIO                   |
|    40    | PB4      | GPIO           | JNTRST           | 预留                    | 可做GPIO                   |
|    41    | PB5      | GPIO           | I2C1_SMBA        | 预留                    | 可做GPIO                   |
|    42    | PB6      | GPIO           | I2C1_SCL         | 预留                    | 可做GPIO                   |
|    43    | PB7      | GPIO           | I2C1_SDA         | 预留                    | 可做GPIO                   |
|    44    | BOOT0    | 启动选择       | -                | 通过跳线帽接地          | 启动模式选择               |
|    45    | PB8      | GPIO           | TIM4_CH3         | 预留                    | 可做蜂鸣器输出             |
|    46    | PB9      | GPIO           | TIM4_CH4         | 预留                    | 可做按键输入               |
|    47    | VSS      | 地             | -                | GND                     | 数字地                     |
|    48    | VDD      | 电源           | -                | 3.3V                    | 数字电源                   |

> **说明**：实际焊接/使用杜邦线连接时，可根据上表颜色区分已用引脚。调试接口（PA13/PA14）勿占用。ESP8266 工作于 3.3V，与 STM32 可直接连接。

## 4. 软件技术栈详细设计

### 4.1 STM32 终端软件架构
整体基于 **FreeRTOS** 实时操作系统，划分四个任务，最大程度利用 MCU 资源并保证实时性。

#### 4.1.1 任务划分与通信机制
| 任务名称       | 优先级 | 功能                                           | 栈深  | 交互方式                  |
| :------------- | :----: | :--------------------------------------------- | :---: | :------------------------ |
| **SensorTask** |   高   | 周期读取 SHT30 传感器，打包 JSON               | 512B  | 发送消息到 `sensorQueue`  |
| **WiFiTask**   |   中   | 负责 ESP8266 初始化、AT 指令响应、TCP 数据发送 | 1024B | 从 `sensorQueue` 接收数据 |
| **LVGLTask**   |   中   | 驱动 LCD 屏幕，显示温度、湿度、IP 等           | 2048B | 直接读取全局变量或队列    |
| **DebugTask**  |   低   | 通过 USART1 输出系统运行日志                   | 256B  | 串口发送                  |

**通信核心**：使用 FreeRTOS 队列 `xQueueCreate` 传递 JSON 字符串指针，WiFiTask 阻塞等待队列消息。

#### 4.1.2 关键技术点
**a) FreeRTOS 配置**  
   - 在 `FreeRTOSConfig.h` 中设置 `configUSE_PREEMPTION=1`，开启抢占式调度，确保传感器采集不被阻塞。  
   - 总堆大小 `configTOTAL_HEAP_SIZE` 设为 12KB（适合 C8T6 20KB SRAM）。  
   - 使用 CMSIS-RTOS v2 API 封装，便于移植。

**b) I2C 驱动 SHT30**  
   - 使用 STM32 HAL 库的 `HAL_I2C_Mem_Read` 进行 16 位寄存器读取。  
   - 通信速率设为 100kHz (标准模式)。  
   - 数据解析公式：温度 `T = -45 + 175 * (raw / 65535)`，湿度类似。  
   - 加入 CRC8 校验，保证数据完整性。

**c) UART 驱动 ESP8266**  
   - USART2 波特率设为 115200，使能空闲中断 (IDLE) + DMA 接收不定长数据。  
   - 封装 AT 指令发送与应答解析函数。典型流程：  
     `AT+CWMODE=1` → 设为 Station 模式  
     `AT+CWJAP="SSID","PASS"` → 连接路由器  
     `AT+CIPSTART="TCP","192.168.1.xxx",5000` → 连接网关服务器  
     `AT+CIPSEND=len` → 发送数据  
   - JSON 数据发送时，长度控制在 256 字节以内，避免分包。

**d) SPI 驱动 LCD (ST7735)**  
   - 使用 SPI1，速率 9MHz，发送格式 MSB First，CPOL=0, CPHA=0。  
   - PA4 作软件片选，每次操作前拉低，完成拉高。  
   - 移植 LVGL 时提供 `lv_port_disp_init`，实现 `disp_flush` 回调，用 SPI DMA 加速刷屏。

**e) LVGL 界面设计**  
   - LVGL 心跳由 `SysTick` 1ms 中断调用 `lv_tick_inc(1)`。  
   - `lv_task_handler` 在 LVGLTask 中周期调用 (5ms 周期)。  
   - 界面元素：一个 `lv_label` 显示温度和湿度，一个 `lv_arc` 模拟仪表盘。  
   - 数据更新：LVGLTask 轮询全局变量 `g_temp`、`g_humi`，由 SensorTask 更新这些变量（配合互斥锁保护）。

**f) JSON 生成**  
   - 使用轻量级库 **cJSON** 生成 JSON 字符串：  
     ```c
     cJSON *root = cJSON_CreateObject();
     cJSON_AddNumberToObject(root, "temp", 25.6);
     cJSON_AddNumberToObject(root, "humi", 60.2);
     char *json_str = cJSON_PrintUnformatted(root);
     // 发送到队列后，释放内存
     ```

### 4.2 Linux 网关软件架构

#### 4.2.1 开发环境
在 Windows 上安装 **VMware Workstation**（或 VirtualBox），创建 Ubuntu 20.04 虚拟机，分配 2 核 CPU、2GB 内存、20GB 硬盘。网络模式设为**桥接模式**，使虚拟机与主机及开发板处于同一局域网。

#### 4.2.2 模块设计与核心技术
**a) TCP 并发服务器 (核心)**  
   - 使用 **epoll** I/O 多路复用，支持同时连接多个 STM32 终端。  
   - 流程：`socket()` → `bind()` → `listen()` → `epoll_create1()` → 注册 `listenfd` 和所有 `connfd`，关注 `EPOLLIN` 事件。  
   - 当 `listenfd` 就绪，调用 `accept` 获得新连接，加入 epoll 监视。  
   - 当客户端 fd 有数据到达，读取数据，解析 JSON，然后进行存储和转发。  
   - 采用**边缘触发 (ET) 模式** + 非阻塞 fd，配合 while 循环读取直到 `EAGAIN`，提高效率。

**b) 多线程处理**  
   - 主线程负责 epoll 事件循环。  
   - 创建**工作者线程池**（例如 4 个线程），用于处理耗时的文件 I/O 和 MQTT 发布，避免阻塞主循环。  
   - 线程间通过任务队列与互斥锁、条件变量协作。主线程将解析后的 JSON 数据插入队列，通知工作线程处理。

**c) JSON 解析与数据验证**  
   - 使用 **cJSON** 库解析接收到的 JSON 字符串，提取温湿度数值。  
   - 进行合理性检查（如温度范围 -40~80℃），非法数据丢弃并记录日志。

**d) 文件 I/O 存储**  
   - 工作线程将有效数据以 CSV 格式追加写入 `/var/iotdata/sensor_log.csv`。  
   - 每一行格式：`时间戳,温度,湿度`，示例 `2025-07-20 14:30:02,25.6,60.2`。  
   - 使用 Linux 系统调用 `open()`, `write()`, `close()` 保证数据安全，用**文件锁**防止多线程交错写入。  
   - 每日生成一个新文件，便于查看。

**e) MQTT 客户端**  
   - 使用 **Eclipse Paho MQTT C 库**，在另一工作线程中维护与云端 broker (如 test.mosquitto.org 或 OneNET) 的长连接。  
   - 发布主题：`/dorm/sensor/data`，QoS 1。  
   - 消息内容为 JSON 字符串，增加设备 ID 字段：`{"dev":"stm32_01","t":25.6,"h":60.2}`。  
   - 心跳保持：设置 keepAlive 60 秒，启用自动重连。

**f) 日志与调试**  
   - 主线程控制台实时打印连接记录和数据。  
   - 使用 `syslog` 或简单 `fprintf(stderr, ..)` 输出到日志文件。

## 5. 通信协议设计

### 5.1 STM32 与 Linux 网关通信协议 (基于 TCP)
- 传输层：TCP，端口号 **5000**。
- 数据格式：JSON 字符串，UTF-8 编码，以换行符 `\n` 作为帧结束标志。
- 示例数据包：
  ```json
  {"temp":25.6,"humi":60.2}\n
  ```
- 心跳包：每隔 10 秒发送 `{"ping":1}\n`，网关回复 `{"pong":1}\n`，用于保持连接和检测离线。

### 5.2 MQTT 发布主题定义
- 主题：`/student/project/sensor`  (可自定义)
- 消息：`{"id":"stm32_01","ts":"2025-07-20T14:30:02","temp":25.6,"humi":60.2}`
- QoS：1 (至少一次，保证可靠到达)
- 演示时可用公共 broker：`broker.emqx.io:1883`，使用客户端工具 (MQTTX) 订阅观察。

## 6. 系统实现步骤

### 6.1 开发顺序建议
1.  **STM32 底层驱动验证**  
    - 点亮 LED，调试 USART1 打印。  
    - 移植 FreeRTOS，测试任务切换。  
    - 分别调试 I2C 读 SHT30、SPI 刷屏、UART2 与 ESP8266 AT 指令通信。
2.  **STM32 集成与 LVGL 移植**  
    - 把三个外设驱动封装成任务，加入队列通信。  
    - 移植 LVGL，展示传感器值。  
    - 完成 ESP8266 TCP 透传，与网络调试助手通信成功。
3.  **Linux 网关开发**  
    - 搭建 Ubuntu 环境，编写简单的 TCP Server 和客户端测试。  
    - 引入 epoll，实现多连接管理。  
    - 集成 cJSON 解析，测试与 STM32 数据交互。  
    - 添加文件存储和 MQTT 发布。
4.  **系统联调**  
    - 确保整个链路数据完整、实时。  
    - 录制演示视频，截图关键代码。  
    - 记录遇到的重难点及解决方案，充实简历。

### 6.2 工具链
- STM32CubeIDE / Keil MDK + STM32CubeMX 生成初始化代码。
- 串口调试助手 (putty / mobaxterm)。
- 网络调试助手 (NetAssist) 模拟 TCP 客户端。
- MQTTX 订阅测试。
- Git 版本管理。

## 7. 预期成果与展示
- **STM32 节点**：一块带 1.8 寸彩屏、Wi-Fi 天线的终端板，实时显示温湿度，并无线发送。  
- **Linux 网关**：Ubuntu 终端显示连接日志，磁盘文件持续记录数据，云端仪表盘实时更新。  
- **项目简历描述**：  
  > 独立设计并实现基于 STM32 与 Linux 的物联网数据采集系统。在 STM32 上移植 FreeRTOS 与 LVGL，实现四任务并发与 SPI/I2C 驱动；利用 ESP8266 实现 TCP 无线通信，自定义 JSON 协议；在 Ubuntu 上开发 epoll 高并发 TCP 服务器，配合多线程与文件 I/O 完成数据持久化，并集成 MQTT 上云。打通了从传感器到云端的全链路，具备嵌入式 Linux 应用开发所需的网络编程、并发处理和系统集成能力。

## 8. 总结
本设计充分利用有限的低成本硬件，模拟了真实物联网网关的核心功能，覆盖了嵌入式 Linux 应用开发方向的绝大部分技术要点。对于普通二本院校学生，该项目足以在秋招中证明你对 Linux 网络编程、多线程、FreeRTOS 以及外设驱动等技术的掌握程度，也为后续学习更复杂的 Linux 系统编程打下坚实基础。

---
**附录 A：参考文献**
- STM32F103C8T6 Datasheet, STMicroelectronics.
- FreeRTOS Reference Manual.
- LVGL Documentation v8.3.
- EPOLL(7) Linux Programmer's Manual.
- ESP8266 AT Instruction Set.

**附录 B：组装接线表 (简化)**
| 信号          | STM32 引脚 | 目标模块引脚       |
| :------------ | :--------: | :----------------- |
| I2C SCL       |    PB10    | SHT30 SCL          |
| I2C SDA       |    PB11    | SHT30 SDA          |
| SPI SCK       |    PA5     | LCD SCK            |
| SPI MOSI      |    PA7     | LCD SDA            |
| SPI CS        |    PA4     | LCD CS             |
| LCD DC        | PB0 (预留) | LCD DC (命令/数据) |
| LCD RST       | PB1 (预留) | LCD RST            |
| UART2 TX      |    PA2     | ESP8266 RXD        |
| UART2 RX      |    PA3     | ESP8266 TXD        |
| ESP8266 CH_PD |    3.3V    | ESP8266 EN         |
| 背光PWM       |    PA8     | LCD BL             |

> 注：LCD DC/RST 可选其他 GPIO，本表给出示例，修改时调整代码宏定义即可。

---

这份方案既详细又实际，所有技术点都是你培训课程里会学到的，完全可以动手操作。你只要按照步骤一个个调通，秋招时这将是一份沉甸甸的项目经历。祝顺利！