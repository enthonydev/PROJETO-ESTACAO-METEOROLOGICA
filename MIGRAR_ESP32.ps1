param(
    [ValidatePattern("^COM[0-9]+$")][string]$Porta = "COM7",
    [switch]$SomenteArquivos
)
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
Write-Host "Feche o Arduino IDE/Monitor Serial e o Thonny antes de continuar."
if (-not (Test-Path ".tools-venv\Scripts\python.exe")) {
    py -3 -m venv .tools-venv
    if ($LASTEXITCODE -ne 0) { throw "Instale Python 3.10+ no Windows e tente novamente." }
}
$Python = Join-Path $PSScriptRoot ".tools-venv\Scripts\python.exe"
& $Python -m pip install -r tools/requirements-migration.txt
if ($LASTEXITCODE -ne 0) { throw "Falha ao preparar ferramentas; placa ainda não foi alterada." }
$Modo = if ($SomenteArquivos) { "--deploy" } else { "--flash" }
& $Python tools/migrate_esp32.py --port $Porta $Modo
if ($LASTEXITCODE -ne 0) { throw "Procedimento interrompido. Preserve a pasta backups." }
