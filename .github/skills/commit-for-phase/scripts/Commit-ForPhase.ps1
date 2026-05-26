param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string] $PhaseNumber,

    [switch] $DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$script:GitSafeDirectory = $null

function Stop-WithMessage {
    param([string] $Message)
    Write-Error $Message
    exit 1
}

function Find-RepositoryRoot {
    $current = Get-Item -LiteralPath (Get-Location).ProviderPath
    while ($null -ne $current) {
        if (Test-Path -LiteralPath (Join-Path $current.FullName ".git")) {
            return $current.FullName
        }
        $current = $current.Parent
    }

    Stop-WithMessage "Could not find a Git repository root from the current directory."
}

function Invoke-Git {
    param([string[]] $Arguments)

    if ([string]::IsNullOrWhiteSpace($script:GitSafeDirectory)) {
        $output = & git @Arguments 2>&1
    } else {
        $output = & git -c "safe.directory=$script:GitSafeDirectory" @Arguments 2>&1
    }
    if ($LASTEXITCODE -ne 0) {
        $command = "git " + ($Arguments -join " ")
        Stop-WithMessage "$command failed: $output"
    }
    return $output
}

function Get-SectionLines {
    param(
        [string[]] $Lines,
        [string] $Heading
    )

    $start = -1
    for ($index = 0; $index -lt $Lines.Count; $index++) {
        if ($Lines[$index] -match "^##\s+$([regex]::Escape($Heading))\s*$") {
            $start = $index + 1
            break
        }
    }

    if ($start -lt 0) {
        return @()
    }

    $section = New-Object System.Collections.Generic.List[string]
    for ($index = $start; $index -lt $Lines.Count; $index++) {
        if ($Lines[$index] -match "^##\s+") {
            break
        }
        $section.Add($Lines[$index])
    }
    return $section.ToArray()
}

function Get-ChangedPaths {
    $paths = @(Invoke-Git @("status", "--short") | ForEach-Object {
        $line = $_.ToString()
        if ($line.Length -ge 4) {
            $line.Substring(3).Trim()
        }
    } | Where-Object { $_ -ne "" })

    return $paths
}

function Get-PhasePlanFile {
    param(
        [string] $RepositoryRoot,
        [string] $PhasePrefix
    )

    $planDirectory = Join-Path $RepositoryRoot "workflow\plans"
    if (-not (Test-Path -LiteralPath $planDirectory)) {
        return $null
    }

    $matches = @(Get-ChildItem -LiteralPath $planDirectory -File -Filter "phase-${PhasePrefix}-*.md")
    if ($matches.Count -eq 0) {
        return $null
    }
    if ($matches.Count -gt 1) {
        $names = ($matches | ForEach-Object { $_.Name }) -join ", "
        Stop-WithMessage "Multiple phase plan files found for phase ${PhasePrefix}: $names"
    }

    return $matches[0]
}

function Set-PhasePlanStatus {
    param(
        [System.IO.FileInfo] $PlanFile,
        [string] $CompletedDate,
        [switch] $DryRun
    )

    $desiredStatus = "Completed $CompletedDate"
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.AddRange([System.IO.File]::ReadAllLines($PlanFile.FullName))

    $statusHeadingIndex = -1
    for ($index = 0; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^##\s+Status\s*$") {
            $statusHeadingIndex = $index
            break
        }
    }

    if ($statusHeadingIndex -lt 0) {
        Stop-WithMessage "Phase plan has no ## Status section: $($PlanFile.FullName)"
    }

    $sectionEnd = $lines.Count
    for ($index = $statusHeadingIndex + 1; $index -lt $lines.Count; $index++) {
        if ($lines[$index] -match "^##\s+") {
            $sectionEnd = $index
            break
        }
    }

    $currentStatus = @(@(
        for ($index = $statusHeadingIndex + 1; $index -lt $sectionEnd; $index++) {
            $lines[$index].Trim()
        }
    ) | Where-Object { $_ -ne "" })

    if ($currentStatus.Count -eq 1 -and $currentStatus[0] -eq $desiredStatus) {
        return "already set to $desiredStatus"
    }

    if ($DryRun) {
        return "would set to $desiredStatus"
    }

    $updated = [System.Collections.Generic.List[string]]::new()
    for ($index = 0; $index -le $statusHeadingIndex; $index++) {
        $updated.Add($lines[$index])
    }
    $updated.Add("")
    $updated.Add($desiredStatus)
    $updated.Add("")
    for ($index = $sectionEnd; $index -lt $lines.Count; $index++) {
        $updated.Add($lines[$index])
    }

    [System.IO.File]::WriteAllLines($PlanFile.FullName, $updated, [System.Text.UTF8Encoding]::new($false))
    return "set to $desiredStatus"
}

function New-CommitDescription {
    param([string[]] $ChangedPaths)

    if ($ChangedPaths.Count -eq 0) {
        Stop-WithMessage "No repository changes to commit."
    }

    $topLevelGroups = @($ChangedPaths | ForEach-Object {
        $normalized = $_ -replace "\\", "/"
        if ($normalized.Contains("/")) {
            $normalized.Split("/")[0]
        } else {
            $normalized
        }
    } | Sort-Object -Unique)

    if ($topLevelGroups.Count -eq 1) {
        return "Update $($topLevelGroups[0])"
    }

    if ($ChangedPaths.Count -eq 1) {
        return "Update $($ChangedPaths[0])"
    }

    return "Update phase implementation"
}

if ($PhaseNumber -notmatch "^0*[1-9][0-9]*$") {
    Stop-WithMessage "Phase number must be a positive integer; received '$PhaseNumber'."
}

$phaseValue = [int] $PhaseNumber
$phasePrefix = "{0:D2}" -f $phaseValue

$script:GitSafeDirectory = (Find-RepositoryRoot) -replace "\\", "/"
$repoRoot = (Invoke-Git @("rev-parse", "--show-toplevel") | Select-Object -First 1).ToString().Trim()
$script:GitSafeDirectory = $repoRoot -replace "\\", "/"
Set-Location -LiteralPath $repoRoot

$phaseDirectory = Join-Path $repoRoot "workflow\phases"
if (-not (Test-Path -LiteralPath $phaseDirectory)) {
    Stop-WithMessage "Phase directory not found: $phaseDirectory"
}

$phaseMatches = @(Get-ChildItem -LiteralPath $phaseDirectory -File -Filter "${phasePrefix}_*.md")
if ($phaseMatches.Count -eq 0) {
    Stop-WithMessage "No phase file found for phase $PhaseNumber using pattern workflow/phases/${phasePrefix}_*.md."
}
if ($phaseMatches.Count -gt 1) {
    $names = ($phaseMatches | ForEach-Object { $_.Name }) -join ", "
    Stop-WithMessage "Multiple phase files found for phase ${PhaseNumber}: $names"
}

$phaseFile = $phaseMatches[0]
$phaseLines = @(Get-Content -LiteralPath $phaseFile.FullName)

$titleLine = $phaseLines | Where-Object { $_ -match "^#\s+(.+?)\s*$" } | Select-Object -First 1
if ($null -eq $titleLine -or $titleLine -notmatch "^#\s+(.+?)\s*$") {
    Stop-WithMessage "Phase file has no H1 title: $($phaseFile.FullName)"
}
$phaseTitle = $Matches[1].Trim()

$ticketSection = @(Get-SectionLines -Lines $phaseLines -Heading "Tickets")
$tickets = @($ticketSection | ForEach-Object {
    if ($_ -match "^\s*[*-]\s+(.+?)\s*$") {
        $Matches[1].Trim()
    }
} | Where-Object { $_ -ne "" })

if ($tickets.Count -eq 0) {
    Stop-WithMessage "Phase file has no tickets in the ## Tickets section: $($phaseFile.FullName)"
}

$loginName = $env:USERNAME
if ([string]::IsNullOrWhiteSpace($loginName)) {
    $loginName = $env:USER
}
if ([string]::IsNullOrWhiteSpace($loginName)) {
    $loginName = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name.Split("\")[-1]
}
if ([string]::IsNullOrWhiteSpace($loginName)) {
    Stop-WithMessage "Could not determine current OS login name."
}

$date = Get-Date -Format "yyyy.MM.dd"
$phasePlanFile = Get-PhasePlanFile -RepositoryRoot $repoRoot -PhasePrefix $phasePrefix
$phasePlanStatus = "not found; no status update applied"
if ($null -ne $phasePlanFile) {
    $phasePlanStatus = Set-PhasePlanStatus -PlanFile $phasePlanFile -CompletedDate $date -DryRun:$DryRun
}

$changedPaths = @(Get-ChangedPaths)
if ($DryRun -and $null -ne $phasePlanFile -and $phasePlanStatus.StartsWith("would set")) {
    $planRelativePath = [System.IO.Path]::GetRelativePath($repoRoot, $phasePlanFile.FullName) -replace "\\", "/"
    if ($changedPaths -notcontains $planRelativePath) {
        $changedPaths += $planRelativePath
    }
}
$description = New-CommitDescription -ChangedPaths $changedPaths
$message = "$date $loginName $($tickets -join " ") ${phaseTitle}: $description"

if ($DryRun) {
    Write-Output "Dry run: no files staged and no commit created."
    Write-Output "Phase file: $($phaseFile.FullName)"
    if ($null -ne $phasePlanFile) {
        Write-Output "Phase plan: $($phasePlanFile.FullName)"
    } else {
        Write-Output "Phase plan: not found"
    }
    Write-Output "Phase plan status: $phasePlanStatus"
    Write-Output "Changed paths: $($changedPaths.Count)"
    Write-Output "Commit message: $message"
    exit 0
}

Invoke-Git @("add", ".") | Out-Null
$commitOutput = Invoke-Git @("commit", "-m", $message)
$commitHash = (Invoke-Git @("rev-parse", "--short", "HEAD") | Select-Object -First 1).ToString().Trim()

Write-Output $commitOutput
Write-Output "Created commit: $commitHash"
Write-Output "Commit message: $message"
