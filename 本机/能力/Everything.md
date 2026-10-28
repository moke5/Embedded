---
type: 工具
tags: [everything, 搜索, cli, windows]
status: 进行中
target: 晶体
input: voidtools Everything 命令行文档与本机实测
output: es.exe 的调用方式与路径配置
review: 2026-11-17
created: 2026-10-20
updated: 2026-10-20
related: ["[[本机/MOC|本机 MOC]]", "[[WSL打开器]]"]
---
# Everything

> 用途：按文件名或路径快速检索本机 NTFS 卷，返回匹配文件路径。查询走 Everything 的内存索引，速度与目录遍历无关。

## 组成

| 组件 | 作用 |
| --- | --- |
| Everything 主程序 | 建立并维护文件索引；CLI 查询要求它正在运行 |
| `es.exe` | 命令行接口，向主程序查询并输出结果 |

## 路径配置

`es.exe` 不保证在 `PATH` 中。适配器按以下顺序解析：

1. 环境变量 `ES_EXE`
2. `PATH` 中的 `es.exe`
3. `C:\Program Files\Everything\es.exe`
4. `C:\Program Files (x86)\Everything\es.exe`
5. `%LOCALAPPDATA%\Programs\Everything\es.exe`

任一步命中即使用；全部失败时返回 127。推荐把实际路径写入 `self/local.md` 并设置 `ES_EXE`。

## 常用参数

| 参数 | 含义 |
| --- | --- |
| `-n <num>` | 最多返回 num 条 |
| `-i` | 忽略大小写 |
| `-r <regex>` | 按正则匹配 |
| `-p` | 输出完整路径 |
| `-path <dir>` | 限定搜索目录 |
| `-export-csv <file>` | 导出 CSV |
| `-no-header` | CSV 不输出表头 |

参数以 `es.exe -help` 的当前版本为准。

## 调用

```powershell
# 直接调用
es.exe -n 20 -p "报告"

# 通过统一入口
.\script\local.ps1 run file-search -n 20 -p "报告"
```

## 注意

- Everything 未运行或索引未建立时，查询结果为空而非报错。
- 只覆盖 NTFS 卷；网络盘与未索引目录不在结果中。
- 输出编码由终端决定，脚本处理时应按 UTF-8 读取。
