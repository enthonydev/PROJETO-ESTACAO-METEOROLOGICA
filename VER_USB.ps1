param([ValidatePattern("^COM[0-9]+$")][string]$Porta = "COM7")
Set-Location $PSScriptRoot
& .\.tools-venv\Scripts\python.exe -m serial.tools.miniterm $Porta 115200 --raw
