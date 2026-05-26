<#
.SYNOPSIS
Codex UserPromptSubmit governance hook.

.DESCRIPTION
Reads the Codex UserPromptSubmit payload from stdin and injects lightweight
developer context based on the user's prompt.

It does not block prompts by default.
It detects:
- likely AI Operating Mode,
- possible ADR impact,
- useful Skill candidates,
- vague prompt risk,
- debugging/refactoring/verification cues.

This hook is intentionally advisory. It nudges Codex before the turn begins
without pretending to be a magical enterprise architecture oracle. Humanity
already has enough of those in PowerPoint.
#>

$ErrorActionPreference = "Stop"

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

    if ([string]::IsNullOrWhiteSpace($inputText)) {
        return [pscustomobject]@{}
    }

    try {
        return $inputText | ConvertFrom-Json
    }
    catch {
        return [pscustomobject]@{
            rawInput = $inputText
            parseError = $_.Exception.Message
        }
    }
}

function ConvertTo-CompactJson {
    param([object] $Value)
    return ($Value | ConvertTo-Json -Compress -Depth 20)
}

function Test-AnyRegex {
    param(
        [string] $Text,
        [string[]] $Patterns
    )

    foreach ($pattern in $Patterns) {
        if ($Text -match $pattern) {
            return $true
        }
    }

    return $false
}

function Add-Line {
    param(
        [System.Collections.Generic.List[string]] $Lines,
        [string] $Text
    )
    $Lines.Add($Text) | Out-Null
}

$payload = Read-HookPayload -InputText ($input | Out-String)
$prompt = ""

if ($payload.prompt) {
    $prompt = [string]$payload.prompt
}
elseif ($payload.rawInput) {
    $prompt = [string]$payload.rawInput
}

$promptLower = $prompt.ToLowerInvariant()
$lines = New-Object System.Collections.Generic.List[string]

# Explicit mode detection.
$hasExplicitMode = $prompt -match '(?i)\bEnter\s+(Exploration|Implementation|Review|Refactoring|Incident\s*/\s*Debugging|Incident|Debugging)\s+Mode\b'

# Suggested mode detection.
$suggestedMode = $null

if (-not $hasExplicitMode) {
    if (Test-AnyRegex $promptLower @(
        '\bbug\b',
        '\berror\b',
        '\bfail',
        '\bexception\b',
        '\bdebug\b',
        '\bincident\b',
        '\broot cause\b',
        '\breproduce\b',
        '\bstack trace\b',
        '\blog\b'
    )) {
        $suggestedMode = "Incident / Debugging Mode"
    }
    elseif (Test-AnyRegex $promptLower @(
        '\brefactor\b',
        '\bcleanup\b',
        '\brestructure\b',
        '\brename\b',
        '\bextract\b',
        '\breduce duplication\b',
        '\bsimplify structure\b'
    )) {
        $suggestedMode = "Refactoring Mode"
    }
    elseif (Test-AnyRegex $promptLower @(
        '\breview\b',
        '\banalyze\b',
        '\bassess\b',
        '\bcheck\b',
        '\bfind issues\b',
        '\bwhat do you think\b',
        '\bdoes this look\b'
    )) {
        $suggestedMode = "Review Mode"
    }
    elseif (Test-AnyRegex $promptLower @(
        '\balternative\b',
        '\bbrainstorm\b',
        '\bexplore\b',
        '\boptions\b',
        '\btradeoff\b',
        '\bdesign\b',
        '\barchitecture\b'
    )) {
        $suggestedMode = "Exploration Mode"
    }
    elseif (Test-AnyRegex $promptLower @(
        '\bimplement\b',
        '\bcreate\b',
        '\badd\b',
        '\bmodify\b',
        '\bfix\b',
        '\bwrite\b',
        '\bgenerate\b'
    )) {
        $suggestedMode = "Implementation Mode"
    }
}

# ADR / governance trigger detection.
$adrCandidate = Test-AnyRegex $promptLower @(
    '\badr\b',
    '\barchitecture decision\b',
    '\bdecision[- ]log\b',
    '\bmodule boundary\b',
    '\bdependency direction\b',
    '\bnew dependency\b',
    '\bframework\b',
    '\bpersistence\b',
    '\bdatabase\b',
    '\bserialization\b',
    '\bexternal contract\b',
    '\bapi contract\b',
    '\bconcurrency\b',
    '\basync\b',
    '\bthread\b',
    '\bcache\b',
    '\bretry\b',
    '\bobservability\b',
    '\blogging strategy\b',
    '\bsecurity boundary\b',
    '\bruntime\b',
    '\bdeployment\b'
)

# Skill suggestions.
$skillSuggestions = New-Object System.Collections.Generic.List[string]

if ($adrCandidate -or (Test-AnyRegex $promptLower @('\badr\b', '\bdecision[- ]log\b'))) {
    $skillSuggestions.Add('adr-writer') | Out-Null
}

if (Test-AnyRegex $promptLower @(
    '\bruff\b',
    '\bmypy\b',
    '\bpyright\b',
    '\bbandit\b',
    '\bpip-audit\b',
    '\bstatic analysis\b',
    '\btype[- ]?check\b',
    '\bdependency audit\b'
)) {
    $skillSuggestions.Add('static-analysis-remediation') | Out-Null
}

if (Test-AnyRegex $promptLower @(
    '\bpytest\b',
    '\bpython -m\b',
    '\bverify\b',
    '\bbuild failed\b',
    '\btest failed\b',
    '\bci failed\b',
    '\bpackage\b'
)) {
    $skillSuggestions.Add('python-verification') | Out-Null
}

if (Test-AnyRegex $promptLower @(
    '\badapter\b',
    '\bxml\b',
    '\bjson\b',
    '\bexcel\b',
    '\bhttp\b',
    '\bapi client\b',
    '\bmapper\b',
    '\bdto\b',
    '\bexternal system\b',
    '\bimporter\b',
    '\bexporter\b'
)) {
    $skillSuggestions.Add('adapter-creation') | Out-Null
}

if ($suggestedMode -eq "Refactoring Mode" -or (Test-AnyRegex $promptLower @('\brefactor\b', '\bcleanup\b', '\brestructure\b'))) {
    $skillSuggestions.Add('refactoring-safety') | Out-Null
}

# Vague prompt warning.
$vaguePrompt = $false
if ($prompt.Trim().Length -lt 40 -and (Test-AnyRegex $promptLower @(
    '^fix it$',
    '^make it better$',
    '^improve this$',
    '^review this$',
    '^do it$',
    '^continue$',
    '^what now\??$'
))) {
    $vaguePrompt = $true
}

# Secret-ish prompt warning.
$possibleSecret = Test-AnyRegex $prompt @(
    'sk-[A-Za-z0-9_\-]{20,}',
    'ghp_[A-Za-z0-9_]{20,}',
    'github_pat_[A-Za-z0-9_]{20,}',
    'AKIA[0-9A-Z]{16}',
    '(?i)password\s*[:=]\s*\S{8,}',
    '(?i)token\s*[:=]\s*\S{12,}'
)

if ($hasExplicitMode) {
    Add-Line $lines "AI governance hint: the prompt explicitly selects an AI Operating Mode. Respect that mode, but do not override AGENTS.md, ADR governance, security, static-analysis, or reproducibility rules."
}
elseif ($suggestedMode) {
    Add-Line $lines "AI governance hint: this prompt appears to fit $suggestedMode. Use that mode's priorities unless the user's wording implies otherwise."
}

if ($adrCandidate) {
    Add-Line $lines "ADR governance hint: this prompt may affect architecture, dependencies, contracts, runtime assumptions, or operational policy. Evaluate whether an ADR or decision-log entry is required before implementing."
}

if ($skillSuggestions.Count -gt 0) {
    $uniqueSkills = $skillSuggestions | Select-Object -Unique
    Add-Line $lines ("Skill hint: consider using these repository skills if available: " + ($uniqueSkills -join ", ") + ".")
}

if ($vaguePrompt) {
    Add-Line $lines "Precision hint: the prompt is vague. State assumptions and avoid broad edits unless the intent is clear from repository context."
}

if ($possibleSecret) {
    Add-Line $lines "Security hint: the prompt may contain a token, password, or credential-like value. Do not echo it, store it, commit it, or write it to logs."
}

# Always include a tiny reminder only when something was detected.
if ($lines.Count -gt 0) {
    Add-Line $lines "General rule: prefer small, reviewable changes; preserve architectural boundaries; verify non-trivial work."
}

if ($lines.Count -eq 0) {
    [Console]::Out.WriteLine("{}")
    exit 0
}

$context = ($lines -join "`n")

$response = @{
    hookSpecificOutput = @{
        hookEventName = "UserPromptSubmit"
        additionalContext = $context
    }
}

[Console]::Out.WriteLine(($response | ConvertTo-Json -Compress -Depth 20))
exit 0
