# embedded — 个人技术笔记仓库

> Typora 编辑，Obsidian 兼容。主线：嵌入式 Linux、C/C++、STM32、ESP32、物联网。
> 双远程 GitHub + Gitee；配图放同级 `img/`，已 gitignore，远程只备文本。
> AI 助手先读 [AGENTS.md](./AGENTS.md)；仓库规范入口见 [规范/MOC.md](./规范/MOC.md)。

[toc]

## 目录导航

| 目录 | 内容 | 入口 |
| --- | --- | --- |
| `L0-物理与电路/` | 电路、PCB、焊接与硬件实现 | [L0 MOC](./L0-物理与电路/MOC.md) |
| `L1-芯片与外设/` | 芯片、启动与外设 | [L1 MOC](./L1-芯片与外设/MOC.md) |
| `L2-驱动与固件/` | 驱动、封装与阶段实验 | [L2 MOC](./L2-驱动与固件/MOC.md) |
| `L3-实时与内核/` | Linux 内核、文件 IO、并发；RTOS | [L3 MOC](./L3-实时与内核/MOC.md) |
| `L4-系统编程与构建/` | C、数据结构、编译链接与构建工具 | [L4 MOC](./L4-系统编程与构建/MOC.md) |
| `L5-网络与协议/` | socket、TCP/UDP、应用协议 | [L5 MOC](./L5-网络与协议/MOC.md) |
| `L6-应用与交互/` | LVGL、微信小程序等应用层与交互界面 | [L6 MOC](./L6-应用与交互/MOC.md) |
| `L7-集成与产品/` | 待迁移 | [知识分层方案](./规范/知识分层方案.md) |
| `X-工具与方法/` | 工具、环境、Linux、服务器、收藏、学习方法、AI | [X MOC](./X-工具与方法/MOC.md) |
| `知识地图/` | 由 frontmatter 生成的层级、领域与依赖索引 | [知识地图/MOC.md](./知识地图/MOC.md) |
| `项目/` | 实践项目 | [项目/MOC.md](./项目/MOC.md) |
| `本机/` | 本机能力清单与适配器；个人信息在 `self/` | [本机/MOC.md](./本机/MOC.md) |
| `规范/` | 写作、校验与提交、Agent 协作、信息架构 | [规范/MOC.md](./规范/MOC.md) |
| `模板/` | 笔记模板与 frontmatter | [模板/模板说明.md](./模板/模板说明.md) |
| `script/` | 校验、适配器与本地脚本 | 不要求 MOC |

迁移已完成：`课程/`、`杂记/` 已删除；新笔记按 `layer`/`domain` 归档，层级定义见 [知识分层方案](./规范/知识分层方案.md)。

## 快速开始

1. 克隆仓库并进入根目录。
2. 用 Obsidian 打开仓库，或直接用 Typora 编辑 Markdown。
3. 新建笔记时从 `模板/` 复制对应模板，按 [模板说明](./模板/模板说明.md) 填写 frontmatter。
4. 完成后运行 `python script/notes_lint.py --strict`。

## 规范

| 需要 | 打开 |
| --- | --- |
| 命名、文风、配图、新建流程 | [写作与笔记规范](./规范/写作与笔记规范.md) |
| frontmatter 与模板 | [模板说明](./模板/模板说明.md) |
| 校验、分支、提交、推送 | [校验与提交规范](./规范/校验与提交规范.md) |
| 工具适配、权限、本机能力、跨库 | [Agent协作规范](./规范/Agent协作规范.md) |
| 信息架构与迁移方案 | [仓库信息架构](./规范/仓库信息架构.md) |

## AI 助手

- 统一入口：[AGENTS.md](./AGENTS.md)
- Claude Code：[CLAUDE.md](./CLAUDE.md)
- Cursor 规则：`.cursor/rules/`
- 知识沉淀 Skill：[.skills/embedded-knowledge-sync/SKILL.md](./.skills/embedded-knowledge-sync/SKILL.md)

## 远程与备份

- 远程：GitHub + Gitee 双仓库。
- 文本入库，配图放同级 `img/` 且不入库。
- 敏感信息、本机明细与凭据放 `self/`，已 gitignore。
- 提交与推送规则见 [校验与提交规范](./规范/校验与提交规范.md)。
