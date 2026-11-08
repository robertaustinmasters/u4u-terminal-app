$baseUrl = "https://u4u-master-bridge.onrender.com"
$headers = @{
    "Content-Type" = "application/json"
    "X-U4U-Auth"   = $env:MESH_AUTH_TOKEN
}

$endpoints = @(
    @{ Route = "/api/synthesize"; Command = "live_audit"; Text = "Verify physics telemetry." },
    @{ Route = "/api/paymaster/sponsor"; Command = "sponsor_tx"; Text = "Request EIP-7702 sponsorship." }
)

Clear-Host
Write-Host "================================================================="
Write-Host "  U-for-Us O Regenerative Mesh - Dual Endpoint Audit"
Write-Host "================================================================="

foreach ($ep in $endpoints) {
    $url = "$baseUrl$($ep.Route)"
    $body = @{ command = $ep.Command; text = $ep.Text } | ConvertTo-Json
    Write-Host "`n[*] Testing: POST $($ep.Route)" -ForegroundColor Cyan
    
    try {
        # Execute request and force variable overwrite
        $res = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $body -ErrorAction Stop
        Write-Host "    [OK] Authorized response received:" -ForegroundColor Green
        $res | ConvertTo-Json -Depth 4 | Write-Host
    } catch {
        Write-Host "    [ERROR] $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Message -match "405") {
            Write-Host "    -> Render is still serving the old version. Try again in 60 seconds." -ForegroundColor DarkGray
        }
    }
}
Write-Host "`n[*] Dual endpoint audit complete."
