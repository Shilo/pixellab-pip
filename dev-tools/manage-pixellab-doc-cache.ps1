param(
    [ValidateSet("init", "refresh", "status", "cancel")]
    [string]$Action
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

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

    if ((Test-JsonProperty -Object $manifest -Name "last_refresh_had_failures") -and $manifest.last_refresh_had_failures) {
        Write-Host "- Last refresh was partial. Choose refresh again; do not update routing claims from a failed source unless that source fetched successfully." -ForegroundColor Yellow
        if (Test-JsonProperty -Object $manifest -Name "last_report") {
            $reportPath = $manifest.last_report -replace '\\', '/'
            Write-Host "- Review the partial report: .local/pixellab-doc-watch/$reportPath"
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

    $refreshedAt = [datetime]::MinValue
    if ([datetime]::TryParse($manifest.last_refreshed_at, [ref]$refreshedAt)) {
        $age = [datetime]::UtcNow - $refreshedAt.ToUniversalTime()
        if ($age.TotalDays -ge 7) {
            Write-Host "- Cache is complete, but it is $([math]::Floor($age.TotalDays)) days old. Choose refresh before making current PixelLab endpoint or MCP-tool claims." -ForegroundColor Yellow
            return
        }
    }

    Write-Host "- Cache is complete and the last refresh found no skill-relevant drift."
    if (Test-JsonProperty -Object $manifest -Name "last_report") {
        $reportPath = $manifest.last_report -replace '\\', '/'
        Write-Host "- Latest report: .local/pixellab-doc-watch/$reportPath"
    }
}

function Find-PythonCommand {
    foreach ($candidate in @("python", "py")) {
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
        [Parameter(Mandatory = $true)][string[]]$Arguments
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

    if ($exitCode -eq 2) {
        Write-Host ""
        Write-Host "Refresh completed and detected documentation changes." -ForegroundColor Yellow
        return
    }

    if ($exitCode -ne 0) {
        throw "pixellab-doc-watch.py failed with exit code $exitCode"
    }
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
            Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("init")
            Write-Host ""
            Write-Host "Initialized or updated local PixelLab docs cache." -ForegroundColor Green
        }
        "refresh" {
            Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("refresh")
            Write-Host ""
            Write-Host "Refresh complete. Run status to see the latest report path." -ForegroundColor Green
        }
        "status" {
            Invoke-DocWatch -RepoRoot $repoRoot -Arguments @("status")
            $state = Get-CacheState -CacheRoot $cacheRoot
            Write-StatusGuidance -CacheRoot $cacheRoot -State $state
        }
        default {
            throw "Unknown action: $($selection.Action)"
        }
    }
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
