---
type: MOC
tags: [本机, 工具, agent]
status: 进行中
target: 晶体
input: 本机软件实测与系统信息
output: 本机能力的单一事实来源与调用规范
review: 2026-11-17
created: 2026-10-20
updated: 2026-10-20
related: ["[[YAML]]", "[[claude]]"]
---
# 本机 MOC

> 本机能力的单一事实来源。AI 处理搜索、打开、本机软件类任务时先读这里，
> 再决定用现有能力、查 GitHub，还是向用户申请安装。

## 使用协议

1. 发现：运行 `.\script\local.ps1 list`，或直接读 [能力清单.json](./能力清单.json)。
2. 命中：运行 `.\script\local.ps1 run <id> [参数...]`。
3. 未命中：查官方文档或 GitHub，报告仓库、许可证、安装方式与风险。
4. 安装、下载、改系统、写凭据前：必须征得用户同意。
5. 新增能力：按 [规范](./规范.md) 登记，四步齐全。

## 内容索引

- 能力清单（机器可读）：[能力清单.json](./能力清单.json)
- 能力说明：
  - [Everything](./能力/Everything.md) — 文件名搜索 CLI
  - [WSL打开器](./能力/WSL打开器.md) — 搜索、选择、Windows 打开
  - [MQTTX](./能力/MQTTX.md) — MQTT CLI
- 本机信息（本地，不入库）：[本机信息](../self/本机信息.md)
- 移动端信息（本地，不入库）：[移动端](../self/移动端.md)
- 规范：[本机能力规范](./规范.md)

## 相关 MOC

- [AI MOC](../AI/MOC.md)
- [杂记 MOC](../杂记/MOC.md)
