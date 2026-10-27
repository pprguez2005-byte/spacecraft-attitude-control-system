# ==============================================================================
# Script de Respaldo Automatizado - TFG
# Copia el directorio de trabajo 'DESARROLLO_TFG' hacia '../backups/'
# ==============================================================================

param(
    [string]$Tag = ""
)

$dateStr = Get-Date -Format "yyyy_MM_dd"
if ($Tag -ne "") {
    $backupFolderName = "backup_${dateStr}_${Tag}"
} else {
    $timeStr = Get-Date -Format "HHmmss"
    $backupFolderName = "backup_${dateStr}_${timeStr}"
}

$sourceDir = $PSScriptRoot
$backupsDir = Join-Path (Split-Path $sourceDir -Parent) "backups"
$targetDir = Join-Path $backupsDir $backupFolderName

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "INICIANDO COPIA DE SEGURIDAD DEL TFG" -ForegroundColor Cyan
Write-Host "Origen:  $sourceDir"
Write-Host "Destino: $targetDir"
Write-Host "========================================="

if (-not (Test-Path $backupsDir)) {
    New-Item -ItemType Directory -Path $backupsDir -Force | Out-Null
}

robocopy $sourceDir $targetDir /E /XF *.log /XD .git

if ($LASTEXITCODE -le 7) {
    Write-Host "[OK] Copia de seguridad completada con exito en: $targetDir" -ForegroundColor Green
} else {
    Write-Host "[ALERTA] Hubo advertencias o errores durante el backup (codigo: $LASTEXITCODE)" -ForegroundColor Yellow
}
