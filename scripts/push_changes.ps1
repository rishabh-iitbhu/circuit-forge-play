param(
    [string]$Message = "Auto-deploy: update from local workspace"
)

Set-Location -Path (Split-Path -Path $MyInvocation.MyCommand.Definition -Parent)\..\

if (-not (Test-Path .git)) {
    Write-Host ".git not found in repository root. Ensure this script is run from inside the repo." -ForegroundColor Yellow
    exit 1
}

git add -A
$commitResult = & git commit -m $Message 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "No changes to commit or commit failed:" -ForegroundColor Yellow
    Write-Host $commitResult
} else {
    Write-Host "Committed changes: $Message"
}

Write-Host "Pushing to origin/main..."
git push origin main
