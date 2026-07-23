# Auto

Reference for the `auto` command and the cost-approval gate it governs. The gate is Pip's single, up-front permission check before spending PixelLab credits. `auto` is off by default, so Pip asks before paid work; turning `auto` on lets jobs run without that check.

## Commands

One word after the skill trigger; the `/`, `@`, `$` prefixes and the `on`/`off` variants all work, whether the app passes it as an argument or as prose:

```text
/pixellab-pip auto
@pixellab-pip auto on
$pixellab-pip auto off
```

- `auto`: read the persisted state, toggle it, write the new state.
- `auto on`: write `"auto": true`.
- `auto off`: write `"auto": false`.

Persist `auto` as a boolean in the same `pixellab-pip.json` that bark uses; follow the config location, precedence, read-only fallback, and field-preserving write rules in `references/bark.md`, writing `auto` without disturbing `bark`. Default is off: no config, no `auto` key, or a non-boolean value all mean off. After a successful write, reply `Auto is on.` or `Auto is off.` If persistence fails everywhere, say it could not be saved and do not claim it changed.

## The cost-approval gate

Fire this gate once per job, as early as feasible: after any blocking clarification and after prompt enhancement, immediately before the first PixelLab call that spends credits. Read the `auto` setting exactly once, at this moment, and apply that one decision for the rest of the job — never re-read it mid-job.

Plan the whole paid chain before the gate so the user approves everything in one message and never waits between steps. This covers single jobs, multi-asset batches, all-direction runs, and multi-shot cinematics alike. It does not remove per-shot output validation (e.g. `references/cinematic.md`) — that checks results, not permission.

### When auto is off — ask first

Show a concise, readable approval block listing, in order, every predicted paid call:

- the tool or endpoint name (e.g. MCP `create_character`, REST `create-image-pixen`);
- its material inputs, including the exact final `description`/`prompt`/`action` text that will be sent;
- a rough cost per call and a rough total, in generations (use `references/cost-routing.md` counts and ranges; ranges are fine — the goal is awareness, not precision);
- a short flag on any call changed from the user's literal request (enhanced prompt, re-routed endpoint).

End with one concise question that infers the choices — approve, change anything, or decline — plus a footer noting autonomous runs. Do not enumerate every option; keep it intuitive. Illustrative shape only:

```text
💳 Cost check — approve before I spend PixelLab credits

1. MCP create_character (v3)  ~2 gen
   description: "stout dwarf blacksmith, flat pixel art, leather apron"  (prompt enhanced)
2. MCP animate_character — south, template walking-8-frames  ~1 gen

Estimated total: ~3 generations (rough)

Approve, tell me what to change, or say no?
Tip: reply "auto" (or run /pixellab-pip auto) to run future jobs without this check.
```

Handle the reply:

- approve / continue / ok / yes → run the approved chain, with no further per-call permission asks.
- "auto" → run the `auto` command (turn it on and persist it), then continue the chain without re-prompting.
- change → adjust, and re-show the block only if the paid plan materially changed; otherwise proceed.
- decline / no → stop before spending.

Ask only once. After approval, run the whole approved chain without re-gating. If the plan later turns into a paid call the user did not approve — a different route, an extra retry or candidate, a batch expansion — that new spend needs its own brief approval. Free or local work (polling, downloads, cropping, assembly, packaging, manifests, verification, balance/status reads) is never gated.

### When auto is on — run, but remind

Skip the approval block. Once, early (before or at the first paid call), show a one-line reminder that auto is on and how to turn it off, then proceed:

```text
⚡ Auto is on — running this job without a cost check. Disable anytime with /pixellab-pip auto.
```

## Scope

`auto` governs only this cost-approval gate. It never overrides an explicit user instruction to ask first, the Destructive Remote Actions gate, or the per-retry asks the user opted into by requesting cheap/budget work (`references/cost-routing.md`). Those still apply regardless of `auto`.
