param(
    [ValidateSet("init", "refresh", "status", "cancel")]
    [string]$Action
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false
}

# Get-NormalizedPath and Select-MenuItem live in lib/common.ps1 (shared with
# manage-codex-plugin.ps1).
. (Join-Path (Join-Path $PSScriptRoot 'lib') 'common.ps1')

function Pause-BeforeExit {
    if (-not [string]::IsNullOrWhiteSpace($script:Action)) {
        return
    }
    if ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected) {
        return
    }

    Write-Host ""
    Read-Host "Press Enter to exit" | Out-Null
}

function Get-CacheState {
    param([Parameter(Mandatory = $true)][string]$CacheRoot)

    $manifestPath = Join-Path $CacheRoot "manifest.json"
    $manifest = $null
    if (Test-Path -LiteralPath $manifestPath) {
        $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    }

    [pscustomobject]@{
        CacheRoot = $CacheRoot
        ManifestPath = $manifestPath
        IsInitialized = $null -ne $manifest
        Manifest = $manifest
    }
}

function Write-CacheState {
    param([Parameter(Mandatory = $true)]$State)

    Write-Host "Cache root: $($State.CacheRoot)"
    if (-not $State.IsInitialized) {
        Write-Host "Status:     not initialized"
        return
    }

    Write-Host "Status:     initialized"
    Write-Host "Created:    $($State.Manifest.created_at)"
    Write-Host "Sources:    $($State.Manifest.source_count)"
    if ($State.Manifest.PSObject.Properties.Name -contains "last_refreshed_at") {
        Write-Host "Refreshed:  $($State.Manifest.last_refreshed_at)"
    }
    if ($State.Manifest.PSObject.Properties.Name -contains "last_change_detected") {
        Write-Host "Changed:    $($State.Manifest.last_change_detected)"
    }
    if ($State.Manifest.PSObject.Properties.Name -contains "last_refresh_had_failures") {
        Write-Host "Failures:   $($State.Manifest.last_refresh_had_failures)"
    }
    if ($State.Manifest.PSObject.Properties.Name -contains "last_report") {
        Write-Host "Report:     $($State.Manifest.last_report)"
    }
}

function Test-JsonProperty {
    param(
        [Parameter(Mandatory = $true)]$Object,
        [Parameter(Mandatory = $true)][string]$Name
    )

    return $Object.PSObject.Properties.Name -contains $Name
}

function Get-LatestCacheCompleteness {
    param([Parameter(Mandatory = $true)][string]$CacheRoot)

    $sourcesPath = Join-Path $CacheRoot "sources.json"
    $missing = @()
    if (-not (Test-Path -LiteralPath $sourcesPath)) {
        return [pscustomobject]@{
            IsComplete = $false
            Missing = @("sources.json")
        }
    }

    $sources = Get-Content -LiteralPath $sourcesPath -Raw | ConvertFrom-Json
    foreach ($source in $sources) {
        $rawPath = Join-Path $CacheRoot "latest\raw\$($source.raw_name)"
        $normalizedPath = Join-Path $CacheRoot "latest\normalized\$($source.id).json"
        if (-not (Test-Path -LiteralPath $rawPath)) {
            $missing += "latest/raw/$($source.raw_name)"
        }
        if (-not (Test-Path -LiteralPath $normalizedPath)) {
            $missing += "latest/normalized/$($source.id).json"
        }
    }

    [pscustomobject]@{
        IsComplete = $missing.Count -eq 0
        Missing = $missing
    }
}

function Write-StatusGuidance {
    param(
        [Parameter(Mandatory = $true)][string]$CacheRoot,
        [Parameter(Mandatory = $true)]$State
    )

    Write-Host ""
    Write-Host "Status guidance:" -ForegroundColor Cyan

    if (-not $State.IsInitialized) {
        Write-Host "- Cache is not initialized. Choose init, or choose refresh to initialize and fetch docs in one step."
        return
    }

    $manifest = $State.Manifest
    $completeness = Get-LatestCacheCompleteness -CacheRoot $CacheRoot
    if (-not $completeness.IsComplete) {
        Write-Host "- Cache is incomplete. Choose refresh before using it for PixelLab routing or Skill updates." -ForegroundColor Yellow
        foreach ($missingPath in $completeness.Missing | Select-Object -First 6) {
            Write-Host "  Missing: $missingPath"
        }
        if ($completeness.Missing.Count -gt 6) {
            Write-Host "  Missing: ...and $($completeness.Missing.Count - 6) more."
        }
        return
    }

    if (-not (Test-JsonProperty -Object $manifest -Name "last_refreshed_at")) {
        Write-Host "- Cache has been initialized but not refreshed yet. Choose refresh to download the current PixelLab docs." -ForegroundColor Yellow
        return
    }

    $staleDays = $null
    $refreshedAt = [datetime]::MinValue
    if ([datetime]::TryParse($manifest.last_refreshed_at, [ref]$refreshedAt)) {
        $age = [datetime]::UtcNow - $refreshedAt.ToUniversalTime()
        if ($age.TotalDays -ge 7) {
            $staleDays = [math]::Floor($age.TotalDays)
        }
    }

    if ((Test-JsonProperty -Object $manifest -Name "last_refresh_had_failures") -and $manifest.last_refresh_had_failures) {
        Write-Host "- Last refresh was partial. Choose refresh again; do not update routing claims from a failed source unless that source fetched and parsed successfully." -ForegroundColor Yellow
        if (Test-JsonProperty -Object $manifest -Name "last_report") {
            $reportPath = $manifest.last_report -replace '\\', '/'
            Write-Host "- Review the partial report: .local/pixellab-doc-watch/$reportPath"
        }
        return
    }

    if ((Test-JsonProperty -Object $manifest -Name "last_refresh_initialized_sources") -and $manifest.last_refresh_initialized_sources -and (-not (Test-JsonProperty -Object $manifest -Name "last_change_detected") -or -not $manifest.last_change_detected)) {
        Write-Host "- Last refresh initialized the local baseline. No prior cache existed for one or more sources, so this is not documentation drift."
        if (Test-JsonProperty -Object $manifest -Name "last_report") {
            $reportPath = $manifest.last_report -replace '\\', '/'
            Write-Host "- Baseline report: .local/pixellab-doc-watch/$reportPath"
        }
        if ($null -ne $staleDays) {
            Write-Host "- Cache is complete, but it is $staleDays days old. Choose refresh before making current PixelLab endpoint or MCP-tool claims." -ForegroundColor Yellow
        }
        return
    }

    if ((Test-JsonProperty -Object $manifest -Name "last_change_detected") -and $manifest.last_change_detected) {
        Write-Host "- Last successful refresh detected skill-relevant PixelLab documentation drift." -ForegroundColor Yellow
        if (Test-JsonProperty -Object $manifest -Name "last_report") {
            $reportPath = $manifest.last_report -replace '\\', '/'
            Write-Host "- Open the report and review the Agent Skill impact checklist: .local/pixellab-doc-watch/$reportPath"
        }
        Write-Host "- Update only the affected Skill/docs files, then refresh again when you want to confirm the current upstream state."
        return
    }

    if ($null -ne $staleDays) {
        Write-Host "- Cache is complete, but it is $staleDays days old. Choose refresh before making current PixelLab endpoint or MCP-tool claims." -ForegroundColor Yellow
        return
    }

    Write-Host "- Cache is complete and the last refresh found no skill-relevant drift."
    if (Test-JsonProperty -Object $manifest -Name "last_report") {
        $reportPath = $manifest.last_report -replace '\\', '/'
        Write-Host "- Latest report: .local/pixellab-doc-watch/$reportPath"
    }
}

function Find-PythonCommand {
    foreach ($candidate in @("py", "python")) {
        if (-not (Get-Command $candidate -ErrorAction SilentlyContinue)) {
            continue
        }
        $output = & $candidate --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return $candidate
        }
    }

    throw "Could not find python or py on PATH."
}

function Invoke-DocWatch {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [int[]]$AllowedExitCodes = @(0)
    )

    $watchScript = Join-Path $RepoRoot "dev-tools\pixellab-doc-watch.py"
    if (-not (Test-Path -LiteralPath $watchScript)) {
        throw "Could not find watcher script: $watchScript"
    }

    $pythonCommand = Find-PythonCommand
    Write-Host "> $pythonCommand dev-tools/pixellab-doc-watch.py $($Arguments -join ' ')" -ForegroundColor DarkGray

    Push-Location -LiteralPath $RepoRoot
    try {
        & $pythonCommand $watchScript @Arguments
        $exitCode = $LASTEXITCODE
    }
    finally {
        Pop-Location
    }
    $script:LastDocWatchExitCode = $exitCode

    if ($AllowedExitCodes -notcontains $exitCode) {
        throw "pixellab-doc-watch.py failed with exit code $exitCode"
    }

    return $exitCode
}

function Invoke-Main {
    $scriptDir = Split-Path -Parent $PSCommandPath
    $repoRoot = Get-NormalizedPath (Split-Path -Parent $scriptDir)
    $cacheRoot = Join-Path $repoRoot ".local\pixellab-doc-watch"

    Write-Host "Repo root:  $repoRoot"
    Write-Host ""

    $state = Get-CacheState -CacheRoot $cacheRoot
    Write-CacheState -State $state
    Write-Host ""

    if ([string]::IsNullOrWhiteSpace($script:Action)) {
        if ($state.IsInitialized) {
            $options = @(
                [pscustomobject]@{ Action = "refresh"; Label = "Refresh and compare docs" },
                [pscustomobject]@{ Action = "status"; Label = "Show cache status" },
                [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
            )
        }
        else {
            $options = @(
                [pscustomobject]@{ Action = "init"; Label = "Initialize local docs cache" },
                [pscustomobject]@{ Action = "refresh"; Label = "Refresh and compare docs (auto-initializes)" },
                [pscustomobject]@{ Action = "cancel"; Label = "Cancel" }
            )
        }

        $selection = Select-MenuItem -Options $options -Prompt "Choose a PixelLab docs cache action:"
    }
    else {
        $selection = [pscustomobject]@{ Action = $script:Action; Label = $script:Action }
    }
    Write-Host "Selected: $($selection.Label)"
    Write-Host ""

    switch ($selection.Action) {
        "cancel" {
            Write-Host "No changes made."
            return
        }
        "init" {
            if ($state.IsInitialized) {
                Write-Host "Local PixelLab docs cache is already initialized; syncing cache metadata and sources."
            }
            $script:ProcessExitCode = Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("init")
            Write-Host ""
            Write-Host "Initialized or updated local PixelLab docs cache." -ForegroundColor Green
        }
        "refresh" {
            $watchExitCode = Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("refresh") -AllowedExitCodes @(0, 1, 2, 3)
            $script:ProcessExitCode = $watchExitCode
            Write-Host ""
            if ($watchExitCode -eq 1) {
                Write-Host "Refresh completed with source failures. Run status to see the partial report path." -ForegroundColor Yellow
            }
            elseif ($watchExitCode -eq 2) {
                Write-Host "Refresh completed and detected documentation changes. Run status to see the latest report path." -ForegroundColor Yellow
            }
            elseif ($watchExitCode -eq 3) {
                Write-Host "Refresh detected documentation changes, but one or more sources failed. Run status to see the partial report path." -ForegroundColor Yellow
            }
            else {
                Write-Host "Refresh complete. Run status to see the latest report path." -ForegroundColor Green
            }
        }
        "status" {
            $watchExitCode = Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("status") -AllowedExitCodes @(0, 1)
            $script:ProcessExitCode = $watchExitCode
            $state = Get-CacheState -CacheRoot $cacheRoot
            Write-StatusGuidance -CacheRoot $cacheRoot -State $state
        }
        default {
            throw "Unknown action: $($selection.Action)"
        }
    }
}

$script:ProcessExitCode = 0
try {
    Invoke-Main
}
catch {
    Write-Host ""
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    $script:ProcessExitCode = 1
}
finally {
    Pause-BeforeExit
}

exit $script:ProcessExitCode
