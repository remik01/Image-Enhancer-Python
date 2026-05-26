. "$PSScriptRoot/CopilotHook.Common.ps1"

$payload = Read-HookPayload -InputText ($input | Out-String)
$repositoryRoot = Get-RepositoryRoot -Payload $payload
Ensure-HookStateDirectory -RepositoryRoot $repositoryRoot | Out-Null
Write-HookLog -RepositoryRoot $repositoryRoot -Message "Session started. Source=$( $payload.source )"

$context = @"
Repository governance reminder:
- Respect AGENTS.md, ADRs, decision logs, and .github/instructions/*.instructions.md.
- Do not bypass domain/application/adapter/UI/CLI/bootstrap boundaries.
- Propose ADR discussion for architectural impact, dependencies, runtime assumptions, or boundary changes.
- After file edits, run relevant verification before commit/push.
- Dangerous shell commands may be blocked by repository hooks.
"@
$response = @{
    hookSpecificOutput = @{
        hookEventName = "SessionStart"
        additionalContext = $context
    }
}

[Console]::Out.WriteLine(($response | ConvertTo-Json -Compress -Depth 20))
exit 0
