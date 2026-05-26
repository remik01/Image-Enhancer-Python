. "$PSScriptRoot/CopilotHook.Common.ps1"

$payload = Read-HookPayload -InputText ($input | Out-String)
$repositoryRoot = Get-RepositoryRoot -Payload $payload
$commandText = Get-ToolCommandText -Payload $payload
$stateDir = Ensure-HookStateDirectory -RepositoryRoot $repositoryRoot
$verificationNeeded = Join-Path $stateDir "verification-needed"
$verificationOk = Join-Path $stateDir "verification-ok"

$releaseOrPublishPatterns = @(
    '(?i)\bgit\s+commit\b',
    '(?i)\bgit\s+push\b',
    '(?i)\bpython\s+-m\s+build\b.*\b(upload|publish)\b',
    '(?i)\btwine\s+upload\b',
    '(?i)\bgh\s+pr\s+create\b',
    '(?i)\bgh\s+release\b'
)

if ((Test-CommandMatchesAny -CommandText $commandText -Patterns $releaseOrPublishPatterns) -and (Test-Path $verificationNeeded) -and -not (Test-Path $verificationOk)) {
    Write-HookLog -RepositoryRoot $repositoryRoot -Message "DENY release/publish command before verification: $commandText"
    $response = @{
        hookSpecificOutput = @{
            hookEventName = "PermissionRequest"
            decision = @{
                behavior = "deny"
                message = "Blocked by repository hook: file changes were made and verification is still marked as needed. Run relevant checks, for example python -m pytest / python -m ruff check ., then create .copilot-hooks/verification-ok or let the verification hook create it."
            }
        }
    }
    Write-Output (ConvertTo-CompactJson $response)
    exit 0
}
Write-Output "{}"
exit 0
