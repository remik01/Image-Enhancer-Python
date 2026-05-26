<#
.SYNOPSIS
Transfers repository-local GitHub skills into Codex by linking them into the
user's Codex skills directory.

.DESCRIPTION
This repository stores project-owned skill definitions under .github\skills so
they can live next to the rest of the GitHub-oriented project instructions.
Codex discovers active skills from the user's Codex skills directory at session
startup, so this script transfers those GitHub skill folders into Codex by
creating Windows junctions from .github\skills\*\SKILL.md directories into
$env:USERPROFILE\.codex\skills.

Existing destination skill junctions or symlinks with the same name are replaced
with links to this repository's skills. Real directories or files are not
deleted, because they may contain user-owned content. Restart Codex after
running this script so the linked skills appear in the active skills list.
#>

[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string] $RepoSkillsPath,
    [string] $CodexSkillsPath
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($RepoSkillsPath)) {
    $RepoSkillsPath = Join-Path $PSScriptRoot '..\.github\skills'
}

if ([string]::IsNullOrWhiteSpace($CodexSkillsPath)) {
    $CodexSkillsPath = Join-Path $env:USERPROFILE '.codex\skills'
}

function Resolve-FullPath {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    $executionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
}

function Test-ReparsePoint {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return $false
    }

    return [bool] ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
}

function Remove-ReparsePoint {
    param(
        [Parameter(Mandatory = $true)]
        [string] $Path
    )

    $item = Get-Item -LiteralPath $Path -Force -ErrorAction Stop
    if (-not ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint)) {
        throw "Refusing to remove non-link path: $Path"
    }

    if ($item.PSIsContainer) {
        # Directory.Delete removes the directory reparse point itself. Passing
        # $false avoids recursive deletion and prevents following link children.
        [System.IO.Directory]::Delete($item.FullName, $false)
    } else {
        Remove-Item -LiteralPath $item.FullName -Force
    }
}

$sourceRoot = Resolve-FullPath -Path $RepoSkillsPath
$destinationRoot = Resolve-FullPath -Path $CodexSkillsPath

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Repository skills directory does not exist: $sourceRoot"
}

if (-not (Test-Path -LiteralPath $destinationRoot -PathType Container)) {
    New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null
    Write-Host "Created Codex skills directory: $destinationRoot"
}

$markerPath = Join-Path $destinationRoot '###PYTHON SKILLS###'
if (Test-Path -LiteralPath $markerPath -PathType Container) {
    throw "Python skills marker path is a directory, expected a file: $markerPath"
}
if ($PSCmdlet.ShouldProcess($markerPath, 'Create empty Python skills marker file')) {
    [System.IO.File]::WriteAllText($markerPath, '')
    Write-Host "Created Python skills marker: $markerPath"
}

$skillDirectories = Get-ChildItem -LiteralPath $sourceRoot -Directory |
    Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') -PathType Leaf } |
    Sort-Object -Property Name

if (-not $skillDirectories) {
    Write-Host "No skills with SKILL.md found in: $sourceRoot"
    return
}

foreach ($skillDirectory in $skillDirectories) {
    $destination = Join-Path $destinationRoot $skillDirectory.Name

    if (Test-Path -LiteralPath $destination) {
        if (-not (Test-ReparsePoint -Path $destination)) {
            throw "Refusing to overwrite non-link skill path: $destination"
        }

        if ($PSCmdlet.ShouldProcess($destination, "Replace existing link with $($skillDirectory.FullName)")) {
            Remove-ReparsePoint -Path $destination
            Write-Host "Removed existing skill link: $($skillDirectory.Name)"
        }
    }

    if ($PSCmdlet.ShouldProcess($destination, "Link to $($skillDirectory.FullName)")) {
        # A junction keeps the GitHub-owned skill source in the repository while
        # exposing it at Codex's startup discovery location.
        New-Item -ItemType Junction -Path $destination -Target $skillDirectory.FullName | Out-Null
        Write-Host "Linked skill: $($skillDirectory.Name)"
    }
}

Write-Host 'Restart Codex to pick up newly linked skills.'
