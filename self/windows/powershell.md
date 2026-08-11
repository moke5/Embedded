# powershell

[toc]

> .ps1

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

