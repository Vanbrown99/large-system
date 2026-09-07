param(
    [ValidateSet("backup", "restore")]
    [string]$Action = "backup",
    [string]$File = "school_erp.backup"
)

if ($Action -eq "backup") {
    docker compose exec -T mysql mysqldump -u erp_user -perp_password_change_me school_erp > $File
    Write-Host "Backup written to $File"
} else {
    Get-Content -Raw $File | docker compose exec -T mysql mysql -u erp_user -perp_password_change_me school_erp
    Write-Host "Database restored from $File"
}
