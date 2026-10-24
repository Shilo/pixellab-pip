# Game Art × Pip Merge Position

Merge position · pixellab-game-art → PixelLab Pip

From the Game Art maintainer, 2026-10-21. Written against Pip v2.3.0 and its merge research spike (reviews of 2026-10-15/16, which used Game Art v1.4.0). Game Art 1.5.0 is built locally and not yet pushed.

## Our position in short

We agree with the spike's core recommendation: one jointly maintained product, with Pip's general routing as the foundation and Game Art's project workflow added on demand. We accept Pip's rules on spending, raw outputs and secrets.

We ask that the production layer (style memory, finishing, batches, and the new animation doctor) comes in as a first-class part of the product, not only "style memory". We propose `/pga-fix` as the first joint contribution, because neither project has anything like it and it already follows Pip's strictest rules.

## What changed since your review

Game Art 1.5.0 adds an animation doctor and fixes all five helper weaknesses your comparison listed.

| Your finding (v1.4.0) | Now in 1.5.0 |
| --- | --- |
| `qa.py` always exits successfully | `--strict` exits 1 when anything is flagged; the default stays informational |
| `preview_gif.py` is not a faithful copy | `--faithful`: only the given frames, transparent, 1:1, their own durations, disposal 2 |
| `colormatch.py` overwrites by default | Still in place (recipes depend on it), but each untouched original is kept in `orig/` before the first overwrite |
| `tileset_preview.py` rejects one sheet | Argument guard fixed: `out.png sheet.png` works |
| `normal_map.py` has no DirectX switch | `preview --directx` flips green for Unreal-style maps |

Each fix has a test that fails on the 1.4 script and passes on 1.5.

## The animation doctor, `/pga-fix`

It checks a set of frames against "game ready", fixes for free what it can from pixels the set already has, and hands the agent a priced re-roll plan for the rest. No generations, no GPU, no model: Python with Pillow, numpy and scipy.

### What it measures

`brightness`, `palette`, `colour_count`, `specks`, `holes`, `bg_leak`, `edge`, `ground`, `detached`, `jump`, `size_pop`, `missing_inbetween`, `loop_seam`, `return_to_stand`, `flash`, `effect`, `weird_change`, `weapon_lost`, `broken_thin`, `grid`, `mixels`, `soft_edge`, `size`

### How it behaves

- Originals are never written. Fixed frames go to a new folder with the same frame count and file names, so they still drop into an engine.
- Every change is reported with *fixed* or *still failing*, after measuring again.
- Effects (slashes, glows, smoke) and soft effect edges are never changed on their own. They come back as proposals; the agent asks one question and re-runs with `--accept`.
- Timing fixes (drop a bad frame and hold its neighbour, reorder a hurt) are allowed and always reported.
- What can't be fixed locally gets a re-roll plan: the frames, the tool, the one wording change that addresses the cause, the cost in generations, and the original job from the log when there is one.
- Thresholds were calibrated on 818 hand-approved animations from a shipped game. Checks that lead to a paid re-roll flag about 2% of that set; checks whose fix is free flag 5-8%.

This matches the spike's conditions for final pixels: raw outputs are kept, derivatives are labelled, and transforms are disclosed. A user who asks the doctor to fix a set has accepted its body-only fixes for that job; anything touching effects still needs their answer.

## What we accept from Pip's rules

| Area | Pip's rule | Our answer |
| --- | --- | --- |
| Paid work | Ask before spending; whole-chain approval; no open-ended retries | **accept** Ask-first becomes the default. Our no-prompt loop becomes an opt-in mode with a budget and attempt limits. |
| Final pixels | Keep raw outputs; disclose transforms | **accept** Already true for `/pga-fix` and now for `colormatch.py`. |
| Aesthetic defaults | No house look without the user's direction | **accept** House recipes load only when a project style selects them. |
| Schema authority | Live schemas decide accepted fields | **accept** Measured behaviour stays as separate evidence, as the spike proposes. |
| Secrets | Pip's handling; never import credential values | **accept** |
| Logging | No second log | **open** Our `log.jsonl` holds prompt, tool, seed and cost per job; targeted re-rolls depend on it. We propose it, or Pip's records extended with those fields, as the one shared record. |
| External sharing | No sharing channel as a merge side effect | **accept** Our opt-in outcome sharing stays out of the merged product. |

## What we ask for

- **ask** **A production module, loaded on demand**: project styles and reference anchors, finishing helpers, batch runs, job history, engine exports, tileset and normal-map previews. One core skill is fine; this is its "project mode".
- **ask** **`/pga-fix` as the first joint contribution**, ported as a helper plus one reference file, with its tests in Pip's CI.
- **ask** **Short commands for Claude Code users**: thin aliases into the core (for example "fix", "batch", "style"), so current users keep their muscle memory.
- **ask** **Shared credit and naming**, agreed before any combined release.
- **ask** **Clear ownership**: Pip owns routing, hosts, CI and the benchmark; Game Art owns the production module and the doctor; both review changes to the shared rules.
- **ask** **A migration path** for existing Game Art installs: profiles keep working, and old no-ask instructions are removed cleanly.

## Proposed phases

### Phase 0: Agree the shared rules

Spending, raw outputs, authority of saved styles, the job record. One page, both maintainers sign off. Work happens on a feature branch, as the spike says.

### Phase 1: The doctor as the first contribution

Port `/pga-fix` into Pip's core with its tests. It fills a gap in both projects and needs no style system, so it can ship on its own.

### Phase 2: Project styles

Pip reads `pixellab.json` named styles and approved reference anchors, with guided setup and a small validated writer. This is the spike's MVP.

### Phase 3: Production module

Finishing helpers, batches, history and exports move in behind the project mode, each with tests and the agreed disclosure rules.

### Phase 4: Migration and release

Representative-project tests, migration notes, then one combined release; the standalone Game Art repo points to it.

## Open questions for both of us

1. Product name, and how both projects are credited.
2. One shared job record: ours, yours, or a merged format?
3. Which Game Art recipes become opt-in project presets, and which stay as documentation only?
4. Do Claude Code command aliases count as "multiple skills" under the spike's rule, or as a host feature of one core?
5. Release cadence and who cuts releases.

---

Game Art: pixellab-game-art (Claude Code bundle and any-agent package), 1.5.0 local. Pip: Shilo/pixellab-pip v2.3.0, MIT. Nothing here is agreed yet; it is a starting position for the conversation.
