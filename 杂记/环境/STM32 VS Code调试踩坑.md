---
type: 踩坑
tags: [杂记, 环境, stm32, vscode, 调试]
status: 已完成
target: 流体
input: STM32F103C8 + ST-Link V2 克隆版 + VS Code Cortex-Debug
output: 可用的 OpenOCD 调试配置、两个错误的根因与排查顺序
review: 2026-11-20
created: 2026-10-20
updated: 2026-10-29
related: ["[[vscode]]", "[[vscodeCC++]]"]
---
# VS Code + ST-Link 调试环境踩坑

> 场景：在 VS Code 中使用 Cortex-Debug 调试 STM32F103C8，烧录正常，但 F5 启动失败。先后出现两个独立问题：VS Code 找不到 `cortex-debug` 调试类型，以及 ST-Link GDB server 无法验证目标芯片。

## 环境

| 项 | 值 |
| --- | --- |
| 目标芯片 | STM32F103C8T6，Cortex-M3，128 KiB Flash |
| 调试器 | ST-Link V2 克隆版，固件 `V2J48S7` |
| 目标电压 | 3.25 V |
| VS Code | 1.142.0 |
| Cortex-Debug | 1.12.1 |
| STM32CubeProgrammer | 2.23.0 |
| ST-Link GDB server | 7.14.0+st.2 |
| OpenOCD | 0.12.0（ESP-IDF 自带版本，支持 `st-link` 驱动） |
| 串口 | CH340K，`COM7`，115200 |

## 问题一：配置的类型 `cortex-debug` 不受支持

### 现象

按 F5 后 VS Code 弹出：

```text
配置的类型 "cortex-debug" 不受支持
```

`launch.json` 本身存在，`type` 也写的是 `cortex-debug`。

### 排查过程

1. 确认扩展已安装：

   ```powershell
   code --list-extensions --show-versions | Select-String cortex
   ```

   输出包含 `marus25.cortex-debug@1.12.1`，扩展版本满足 VS Code 1.142.0。

2. 查看扩展宿主日志，发现 `marus25.cortex-debug` 从未被激活；F5 触发的是其他调试类型。

3. 检查 VS Code 配置文件（Profile）绑定：

   ```text
   file:///<本地路径>/gateway -> 56efabe9
   ```

   在同步配置中，`56efabe9` 对应配置文件 `stm32cubemx-make`。

4. 对比各配置文件的 `extensions.json`：`marus25.cortex-debug` 只存在于默认配置文件和 `STM32` 配置文件，`stm32cubemx-make` 中没有该扩展。

### 根因

VS Code 的多配置文件彼此隔离。网关工作区绑定到了 `stm32cubemx-make`，而 Cortex-Debug 安装在另一个配置文件，导致该工作区识别不到 `cortex-debug` 调试类型。

### 解决

把扩展安装到工作区实际使用的配置文件：

```powershell
code --profile stm32cubemx-make --install-extension marus25.cortex-debug --force
code --profile stm32cubemx-make --install-extension ms-vscode.vscode-serial-monitor --force
```

然后在 VS Code 中执行：

```text
Ctrl+Shift+P -> Developer: Reload Window
```

验证：

```powershell
code --profile stm32cubemx-make --list-extensions --show-versions |
  Select-String "cortex|serial"
```

### 预防

- 安装扩展前先确认当前窗口使用的配置文件；不同配置文件的扩展集合不共享。
- 工作区与配置文件的绑定保存在 `%APPDATA%\Code\User\globalStorage\storage.json` 的 `profileAssociations.workspaces` 中。
- 出现“类型不受支持”时，先看扩展宿主日志是否激活了对应扩展，不要只检查 `extensions` 目录。

## 问题二：ST-Link GDB server 报 `Could not verify ST device`

### 现象

ST-Link GDB server 启动后立即退出：

```text
Error in initializing ST-LINK device.
Reason: ST-LINK: Could not verify ST device! Abort connection.
```

同样的目标板和探针，STM32CubeProgrammer CLI 可以正常连接并烧录：

```powershell
STM32_Programmer_CLI.exe -c port=SWD freq=1800 mode=NORMAL reset=SWrst `
  -w build/Debug/gateway.elf -v -rst
```

输出包含：

```text
Device ID   : 0x410
Device name : STM32F101/F102/F103 Medium-density
NVM size    : 128 KBytes
Download verified successfully
```

### 排查过程

1. 先排除目标板与接线：CubeProgrammer 在 1800 kHz 下可连接，说明供电、SWD 接线、芯片和探针的 USB 通道均正常。

2. 检查 GDB server 参数：`-cp` 必须指向直接包含 `STM32_Programmer_CLI.exe` 的 `bin` 目录；参数错误时 GDB server 会报 “Missing application STM32CubeProgrammer”，与本次错误不同。

3. 调整 SWD 频率：分别尝试 480、950、1800、4000 kHz，均报同一错误。

4. 尝试 connect under reset：分别测试带 `-k` 和不带 `-k`，均失败。

5. 换用 OpenOCD 0.12.0，使用其 `st-link` 驱动，连接成功：

   ```text
   Info : SWD DPIDR 0x1ba01477
   Info : Cortex-M3 r1p1 processor detected
   Info : flash size = 128 KiB
   ```

### 根因

目标板、SWD 链路和探针硬件均正常；问题位于 ST-Link GDB server 7.14.0 与克隆 ST-Link 固件 `V2J48S7` 的兼容层。CubeProgrammer 使用另一条连接路径，因此不受影响。

### 解决

调试链路改用 OpenOCD，烧录仍可使用 CubeProgrammer。

新建 `tools/openocd/stm32f103c8.cfg`：

```tcl
source [find interface/stlink.cfg]
transport select swd
adapter speed 950

source [find target/swj-dp.tcl]
swj_newdap stm32f1x cpu -irlen 4 -ircapture 0x1 -irmask 0xf -expected-id 0x3ba00477
dap create stm32f1x.dap -chain-position stm32f1x.cpu
target create stm32f1x.cpu cortex_m -dap stm32f1x.dap
stm32f1x.cpu configure -work-area-phys 0x20000000 -work-area-size 0x4000 -work-area-backup 0

flash bank stm32f1x.flash stm32f1x 0x08000000 0 0 0 stm32f1x.cpu
```

`swj_newdap` 由 `target/swj-dp.tcl` 提供，缺少该 `source` 时会报 `invalid command name "swj_newdap"`。OpenOCD 0.12 的 ST-Link 驱动使用 `transport select swd`，不使用旧版 `hla_swd`。

`launch.json` 的关键字段：

```json
{
  "type": "cortex-debug",
  "servertype": "openocd",
  "openOCDPath": "D:/app/IDEA/Espressif/tools/openocd-esp32/v0.12.0-esp32-20251215/openocd-esp32/bin/openocd.exe",
  "configFiles": ["${workspaceFolder}/tools/openocd/stm32f103c8.cfg"],
  "openOCDLaunchCommands": ["init", "reset halt"],
  "runToEntryPoint": "main",
  "preLaunchTask": "Build"
}
```

### 验证

使用 OpenOCD 启动 GDB server 后执行下载与断点：

```text
SWD DPIDR 0x1ba01477
Cortex-M3 r1p1 processor detected
flash size = 128 KiB
Loading section .text, size 0x7db4
Start address 0x0800526c, load size 34300
Breakpoint 1 at 0x8004a64: file Core/Src/main.c, line 81
```

F5 可停在 `main()`，说明下载、符号加载和断点均可用。

`reset halt` 只复位 Cortex-M 内核时会出现：

```text
Only resetting the Cortex-M core
```

该 warning 不影响本次调试；需要复位外设时，应另行配置 `reset-init` 事件或硬件 SRST。

### 预防

- 按层排查：USB/驱动 → SWD 连接 → Flash 算法 → GDB server。CubeProgrammer 能连接时，优先怀疑 GDB server，而不是目标板。
- 克隆 ST-Link 不必先反复升级固件；先用 OpenOCD 做交叉验证。
- 使用 OpenOCD 0.12+ 时确认驱动为 `st-link`、传输为 `swd`；`hla_swd` 仅适用于旧版 HLA 驱动。

## 结论

两个问题相互独立：第一个是 VS Code 配置文件隔离导致的扩展缺失，第二个是 ST-Link GDB server 的兼容性故障。最终配置为：

- 编译：VS Code `Build` task
- 烧录：STM32CubeProgrammer CLI
- 调试：Cortex-Debug + OpenOCD + ST-Link
- 串口：VS Code Serial Monitor，115200

按此分层，任一环节替换后仍可单独验证，不需要同时改动整条链路。

## 相关笔记

- [[vscodeCC++]]
