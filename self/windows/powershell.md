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



