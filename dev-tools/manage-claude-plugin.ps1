[CmdletBinding()]
param(
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

# Get-NormalizedPath and Select-MenuItem live in common.ps1 (shared with
# manage-codex-plugin.ps1 and manage-pixellab-doc-cache.ps1).
. (Join-Path $PSScriptRoot 'common.ps1')

function Show-Usage {
    Write-Host "Usage: powershell -NoProfile -File dev-tools\manage-claude-plugin.ps1 [-Help]"
    Write-Host ""
    Write-Host "Refresh the local Claude Code install for this plugin or switch between development and production installs."
    Write-Host "Interactive menu actions can install, update, or uninstall the plugin."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Help    Show this help and exit without changing Claude Code plugin state."
}

# Only `claude plugin list` and `claude plugin marketplace list` support --json;
# every mutating subcommand prints plain text, so -Json is used for the two list calls only.
function Invoke-Claude {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [switch]$Json
    )

    Write-Host "> claude $($Arguments -join ' ')" -ForegroundColor DarkGray
    $stderrPath = [System.IO.Path]::GetTempFileName()
    try {
        $output = & claude @Arguments 2> $stderrPath
        $exitCode = $LASTEXITCODE
        $text = ($output | Out-String).Trim()
        $rawErrorText = if (Test-Path -LiteralPath $stderrPath) {
            Get-Content -LiteralPath $stderrPath -Raw
        }
        else {
            ""
        }
        $errorText = if ($null -eq $rawErrorText) { "" } else { $rawErrorText.Trim() }
    }
    finally {
        if (Test-Path -LiteralPath $stderrPath) {
            Remove-Item -LiteralPath $stderrPath -Force -ErrorAction SilentlyContinue
        }
    }

    if ($exitCode -ne 0) {
        if ($text) {
            Write-Host $text
        }
        if ($errorText) {
            Write-Host $errorText
        }
        throw "claude command failed with exit code $exitCode"
    }

    if ($Json) {
        if ([string]::IsNullOrWhiteSpace($text)) {
            return $null
        }
        return $text | ConvertFrom-Json
    }

    return $text
}

function Get-RepositorySource {
    param([Parameter(Mandatory = $true)][string]$Repository)

    if ($Repository -match 'github\.com[:/]([^/]+)/([^/.]+)(?:\.git)?/?$') {
        return "$($Matches[1])/$($Matches[2])"
    }

    return $Repository
}

function Get-CachebusterVersion {
    param([Parameter(Mandatory = $true)][string]$Version)

    # Claude Code copies each plugin into a per-version cache dir and keys update
    # detection on the resolved version (plugin.json version wins over the
    # marketplace entry and the git SHA), so a unique build-metadata suffix forces
    # a fresh copy of local edits. Mirrors the Codex dev-install cachebuster.
    $baseVersion = $Version.Split("+", 2)[0]
    $stamp = [DateTime]::UtcNow.ToString("yyyyMMddHHmmss")
    return "$baseVersion+claude.dev-$stamp"
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)][string]$Text
    )

    $encoding = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Text, $encoding)
}

function Test-JsonProperty {
    param(
        [AllowNull()]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )

    return $null -ne $Object -and $Object.PSObject.Properties.Name -contains $Name
}

function Install-DevelopmentLocal {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$PluginSelector
    )

    $claudeManifestPath = Join-Path $RepoRoot ".claude-plugin\plugin.json"
    if (-not (Test-Path -LiteralPath $claudeManifestPath)) {
        throw "Could not find Claude plugin manifest: $claudeManifestPath"
    }

    $originalManifestText = Get-Content -LiteralPath $claudeManifestPath -Raw
    try {
        $claudeManifest = $originalManifestText | ConvertFrom-Json
        $claudeManifest.version = Get-CachebusterVersion -Version ([string]$claudeManifest.version)
        $nextManifestText = ($claudeManifest | ConvertTo-Json -Depth 50) + [Environment]::NewLine
        Write-Utf8NoBom -Path $claudeManifestPath -Text $nextManifestText

        Write-Host "  Cachebuster: $($claudeManifest.version)"
        Invoke-Claude -Arguments @("plugin", "marketplace", "add", $RepoRoot) | Out-Null
        Invoke-Claude -Arguments @("plugin", "install", $PluginSelector) | Out-Null
    }
    finally {
        Write-Utf8NoBom -Path $claudeManifestPath -Text $originalManifestText
    }
}

function Install-ProductionRemote {
    param(
        [Parameter(Mandatory = $true)][string]$RemoteSource,
        [Parameter(Mandatory = $true)][string]$PluginSelector
    )

    Invoke-Claude -Arguments @("plugin", "marketplace", "add", $RemoteSource) | Out-Null
    Invoke-Claude -Arguments @("plugin", "install", $PluginSelector) | Out-Null
}

function Remove-CurrentInstall {
    param(
        [AllowNull()]$InstalledPlugin,
        [AllowNull()]$InstalledMarketplace
    )

    if ($InstalledPlugin) {
        Invoke-Claude -Arguments @("plugin", "uninstall", $InstalledPlugin.id) | Out-Null
    }

    if ($InstalledMarketplace) {
        Invoke-Claude -Arguments @("plugin", "marketplace", "remove", $InstalledMarketplace.name) | Out-Null
    }
}

function Pause-BeforeExit {
    if ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
        return
    }

    Write-Host ""
    Read-Host "Press Enter to exit" | Out-Null
}

function Get-InstallState {
    param(
        [Parameter(Mandatory = $true)][string]$PluginName,
        [Parameter(Mandatory = $true)][string]$PluginSelector,
        [Parameter(Mandatory = $true)][string]$RemoteSource
    )

    $pluginList = Invoke-Claude -Arguments @("plugin", "list", "--json") -Json
    $installedPlugin = @($pluginList) |
        Where-Object { $_.id -eq $PluginSelector } |
        Select-Object -First 1

    $marketplaceList = Invoke-Claude -Arguments @("plugin", "marketplace", "list", "--json") -Json
    $installedMarketplace = @($marketplaceList) |
        Where-Object { $_.name -eq $PluginName } |
        Select-Object -First 1

    $installedVersion = if ($installedPlugin) { [string]$installedPlugin.version } else { $null }

    $isLocalSource = (Test-JsonProperty -Object $installedMarketplace -Name "source") -and
        $installedMarketplace.source -eq "directory"
    $hasCachebuster = $installedVersion -match '\+claude\.'
    $isLocalDev = $isLocalSource -and $hasCachebuster
    $isStaleLocalDev = $isLocalSource -and -not $hasCachebuster

    $isProductionRemote = $false
    if ((Test-JsonProperty -Object $installedMarketplace -Name "source") -and
        $installedMarketplace.source -eq "github" -and
        (Test-JsonProperty -Object $installedMarketplace -Name "repo")) {
        $installedRemoteSource = Get-RepositorySource -Repository ([string]$installedMarketplace.repo)
        $isProductionRemote = $installedRemoteSource -eq $RemoteSource
    }

    $mode = if (-not $installedPlugin) {
        "not installed"
    }
    elseif ($isLocalDev) {
        "development local"
    }
    elseif ($isStaleLocalDev) {
        "development local (stale cache)"
    }
    elseif ($isProductionRemote) {
        "production remote"
    }
    else {
        "unknown install"
    }

    [pscustomobject]@{
        Plugin = $installedPlugin
        Marketplace = $installedMarketplace
        Version = $installedVersion
        Mode = $mode
        IsLocal = $isLocalDev -or $isStaleLocalDev
        IsProductionRemote = $isProductionRemote
    }
}

function Write-InstallState {
    param(
        [Parameter(Mandatory = $true)]$State
    )

    if ($State.Plugin) {
        Write-Host "Current install:"
        Write-Host "  Plugin ID:   $($State.Plugin.id)"
        Write-Host "  Version:     $($State.Plugin.version)"
        Write-Host "  Enabled:     $($State.Plugin.enabled)"
        Write-Host "  Scope:       $($State.Plugin.scope)"
        if (Test-JsonProperty -Object $State.Plugin -Name "installPath") {
            Write-Host "  Cache path:  $($State.Plugin.installPath)"
        }
    }
    else {
        Write-Host "Current install: not installed"
    }

    if ($State.Marketplace) {
        $marketplaceSource = if ($State.Marketplace.source -eq "directory") {
            "directory: $($State.Marketplace.path)"
        }
        elseif ($State.Marketplace.source -eq "github") {
            "github: $($State.Marketplace.repo)"
        }
        else {
            [string]$State.Marketplace.source
        }
        Write-Host "  Marketplace: $marketplaceSource"
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
    $manifestPath = Join-Path $repoRoot ".claude-plugin\plugin.json"

    if (-not (Test-Path -LiteralPath $manifestPath)) {
        throw "Could not find .claude-plugin\plugin.json under repo root: $repoRoot"
    }

    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $pluginName = [string]$manifest.name
    $repository = [string]$manifest.repository

    if ([string]::IsNullOrWhiteSpace($pluginName)) {
        throw ".claude-plugin\plugin.json must include a name."
    }

    if ([string]::IsNullOrWhiteSpace($repository)) {
        throw ".claude-plugin\plugin.json must include a repository URL for production remote installs."
    }

    # Marketplace name comes from .claude-plugin/marketplace.json; for this repo it
    # matches the plugin name, so the selector is pluginName@pluginName either way.
    $pluginSelector = "$pluginName@$pluginName"
    $remoteSource = Get-RepositorySource -Repository $repository

    Write-Host "Repo root: $repoRoot"
    Write-Host "Plugin:   $pluginName"
    Write-Host ""

    $state = Get-InstallState -PluginName $pluginName -PluginSelector $pluginSelector -RemoteSource $remoteSource
    Write-InstallState -State $state
    Write-Host ""

    if ($state.Mode -eq "not installed") {
        $options = @(
            [pscustomobject]@{ Action = "install-local"; Label = "Install development local" },
            [pscustomobject]@{ Action = "install-remote"; Label = "Install production remote" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall $pluginName (not installed)" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }
    elseif ($state.Mode -eq "unknown install") {
        $options = @(
            [pscustomobject]@{ Action = "install-local"; Label = "Install development local" },
            [pscustomobject]@{ Action = "install-remote"; Label = "Install production remote" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall unknown install" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }
    else {
        $targetMode = if ($state.IsLocal) { "production remote" } else { "development local" }
        $targetAction = if ($state.IsLocal) { "install-remote" } else { "install-local" }
        $options = @(
            [pscustomobject]@{ Action = "update-current"; Label = "Update $($state.Mode)" },
            [pscustomobject]@{ Action = $targetAction; Label = "Install $targetMode" },
            [pscustomobject]@{ Action = "uninstall"; Label = "Uninstall $($state.Mode)" },
            [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
        )
    }

    $selection = Select-MenuItem -Options $options -Prompt "Choose an action for ${pluginName}:"
    Write-Host "Selected: $($selection.Label)"
    Write-Host ""

    switch ($selection.Action) {
        "cancel" {
            Write-Host "No changes made."
            return
        }
        "uninstall" {
            if (-not $state.Plugin -and -not $state.Marketplace) {
                Write-Host "$pluginName is not installed."
                return
            }
            Remove-CurrentInstall -InstalledPlugin $state.Plugin -InstalledMarketplace $state.Marketplace
            Write-Host ""
            Write-Host "Uninstalled $pluginName." -ForegroundColor Green
            return
        }
        "install-local" {
            Remove-CurrentInstall -InstalledPlugin $state.Plugin -InstalledMarketplace $state.Marketplace
            Install-DevelopmentLocal -RepoRoot $repoRoot -PluginSelector $pluginSelector
            Write-Host ""
            Write-Host "Installed $pluginName as development local." -ForegroundColor Green
        }
        "install-remote" {
            Remove-CurrentInstall -InstalledPlugin $state.Plugin -InstalledMarketplace $state.Marketplace
            Install-ProductionRemote -RemoteSource $remoteSource -PluginSelector $pluginSelector
            Write-Host ""
            Write-Host "Installed $pluginName as production remote." -ForegroundColor Green
        }
        "update-current" {
            if (-not $state.Plugin) {
                Write-Host "$pluginName is not installed."
                return
            }

            if ($state.IsLocal) {
                Remove-CurrentInstall -InstalledPlugin $state.Plugin -InstalledMarketplace $state.Marketplace
                Install-DevelopmentLocal -RepoRoot $repoRoot -PluginSelector $pluginSelector
                Write-Host ""
                Write-Host "Updated $pluginName as development local." -ForegroundColor Green
            }
            elseif ($state.IsProductionRemote) {
                Invoke-Claude -Arguments @("plugin", "marketplace", "update", $state.Marketplace.name) | Out-Null
                Invoke-Claude -Arguments @("plugin", "update", $pluginSelector) | Out-Null
                Write-Host ""
                Write-Host "Updated $pluginName as production remote." -ForegroundColor Green
            }
            else {
                throw "Cannot update unknown install. Choose an install option to replace it, or uninstall it first."
            }
        }
        default {
            throw "Unknown action: $($selection.Action)"
        }
    }

    Write-Host "Restart Claude Code or run /reload-plugins before testing $pluginName."
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
