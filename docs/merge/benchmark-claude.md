# Benchmark check on the merge branch

Historical prototype benchmark, not a test of the revised implementation. See the [current integration record](README.md).

The later scenarios `inspect-without-repair`, `simple-attack`, `auto-preserves-art-authority` and `blueprint-as-reference` have not been run through the CLI benchmark at the revised head. Offline reviewer exercises and regex checks do not replace those agent runs; the results below apply only to the original 23-scenario prototype run.

Claude arm only, 1 rep, working-tree skill (`python dev-tools/skill_benchmark.py --agents claude --variants current`), 2026-10-22. Dry: no PixelLab credits.

Every one of the 23 scenarios passed all its checks (the 20 upstream scenarios plus 3 new routes: animation doctor, key-pose move, styled icons). The published upstream run (2026-07-06) scored about 98%.

Static context grew from about 14k to about 15k tokens of injected `SKILL.md` (new router rows); median input tokens per session are higher than the published run, partly from that and partly from run-to-run variance (one rep).

| Scenario | Checks | Input tokens |
|---|---|---|
| cheap-animation | 100% | 69831 |
| check-balance | 100% | 26277 |
| plan-item-icon-sheet | 100% | 57561 |
| refuse-internal-endpoint | 100% | 26320 |
| replay-blueprint | 100% | 60471 |
| route-1bit-tileset-palette | 100% | 64834 |
| route-animation-doctor | 100% | 55904 |
| route-background-scene | 100% | 26286 |
| route-bg-removal-fallback | 100% | 59192 |
| route-character | 100% | 71324 |
| route-font | 100% | 26287 |
| route-gui-modular | 100% | 26299 |
| route-hex-tiles | 100% | 60757 |
| route-isometric-tile | 100% | 26284 |
| route-key-pose-move | 100% | 69303 |
| route-object-prop | 100% | 26288 |
| route-paperdoll-layer | 100% | 57000 |
| route-sidescroller-tileset | 100% | 64472 |
| route-skill-icons | 100% | 61718 |
| route-styled-icons | 100% | 62418 |
| route-tiles-vs-tileset | 100% | 69040 |
| setup-codex | 100% | 62191 |
| skeleton-pipeline | 100% | 64833 |
