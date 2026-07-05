param(
    [ValidateSet("static", "dry-claude", "dry-all", "live-balance", "live-image", "list", "cancel")]
    [string]$Preset,
    [int]$Reps = 3
)

# Convenience launcher for dev-tools/skill_benchmark.py. It only assembles the
# documented flags for the common presets, runs preflight checks so a missing
# CLI or secret fails with a clear message, and points at the report folder.
# The benchmark itself lives in skill_benchmark.py; this adds no measurement logic.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false  # let python's own exit code surface
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$benchmark = Join-Path $repoRoot "dev-tools/skill_benchmark.py"
$interactive = -not ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected)

# preset -> { Args, NeedCli (agent exes that must be on PATH), NeedSecret, Paid }
$presets = [ordered]@{
    "static"       = @{ Label = "static      - free context-size comparison, no CLI calls, no secret"; Args = @("--static"); NeedCli = @(); NeedSecret = $false; Paid = $false }
    "dry-claude"   = @{ Label = "dry-claude  - claude only, dry scenarios ($Reps reps)"; Args = @("--agents", "claude", "--reps", "$Reps"); NeedCli = @("claude"); NeedSecret = $false; Paid = $false }
    "dry-all"      = @{ Label = "dry-all     - claude + codex + deepseek-v4-pro, dry scenarios ($Reps reps)"; Args = @("--agents", "claude,codex,deepseek-v4-pro", "--reps", "$Reps"); NeedCli = @("claude", "codex", "opencode"); NeedSecret = $false; Paid = $false }
    "live-balance" = @{ Label = "live-balance- claude + free GET /balance (needs PIXELLAB_SECRET)"; Args = @("--agents", "claude", "--live"); NeedCli = @("claude"); NeedSecret = $true; Paid = $false }
    "live-image"   = @{ Label = "live-image  - claude + PAID cheap generation (spends credits)"; Args = @("--agents", "claude", "--live", "--allow-paid"); NeedCli = @("claude"); NeedSecret = $true; Paid = $true }
    "list"         = @{ Label = "list        - print scenarios and exit"; Args = @("--list"); NeedCli = @(); NeedSecret = $false; Paid = $false }
}

if (-not $Preset) {
    if (-not $interactive) {
        Write-Host "Usage: run-skill-benchmark.ps1 -Preset <name> [-Reps N]"
        $presets.Keys | ForEach-Object { Write-Host "  $($presets[$_].Label)" }
        exit 2
    }
    Write-Host "PixelLab Pip skill benchmark"
    $keys = @($presets.Keys)
    for ($i = 0; $i -lt $keys.Count; $i++) { Write-Host "  $($i + 1). $($presets[$keys[$i]].Label)" }
    Write-Host "  $($keys.Count + 1). cancel"
    $answer = Read-Host "Choose 1-$($keys.Count + 1)"
    if ($answer -notmatch '^\d+$' -or [int]$answer -lt 1 -or [int]$answer -gt $keys.Count) {
        Write-Host "Cancelled."
        exit 0
    }
    $Preset = $keys[[int]$answer - 1]
}

if ($Preset -eq "cancel") { Write-Host "Cancelled."; exit 0 }

$config = $presets[$Preset]

# Preflight: python, required agent CLIs, and secret for live presets.
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python was not found on PATH."
    exit 1
}
$missing = @($config.NeedCli | Where-Object { -not (Get-Command $_ -ErrorAction SilentlyContinue) })
if ($missing.Count -gt 0) {
    Write-Warning "Missing agent CLI(s): $($missing -join ', '). The benchmark will skip cells it cannot run."
}
if ($config.NeedSecret -and [string]::IsNullOrWhiteSpace($env:PIXELLAB_SECRET)) {
    Write-Error "PIXELLAB_SECRET is not set; this preset needs it for live PixelLab calls."
    exit 1
}
if ($config.Paid) {
    $confirm = Read-Host "This preset SPENDS PixelLab credits. Type YES to continue"
    if ($confirm -ne "YES") { Write-Host "Cancelled."; exit 0 }
}

Write-Host "Running: python dev-tools/skill_benchmark.py $($config.Args -join ' ')"
Push-Location $repoRoot
try {
    & python $benchmark @($config.Args)
    $code = $LASTEXITCODE
}
finally {
    Pop-Location
}

# Point at the newest report (skill_benchmark.py writes .local/bench/<stamp>/).
if ($code -eq 0 -and $Preset -notin @("list")) {
    $latest = Get-ChildItem -Path (Join-Path $repoRoot ".local/bench") -Directory -ErrorAction SilentlyContinue |
        Sort-Object Name -Descending | Select-Object -First 1
    if ($latest) { Write-Host "Report: $(Join-Path $latest.FullName 'SUMMARY.md')" }
}

if ($interactive) { Read-Host "Press Enter to close" | Out-Null }
exit $code
