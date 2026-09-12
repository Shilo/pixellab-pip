# PixelLab PixMiniMax Website Pricing Observation

Observed: 2026-09-12.

Source: [PixelLab API catalog](https://www.pixellab.ai/pixellab-api), the
“Animate with text (PixMiniMax)” entry.

This is a short, dated transcription of the public catalog's displayed USD
estimates. It is not a raw website capture, is not part of the repository's
REST/MCP doc-watch source set, and does not define a conversion to subscription
generations. Recheck the live catalog before quoting a current USD estimate.

| Canvas | Generated frames | Displayed estimate |
|---|---:|---:|
| 64×64 | 4 | $0.0123 |
| 64×64 | 8 | $0.0153 |
| 256×256 | 8 | $0.0153 |
| 256×256 | 40 | $0.0471 |

For charged usage, use the completed response's `usage.generations` when it is
present. Keep that value separate from the website's USD estimate and from the
REST description's generation-unit examples.
