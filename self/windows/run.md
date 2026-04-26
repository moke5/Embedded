# win + r

> > enter : 运行
>
> >  ctrl + shift + enter : 以管理员身份运行
>
> ​	在弹出的 **UAC（用户账户控制）** 窗口点击 **是**，即可以管理员权限启动

命令行选项优先于注册表设置。

## 以管理员身份运行

- ctrl + shift + 鼠标左键点击确定
- powershell

```
PowerShell Start-Process 命令名 -Verb RunAs
```

若需管理员权限，可在命令前加 `runas /user:Administrator `（需管理员账户）。

## Content

> 常见

```
系统核心与设置、管理工具、 常用工具、系统维护
```



- 🔧 系统核心与设置



```
winver          // 查看Windows版本与激活
msinfo32        // 系统详细信息
dxdiag          // DirectX诊断（硬件信息）
systeminfo      // 系统信息（也可在CMD用）
control			// 打开控制面板（传统设置入口）
sysdm.cpl		// 系统属性（计算机名、硬件、环境变量）
ncpa.cpl		// 网络连接（适配器设置）
mmsys.cpl		// 声音设置（播放、录音、通信）
appwiz.cpl		// 程序和功能（卸载或更改程序）
msconfig		// 系统配置（启动项、服务、引导）
gpedit.msc		// 本地组策略编辑器（专业版/企业版）
secpol.msc		// 本地安全策略（专业版/企业版）
```



- 🛠️ 管理工具



```
compmgmt.msc    // 计算机管理
devmgmt.msc     // 设备管理器
diskmgmt.msc    // 磁盘管理
services.msc    // 服务
gpedit.msc      // 组策略（专业版/企业版）
secpol.msc      // 安全策略
eventvwr.msc    // 事件查看器
taskschd.msc    // 任务计划
lusrmgr.msc     // 用户和组
```



- 📝 常用工具



```
regedit         // 注册表
taskmgr         // 任务管理器
resmon          // 资源监视器
perfmon         // 性能监视器
msconfig        // 系统配置（启动项）
mstsc           // 远程桌面
notepad         // 记事本
calc            // 计算器
mspaint         // 画图
cleanmgr        // 磁盘清理
osk             // 屏幕键盘
```



- 🧩 系统维护

```
rstrui			// 系统还原
sfc /scannow	// 系统文件扫描修复
slmgr.vbs -dlv	// 查看系统激活详细信息
```



## 规则

### 1.特殊协议与逻辑路径（优先级最高）

- Shell 协议 (`shell:`)：
    - 用于打开特殊的系统文件夹。
    - **示例**：输入 `shell:startup` 打开开机启动文件夹；`shell:desktop` 打开桌面文件夹；`shell:sendto` 打开“发送到”菜单的目录。
- CLSID/GUID (类标识符)：
    - 这是系统底层的“虚拟命名空间”，格式为 `::{一串字符}`。
    - **示例**：输入 `::{20D04FE0-3AEA-1069-A2D8-08002B30309D}` 可以直接打开“此电脑”；`::{645FF040-5081-101B-9F08-00AA002F954E}` 打开“回收站”。



### **2. 环境变量（动态路径）**

Windows 允许你通过变量名来指代经常变动的路径，这在写脚本或快速跳转时非常有用。格式是 `%变量名%`。

- 常见变量：
    - `%temp%`：直接跳转到当前用户的临时文件夹（清理垃圾必用）。
    - `%appdata%`：跳转到 `C:\Users\用户名\AppData\Roaming`（很多软件配置藏在这里）。
    - `%userprofile%`：跳转到当前用户的主目录。
    - `%windir%`：跳转到 Windows 安装目录（通常是 C:\Windows）。



### **3. 系统 PATH 中的可执行程序（最常用）**

这是大家最熟悉的用法。Windows 会在系统环境变量 `PATH` 定义的目录（主要是 `C:\Windows\System32` 和 `C:\Windows`）里搜索你输入的名字。

- 系统工具：
    - **`.exe` 文件**：如 `notepad` (记事本), `calc` (计算器), `mspaint` (画图), `cmd` (命令提示符), `powershell`。
    - **`.msc` 文件**（管理控制台）：如 `services.msc` (服务), `devmgmt.msc` (设备管理器), `diskmgmt.msc` (磁盘管理)。
    - **`.cpl` 文件**（控制面板项）：如 `appwiz.cpl` (卸载程序), `ncpa.cpl` (网络连接), `powercfg.cpl` (电源选项)。
- 如何发现新命令？
    - 你可以直接打开 `C:\Windows\System32` 文件夹，里面所有的 `.exe`, `.msc`, `.cpl` 文件，理论上都可以直接在 `Win + R` 里输入文件名运行。



### **4. 绝对路径与网络路径**

就像在文件资源管理器的地址栏一样，你可以直接粘贴路径。

- **本地路径**：输入 `C:\Windows` 或 `D:\Games` 会直接打开文件夹。
- **网络路径**：输入 `\\192.168.1.100` 或 `\\ServerName\Share` 可以直接访问局域网共享文件夹。



### **5. 网址与应用程序协议**

`Win + R` 也能充当简易的浏览器启动器。

- **网址**：输入 `www.example.com` 或 `https://...`，系统会调用默认浏览器打开。
- **应用协议**：如果安装了特定软件，可以调用其协议。例如输入 `ms-settings:` 会打开 Windows 11 的设置主页（这是 Win10/11 特有的，比传统的控制面板更现代）。



### 查找

1. **查看系统命令库**：
    - 进入 `C:\Windows\System32`。
    - 在搜索框搜 `*.msc`，你会看到所有能用的管理工具（如 `compmgmt.msc` 计算机管理）。
    - 搜 `*.cpl`，你会看到所有控制面板的快捷入口。
2. **利用“上帝模式” (God Mode)**：
    - 在桌面新建文件夹，重命名为 `GodMode.{ED7BA470-8E54-465E-825C-99712043E01C}`。
    - 打开这个文件夹，你会看到 Windows 所有设置项的全列表，虽然不能直接在这里运行，但鼠标悬停可以看到很多功能的真实名称和调用方式。

































