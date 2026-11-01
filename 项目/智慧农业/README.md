---
type: 项目
tags: [项目, 智慧农业, stm32, esp8266, mqtt]
status: 进行中
target: 晶体
input: D:\git\IntelligentAgri-System-ai 源码与 gateway/README.md；D:\code\javawebP 平台源码与 docs/
output: 两仓库分工、分支与部署状态的单一记录
review: 2026-11-29
created: 2026-10-16
updated: 2026-10-29
related: ["[[网关]]", "[[终端]]", "[[遇到的问题]]", "[[配置记录]]", "[[MQTT]]"]
---
# 智慧农业系统

## 仓库与分支

本项目由两个独立 Git 仓库组成，分工是「设备侧固件」与「云端平台」：

| 角色 | 本地路径 | 分支 | 说明 |
| --- | --- | --- | --- |
| 设备侧固件 | `D:\git\IntelligentAgri-System` | `main`（工作区当前为 detached HEAD `85ac93b`） | 主 worktree；未跟踪的 `app_led.c/.h`、`tools/` 只存在于此 |
| 设备侧固件（在用） | `D:\git\IntelligentAgri-System-ai` | `ai`（`aac4bfc`） | **实际开发使用此目录**；与前者是同一仓库的两个 worktree |
| 云端平台 | `D:\code\javawebP` | `main` | 服务器部署的 Web 监控平台，见 [配置记录](../../杂记/服务器/配置记录.md) |

`git worktree list` 输出：

```text
D:/git/IntelligentAgri-System     85ac93b (detached HEAD)
D:/git/IntelligentAgri-System-ai  aac4bfc [ai]
```

关键事实：

- 两个目录共享同一个 `.git` 对象库，不是两份独立仓库。在 `-ai` 目录提交会推进 `ai` 分支，`IntelligentAgri-System` 目录的 HEAD 不会随之移动。
- `ai` 比 `main` 领先 1 个提交（`main...ai` 计数 `0 1`）。`aac4bfc feat: Add MQTT application layer and ESP8266 integration` 只存在于 `ai` 分支，尚未合入 `main`。
- 主 worktree 停在 detached HEAD `85ac93b`，并有未提交改动（`gateway/CMakeLists.txt`、`Core/Src/freertos.c`、`app/src/app.c`、`app/src/keytask.c`，以及未跟踪的 `app_led.c/.h`、`tools/`）。这些改动与 `ai` 分支内容不一致，切换分支前先确认归属。
- 两个仓库都**没有配置远程**，全部为本地提交。

## 固件分支差异（`main` → `ai`）

`ai` 分支的提交新增 MQTT 应用层与 ESP8266 接入，共 15 个文件、+970/−50：

| 模块 | 文件 | 内容 |
| --- | --- | --- |
| 应用层 | `app/src/mqtt_app.c`、`app/inc/mqtt_app.h` | MQTT 主题拼装、AT 指令封装、LWT、遥测上报、指令解析与回执 |
| 板级驱动 | `bsp/src/esp.c`、`bsp/src/esp_port.c`、`bsp/inc/esp.h`、`bsp/inc/esp_port.h` | ESP8266 AT 指令收发与 URC 解析 |
| 配置 | `app/inc/gateway_config.h` | WiFi SSID/密码、MQTT 主机、设备 ID |
| 构建 | `gateway/CMakeLists.txt`、`MDK-ARM/gateway.uvprojx` | 纳入新增源文件 |
| 调试 | `tools/openocd/stm32f103c8.cfg`、`.vscode` 配置 | OpenOCD 连接 STM32F103C8 |

## 与云端平台的契约

设备固件与 `javawebP` 通过同一套 MQTT 主题对接，契约在 `javawebP/docs/MQTT接口.md`：

| 主题 | 方向 | QoS | Retain |
| --- | --- | --- | --- |
| `dev/{deviceId}/telemetry` | 设备 → 平台 | 0 | 否 |
| `dev/{deviceId}/status` | 设备 → 平台 | 1 | 是（配合 LWT） |
| `dev/{deviceId}/cmd` | 平台 → 设备 | 1 | 否 |
| `dev/{deviceId}/cmd/ack` | 设备 → 平台 | 1 | 否 |

固件侧设备 ID 为 `stm32-gw-01`，主题在 `mqtt_app.c` 的 `build_topics()` 中拼装；遥测周期 5 s，断线重试 10 s。平台侧浏览器与后端同时消费这三类主题：浏览器直连 `/mqtt` 收实时数据，Spring Boot 旁路订阅并落 PostgreSQL。

## 当前状态

- 设备侧：`ai` 分支已完成 WiFi/MQTT 链路，串口可输出 `[mqtt] ready`；遥测中的 `temp`/`hum` 为演示值，`rssi` 固定；LoRa（LLCC68）驱动 `Lora/` 尚未纳入仓库。
- 平台侧：`javawebP` 一期实时链路与二期持久化均已实现，已在阿里云服务器部署运行。
- 未完成：EMQX 认证/ACL、后端登录与权限、HTTPS；`ai` 分支未合入 `main`。

## 敏感信息

`gateway/app/inc/gateway_config.h` 含真实 WiFi SSID/密码与服务器地址。该文件在 `ai` 分支**已被 Git 跟踪**（提交里是占位符，工作区被改成真实值），仅在 `.gitignore` 追加了一行，忽略规则对已跟踪文件不生效。真实值见 [self/local.md](../../self/local.md)，本文件不记录。

## 后续（大 / 中 / 小）

- **大**：把 `ai` 分支合入 `main` 并统一两个 worktree 的工作区；接入 LoRa 传感器帧替换演示遥测。
- **中**：将 `gateway_config.h` 从索引移除（`git rm --cached`）并改为 `gateway_config.h.example` 模板；补齐平台侧 EMQX 认证与 ACL。
- **小**：在两个 worktree 各执行一次 `git status`，确认未提交改动归属后再继续开发。
