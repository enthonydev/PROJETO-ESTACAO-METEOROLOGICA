param([ValidatePattern("^COM[0-9]+$")][string]$Porta = "COM7")
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Python = Join-Path $PSScriptRoot ".tools-venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw "Execute MIGRAR_ESP32.ps1 primeiro." }
& $Python -m pip install -r backend/requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Falha ao instalar dependências do dashboard." }
$env:PYTHONPATH = Join-Path $PSScriptRoot "backend"
$env:ENABLE_HTTP_INGESTION = "true"
$ApiArguments = '"' + $Python + '" -m uvicorn app.main:app --host 127.0.0.1 --port 8000'
$BridgeArguments = '"' + $Python + '" tools/serial_bridge.py --port ' + $Porta
Start-Process -FilePath "cmd.exe" -ArgumentList @('/k', $ApiArguments) -WorkingDirectory $PSScriptRoot
Start-Process -FilePath "cmd.exe" -ArgumentList @('/k', $BridgeArguments) -WorkingDirectory $PSScriptRoot
Start-Process "http://127.0.0.1:8000/dashboard/?station=estacao-esp32-real"
