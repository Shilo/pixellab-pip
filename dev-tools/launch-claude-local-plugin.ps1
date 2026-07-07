param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ClaudeArgs = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Launch Claude Code with this repository loaded in place via --plugin-dir: no
# copy, no per-version cache, no cachebuster. Edits to skills/pixellab-pip/ go
# live after /reload-plugins (or a relaunch). This is the recommended local dev
# loop; use manage-claude-plugin.ps1 only to install/update/uninstall the real
# cached plugin or to verify the production install flow.
#
# --plugin-dir is session-scoped to this terminal launch and shadows any installed
# copy of the same name for that session only (the installed plugin is untouched).
# For a persistent, in-place setup that also reaches the IDE/desktop, symlink the
# skill instead (loads as pixellab-pip@skills-dir across all surfaces):
#   New-Item -ItemType SymbolicLink `
#     -Path "$env:USERPROFILE\.claude\skills\pixellab-pip" `
#     -Target "<repo>\skills\pixellab-pip"
#
# Extra arguments are forwarded to claude, e.g.:
#   .\dev-tools\launch-claude-local-plugin.ps1 -p "@pixellab-pip bark off"

$scriptDir = Split-Path -Parent $PSCommandPath
$repoRoot = Split-Path -Parent $scriptDir
$manifestPath = Join-Path $repoRoot ".claude-plugin\plugin.json"

if (-not (Test-Path -LiteralPath $manifestPath)) {
    Write-Host "Error: could not find .claude-plugin\plugin.json under $repoRoot" -ForegroundColor Red
    exit 1
}

Write-Host "Loading local plugin in place from: $repoRoot" -ForegroundColor Cyan
Write-Host "After editing the skill, run /reload-plugins in the session to reload." -ForegroundColor DarkGray
Write-Host "> claude --plugin-dir `"$repoRoot`" $ClaudeArgs" -ForegroundColor DarkGray
Write-Host ""

& claude --plugin-dir $repoRoot @ClaudeArgs
exit $LASTEXITCODE
