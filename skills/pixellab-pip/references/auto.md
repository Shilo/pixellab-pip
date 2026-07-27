# Auto

Reference for the `auto` command and the cost-approval gate it governs. The gate is Pip's single, up-front permission check before a job spends any PixelLab **generations** — or **credits**, once the account's included generation allowance is used up. `auto` is off by default, so Pip asks before paid work; turning `auto` on lets jobs run without that check.

## Commands

One short word after the skill trigger; the `/`, `@`, `$` prefixes and the `on`/`off` variants all work, whether the app passes it as an argument or as prose:

```text
/pixellab-pip auto
@pixellab-pip auto on
$pixellab-pip auto off
```

- `auto`: run `python assets/bark.py auto` (reads, flips, and persists the value).
- `auto on`: run `python assets/bark.py auto-on`.
- `auto off`: run `python assets/bark.py auto-off`.

`auto` is off by default: no config, no `auto` key, or a non-boolean value all mean off. After a successful write, reply `Auto is on.` or `Auto is off.`

## Config

`pixellab-pip.json` holds a boolean per setting:

```json
{
  "auto": false
}
```

The helper writes `auto` to `pixellab-pip.json` beside `SKILL.md` atomically, preserving the other key (notably `bark`). Do not hand-edit the JSON — the read-modify-write is what a short-turn agent corrupts (misreading the current value flips the toggle backwards). If Python is unavailable, hand-write `auto` as a boolean in that file, preserving `bark`; if the skill directory is read-only, write instead to `pixellab-pip/pixellab-pip.json` inside the OS user-config dir (`%APPDATA%` on Windows, `~/Library/Application Support` on macOS, `${XDG_CONFIG_HOME:-~/.config}` on Linux) — where the helper also reads it. Do not scan other config, home, shell, credential, or project directories for it. Do not rewrite config except when the user runs an explicit `auto` command. If persistence fails everywhere, say the setting could not be saved and do not claim it changed.

## The cost-approval gate

Fire this gate once per job, as early as feasible: after any blocking clarification and after prompt enhancement, immediately before the first paid PixelLab call. Read the `auto` setting exactly once, at this moment, and apply that one decision for the rest of the job — never re-read it mid-job.

Plan the whole paid chain before the gate so the user approves the whole job — both the spend and how each call is set up — in one message, instead of a cost prompt between each step. This covers single jobs, multi-asset batches, and multi-shot cinematics alike. The gate replaces repeated cost-permission asks only — not the content and quality checkpoints (produce-one-candidate-first, the `south`-first animation default, ask-before-all-directions, per-shot validation). When your listed plan explicitly includes that wider scope and the user approves it, that approval also covers those scope asks, so you neither skip them silently nor ask twice.

### When auto is off — ask first

Post a short, readable **Markdown** approval message — render it, do not wrap it in a code fence — listing, in order, every predicted paid call:

- the tool or endpoint name;
- its material inputs as `key: value` pairs — not only the `description`/`prompt`/`action`, but every input that shapes the result or that you chose or changed for the user: size, mode/view, direction(s) and counts, `no_background`, template/skeleton id, style/reference/palette/mask inputs (named by role), negative prompt, and `seed` when you set one. Skip inputs left at harmless defaults;
- a rough cost per call and a rough total, in generations (use `references/cost-routing.md` counts and ranges; ranges are fine — the goal is awareness, not precision);
- a short flag on any call you changed from the user's literal request (enhanced prompt, re-routed endpoint).

For prompt text, show what will actually be sent: if you enhanced it agent-side, show the enhanced value; if you are using inline `enhance_prompt` (server-side refinement), show the literal prompt and note PixelLab will refine it — never run a separate paid enhancer before the gate just to populate it.

The user approves both the spend and how each call is set up, so show enough of each call to judge that. Use the template below every time so the message stays predictable to read: keep the header, closing question, and tip lines consistent in phrasing and order across jobs (only the generation count and the call list change); fill one numbered block per predicted paid call. Keep keywords in backticks or bold so they stand out, and the tip quiet. For a non-English user, localization overrides this: localize the template's prose, and show each human-readable value both as the exact English that will be sent and as its translation, per `references/localization.md`.

Template:

> 💳 **Approve this PixelLab run?** — **~{N} generations** *(or credits)*.
>
> 1. **`{tool or endpoint}`** · {surface} · {mode/key notes} · ~{cost}
>    - `{long prompt/description}`: "{exact text to send}" *(flag `(enhanced)` or `(rerouted)` if you changed it)*
>    - `{short param}`: {value} · `{short param}`: {value}  — group short inputs on one line
> 2. …one numbered entry per predicted paid call…
>
> Reply **yes / no**, or say what to **change**.
> *Tip: reply `auto` (or `/pixellab-pip auto`) to run future jobs without this check.*

Filled example:

> 💳 **Approve this PixelLab run?** — **~3 generations** *(or credits)*.
>
> 1. **`create_character`** · MCP · v3 · ~2 gen
>    - `description`: "stout dwarf blacksmith, flat pixel art, leather apron" *(enhanced)*
>    - `size`: 48 · `view`: side · `detail`: high detail
> 2. **`animate_character`** · MCP · ~1 gen
>    - `action_description`: "walk" · `directions`: ["south"] · `template_animation_id`: `walking-8-frames`
>
> Reply **yes / no**, or say what to **change**.
> *Tip: reply `auto` (or `/pixellab-pip auto`) to run future jobs without this check.*

Handle the reply by intent, not literal tokens — infer what the user means from whatever they write (any wording, any language) and map it to one of these:

- yes / ok / approve / continue → run the approved chain, with no further per-call permission asks.
- "auto" → run the `auto` command (turn it on and persist it), then continue the chain without re-prompting. This reply approves the current job; if the setting cannot be persisted, still continue and report that separately rather than re-asking.
- change → adjust, and re-show the block only if the paid plan materially changed; otherwise proceed.
- decline / no → stop before spending.

Ask only once. After approval, run the whole approved chain without re-gating. If the plan later turns into a paid call the user did not approve — a different route, an extra retry or candidate, a batch expansion — that new spend needs its own brief approval. Free or local work (downloads, assembly, verification, balance/status reads, and the like) is never gated.

### When auto is on — run, but show what's happening

Don't pause and don't gate per call, but still show the plan. Once, early (before or at the first paid call), post the same numbered list of predicted paid calls as the off-mode message above — identical per-call inputs, rough per-call and total cost, `(enhanced)`/`(rerouted)` flags, and the same localization rules. Only the framing changes: the ⚡ auto header replaces the 💳 approval header, the reply prompt is dropped, and a disable tip replaces the enable tip. Then run the whole chain without re-prompting.

Template — reuse the off-mode numbered blocks verbatim; only the header and footer differ:

> ⚡ **Auto is on — running PixelLab job(s)** — **~{N} generations** *(or credits)*.
>
> {off-mode numbered per-call blocks, verbatim}
>
> *Disable auto with `/pixellab-pip auto`.*

## Scope

`auto` governs only this cost-approval gate. It never overrides an explicit user instruction to ask first, the Destructive Remote Actions gate, or the per-retry asks the user opted into by requesting cheap/budget work (`references/cost-routing.md`). Those still apply regardless of `auto`.
