. "$PSScriptRoot/CopilotHook.Common.ps1"

$payload = Read-HookPayload -InputText ($input | Out-String)
$repositoryRoot = Get-RepositoryRoot -Payload $payload
$stateDir = Ensure-HookStateDirectory -RepositoryRoot $repositoryRoot

$verificationNeeded = Join-Path $stateDir "verification-needed"
$verificationOk = Join-Path $stateDir "verification-ok"

Set-Content -Path $verificationNeeded -Value "File changes detected at $(Get-Date -Format o). Run relevant verification before commit/push." -Encoding UTF8
if (Test-Path $verificationOk) { Remove-Item $verificationOk -Force -ErrorAction SilentlyContinue }
$toolName = Get-HookToolName -Payload $payload
Write-HookLog -RepositoryRoot $repositoryRoot -Message "Change detected by tool '$toolName'. Verification marker created."

if ($env:COPILOT_HOOK_AUTO_TEST -eq "1") {
    Push-Location $repositoryRoot
    try {
        & python -m pytest
        if ($LASTEXITCODE -eq 0) {
            Set-Content -Path $verificationOk -Value "Automatic test verification passed at $(Get-Date -Format o)." -Encoding UTF8
            Remove-Item $verificationNeeded -Force -ErrorAction SilentlyContinue
            Write-HookLog -RepositoryRoot $repositoryRoot -Message "Automatic tests passed."
        } else {
            Write-HookLog -RepositoryRoot $repositoryRoot -Message "Automatic tests failed with exit code $LASTEXITCODE."
        }
    } finally { Pop-Location }
}
exit 0
