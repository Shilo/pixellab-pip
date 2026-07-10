[CmdletBinding()]
param(
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

# Get-NormalizedPath and Select-MenuItem live in lib/common.ps1 (shared with
# manage-claude-plugin.ps1, manage-codex-plugin.ps1, manage-pixellab-doc-cache.ps1).
. (Join-Path (Join-Path $PSScriptRoot 'lib') 'common.ps1')

# OpenCode has no skill marketplace or CLI. Skills are directory-discovered:
# OpenCode loads SKILL.md from folders it scans, including the global path
# ~/.config/opencode/skills/<name>/SKILL.md (see https://opencode.ai/docs/skills).
# (`opencode plugin` is a different mechanism -- it installs JS/TS code plugins
# with event hooks, not skills.) So this script manages a filesystem entry there:
#   development local -> a directory junction/symlink to the repo skill (live edits)
#   production copy   -> a plain recursive copy (what a manual/release install looks like)
$SkillName = "pixellab-pip"
$SkillSourceRelative = "skills\pixellab-pip"

function Show-Usage {
    Write-Host "Usage: powershell -NoProfile -File dev-tools\manage-opencode-plugin.ps1 [-Help]"
    Write-Host ""
    Write-Host "Refresh the local OpenCode install for this skill or switch between development and production installs."
    Write-Host "Interactive menu actions can install, update, or uninstall the skill at OpenCode's global skills path."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Help    Show this help and exit without changing OpenCode skill state."
}

function Get-OpenCodeSkillPath {
    param([Parameter(Mandatory = $true)][string]$SkillName)

    # OpenCode resolves its global config dir via xdg-basedir: $XDG_CONFIG_HOME
    # when set, else ~/.config -- on Windows too (OpenCode issue #8235). Honor the
    # override so the install lands where OpenCode actually reads skills.
    $configBase = if (-not [string]::IsNullOrWhiteSpace($env:XDG_CONFIG_HOME)) {
        $env:XDG_CONFIG_HOME
    }
    else {
        Join-Path $env:USERPROFILE ".config"
    }
    return Join-Path $configBase "opencode\skills\$SkillName"
}

function Format-FolderLink {
    # Emit an OSC 8 terminal hyperlink so the install folder is clickable in
    # Windows Terminal / VS Code; the visible text stays the plain path, so
    # terminals without OSC 8 support just show the readable location.
    param([Parameter(Mandatory = $true)][string]$Path)

    $uri = 'file:///' + (($Path -replace '\\', '/') -replace ' ', '%20')
    $esc = [char]27
    return "$esc]8;;$uri$esc\$Path$esc]8;;$esc\"
}

function Test-ReparsePoint {
    param([Parameter(Mandatory = $true)][string]$Path)

    $item = Get-Item -LiteralPath $Path -Force
    return ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -eq [System.IO.FileAttributes]::ReparsePoint
}

function Get-ReparseTarget {
    param([Parameter(Mandatory = $true)][string]$Path)

    $target = (Get-Item -LiteralPath $Path -Force).Target
    if ($target -is [System.Collections.IEnumerable] -and $target -isnot [string]) {
        $target = @($target)[0]
    }
    if ([string]::IsNullOrWhiteSpace($target)) {
        return $null
    }
    return Get-NormalizedPath ([string]$target)
}

function Pause-BeforeExit {
    if ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
        return
    }

    Write-Host ""
    Read-Host "Press Enter to exit" | Out-Null
}

function Install-DevelopmentLocal {
    param(
        [Parameter(Mandatory = $true)][string]$SkillPath,
        [Parameter(Mandatory = $true)][string]$SkillSource
    )

    $parent = Split-Path -Parent $SkillPath
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    # Prefer a junction: it needs no admin rights or Developer Mode on Windows.
    # Fall back to a symbolic link only if the junction cannot be created.
    try {
        New-Item -ItemType Junction -Path $SkillPath -Target $SkillSource -ErrorAction Stop | Out-Null
        Write-Host "  Linked (junction): $SkillPath -> $SkillSource"
    }
    catch {
        Write-Host "  Junction failed ($($_.Exception.Message)); trying a symbolic link..." -ForegroundColor Yellow
        New-Item -ItemType SymbolicLink -Path $SkillPath -Target $SkillSource -ErrorAction Stop | Out-Null
        Write-Host "  Linked (symlink): $SkillPath -> $SkillSource"
    }
}

function Install-ProductionCopy {
    param(
        [Parameter(Mandatory = $true)][string]$SkillPath,
        [Parameter(Mandatory = $true)][string]$SkillSource
    )

    $parent = Split-Path -Parent $SkillPath
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }

    Copy-Item -LiteralPath $SkillSource -Destination $SkillPath -Recurse -Force
    Write-Host "  Copied: $SkillSource -> $SkillPath"
}

function Remove-CurrentInstall {
    param([Parameter(Mandatory = $true)]$State)

    if (-not $State.Exists) {
        return
    }

    if ($State.IsLink) {
        # Delete only the reparse point, never recurse into the repo source it
        # points at. Directory.Delete(path, recursive:$false) removes the link.
        [System.IO.Directory]::Delete($State.Path, $false)
        Write-Host "  Removed link: $($State.Path)"
    }
    else {
        Remove-Item -LiteralPath $State.Path -Recurse -Force
        Write-Host "  Removed copy: $($State.Path)"
    }
}

function Get-InstallState {
    param(
        [Parameter(Mandatory = $true)][string]$SkillPath,
        [Parameter(Mandatory = $true)][string]$SkillSource
    )

    $exists = Test-Path -LiteralPath $SkillPath
    $isLink = $false
    $linkTarget = $null

    if ($exists) {
        $isLink = Test-ReparsePoint -Path $SkillPath
        if ($isLink) {
            $linkTarget = Get-ReparseTarget -Path $SkillPath
        }
    }

    $normalizedSource = Get-NormalizedPath $SkillSource
    $isDevLocal = $isLink -and ($linkTarget -eq $normalizedSource)
    $isProductionCopy = $exists -and (-not $isLink)

    $mode = if (-not $exists) {
        "not installed"
    }
    elseif ($isDevLocal) {
        "development local"
    }
    elseif ($isLink) {
        "unknown install"
    }
    else {
        "production copy"
    }

    [pscustomobject]@{
        Path = $SkillPath
        Exists = $exists
        IsLink = $isLink
        LinkTarget = $linkTarget
        Mode = $mode
        IsDevLocal = $isDevLocal
        IsProductionCopy = $isProductionCopy
    }
}

function Write-InstallState {
    param([Parameter(Mandatory = $true)]$State)

    if ($State.Exists) {
        Write-Host "Current install:"
        Write-Host "  Skill path:  $(Format-FolderLink $State.Path)"
        if ($State.IsLink) {
            Write-Host "  Link target: $(Format-FolderLink $State.LinkTarget)"
        }
    }
    else {
        # Not installed yet, so the folder does not exist -- show it plainly
        # (no link to a folder that is not there) so you know where it will land.
        Write-Host "Current install: not installed"
        Write-Host "  Skill path:  $($State.Path)"
    }

    Write-Host "  Mode:        $($State.Mode)"
}

function Invoke-Main {
    if ($Help) {
        Show-Usage
        return
    }

    $scriptDir = Split-Path -Parent $PSCommandPath
    $repoRoot = Get-NormalizedPath (Split-Path -Parent $scriptDir)
    $skillSource = Get-NormalizedPath (Join-Path $repoRoot $SkillSourceRelative)
    $skillPath = Get-OpenCodeSkillPath -SkillName $SkillName

    $sourceSkillMd = Join-Path $skillSource "SKILL.md"
    if (-not (Test-Path -LiteralPath $sourceSkillMd)) {
        throw "Could not find skill source: $sourceSkillMd"
    }

    Write-Host "Repo root: $repoRoot"
    Write-Host "Skill:    $SkillName"
    Write-Host ""

    $state = Get-InstallState -SkillPath $skillPath -SkillSource $skillSource
    Write-InstallState -State $state
    Write-Host ""

    if ($state.Mode -eq "not installed") {
        $options = @(
            [pscustomobject]@{ Action = "install-local"; Label = "Install development local" },
            [pscustomobject]@{ Action = "install-copy"; Label = "Install production copy" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall $SkillName (not installed)" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }
    elseif ($state.Mode -eq "unknown install") {
        $options = @(
            [pscustomobject]@{ Action = "install-local"; Label = "Install development local" },
            [pscustomobject]@{ Action = "install-copy"; Label = "Install production copy" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall unknown install" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }
    else {
        $targetMode = if ($state.IsDevLocal) { "production copy" } else { "development local" }
        $targetAction = if ($state.IsDevLocal) { "install-copy" } else { "install-local" }
        $options = @(
            [pscustomobject]@{ Action = "update-current"; Label = "Update $($state.Mode)" },
            [pscustomobject]@{ Action = $targetAction; Label = "Install $targetMode" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall $($state.Mode)" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }

    $selection = Select-MenuItem -Options $options -Prompt "Choose an action for ${SkillName}:"
    Write-Host "Selected: $($selection.Label)"
    Write-Host ""

    switch ($selection.Action) {
        "cancel" {
            Write-Host "No changes made."
            return
        }
        "uninstall" {
            if (-not $state.Exists) {
                Write-Host "$SkillName is not installed."
                return
            }
            Remove-CurrentInstall -State $state
            Write-Host ""
            Write-Host "Uninstalled $SkillName." -ForegroundColor Green
            return
        }
        "install-local" {
            Remove-CurrentInstall -State $state
            Install-DevelopmentLocal -SkillPath $skillPath -SkillSource $skillSource
            Write-Host ""
            Write-Host "Installed $SkillName as development local." -ForegroundColor Green
        }
        "install-copy" {
            Remove-CurrentInstall -State $state
            Install-ProductionCopy -SkillPath $skillPath -SkillSource $skillSource
            Write-Host ""
            Write-Host "Installed $SkillName as production copy." -ForegroundColor Green
        }
        "update-current" {
            if (-not $state.Exists) {
                Write-Host "$SkillName is not installed."
                return
            }

            if ($state.IsDevLocal) {
                Remove-CurrentInstall -State $state
                Install-DevelopmentLocal -SkillPath $skillPath -SkillSource $skillSource
                Write-Host ""
                Write-Host "Updated $SkillName as development local." -ForegroundColor Green
            }
            elseif ($state.IsProductionCopy) {
                Remove-CurrentInstall -State $state
                Install-ProductionCopy -SkillPath $skillPath -SkillSource $skillSource
                Write-Host ""
                Write-Host "Updated $SkillName as production copy." -ForegroundColor Green
            }
            else {
                throw "Cannot update unknown install. Choose an install option to replace it, or uninstall it first."
            }
        }
        default {
            throw "Unknown action: $($selection.Action)"
        }
    }

    Write-Host ""
    Write-Host "Skill folder: $(Format-FolderLink $skillPath)"
    Write-Host "Restart OpenCode or open a fresh session before testing $SkillName."
}

$exitCode = 0
try {
    Invoke-Main
}
catch {
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    $exitCode = 1
}
finally {
    Pause-BeforeExit
}

exit $exitCode
