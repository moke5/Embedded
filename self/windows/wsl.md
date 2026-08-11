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

