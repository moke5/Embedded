---
type: 工具
tags: [杂记, 工具, powershell, profile]
status: 进行中
created: 2026-05-20
updated: 2026-10-29
related: ["[[bash]]", "[[bash]]"]
---
# powershell

[toc]

> .ps1

## `$PROFILE`

`$PROFILE` 是 PowerShell 的自动变量，保存当前用户、当前宿主对应的配置文件路径。配置文件是一段 `.ps1` 脚本，PowerShell 启动时自动执行；别名、函数、环境变量和模块导入通常放在这里。变量只保存路径，文件不存在时不会自动创建。

宿主指承载 PowerShell 引擎的程序，例如 `powershell.exe`、`pwsh.exe`、VS Code 集成终端和 PowerShell ISE。宿主不同，`$PROFILE` 可能指向不同文件。

### 作用域与加载顺序

| 属性 | 作用域 | 典型路径 |
| --- | --- | --- |
| `$PROFILE.AllUsersAllHosts` | 所有用户、所有宿主 | `$PSHOME\profile.ps1` |
| `$PROFILE.AllUsersCurrentHost` | 所有用户、当前宿主 | `$PSHOME\Microsoft.PowerShell_profile.ps1` |
| `$PROFILE.CurrentUserAllHosts` | 当前用户、所有宿主 | `Documents\PowerShell\profile.ps1` |
| `$PROFILE.CurrentUserCurrentHost` | 当前用户、当前宿主 | `Documents\PowerShell\Microsoft.PowerShell_profile.ps1` |

`$PROFILE` 等价于 `$PROFILE.CurrentUserCurrentHost`。四个配置按表中顺序加载，后执行的同名定义覆盖先执行的。

路径随版本和宿主变化：

- Windows PowerShell 5.1 的用户目录是 `Documents\WindowsPowerShell\`。
- PowerShell 7 的用户目录是 `Documents\PowerShell\`。
- VS Code 集成终端可能使用 `Microsoft.VSCode_profile.ps1`。
- PowerShell ISE 使用 `Microsoft.PowerShellISE_profile.ps1`。
- 文档目录被 OneDrive 重定向时，实际路径仍在 `Documents` 下，以 `$PROFILE` 输出为准。

`$PROFILE` 与 Bash 的 `.bashrc` 都用于启动时加载用户配置；PowerShell 按用户与宿主拆成四个作用域，Bash 的配置文件由 shell 类型和登录方式决定。参见 [[bash]]。

### 创建与编辑

先查看实际路径和文件状态：

```powershell
$PROFILE
Test-Path $PROFILE
```

路径不存在时创建父目录和文件：

```powershell
$dir = Split-Path -Parent $PROFILE
if (-not (Test-Path $dir)) {
    New-Item -ItemType Directory -Path $dir | Out-Null
}
if (-not (Test-Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE | Out-Null
}
notepad $PROFILE
```

`notepad` 可以换成 `code`，用 VS Code 打开。保存后重启终端，或在当前会话执行：

```powershell
. $PROFILE
```

点号表示在当前作用域执行脚本。配置文件内如果有 `exit`，重新加载会退出当前会话。

### 执行策略

Windows 默认可能禁止运行本地脚本。查看各作用域策略：

```powershell
Get-ExecutionPolicy -List
```

只对当前用户放行本地脚本：

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

`RemoteSigned` 允许本地脚本运行；从网络下载的脚本需要有效签名，或先执行 `Unblock-File`。执行策略控制脚本加载规则，不能替代代码来源审查；不要运行来源不明的配置文件。

### 验证

重新加载后检查配置是否生效：

```powershell
Get-Content $PROFILE
Get-Command ll
```

`Get-Command` 只对配置中真实定义的命令有效。修改后仍不生效时，先确认当前宿主的 `$PROFILE` 路径：

```powershell
$PROFILE
```

控制台、VS Code 和 ISE 可能读取不同文件。需要跨宿主共享的配置放在 `$PROFILE.CurrentUserAllHosts`，宿主专属配置放在 `$PROFILE.CurrentUserCurrentHost`。

### 常见问题

| 现象 | 原因 | 处理 |
| --- | --- | --- |
| `running scripts is disabled` | 执行策略禁止脚本 | 设置 `CurrentUser` 为 `RemoteSigned` |
| 修改后命令不存在 | 编辑了其他宿主的配置文件 | 用 `$PROFILE` 确认当前路径，重新加载或重启 |
| 启动明显变慢 | 配置中导入模块或执行网络请求 | 用 `Measure-Command { . $PROFILE }` 定位耗时语句 |
| 怀疑配置导致异常 | 配置脚本报错或改变环境 | 用 `powershell.exe -NoProfile` 或 `pwsh -NoProfile` 启动对照 |

### 最小示例

```powershell
Set-Alias ll Get-ChildItem
$env:EDITOR = "code"
```

### 快速打开本笔记

在 Obsidian 中按 `Ctrl+O` 打开快速切换，输入 `powershell`，回车进入本笔记；也可以右键笔记选择收藏，之后从书签面板进入。

需要从 PowerShell 直接打开时，在 `$PROFILE` 中加入：

```powershell
function note-powershell {
    Invoke-Item "D:\git\embedded\杂记\工具\powershell.md"
}
```

保存后执行 `. $PROFILE`，之后在任意 PowerShell 会话输入 `note-powershell` 即可用默认 Markdown 应用打开本笔记。

## 文件



### 查看文件大小



##### 一键显示（名称 + 大小自动单位）

```powershell
Get-ChildItem | Select-Object Name, @{
    Name = "Size"
    Expression = {
        $size = $_.Length
        if ($size -ge 1GB) { "{0:N2} GB" -f ($size / 1GB) }
        elseif ($size -ge 1MB) { "{0:N2} MB" -f ($size / 1MB) }
        elseif ($size -ge 1KB) { "{0:N2} KB" -f ($size / 1KB) }
        else { "$size B" }
    }
}
```



## WIFI

### 获取网卡信息

```powershell
Get-NetAdapter
```



### 开关

```powershell
# 开启（把 "WLAN" 换成你自己的网卡名）
Enable-NetAdapter -Name "WLAN" -Confirm:$false

# 关闭
Disable-NetAdapter -Name "WLAN" -Confirm:$false
```



### command

```
(get-date) - (gcim Win32_OperatingSystem).LastBootUpTime

开机时间点
(Get-CimInstance Win32_OperatingSystem).LastBootUpTime

gcim = Get-CimInstance，用于读取系统硬件 / 系统信息
Win32_OperatingSystem 是系统操作系统类，LastBootUpTime 记录最后一次开机时间
```

## 相关笔记

- [[bash]]
