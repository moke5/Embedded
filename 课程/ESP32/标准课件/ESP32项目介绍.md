# ESP32项目介绍

[toc]



## **一、ESP32-S3概述**

![img](./img/57932.png)

**ESP32-S3** 是一款集成 2.4 GHz Wi-Fi 和 Bluetooth 5 (LE) 的 MCU 芯片，支持远距离模式 (Long Range)。ESP32-S3 搭载 Xtensa® 32 位 LX7 双核处理器，主频高达 240 MHz，内置 512 KB SRAM (TCM)，具有 45 个可编程 GPIO 管脚和丰富的通信接口。ESP32-S3 支持更大容量的高速 Octal SPI flash 和片外 RAM，支持用户配置数据缓存与指令缓存。

 

**丰富的 IO 接口**

ESP32-S3 拥有 45 个可编程 GPIO 以及 SPI、I2S、I2C、PWM、RMT、ADC、UART、SD/MMC 主机控制器和 TWAITM 控制器等常用外设接口。其中的 14 个 GPIO 可被配置为 HMI 交互的电容触摸输入端。此外，ESP32-S3 搭载了超低功耗协处理器 (ULP)，支持多种低功耗模式，广泛适用于各类低功耗应用场景。

 

**Wi-Fi + Bluetooth 5 (LE)**

ESP32-S3 集成 2.4 GHz Wi-Fi (802.11 b/g/n)，支持 40 MHz 带宽；其低功耗蓝牙子系统支持 Bluetooth 5 (LE) 和 Bluetooth Mesh，可通过 Coded PHY 与广播扩展实现远距离通信。它还支持 2 Mbps PHY，用于提高传输速度和数据吞吐量。ESP32-S3 的 Wi-Fi 和 Bluetooth LE 射频性能优越，在高温下也能稳定工作。

 

**支持 AI 加速**

ESP32-S3 MCU 增加了用于加速神经网络计算和信号处理等工作的向量指令 (vector instructions)。AI 开发者们通过 ESP-DSP 和 ESP-NN 库使用这些向量指令，可以实现高性能的图像识别、语音唤醒和识别等应用。ESP-WHO 和 ESP-Skainet 也将支持此功能。

 

**完善的安全机制**

ESP32-S3 为物联网设备提供了完善的安全机制和保护措施，防止各类恶意攻击和威胁。它支持基于 AES-XTS 算法的 flash 加密、基于 RSA 算法的安全启动、数字签名和 HMAC。ESP32-S3 还新增了一个“世界控制器 (World Controller)”模块，提供了两个互不干扰的执行环境，实现可信执行环境或权限分离机制。

 

**成熟的软件支持**

ESP32-S3 沿用乐鑫成熟的物联网开发框架 ESP-IDF。ESP-IDF 已成功赋能了数以亿计物联网设备，历经了严格的测试和发布周期，具有清晰有效的支持策略。开发人员基于其成熟的软件架构，凭借对工具和 API 的熟悉，将更容易构建应用程序或迁移原有程序至 ESP32-S3 平台。

 

**官网链接**

- **乐鑫官网资料：**https://www.espressif.com.cn/zh-hans/products/socs/esp32/resources﻿

- **立创官网资料：**https://lceda001.feishu.cn/wiki/JNDHwxPWWi99CJk6SkMc6Z3Yn2e﻿

 

## **二、小智AI**

#### **2.1 官方产品功能介绍**

小智AI项目是由虾哥发起并开源的一个项目。该项目能帮助更多人入门AI硬件开发，了解如何将当下飞速发展的大语言模型应用到实际的硬件设备中。

小智AI功能如下：

- WiFi / ML307 Cat.1 4G

- BOOT键唤醒和打断，支持点击和长按两种触发方式

- 离线语音唤醒ESP-SR

- 流式语音对话（WebSocket或UDP协议）

- 支持国语、粤语、英语、日语、韩语5种语言识别（SenseVoice）

- 声纹识别，识别是谁在喊AI的名字（3D Speaker）

- 大模型TTS（火山引擎或CosyVoice）

- 大模型LLM（Qwen2.5 72B 或 豆包API）

- 可配置的提示词和音色（自定义角色）

- 短期记忆，每轮对话后自我总结

- OLED / LCD显示屏，显示信号强弱或对话内容

- 支持LCD显示图片表情

 

**硬件细节**

（1）系统使用 ESP32-S3-N16R8 为主控芯片，集成 Wi-Fi（2.4G）与蓝牙 5.0 双模通信，支持多网络环境接入。

（2）搭载 INMP441 麦克风模块与 MAX98357 音频解码芯片，实现高精度语音采集与立体声播放，支持自定义唤醒词（如 “小智你好”）及连续对话功能。

（3）集成 0.91 英寸 OLED_I2C 显示屏，实时显示设备状态、对话内容、AI 响应结果等信息，支持中 / 英文图文界面自定义。

（4）支持多 AI 智能体无缝切换，可通过 Web 配置界面或语音指令切换豆包大模型、DeepSeek、阿里云 Qwen 等云端 AI 服务，实现个性化交互体验。

（5）内置本地语音预处理算法，支持环境降噪、关键词检测，优化离线唤醒与在线语音识别效率。

#### **2.2 最新版本**

**📢访问地址：**[xiaozhi-esp32: 小智 AI 聊天机器人 （XiaoZhi AI Chatbot） 小智国内同步镜像](https://gitee.com/ghosthack/xiaozhi-esp32)﻿

![img](./img/57964.png)

#### **2.3 官方描述-An MCP-based Chatbot（基于MCP的聊天机器人）**

（中文 | [English](https://gitee.com/ghosthack/xiaozhi-esp32/blob/main/README_en.md) | [日本語](https://gitee.com/ghosthack/xiaozhi-esp32/blob/main/README_ja.md)）

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#介绍)**2.3.1 介绍**

👉 [人类：给 AI 装摄像头 vs AI：当场发现主人三天没洗头【bilibili】](https://gitee.com/link?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1bpjgzKEhd%2F)

👉 [手工打造你的 AI 女友，新手入门教程【bilibili】](https://gitee.com/link?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1XnmFYLEJN%2F)

小智 AI 聊天机器人作为一个语音交互入口，利用 Qwen / DeepSeek 等大模型的 AI 能力，通过 MCP 协议实现多端控制。

![img](./img/57926.png)

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#版本说明)**（一）版本说明**

当前 v2 版本与 v1 版本分区表不兼容，所以无法从 v1 版本通过 OTA 升级到 v2 版本。分区表说明参见 [partitions/v2/README.md](https://gitee.com/ghosthack/xiaozhi-esp32/blob/main/partitions/v2/README.md)。

使用 v1 版本的所有硬件，可以通过手动烧录固件来升级到 v2 版本。

v1 的稳定版本为 1.9.2，可以通过 git checkout v1 来切换到 v1 版本，该分支会持续维护到 2026 年 2 月。

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#已实现功能)**（二）已实现功能**

- Wi-Fi / ML307 Cat.1 4G

- 离线语音唤醒 [ESP-SR](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fespressif%2Fesp-sr)

- 支持两种通信协议（[Websocket](https://gitee.com/ghosthack/xiaozhi-esp32/blob/main/docs/websocket.md) 或 MQTT+UDP）

- 采用 OPUS 音频编解码

- 基于流式 ASR + LLM + TTS 架构的语音交互

- 声纹识别，识别当前说话人的身份 [3D Speaker](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fmodelscope%2F3D-Speaker)

- OLED / LCD 显示屏，支持表情显示

- 电量显示与电源管理

- 支持多语言（中文、英文、日文）

- 支持 ESP32-C3、ESP32-S3、ESP32-P4 芯片平台

- 通过设备端 MCP 实现设备控制（音量、灯光、电机、GPIO 等）

- 通过云端 MCP 扩展大模型能力（智能家居控制、PC桌面操作、知识搜索、邮件收发等）

- 自定义唤醒词、字体、表情与聊天背景，支持网页端在线修改 ([自定义Assets生成器](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2F78%2Fxiaozhi-assets-generator)

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#硬件)**2.3.2 硬件**

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#面包板手工制作实践)**（一）面包板手工制作实践**

详见飞书文档教程：

👉 [《小智 AI 聊天机器人百科全书》](https://gitee.com/link?target=https%3A%2F%2Fccnphfhqs21z.feishu.cn%2Fwiki%2FF5krwD16viZoF0kKkvDcrZNYnhb%3Ffrom%3Dfrom_copylink)

面包板效果图如下：

![img](./img/57936.png)

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#支持-70-多个开源硬件仅展示部分)**（二）支持 70 多个开源硬件（仅展示部分）**

- 立创·实战派 ESP32-S3 开发板

- 乐鑫 ESP32-S3-BOX3

- M5Stack CoreS3

- M5Stack AtomS3R + Echo Base

- 神奇按钮 2.4

- 微雪电子 ESP32-S3-Touch-AMOLED-1.8

- LILYGO T-Circle-S3

- 虾哥 Mini C3

- 璀璨·AI 吊坠

- 无名科技 Nologo-星智-1.54TFT

- SenseCAP Watcher

- ESP-HI 超低成本机器狗[ ](https://gitee.com/ghosthack/xiaozhi-esp32/blob/main/docs/v1/lichuang-s3.jpg)

![img](./img/57956.png)

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#软件)**2.3.3 软件**

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#固件烧录)**（一）固件烧录**

新手第一次操作建议先不要搭建开发环境，直接使用免开发环境烧录的固件。

固件默认接入 [xiaozhi.me](https://gitee.com/link?target=https%3A%2F%2Fxiaozhi.me) 官方服务器，个人用户注册账号可以免费使用 Qwen 实时模型。

👉 [新手烧录固件教程](https://gitee.com/link?target=https%3A%2F%2Fccnphfhqs21z.feishu.cn%2Fwiki%2FZpz4wXBtdimBrLk25WdcXzxcnNS)

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#开发环境)**（二）开发环境**

- Cursor 或 VSCode

- 安装 ESP-IDF 插件，选择 SDK 版本 5.4 或以上

- Linux 比 Windows 更好，编译速度快，也免去驱动问题的困扰

- 本项目使用 Google C++ 代码风格，提交代码时请确保符合规范

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#开发者文档)**（三）开发者文档**

- 自定义开发板指南 - 学习如何为小智 AI 创建自定义开发板

- MCP 协议物联网控制用法说明 - 了解如何通过 MCP 协议控制物联网设备

- MCP 协议交互流程 - 设备端 MCP 协议的实现方式

- MQTT + UDP 混合通信协议文档

- 一份详细的 WebSocket 通信协议文档

[﻿](https://gitee.com/ghosthack/xiaozhi-esp32#大模型配置)**2.3.4 大模型配置**

如果你已经拥有一个小智 AI 聊天机器人设备，并且已接入官方服务器，可以登录 [xiaozhi.me](https://gitee.com/link?target=https%3A%2F%2Fxiaozhi.me) 控制台进行配置。

👉 [后台操作视频教程（旧版界面）](https://gitee.com/link?target=https%3A%2F%2Fwww.bilibili.com%2Fvideo%2FBV1jUCUY2EKM%2F)

[ ](https://gitee.com/ghosthack/xiaozhi-esp32#相关开源项目)

[ ](https://gitee.com/ghosthack/xiaozhi-esp32#关于项目)

**2.3.5 应用场景**

**智能家居领域：**可接入智能家居设备，用户通过语音指令控制智能音箱播放音乐、查询天气，或让智能家电调整工作模式。

**智能办公场景：**能成为智能办公助手，语音记录会议内容、查询资料、安排日程等。

**智能教育设备：**为学生提供个性化学习辅导，解答学科问题、进行语言学习对话练习。

 

## **四、ESP32与STM32差别**

#### **4.1 STM32**

**厂商：**意法半导体（STMicroelectronics）

**特点：**产品线极丰富（如 **STM32F1**/F4/F7 系列），适合工业控制、嵌入式设备、消费电子等复杂场景。需外接 Wi-Fi / 蓝牙模块（部分型号集成，但非主打功能）。

![img](./img/57960.png)

#### **4.2 ESP32**

**厂商：**乐鑫科技（Espressif）

**特点：**内置 Wi-Fi（2.4G）和蓝牙（经典蓝牙 / BLE），支持 MQTT/HTTP 等网络协议，适合物联网终端（如智能家电、传感器、路由器）。

![img](./img/57918.png)

#### **4.3 ESP32-S3模组**

ESP32-S3-WROOM-1 和 ESP32-S3-WROOM-1U 是两款通用型 Wi-Fi + 低功耗蓝牙 MCU 模组，搭载 ESP32-S3系列芯片。除具有丰富的外设接口外，模组还拥有强大的神经网络运算能力和信号处理能力，适用于 AIoT 领域的多种应用场景，例如唤醒词检测和语音命令识别、人脸检测和识别、智能家居、智能家电、智能控制面板、智能扬声器等。

ESP32-S3-WROOM-1 采用 PCB 板载天线，ESP32-S3-WROOM-1U 采用连接器连接外部天线。两款模组均有多种型号可供选择，具体见表 1 和 2。其中，ESP32-S3-WROOM-1-H4 和 ESP32-S3-WROOM-1U-H4 的工作环境温度为–40 ~ 105 °C，内置 ESP32-S3R8 和 ESP32-S3R16V 的模组工作环境温度为–40 ~ 65 °C，其他型号的工作环境温度均为–40 ~ 85 °C。请注意，针对 R8 和 R16V 系列模组 (内置 Octal SPI PSRAM)，若开启 PSRAMECC 功能，模组最大环境温度可以提高到 85 °C，但是 PSRAM 的可用容量将减少 1/16。

![img](./img/57948.png)

 

![img](./img/57944.png)

ESP32-S3 系列芯片搭载 Xtensa® 32 位 LX7 双核处理器（支持单精度浮点运算单元），工作频率高达 240 MHz。CPU 电源可被关闭，利用低功耗协处理器监测外设的状态变化或某些模拟量是否超出阈值。

 

##### **4.3.1 功能框图**

![img](./img/57940.png)

ESP32-S3-WROOM-1 功能框图

##### **4.3.2 模块原理图**

![img](./img/57929.png)

 

#### **4.4 ESP32和STM32 的异同点** 

ESP32 和 STM32 都属于 32 位微控制器。两者的核心差异在于定位：STM32 是通用型嵌入式平台，ESP32 是物联网专用的 “无线通信 + 轻量计算” 解决方案。

**STM32：**项目需要 高性能、丰富外设、工业级可靠性，且项目涉及 复杂控制、实时系统、多硬件协作（如电机驱动、工业设备）。

**ESP32：**项目需要 内置无线连接、低成本、快速开发，且偏向 物联网轻量应用（如联网传感器、智能家居）。

## **五、 粤嵌ESP32-S3开发板卡**

该开发板几乎包含了ESP32-S3的全部可实现功能，把ESP32-S3的性能发挥到了极致。它具备了彩屏显示、完整的音频输入(2个麦克风)和输出(喇叭)功能。结合自身集成的姿态传感器，以及Wi-Fi和Bluetooth，还有AI图像识别和语音识别功能，就可以做出更多实用和有趣的物联网应用。留出了多个拓展接口，用于连接更多的外部的传感器模块以及执行器。

**5.1 硬件参数**[](https://wiki.lckfb.com/zh-hans/szpi-esp32s3/#硬件参数)

| **类别**   | **型号**               | **参数**                                                     |
| ---------- | ---------------------- | ------------------------------------------------------------ |
| 模组       | ESP32-S3-WROOM-1-N16R8 | 搭载 Xtensa® 32 位 LX7 双核处理器，主频高达 240 MHz，内置SRAM 512kB，外置PSRAM 8MB，外置FLASH 16MB，2.4 GHz Wi-Fi (802.11 b/g/n) 40MHz带宽，Bluetooth 5 (LE) 和 Bluetooth Mesh，集成AI向量指令，加速神经网络计算和信号处理 |
| 显示屏     | ST7796                 | 3.5寸、IPS全视角、分辨率480*320、SPI接口                     |
| 触摸屏     | FT6336U                | 电容触摸、I2C接口                                            |
| 姿态传感器 | QMI8658                | 三轴加速度+三轴陀螺仪、I2C接口                               |
| 音频DAC    | ES8311                 | 单通道、I2C接口                                              |
| 音频ADC    | ES7210                 | 四通道(开发板用三个通道)、I2C接口                            |
| 音频功放   | NS4150B                | 单声道D类音频放大器                                          |
| 麦克风     | ZTS6216                | 配套双路麦克风、模拟输出                                     |
| 喇叭       | DB1811AB50             | 1811音腔喇叭、1W                                             |
| USB HUB    | CH334F                 | USB2.0 HUB                                                   |
| USB转串口  | CH340K                 | 波特率最大2Mbps                                              |
| 电源芯片   | SY8088AAC              | 提供双路、每路1A                                             |
| GH1.25接口 |                        | 两路外拓传感器接口，可以给外部传感器供电5V和3.3V，可以作为GPIO、CAN、I2C、UART、PWM等接口 |
| TF卡接口   |                        | 采用1-SD模式与ESP32连接                                      |
| Type-C接口 |                        | 用于供电、程序下载、程序调试，以及USB数据通信                |
| 按键       |                        | 一个复位按键、二个用户自定义按键                             |

**5.2 底板**

![img](./img/57922.png)

 

**5.3 底板+3.5寸电容屏**

![img](./img/57952.png)

## **六、ESP32开发环境**

对于 ESP32 有三种开发平台：[ESP-Arduino入门手册](https://lceda001.feishu.cn/wiki/RpCAw65FsiHfKSkFVV6ckdPjnlf)、[ESP-MicroPython入门手册](https://lceda001.feishu.cn/wiki/WruJwIsP8iZy4yk8KBxccZtrnSf)、[ESP-IDF入门手册](https://lceda001.feishu.cn/wiki/GOIlwwfbIi1SC3k8594cDeFVn8g)﻿

**我应该选择哪一个手册进行学习？**

1. 如果你是一名新人朋友，建议选择Arduino环境，该环境搭建简单，编程内容也容易。

1. 如果你用惯了C语言，想要扩展自己的知识，建议选择MicroPython语言，该环境搭建也简单，并且基于Python的特性，在了解了python语言的风格后，编程内容也很容易理解。

1. 如果你是一位大佬，想要深究底层的驱动，建议使用官方的**ESP-IDF**，该环境搭建较为复杂，并且是基于**FreeRTOS**操作系统的基础上，进行的扩展。

 

## **七、ESP32开发参考文献**

﻿[**ESP-IDF 烧录问题排查指南**](https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html)﻿

﻿[**ESP32 硬件指南**](https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/index.html)﻿

﻿[**ESP32 故障排查指南**](https://docs.espressif.com/projects/esptool/en/latest/esp32/troubleshooting.html)﻿

 