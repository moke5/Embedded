



```
# 替换成你自己的发行名
wsl --set-version Ubuntu 1

wsl -l -v
# VERSION 变为 1 即成功

wsl --set-version Ubuntu 2
wsl --shutdown
wsl -d Ubuntu
```



```
# 强制关闭所有WSL实例
wsl --shutdown
# 重启WSL底层服务
net stop LxssManager
net start LxssManager
# 查看当前发行版状态
wsl -l -v
```



```
wsl -d Ubuntu
```



```
# 先关闭多余功能
dism.exe /online /disable-feature /featurename:VirtualMachinePlatform /norestart
dism.exe /online /disable-feature /featurename:HypervisorPlatform /norestart
# 重新启用WSL主功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```



