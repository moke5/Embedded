#requires -Version 5.1
<#
能力适配器：file-open
调用用户既有的 WSL 搜索选择脚本：
环境变量 EVERYTHING_OPEN 指向 .sh 时通过 wsl.exe 执行，否则直接执行。
#>

$target = $env:EVERYTHING_OPEN
if (-not $target) {
    [Console]::Error.WriteLine('未配置 EVERYTHING_OPEN：把它设为现有 WSL 打开器脚本的路径，例如 /home/<用户>/bin/everything-open.sh。')
    exit 127
}

if ($target -match '\.sh$') {
    wsl.exe bash $target @args
} else {
    & $target @args
}
exit $LASTEXITCODE
