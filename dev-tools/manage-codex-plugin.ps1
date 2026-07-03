[CmdletBinding()]
param(
    [switch]$Help
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Show-Usage {
    Write-Host "Usage: powershell -NoProfile -File dev-tools\manage-codex-plugin.ps1 [-Help]"
    Write-Host ""
    Write-Host "Refresh the local Codex install for this plugin or switch between development and production installs."
    Write-Host "Interactive menu actions can install, update, or uninstall the plugin."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -Help    Show this help and exit without changing Codex plugin state."
}

function Get-NormalizedPath {
    param([AllowNull()][string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        return $null
    }

    $cleanPath = $Path -replace '^\\\\\?\\', ''
    try {
        return [System.IO.Path]::GetFullPath($cleanPath).TrimEnd('\', '/')
    }
    catch {
        return $cleanPath.TrimEnd('\', '/')
    }
}

function Invoke-Codex {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,

        [switch]$Json
    )

    Write-Host "> codex $($Arguments -join ' ')" -ForegroundColor DarkGray
    $stderrPath = [System.IO.Path]::GetTempFileName()
    try {
        $output = & codex @Arguments 2> $stderrPath
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
        throw "codex command failed with exit code $exitCode"
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

function Get-CodexCachePath {
    param(
        [Parameter(Mandatory = $true)][string]$MarketplaceName,
        [Parameter(Mandatory = $true)][string]$PluginName,
        [Parameter(Mandatory = $true)][string]$Version
    )

    return Join-Path $env:USERPROFILE ".codex\plugins\cache\$MarketplaceName\$PluginName\$Version"
}

function Get-CachebusterVersion {
    param([Parameter(Mandatory = $true)][string]$Version)

    $baseVersion = $Version.Split("+", 2)[0]
    $stamp = [DateTime]::UtcNow.ToString("yyyyMMddHHmmss")
    return "$baseVersion+codex.dev-$stamp"
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

    $codexManifestPath = Join-Path $RepoRoot ".codex-plugin\plugin.json"
    if (-not (Test-Path -LiteralPath $codexManifestPath)) {
        throw "Could not find Codex plugin manifest: $codexManifestPath"
    }

    $originalManifestText = Get-Content -LiteralPath $codexManifestPath -Raw
    try {
        $codexManifest = $originalManifestText | ConvertFrom-Json
        $codexManifest.version = Get-CachebusterVersion -Version ([string]$codexManifest.version)
        $nextManifestText = ($codexManifest | ConvertTo-Json -Depth 50) + [Environment]::NewLine
        Write-Utf8NoBom -Path $codexManifestPath -Text $nextManifestText

        Write-Host "  Cachebuster: $($codexManifest.version)"
        Invoke-Codex -Arguments @("plugin", "marketplace", "add", $RepoRoot, "--json") -Json | Out-Null
        Invoke-Codex -Arguments @("plugin", "add", $PluginSelector, "--json") -Json | Out-Null
    }
    finally {
        Write-Utf8NoBom -Path $codexManifestPath -Text $originalManifestText
    }
}

function Install-ProductionRemote {
    param(
        [Parameter(Mandatory = $true)][string]$RemoteSource,
        [Parameter(Mandatory = $true)][string]$PluginSelector
    )

    Invoke-Codex -Arguments @("plugin", "marketplace", "add", $RemoteSource, "--json") -Json | Out-Null
    Invoke-Codex -Arguments @("plugin", "add", $PluginSelector, "--json") -Json | Out-Null
}

function Remove-CurrentInstall {
    param(
        [AllowNull()]$InstalledPlugin,
        [AllowNull()]$InstalledMarketplace
    )

    if ($InstalledPlugin) {
        Invoke-Codex -Arguments @("plugin", "remove", $InstalledPlugin.pluginId, "--json") -Json | Out-Null
    }

    if ($InstalledMarketplace) {
        Invoke-Codex -Arguments @("plugin", "marketplace", "remove", $InstalledMarketplace.name, "--json") -Json | Out-Null
    }
}

function Select-MenuItem {
    param(
        [Parameter(Mandatory = $true)][object[]]$Options,
        [Parameter(Mandatory = $true)][string]$Prompt
    )

    if ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
        Write-Host $Prompt
        for ($i = 0; $i -lt $Options.Count; $i++) {
            Write-Host "  $($i + 1). $($Options[$i].Label)"
        }
        $answer = Read-Host "Choose 1-$($Options.Count)"
        if ([string]::IsNullOrWhiteSpace($answer)) {
            return $Options[$Options.Count - 1]
        }
        if ($answer -match '^\d+$') {
            $index = [int]$answer - 1
            if ($index -ge 0 -and $index -lt $Options.Count) {
                return $Options[$index]
            }
        }
        return $Options[$Options.Count - 1]
    }

    Write-Host $Prompt
    Write-Host "Use Up/Down, Enter to select, or 1-$($Options.Count)."
    $selected = 0
    $startTop = [Console]::CursorTop

    while ($true) {
        [Console]::SetCursorPosition(0, $startTop)
        for ($i = 0; $i -lt $Options.Count; $i++) {
            $prefix = if ($i -eq $selected) { "> " } else { "  " }
            $line = "$prefix$($i + 1). $($Options[$i].Label)"
            $width = [Math]::Max(1, [Console]::WindowWidth - 1)
            if ($line.Length -gt $width) {
                $line = $line.Substring(0, $width)
            }
            else {
                $line = $line.PadRight($width)
            }

            if ($i -eq $selected) {
                Write-Host $line -ForegroundColor Black -BackgroundColor Gray
            }
            else {
                Write-Host $line
            }
        }

        $key = [Console]::ReadKey($true)
        switch ($key.Key) {
            "UpArrow" {
                $selected = ($selected + $Options.Count - 1) % $Options.Count
            }
            "DownArrow" {
                $selected = ($selected + 1) % $Options.Count
            }
            "Enter" {
                Write-Host ""
                return $Options[$selected]
            }
            "Escape" {
                Write-Host ""
                return $Options[$Options.Count - 1]
            }
            default {
                $digit = $key.KeyChar.ToString()
                if ($digit -match '^\d$') {
                    $index = [int]$digit - 1
                    if ($index -ge 0 -and $index -lt $Options.Count) {
                        Write-Host ""
                        return $Options[$index]
                    }
                }
            }
        }
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
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string]$RemoteSource
    )

    $pluginList = Invoke-Codex -Arguments @("plugin", "list", "--json") -Json
    $installedPlugin = @($pluginList.installed) |
        Where-Object { $_.name -eq $PluginName -or $_.pluginId -eq $PluginSelector } |
        Select-Object -First 1

    $marketplaceList = Invoke-Codex -Arguments @("plugin", "marketplace", "list", "--json") -Json
    $installedMarketplace = @($marketplaceList.marketplaces) |
        Where-Object { $_.name -eq $PluginName } |
        Select-Object -First 1

    $installedPath = $null
    $marketplacePath = $null
    $installedVersion = $null

    if ((Test-JsonProperty -Object $installedPlugin -Name "source") -and
        (Test-JsonProperty -Object $installedPlugin.source -Name "path")) {
        $installedPath = Get-NormalizedPath ([string]$installedPlugin.source.path)
    }

    if ($installedPlugin) {
        $installedVersion = [string]$installedPlugin.version
    }

    if ((Test-JsonProperty -Object $installedMarketplace -Name "marketplaceSource") -and
        $installedMarketplace.marketplaceSource.sourceType -eq "local") {
        $marketplacePath = Get-NormalizedPath ([string]$installedMarketplace.marketplaceSource.source)
    }

    $isLocalSource = ($installedPath -eq $RepoRoot) -or ($marketplacePath -eq $RepoRoot)
    $hasCachebuster = $installedVersion -match '\+codex\.'
    $isLocalDev = $isLocalSource -and $hasCachebuster
    $isStaleLocalDev = $isLocalSource -and -not $hasCachebuster
    $isProductionRemote = $false
    if ((Test-JsonProperty -Object $installedMarketplace -Name "marketplaceSource") -and
        $installedMarketplace.marketplaceSource.sourceType -eq "git") {
        $installedRemoteSource = Get-RepositorySource -Repository ([string]$installedMarketplace.marketplaceSource.source)
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
        InstalledPath = $installedPath
        MarketplacePath = $marketplacePath
        Version = $installedVersion
        Mode = $mode
        IsLocal = $isLocalDev -or $isStaleLocalDev
        IsProductionRemote = $isProductionRemote
    }
}

function Write-InstallState {
    param(
        [Parameter(Mandatory = $true)]$State,
        [Parameter(Mandatory = $true)][string]$PluginName
    )

    if ($State.Plugin) {
        Write-Host "Current install:"
        Write-Host "  Plugin ID:   $($State.Plugin.pluginId)"
        Write-Host "  Version:     $($State.Plugin.version)"
        if ($State.Version) {
            $cachePath = Get-CodexCachePath -MarketplaceName $State.Plugin.marketplaceName -PluginName $PluginName -Version $State.Version
            Write-Host "  Cache path:  $cachePath"
        }
        if ($State.InstalledPath) {
            Write-Host "  Source path: $($State.InstalledPath)"
        }
        else {
            Write-Host "  Source path: (not local path)"
        }
    }
    else {
        Write-Host "Current install: not installed"
    }

    if ($State.Marketplace) {
        $marketplaceSource = if (Test-JsonProperty -Object $State.Marketplace -Name "marketplaceSource") {
            "$($State.Marketplace.marketplaceSource.sourceType): $($State.Marketplace.marketplaceSource.source)"
        }
        else {
            $State.Marketplace.root
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
    $manifestPath = Join-Path $repoRoot "plugin.json"

    if (-not (Test-Path -LiteralPath $manifestPath)) {
        throw "Could not find plugin.json next to repo root: $repoRoot"
    }

    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    $pluginName = [string]$manifest.name
    $repository = [string]$manifest.repository

    if ([string]::IsNullOrWhiteSpace($pluginName)) {
        throw "plugin.json must include a name."
    }

    if ([string]::IsNullOrWhiteSpace($repository)) {
        throw "plugin.json must include a repository URL for production remote installs."
    }

    $pluginSelector = "$pluginName@$pluginName"
    $remoteSource = Get-RepositorySource -Repository $repository

    Write-Host "Repo root: $repoRoot"
    Write-Host "Plugin:   $pluginName"
    Write-Host ""

    $state = Get-InstallState -PluginName $pluginName -PluginSelector $pluginSelector -RepoRoot $repoRoot -RemoteSource $remoteSource
    Write-InstallState -State $state -PluginName $pluginName
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
                if ($state.Marketplace -and
                    (Test-JsonProperty -Object $state.Marketplace -Name "marketplaceSource") -and
                    $state.Marketplace.marketplaceSource.sourceType -eq "git") {
                    Invoke-Codex -Arguments @("plugin", "marketplace", "upgrade", $state.Marketplace.name, "--json") -Json | Out-Null
                }
                Remove-CurrentInstall -InstalledPlugin $state.Plugin -InstalledMarketplace $state.Marketplace
                Install-ProductionRemote -RemoteSource $remoteSource -PluginSelector $pluginSelector
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

    Write-Host "Restart Codex or open a fresh thread before testing @$pluginName."
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
