# =====================================================================
# U-for-Us O Regenerative Mesh - PowerShell Automated Launcher
# =====================================================================
$ErrorActionPreference = "Stop"
$scriptDir = $PSScriptRoot
$envFile = Join-Path $scriptDir ".env"
$envTemplate = Join-Path $scriptDir ".env.template"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "  U-for-Us O Regenerative Mesh - Autonomous Execution Suite" -ForegroundColor Cyan
Write-Host "  Sovereign Key: skinny3388.base.eth | Base Mainnet L2" -ForegroundColor Cyan
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Load .env file if available
if (Test-Path $envFile) {
    Write-Host "[+] Loading environment configuration from .env..." -ForegroundColor Green
    Get-Content $envFile | Where-Object { $_ -match '^\s*[^#\s]+=' } | ForEach-Object {
        $name, $value = $_.Split('=', 2)
        [Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), "Process")
    }
} elseif ((Test-Path $envTemplate) -and -not [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "Process")) {
    Write-Host "[!] No .env file found. Copying .env.template to .env..." -ForegroundColor Yellow
    Copy-Item $envTemplate $envFile
    Write-Host "[!] Created .env from template. Update .env with your GEMINI_API_KEY." -ForegroundColor Yellow
}

# 2. Check for GEMINI_API_KEY
$apiKey = [Environment]::GetEnvironmentVariable("GEMINI_API_KEY", "Process")
if (-not $apiKey -or $apiKey -eq "your_gemini_api_key_here") {
    Write-Host "[!] ERROR: GEMINI_API_KEY is missing or unconfigured." -ForegroundColor Red
    Write-Host "    Please edit $envFile or set it in your shell:" -ForegroundColor Red
    Write-Host "    \$env:GEMINI_API_KEY='your-key-here'" -ForegroundColor Yellow
    exit 1
}

# 3. Check and install Python dependencies if missing
Write-Host "[+] Verifying Python dependencies (google-genai, pydantic)..." -ForegroundColor Green
try {
    python -c "import google.genai, pydantic" 2>$null
} catch {
    Write-Host "[+] Installing required Python packages..." -ForegroundColor Yellow
    pip install -q google-genai pydantic
}

# 4. Execute target script
$targetScript = if ($args.Count -gt 0) { $args[0] } else { "u4u_gemini_sdk_client.py" }
Write-Host "[+] Launching $targetScript..." -ForegroundColor Green
Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
python (Join-Path $scriptDir $targetScript)
