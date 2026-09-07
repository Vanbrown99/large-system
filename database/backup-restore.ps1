param(
    [ValidateSet("backup", "restore")]
    [string]$Action = "backup",
    [string]$File = "school_erp.backup"
)

if ($Action -eq "backup") {
    docker compose exec -T postgres pg_dump -U erp_user -Fc school_erp > $File
    Write-Host "Backup written to $File"
} else {
    Get-Content -Raw $File | docker compose exec -T postgres pg_restore -U erp_user -d school_erp --clean --if-exists
    Write-Host "Database restored from $File"
}
