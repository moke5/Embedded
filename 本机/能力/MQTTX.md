---
type: 工具
tags: [mqtt, mqttx, cli, iot]
status: 进行中
target: 晶体
input: MQTTX CLI 官方文档与本机实测
output: 连接、发布、订阅的常用调用
review: 2026-11-17
created: 2026-10-20
updated: 2026-10-20
related: ["[[MQTT]]", "[[本机/MOC|本机 MOC]]"]
---
# MQTTX

> 用途：通过命令行连接 MQTT broker，完成发布、订阅与压测。本机通过 npm 全局安装，入口为 `mqttx`。

## 子命令

| 子命令 | 作用 |
| --- | --- |
| `mqttx conn` | 建立连接并保持 |
| `mqttx pub` | 发布消息 |
| `mqttx sub` | 订阅主题 |
| `mqttx bench pub` / `bench sub` | 压测 |

## 常用参数

| 参数 | 含义 |
| --- | --- |
| `-h, --host` | broker 地址 |
| `-p, --port` | 端口 |
| `-u, --username` | 用户名 |
| `-P, --password` | 密码 |
| `-t, --topic` | 主题 |
| `-m, --message` | 消息内容 |
| `-q, --qos` | QoS 等级 |

## 调用

```powershell
# 发布
mqttx pub -h broker.emqx.io -p 1883 -t test/topic -m "hello" -q 1

# 订阅
mqttx sub -h broker.emqx.io -p 1883 -t test/topic

# 通过统一入口（需追加 --yes）
.\script\local.ps1 run mqttx pub -h broker.emqx.io -p 1883 -t test/topic -m "hello" -q 1 --yes
```

## 注意

- 凭据不写入命令行历史、清单或笔记；需要认证时从环境变量或 `self/local.md` 读取。
- 该能力标记 `confirm: true`，调度器要求追加 `--yes`，对应"联网操作前先征得同意"。
- 语法以 `mqttx --help` 与 `mqttx <subcommand> --help` 为准。
