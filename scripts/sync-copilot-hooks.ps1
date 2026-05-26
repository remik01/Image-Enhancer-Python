<#[
.SYNOPSIS
Synchronizes repository-local GitHub Copilot hooks into the user-level Copilot hooks directory.
]#>

[CmdletBinding()]
param(
    [ValidateSet("Copy", "Symlink")]
    [string] $Mode = "Copy",

    [string] $SourceDirectory = ".github/hooks",

    [string] $TargetDirectory = "$env:USERPROFILE\.copilot\hooks",

    [switch] $CleanTarget
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path ".").Path
$SourcePath = Join-Path $RepoRoot $SourceDirectory

if (-not (Test-Path $SourcePath)) {
    throw "Source hooks directory not found: $SourcePath"
}

if (-not (Test-Path $TargetDirectory)) {
    New-Item -ItemType Directory -Path $TargetDirectory -Force | Out-Null
}

if ($CleanTarget) {
    Get-ChildItem -Path $TargetDirectory -Filter "*.json" -File |
            Remove-Item -Force
}

$HookFiles = Get-ChildItem -Path $SourcePath -Filter "*.json" -File |
        Sort-Object Name

if ($HookFiles.Count -eq 0) {
    throw "No hook JSON files found in: $SourcePath"
}

foreach ($HookFile in $HookFiles) {
    $TargetFile = Join-Path $TargetDirectory $HookFile.Name

    if (Test-Path $TargetFile) {
        Remove-Item $TargetFile -Force
    }

    if ($Mode -eq "Symlink") {
        New-Item `
            -ItemType SymbolicLink `
            -Path $TargetFile `
            -Target $HookFile.FullName |
                Out-Null

        Write-Host "Linked $TargetFile -> $($HookFile.FullName)"
    }
    else {
        Copy-Item `
            -Path $HookFile.FullName `
            -Destination $TargetFile `
            -Force

        Write-Host "Copied $($HookFile.FullName) -> $TargetFile"
    }
}

Write-Host "Synchronized $($HookFiles.Count) Copilot hook file(s) to $TargetDirectory."