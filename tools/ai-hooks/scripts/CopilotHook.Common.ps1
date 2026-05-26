function Read-HookPayload {
    param([string] $InputText)

    $inputText = $InputText
    if ([string]::IsNullOrWhiteSpace($inputText)) {
        try {
            $callerInput = (Get-Variable -Name input -Scope 1 -ErrorAction Stop).Value
            if ($null -ne $callerInput) {
                $inputText = (@($callerInput) -join "`n")
            }
        } catch { }
    }
    if ([string]::IsNullOrWhiteSpace($inputText)) {
        $inputText = [Console]::In.ReadToEnd()
    }
    if ([string]::IsNullOrWhiteSpace($inputText)) { return [pscustomobject]@{} }
    try { return $inputText | ConvertFrom-Json }
    catch { return [pscustomobject]@{ rawInput = $inputText; parseError = $_.Exception.Message } }
}

function Get-RepositoryRoot {
    param([object] $Payload)
    if ($Payload.cwd) { return $Payload.cwd }
    return (Get-Location).Path
}

function Ensure-HookStateDirectory {
    param([string] $RepositoryRoot)
    $stateDir = Join-Path $RepositoryRoot ".copilot-hooks"
    if (-not (Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
    return $stateDir
}

function Write-HookLog {
    param([string] $RepositoryRoot, [string] $Message)
    try {
        $stateDir = Ensure-HookStateDirectory -RepositoryRoot $RepositoryRoot
        $logFile = Join-Path $stateDir "hooks.log"
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff"
        Add-Content -Path $logFile -Value "[$timestamp] $Message" -Encoding UTF8
    } catch { }
}

function ConvertTo-CompactJson {
    param([object] $Value)
    return ($Value | ConvertTo-Json -Compress -Depth 20)
}

function Get-StringLeaves {
    param([object] $Value)
    $result = New-Object System.Collections.Generic.List[string]
    function Visit { param([object] $Node)
        if ($null -eq $Node) { return }
        if ($Node -is [string]) { if (-not [string]::IsNullOrWhiteSpace($Node)) { $result.Add($Node) }; return }
        if ($Node -is [System.Collections.IEnumerable] -and -not ($Node -is [string])) { foreach ($item in $Node) { Visit $item }; return }
        foreach ($prop in $Node.PSObject.Properties) { Visit $prop.Value }
    }
    Visit $Value
    return $result
}

function Get-ToolCommandText {
    param([object] $Payload)
    $toolArgs = $Payload.toolArgs
    if ($null -eq $toolArgs) { $toolArgs = $Payload.tool_input }
    if ($null -eq $toolArgs) { $toolArgs = $Payload.toolInput }
    if ($null -eq $toolArgs) { $toolArgs = $Payload.tool_input_json }
    if ($null -eq $toolArgs) { $toolArgs = $Payload.input }
    if ($null -eq $toolArgs) { $toolArgs = $Payload.arguments }
    if ($null -eq $toolArgs) { $toolArgs = $Payload.parameters }
    if ($null -eq $toolArgs -and $Payload.command) { $toolArgs = [pscustomobject]@{ command = $Payload.command } }
    if ($null -eq $toolArgs) { return "" }
    $strings = Get-StringLeaves -Value $toolArgs
    return ($strings -join "`n")
}

function Get-HookToolName {
    param([object] $Payload)
    if ($Payload.toolName) { return [string]$Payload.toolName }
    if ($Payload.tool_name) { return [string]$Payload.tool_name }
    if ($Payload.tool) { return [string]$Payload.tool }
    if ($Payload.name) { return [string]$Payload.name }
    return ""
}

function Test-CommandMatchesAny {
    param([string] $CommandText, [string[]] $Patterns)
    foreach ($pattern in $Patterns) {
        if ($CommandText -match $pattern) { return $true }
    }
    return $false
}
