# Requires the supported Go toolchain and Windows PowerShell 5.1 or later.
$ErrorActionPreference = 'Stop'
$previousOS = $env:GOOS
$previousArch = $env:GOARCH
$previousCGO = $env:CGO_ENABLED
Push-Location $PSScriptRoot
try {
    $env:GOOS = 'windows'
    $env:GOARCH = 'amd64'
    $env:CGO_ENABLED = '0'
    $out = Join-Path $PSScriptRoot 'dist'
    [void][IO.Directory]::CreateDirectory($out)
    $exe = Join-Path $out 'UniAnchieta-Studio.exe'
    go build -trimpath -buildvcs=false -ldflags '-H windowsgui -s -w' -o $exe launcher_windows.go
    if ($LASTEXITCODE -ne 0) { throw 'Falha ao compilar o lançador.' }
    Copy-Item -LiteralPath Studio.ps1 -Destination $out
    Copy-Item -LiteralPath README.md -Destination $out
    $archive = Join-Path $out 'UniAnchieta-Studio-windows-x64.zip'
    Compress-Archive -Path @($exe, (Join-Path $out 'Studio.ps1'), (Join-Path $out 'README.md')) -DestinationPath $archive -Force
    Get-FileHash $archive
} finally {
    Pop-Location
    $env:GOOS = $previousOS
    $env:GOARCH = $previousArch
    $env:CGO_ENABLED = $previousCGO
}
