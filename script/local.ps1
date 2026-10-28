#requires -Version 5.1
<#
本机能力统一入口。用法：
  local.ps1 list [tag]
  local.ps1 help <id>
  local.ps1 run <id> [参数...] [--yes]
  local.ps1 doctor
#>

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [Text.Encoding]::UTF8 } catch {}

$Root = Split-Path -Parent $PSScriptRoot
$ManifestPath = Join-Path $Root '本机\能力清单.json'

if (-not (Test-Path -LiteralPath $ManifestPath)) {
    [Console]::Error.WriteLine("清单不存在：$ManifestPath")
    exit 2
}

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$Caps = @($Manifest.capabilities)

function Get-Cap([string]$id) {
    $Caps | Where-Object { $_.id -eq $id } | Select-Object -First 1
}

function Show-Usage {
    @'
用法:
  local.ps1 list [tag]        列出能力，可按 tag 过滤
  local.ps1 help <id>         查看某能力的参数与示例
  local.ps1 run <id> [参数]   调用能力（confirm=true 时须加 --yes）
  local.ps1 doctor            检查依赖是否可用
'@ | Write-Output
}

function Exit-With([int]$code) {
    exit $code
}

$argv = @($args)
$Command = if ($argv.Count -ge 1) { [string]$argv[0] } else { 'list' }

switch ($Command.ToLowerInvariant()) {
    'list' {
        $tag = if ($argv.Count -ge 2) { [string]$argv[1] } else { $null }
        $list = if ($tag) { @($Caps | Where-Object { $_.tags -contains $tag }) } else { @($Caps) }
        '{0,-12} {1,-22} {2,-9} {3}' -f 'ID', 'NAME', 'STATUS', 'SUMMARY'
        foreach ($c in $list) {
            '{0,-12} {1,-22} {2,-9} {3}' -f $c.id, $c.name, $c.status, $c.summary
        }
        if ($list.Count -eq 0) { '没有匹配的能力' }
    }
    'help' {
        if ($argv.Count -lt 2) { Show-Usage; Exit-With 64 }
        $c = Get-Cap ([string]$argv[1])
        if (-not $c) { [Console]::Error.WriteLine("未知能力：$($argv[1])"); Exit-With 3 }
        "id      : $($c.id)"
        "name    : $($c.name)"
        "status  : $($c.status)"
        "summary : $($c.summary)"
        "adapter : $($c.adapter)"
        "requires: $($c.requires -join ', ')"
        "confirm : $($c.confirm)"
        "tags    : $($c.tags -join ', ')"
        'examples:'
        foreach ($e in @($c.examples)) { "  $e" }
    }
    'run' {
        if ($argv.Count -lt 2) { Show-Usage; Exit-With 64 }
        $id = [string]$argv[1]
        $c = Get-Cap $id
        if (-not $c) { [Console]::Error.WriteLine("未知能力：$id"); Exit-With 3 }

        $rest = @()
        if ($argv.Count -ge 3) { $rest = @($argv[2..($argv.Count - 1)]) }

        if ($c.confirm -eq $true) {
            if ($rest -notcontains '--yes') {
                [Console]::Error.WriteLine("能力 '$id' 需要确认：先征得用户同意，再追加 --yes。")
                Exit-With 10
            }
            $rest = @($rest | Where-Object { $_ -ne '--yes' })
        }

        $adapter = Join-Path $Root ($c.adapter -replace '/', '\')
        if (-not (Test-Path -LiteralPath $adapter)) {
            [Console]::Error.WriteLine("适配器不存在：$adapter")
            Exit-With 4
        }

        & $adapter @rest
        if ($null -eq $LASTEXITCODE) { Exit-With 0 }
        Exit-With $LASTEXITCODE
    }
    'doctor' {
        foreach ($c in $Caps) {
            $missing = @()
            foreach ($r in @($c.requires)) {
                if ($r -eq 'es.exe' -and $env:ES_EXE -and (Test-Path -LiteralPath $env:ES_EXE)) { continue }
                if (-not (Get-Command $r -ErrorAction SilentlyContinue)) { $missing += $r }
            }
            if ($missing.Count -eq 0) {
                '[ok]   {0,-12} {1}' -f $c.id, $c.name
            } else {
                '[miss] {0,-12} {1} -> {2}' -f $c.id, $c.name, ($missing -join ', ')
            }
        }
    }
    default {
        Show-Usage
        Exit-With 64
    }
}
