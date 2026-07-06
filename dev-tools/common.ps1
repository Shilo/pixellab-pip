# Shared helpers dot-sourced by the dev-tools management scripts
# (manage-codex-plugin.ps1 and manage-pixellab-doc-cache.ps1). Keep only helpers
# that are identical across both callers here so a fix lands in one place.

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
