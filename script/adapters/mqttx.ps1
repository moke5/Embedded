#requires -Version 5.1
<#
能力适配器：mqttx
把参数原样转发给 MQTTX CLI。
路径解析顺序：MQTTX_EXE 环境变量 → PATH。
#>

$exe = $env:MQTTX_EXE
if (-not $exe) {
    $cmd = Get-Command mqttx -ErrorAction SilentlyContinue
    if ($cmd) { $exe = $cmd.Source }
}

if (-not $exe) {
    [Console]::Error.WriteLine('未找到 mqttx：npm install -g mqttx，或设置环境变量 MQTTX_EXE。')
    exit 127
}

& $exe @args
exit $LASTEXITCODE
