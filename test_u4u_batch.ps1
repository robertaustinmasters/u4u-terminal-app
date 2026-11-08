$apiUrl = "https://u4u-master-bridge.onrender.com/api/synthesize"
$authToken = "YOUR_SECURE_TOKEN_HERE"

$headers = @{
    "Content-Type" = "application/json"
    "x-u4u-auth" = $authToken
}

$commands = @(
    "/job_lead Automate the AI mesh pipeline",
    "/grant_lead Secure regional research funding",
    "swarm --init --nodes=4",
    "apex --target=bridge --sync",
    "evolve --commit --version=4.1.0"
)

$results = @()

foreach ($cmd in $commands) {
    Write-Host "[*] Testing: $cmd"
    
    # FastAPI requires BOTH 'command' and 'text' fields
    $body = @{ command = "batch_test"; text = $cmd } | ConvertTo-Json
    
    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -Body $body -ErrorAction Stop
        $results += @{ Command = $cmd; Status = "Success"; Response = $response }
        Write-Host "    [OK] Authorized response received." -ForegroundColor Green
    } catch {
        Write-Host "    [ERROR] $_" -ForegroundColor Red
        $results += @{ Command = $cmd; Status = "Error"; ErrorMessage = $_.Exception.Message }
    }
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$outFile = "u4u_batch_results_prod_$timestamp.json"
$results | ConvertTo-Json -Depth 4 | Out-File $outFile
Write-Host "[*] Production batch test complete. Results saved to $outFile"
