. "$PSScriptRoot/CopilotHook.Common.ps1"

$payload = Read-HookPayload -InputText ($input | Out-String)
$repositoryRoot = Get-RepositoryRoot -Payload $payload
$commandText = Get-ToolCommandText -Payload $payload

$dangerousPatterns = @(
    '(?i)\brm\s+-rf\s+[/~]',
    '(?i)\brm\s+-rf\s+\*',
    '(?i)\bRemove-Item\b.*\s-Recurse\b.*\s-Force\b.*(\$HOME|~|/|\\|\*)',
    '(?i)\bdel\s+/[fsq]\b',
    '(?i)\brmdir\s+/s\b',
    '(?i)\bformat\s+[a-z]:',
    '(?i)\bdiskpart\b',
    '(?i)\bshutdown\b',
    '(?i)\bRestart-Computer\b',
    '(?i)\bStop-Computer\b',
    '(?i)\bgit\s+reset\s+--hard\b',
    '(?i)\bgit\s+clean\s+-[^\r\n]*[fdx]',
    '(?i)\bgit\s+push\b.*\s--force',
    '(?i)\bgit\s+push\b.*\s-f\b',
    '(?i)\bSet-ExecutionPolicy\b',
    '(?i)\bInvoke-Expression\b',
    '(?i)\biex\b',
    '(?i)\bcurl\b.*\|\s*(bash|sh|powershell|pwsh)',
    '(?i)\biwr\b.*\|\s*(iex|powershell|pwsh)',
    '(?i)\bInvoke-WebRequest\b.*\|\s*(Invoke-Expression|iex|powershell|pwsh)'
)

if (Test-CommandMatchesAny -CommandText $commandText -Patterns $dangerousPatterns) {
    Write-HookLog -RepositoryRoot $repositoryRoot -Message "DENY dangerous command: $commandText"
    $response = @{
        hookSpecificOutput = @{
            hookEventName = "PreToolUse"
            permissionDecision = "deny"
            permissionDecisionReason = "Blocked by repository hook: command looks destructive or unsafe. Ask the user explicitly and propose a safer, narrower command."
        }
    }
    Write-Output (ConvertTo-CompactJson $response)
    exit 0
}

$toolName = Get-HookToolName -Payload $payload
Write-HookLog -RepositoryRoot $repositoryRoot -Message "ALLOW command pre-check for tool '$toolName'"
Write-Output "{}"
exit 0
