#requires -Version 5.1
<#
能力适配器：file-search
把参数原样转发给 Everything 命令行 es.exe。
路径解析顺序：ES_EXE 环境变量 → PATH → 常见安装目录。
#>

$exe = $env:ES_EXE
if ($exe -and -not (Test-Path -LiteralPath $exe)) {
    [Console]::Error.WriteLine("ES_EXE 指向的文件不存在：$exe")
    exit 127
}

if (-not $exe) {
    $cmd = Get-Command es.exe -ErrorAction SilentlyContinue
    if ($cmd) { $exe = $cmd.Source }
}

if (-not $exe) {
    $candidates = @(
        'C:\Program Files\Everything\es.exe',
        'C:\Program Files (x86)\Everything\es.exe',
        (Join-Path $env:LOCALAPPDATA 'Programs\Everything\es.exe')
    )
    $exe = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
}

if (-not $exe) {
    [Console]::Error.WriteLine('未找到 es.exe：安装 Everything 命令行工具，或设置环境变量 ES_EXE 指向 es.exe。')
    exit 127
}

& $exe @args
exit $LASTEXITCODE
