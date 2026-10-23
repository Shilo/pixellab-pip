---
description: "Redo the frames a check found bad"
argument-hint: "<fix_report.json> [plan number]"
allowed-tools: Bash(python *skills/pixellab-pip/assets/*) mcp__pixellab__get_balance mcp__pixellab__get_image mcp__pixellab__get_upload_url mcp__pixellab__wait_for_jobs mcp__plugin_pixellab-pip-studio_pixellab__get_balance mcp__plugin_pixellab-pip-studio_pixellab__get_image mcp__plugin_pixellab-pip-studio_pixellab__get_upload_url mcp__plugin_pixellab-pip-studio_pixellab__wait_for_jobs
---

Use the pixellab-pip skill for: re-roll the planned frames from an animation doctor report, through the approval level.

Request: $ARGUMENTS
