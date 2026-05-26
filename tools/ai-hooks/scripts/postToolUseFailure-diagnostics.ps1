. "$PSScriptRoot/CopilotHook.Common.ps1"

$payload = Read-HookPayload -InputText ($input | Out-String)
$repositoryRoot = Get-RepositoryRoot -Payload $payload
$toolName = Get-HookToolName -Payload $payload
Write-HookLog -RepositoryRoot $repositoryRoot -Message "Tool failure: tool='$toolName' error='$($payload.error)'"

$context = @"
Tool execution failed. Before retrying:
- Read the actual error.
- Avoid repeating the same command blindly.
- Narrow the scope.
- Preserve diagnostic output.
- If this is a Python verification or static-analysis failure, classify the first meaningful root cause before editing.
"@
$response = @{ additionalContext = $context }
Write-Output (ConvertTo-CompactJson $response)
exit 0
