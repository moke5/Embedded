# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 仓库性质

这是 Typora 纯 Markdown 知识库，不是可构建的代码工程，不是 Obsidian Vault（无 .obsidian 配置）。内容以嵌入式 Linux、C 语言、系统编程的技术笔记为主。

## 目录约定

| 目录 | 用途 | 规则 |
|------|------|------|
| `study/` | 系统性课程/大纲学习笔记 | 数字前缀分类（`11C/`、`13linux/` 等），内部按章节拆分 |
| `self/` | 零散备忘、工具配置、个人笔记 | 按主题分子目录（`AI/`、`linux/`、`windows/`）；不成体系的随意记录放这里 |
| `project/` | 实际代码工程项目 | 每个项目有独立子目录，可含自己的 CLAUDE.md |
| `error/` | 报错和问题记录 | 按技术栈分子目录（`gcc/`、`stm32/`、`linux/`、`hardware/` 等），每个文件对应一个具体问题 |
| `img/` | 图片资源 | 笔记中引用的图片 |
| `EmbeddedLinux/` | 嵌入式 Linux 专题笔记 | 新建，待整理 |

### study/ vs self/ 边界
- `study/`：有体系、有章节结构的学习内容，通常是课程大纲或系统教材的笔记
- `self/`：想到什么记什么的零散备忘，没有体系化结构
- 不要试图合并这两个目录，定位不同

## 关键约束

- **不要创建 `.obsidian/` 或任何 Obsidian 配置**，这个仓库不是 Obsidian Vault
- `study/` 中的 C 代码片段是教学示例，不是可编译的独立工程，不要尝试为其创建 Makefile 或编译
- 新建笔记目录前，先确定命名和分类约定，保持一致
- 修改已有笔记时保持原有风格（缩进、代码块语言标注、表格对齐）
- `.gitignore` 已排除编译产物和 `.obsidian/`，无需重复配置

## 子项目

- `project/stm32_linux/` — STM32+Linux 物联网网关项目，其 CLAUDE.md 包含完整的硬件架构、引脚分配、通信协议和开发步骤
