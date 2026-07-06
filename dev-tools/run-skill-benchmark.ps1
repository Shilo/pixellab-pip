param(
    [ValidateSet("full", "static", "dry-claude", "dry-all", "list", "cancel")]
    [string]$Preset,
    [int]$Reps = 1,  # 1 rep keeps the full preset at 240 cells (~2 hours); -Reps 2 for tighter medians. The benchmark is dry — no PixelLab credits.
    [string]$Resume  # path to a prior .local/bench/<stamp> dir to continue instead of starting fresh (reuses completed cells)
)

# Convenience launcher for dev-tools/skill_benchmark.py. It only assembles the
# documented flags for the common presets, preflights that the required CLIs are
# present, and points at the report folder. The benchmark is dry (no PixelLab
# credits); the measurement logic lives in skill_benchmark.py.

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
if (Get-Variable PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue) {
    $PSNativeCommandUseErrorActionPreference = $false  # let python's own exit code surface
}

$repoRoot = Split-Path -Parent $PSScriptRoot
$benchmark = Join-Path $repoRoot "dev-tools/skill_benchmark.py"
$interactive = -not ([Console]::IsInputRedirected -or [Console]::IsOutputRedirected)

# preset -> { Label, Args, NeedCli (agent exes that must be on PATH) }. Every preset is dry (no credits).
$presets = [ordered]@{
    "full"       = @{ Label = "full        - COMPLETE suite: all agents, all 4 variants, refreshes the report ($Reps reps)"; Args = @("--agents", "claude,codex,deepseek-v4-pro", "--variants", "pre-kiss-yagni-refactor,mcp-docs,vanilla", "--reps", "$Reps", "--report", "docs/pixellab-pip-benchmark.md"); NeedCli = @("claude", "codex", "opencode") }
    "static"     = @{ Label = "static      - free context-size comparison, no CLI calls"; Args = @("--static"); NeedCli = @() }
    "dry-claude" = @{ Label = "dry-claude  - claude only ($Reps reps)"; Args = @("--agents", "claude", "--reps", "$Reps"); NeedCli = @("claude") }
    "dry-all"    = @{ Label = "dry-all     - claude + codex + deepseek-v4-pro ($Reps reps)"; Args = @("--agents", "claude,codex,deepseek-v4-pro", "--reps", "$Reps"); NeedCli = @("claude", "codex", "opencode") }
    "list"       = @{ Label = "list        - print scenarios and exit"; Args = @("--list"); NeedCli = @() }
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

# Build run arguments; -Resume continues a prior run dir, reusing its already-completed cells.
$runArgs = @($config.Args)
if ($Resume) { $runArgs += @("--resume", $Resume) }

# Preflight: python and the required agent CLIs.
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "python was not found on PATH."
    exit 1
}
$missing = @($config.NeedCli | Where-Object { -not (Get-Command $_ -ErrorAction SilentlyContinue) })
if ($missing.Count -gt 0) {
    Write-Warning "Missing agent CLI(s): $($missing -join ', '). The benchmark will skip cells it cannot run."
}

Write-Host "Running: python dev-tools/skill_benchmark.py $($runArgs -join ' ')"
Push-Location $repoRoot
try {
    & python $benchmark @($runArgs)
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
