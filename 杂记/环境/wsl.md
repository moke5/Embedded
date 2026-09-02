# WSL

## 目录

[toc]

## WSL1



## WSL2

基于Hyperv的虚拟话平台

### 前置

#### 1任务管理器

<img src="./img/image-20260611215327805.png">

#### 2.win+q

搜索：功能 –> 启用或关闭 Windows 功能

<img src="./img/image-20260611215536773.png">



#### 3CMD(root)

```shell
wsl --install --web-download
```

> 不行
>
> Microsoft store 下载也不得

到官网下载.wsl文件

```bash
# 格式：wsl --import <发行版名称> <安装路径> <你的.wsl文件路径>
wsl --import Ubuntu D:\WSL\Ubuntu D:\WSL\Ubuntu\ubuntu.wsl
```



```powershell
wsl --list
```



**设置默认 WSL 版本为 WSL2**（推荐）

在 PowerShell 执行：

```powershell
wsl --set-default-version 2
wsl --set-version Ubuntu 2
```



### 确认你的 Linux 系统版本

```
cat /etc/os-release
```



### 导出导入

- 导出

```
wsl --export Ubuntu-22.04 D:\Ubuntu_v1.tar
```



- 导入

```
wsl --import Ubuntu-WSL2 D:\app\VMware\wsl\Ubuntu2 D:\Ubuntu_v1.tar --version 2
```



- 删除

```
del D:\Ubuntu_v1.tar
```



## 版本切换与服务修复

> 来自原 `xun/2026/wslv.md`（P4 个人档案迁移并入）。

### WSL1 / WSL2 版本切换

```
wsl --set-version Ubuntu 1    # 切到 WSL1
wsl -l -v                     # VERSION 变为 1 即成功
wsl --set-version Ubuntu 2    # 切回 WSL2
wsl --shutdown
wsl -d Ubuntu
```

### WSL 起不来时的修复序列

```
# 强制关闭所有WSL实例
wsl --shutdown
# 重启WSL底层服务
net stop LxssManager
net start LxssManager
# 查看当前发行版状态
wsl -l -v
```

### 功能损坏时重装 WSL 主功能（dism）

```
# 先关闭多余功能
dism.exe /online /disable-feature /featurename:VirtualMachinePlatform /norestart
dism.exe /online /disable-feature /featurename:HypervisorPlatform /norestart
# 重新启用WSL主功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

