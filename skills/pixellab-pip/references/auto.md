# Auto

Reference for the `auto` command and the cost-approval gate it governs. The gate is Pip's single, up-front permission check before a job spends any PixelLab **generations** — or **credits**, once the account's included generation allowance is used up. `auto` is off by default, so Pip asks before paid work; turning `auto` on lets jobs run without that check.

## Commands

Use `auto` after the skill trigger; the `/`, `@`, `$` prefixes work whether the app passes the command as an argument or as prose:

```text
/pixellab-pip auto
@pixellab-pip auto on
$pixellab-pip auto off
/pixellab-pip auto status
/pixellab-pip auto plan 45 2 make a knight idle animation
```

- `auto`: run `python <skill-dir>/assets/bark.py auto` (reads, flips, and persists the value).
- `auto on`: run `python <skill-dir>/assets/bark.py auto-on`.
- `auto off`: run `python <skill-dir>/assets/bark.py auto-off`.
- `auto status`: run `python <skill-dir>/assets/bark.py status`; report Auto and any legacy-policy warning without writing config.
- `auto plan <budget> [retries] [task]`: bound the named or current requested run using the rules below. This is an agent instruction, not a helper command; it never changes persistent Auto.
- `auto reset`: run `python <skill-dir>/assets/bark.py auto-reset` only for the deliberate legacy-policy reset below; it removes old approval settings and turns Auto off.

`auto` is off by default: no config, no `auto` key, a non-boolean value, or unresolved legacy approval settings all mean off. After a successful toggle/on/off write, reply `Auto is on.` or `Auto is off.`

## Config

Auto and Bark share `pixellab-pip.json`, with a boolean per setting:

```json
{
  "auto": false
}
```

The shared helper writes the requested setting beside `SKILL.md` atomically, preserving unrelated keys, and verifies the active config after writing. Do not hand-edit the JSON — the read-modify-write is what a short-turn agent corrupts (misreading the current value flips the toggle backwards). Read only that exact file, then the OS user-config fallback when no authoritative skill config is selected: `pixellab-pip/pixellab-pip.json` under `%APPDATA%` on Windows, `~/Library/Application Support` on macOS, or `${XDG_CONFIG_HOME:-~/.config}` on Linux. Do not scan other config, home, shell, credential, or project directories. Every parsed JSON object is authoritative, including one with a malformed `bark` field: sound defaults on, while Auto and legacy restrictions are read from that same object. A sound typo must not expose a more permissive fallback or block paid work.

If the skill directory is read-only and no authoritative skill config shadows it, the helper can write the user fallback. An authoritative skill config that cannot be updated makes the change fail; resolve that file rather than claim an ignored fallback changed the setting. Without Python, use host file tools on these same exact paths, apply the same validation/precedence rules, and make only the explicitly requested setting edit while preserving unrelated keys and verifying the active value. Write only for an explicit Auto toggle/on/off/reset or Bark toggle/on/off command; status, planning and generation do not mutate settings. If the active setting cannot be verified, report failure and do not claim it changed; an instruction to ask first still applies to the current run.

Any `invalid_config` warning or failed status read blocks paid work until the source is repaired and its restrictions reconciled; effective Auto is off, not permission to proceed after an ordinary approval. Unparseable/non-object JSON, including nonstandard `NaN`/`Infinity` values, must not be overwritten from fallback/default data by a settings command. Preview a deliberate repair of that exact file, preserve recoverable user data, and obtain acceptance before a manual repair. A malformed Bark value in a parsed object needs only an explicit Bark setting command. Never enable Auto while invalid config remains unresolved.

### Legacy approval settings

Earlier merge builds saved installation-wide `level`, `budget`, and `retries`. `status` exposes them as `legacy_policy` and sets `requires_reconciliation: true` when any exists, including null or invalid values. Auto stays off, enabling is rejected, and ordinary Auto off/Bark commands preserve these restrictions.

Before spending, clarify the old restrictions' units/scope and reconcile them with a named approved plan; never infer zero/unlimited. Explain that `auto reset` deliberately discards all three settings and turns Auto off, preserving other keys. An informed explicit reset supplies acceptance; do not ask again. Reset grants no spending authority or release from applicable current-run restrictions. Without reset, retain them and use only the reconciled plan. Project-profile restrictions follow `project-style.md`.

## The cost-approval gate

Fire this gate once per requested run (including its whole approved chain), as early as feasible: after any blocking clarification and after prompt enhancement, immediately before the first paid PixelLab call. Read `python <skill-dir>/assets/bark.py status` exactly once at this moment, or use the Config section's same-path host-file fallback without Python. Resolve invalid-config and legacy-policy warnings as above, then apply that decision for the rest of the job — never re-read it mid-job. Bounded plans use the same Auto on/off decision and any stricter current-run instructions.

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

`auto` governs only this cost-approval gate. It never overrides an explicit user instruction to ask first, the Destructive Remote Actions gate, or the per-retry asks the user opted into by requesting cheap/budget work (`references/cost-routing.md`), except for the concrete retry scope/count supplied for a bounded run below. Explicit dry-run, `--dry`, free-preview or plan-only requests make no paid calls, even with Auto on; clarify ambiguous preview intent before spending.

## Bounded plans and resuming

`auto plan <budget> [retries] [task]` supplies a generation cap and finite retry count for one requested chain. Parse the initial cap as a finite nonnegative number (fractions are valid), then an optional nonnegative integer retry count, default zero; the remaining prose names the task. Reject negative, nonfinite, boolean or malformed numeric values rather than treating them as task text. Clarify ambiguous numeric-only tails. If neither trailing task text nor current conversation identifies the run, ask which task; never save a setting or grant permission to a later unrelated task. A zero cap permits no positive-cost call.

Show the whole plan, cap, allowed retry operations and stop conditions in the existing card: ask-first when Auto is off or the user requested approval; the Auto-on card otherwise. A cap narrows standing Auto authority and does not add another approval gate. Retries count total additional paid attempts across the chain, not per asset/session; free polling/download recovery does not consume them. The specified retry count covers only those named operations within the cap. Block calls that would exceed the cap and retries beyond their allowance; report work blocked by either limit and never increase limits implicitly. A zero or exhausted retry allowance does not block original approved calls within the cap, provided their required inputs and content checkpoints are satisfied. Natural-language budgets/retry instructions use these same constraints.

These are run constraints, not another persistent setting or permission level; the former Ask and Auto choices remain `auto off` and `auto on`. A budget alone does not authorize unspecified attempts, new asset scope, local fallback art, playback changes, or delegated visual review. Content checkpoints remain in force unless the current user explicitly delegates that review for the named outputs.

Before the first paid call, record the scope, cap, retry limit/usage, remaining work and approval context through the locked manifest plan writer in `usage-reporting.md`; update that audit evidence as work proceeds. A file or unfinished folder is not proof of permission. Resume only identifiable prior approved work; clarify missing or materially changed scope. Recover submitted results with their getter rather than paying again. If submission was interrupted before its ID was recorded, recover the tool result first; an uncertain submission blocks a replacement call.

Before admitting any paid call under a cap, use `python <skill-dir>/assets/manifest.py committed <run> [<run>...]` over every run in the plan, then add the next call's conservative estimate (upper bound when available). A freshly created empty run has no prior spend only before its first submission; a missing ledger during resume is unknown. Unknown cost/accounting blocks comparison; do not count it as zero. Submit admissions serially and record each returned ID immediately before admitting the next call; approved jobs may render concurrently. Actual usage and pending estimates have different fields in `usage-reporting.md`. A failed download or job does not establish a refund. If the provider cannot bound a call within the remaining budget, stop for a revised scope before spending. This is conservative agent-side admission, not a provider billing guarantee or a shared cap across independent agents.

For a requested mixed batch (CSV, text list or grouped assets), resolve each row's asset intent, count, size, references and output names before the gate; ask only about material missing/ambiguous fields. Use the existing per-asset routes and one whole-chain card, not a new submission engine. Show the requested groups and every result or failure in stable input order; a successful sample does not silently approve expanding the batch. Retain per-item identity in the manifest/blueprint for later review or one-call variation.
