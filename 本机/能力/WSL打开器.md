---
type: 工具
tags:
  - wsl
  - everything
  - 打开
  - cli
status: 进行中
target: 晶体
input: 既有 WSL 搜索选择脚本
output: 搜索 → 选择 → Windows 应用打开的调用约定
review: 2026-10-20
created: 2026-10-20
updated: 2026-10-20
related:
  - "[[Everything]]"
  - "[[本机/MOC|本机 MOC]]"
  - "[[wsl]]"
---
# WSL打开器

> 用途：在 WSL 内基于 Everything 的搜索结果做选择，再把选中项交给 Windows 端应用打开。

## 数据流

```mermaid
flowchart LR
    Q[关键词] --> E[Everything 索引查询]
    E --> L[WSL 内列表与选择]
    L --> W[Windows 应用打开]
```

三个阶段解耦：查询由 `es.exe` 完成，选择在 WSL 终端完成，打开由 Windows 侧执行。任一段可单独替换。

## 配置

适配器读取环境变量 `EVERYTHING_OPEN`，指向现有的 WSL 脚本：

```powershell
setx EVERYTHING_OPEN /home/<用户>/bin/everything-open.sh
```

未设置时适配器返回 127，并提示配置方法。

## 调用

```powershell
.\script\local.ps1 run file-open "关键词"
```

## 选择界面约定

- 列表项显示文件名与完整路径，避免同名文件误选。
- 输入序号或关键字筛选，回车确认，`q` 取消。
- 取消时返回非零，供上层判断。

## 注意

- WSL 与 Windows 的路径表示不同：`/mnt/d/...` 与 `D:\...` 需在脚本内转换。
- 带空格与中文的路径必须加引号传递。
- Windows 端打开命令可用 `cmd.exe /c start "" "<路径>"` 或 `explorer.exe "<路径>"`。
