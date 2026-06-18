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

```
# 
wsl --list
```



**设置默认 WSL 版本为 WSL2**（推荐）

在 PowerShell 执行：

```powershell
wsl --set-default-version 2
wsl --set-version Ubuntu 2
```



### 换源

```bash
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
```



```bash
sudo tee /etc/apt/sources.list << EOF
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
EOF
```



如果还有一部分网络走官网的

```bash
# 
ls /etc/apt/sources.list.d/

sudo sed -i 's@//.*archive.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/ubuntu.sources
sudo sed -i 's@//.*security.ubuntu.com@//mirrors.tuna.tsinghua.edu.cn@g' /etc/apt/sources.list.d/ubuntu.sources
```



```
sudo apt clean
sudo apt update
```



### 启动问题

- 问题原因

1. WSL 默认调用 `dash` 作为终端解释器，`dash` 不会加载 `.bashrc`，且不兼容 bash 提示符配置语法，终端仅显示 `$`。
2. 初始 `/etc/wsl.conf` 未指定启动解释器，系统持续使用默认的 `dash`。
3. 仅修改 `.profile`、`.bashrc` 无法生效，启动环境未使用 bash。

- 解决操作

1. 编辑 `/etc/wsl.conf`，添加配置 `shell=/bin/bash`，强制 WSL 启动 bash。
2. 执行 `chsh -s /bin/bash`，修改账户默认解释器为 bash。
3. 执行 `wsl --shutdown`，重启 WSL 使全部配置生效。

