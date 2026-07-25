# Plan: design & build the PixelLab async poll-and-download helper

You are building a helper that lets any coding agent complete PixelLab **async** jobs without
abandoning them or dumping the user into manual status-checking. This plan tells you the *goal* and
the *process you must follow*. It does NOT dictate the design — that is your job to decide from
evidence. Companion: `todo.md` (same folder) holds the requirements and rationale.

**Scope note (read first).** SKILL.md step 12 already makes the *agent* write bark/manifest/blueprint
after a job's generations finish. This helper is NOT about those obligations. It is about **retrieving
async results and autonomy** — completing async jobs (and chains) so their assets land on disk without
the user babysitting a "ask me to check back later" handoff. Keep that boundary clear.

## What is ENFORCED (do these, no shortcuts)

1. **Challenge everything before you build.** Treat this plan, `todo.md`, and the (gitignored, maybe
   absent) `.local/poll_download.py` prototype as *opinions to interrogate, not instructions to obey*.
   Actively look for where they are wrong, incomplete, over-engineered, or would cause regressions.
   Write down what you reject and why. If a script is not even the right shape of solution, say so and
   propose better. Do not inherit the prototype's choices by default. (If the prototype file is gone,
   its pitfalls are captured in `todo.md` regardless.)

2. **Brainstorm first.** Invoke `superpowers:brainstorming` (or your harness's equivalent structured
   design step) before writing any implementation code. This is design work, not a rushed script.

3. **Do your own exhaustive research — the design must be evidence-based, not assumed:**
   - **Every REST endpoint.** Read `https://api.pixellab.ai/v2/openapi.json` in full — enumerate every
     path, its request body schema, and its *response* schema. Note which are synchronous (image
     returned inline) vs asynchronous (`background_job_id`), where images live (`image`, `images`,
     `quantized_image`, `rotation_urls`, `frame_urls`, `storage_urls`, `ttf_base64`, tileset `tiles[]`,
     …), and which return base64 vs URLs vs raw RGBA. The response schemas here are the source of truth
     for output shapes.
   - **Every MCP tool.** Read `https://api.pixellab.ai/mcp/docs` and enumerate the visible
     `mcp__pixellab__*` tools and their getters (`get_character`, `get_object`, `get_topdown_tileset`,
     `get_font`, `get_portrait_character`, `get_map_object`, …). A returned id may be an *asset id*
     (poll `/v2/<kind>/{id}`) or a *job id* (poll `/v2/background-jobs/{id}`).
   - **Real request/response patterns.** Inspect artifacts to see what a real user↔agent interaction
     produces. Note: `*.blueprint.json` files are *request recipes* (what was sent), not API responses;
     `manifest*.json` files record job/asset IDs and usage; actual *response* shapes come from the
     OpenAPI response schemas and live calls. Look at:
     - `skills/pixellab-pip/blueprints/*.blueprint.json` (bundled recipes)
     - `docs/showcase/**/*.blueprint.json` (curated real results across icons, GUI, tilesets, etc.)
     - `pixellab-pip-generations/**/*.blueprint.json` and `**/manifest*.json` (many real runs, incl.
       chained and multi-output jobs, tilesets, animations, cinematics)
     Build your list of "cases the helper must handle" from what you find here, not from a guess.
   - **The skill's own contract.** Read `references/job-lifecycle.md` (polling, statuses, **review
     state**, expiry, rate limits, the "never abandon a paid async result" rule), `references/usage-reporting.md`
     (manifests the agent already writes per job), `references/blueprint.md`, and
     `references/reviewable-candidates.md`. The helper must fit these, not fight them.
   - **The prototype**, `.local/poll_download.py` if present, as a *reference of pitfalls already
     found* (asset vs job id, backblaze URLs 403 the default UA, raw-RGBA vs quantized PNG, detach on
     Windows) — verify each claim yourself; do not assume it's correct or complete.

4. **Confront these worries head-on — research whether a script is even the right answer.** A shipped
   helper script is NOT automatically the solution; it may not work for all agents and can introduce
   the very regressions it's meant to prevent. Investigate each and let evidence shape (or reject) the
   design — do not hand-wave:
   - **Runtime dependency.** It needs a runtime (Python?) installed and on PATH. What about agents with
     no Python, or no way to install it? The skill is agent-agnostic largely *because* it's mostly
     Markdown — a load-bearing script erodes that.
   - **Shell/tool availability.** Some harnesses expose no arbitrary shell/command tool (API-only,
     sandboxed, enterprise-locked). There a script is dead weight. What do those agents do instead?
   - **Duplication & drift.** A "handles every endpoint" script hardcodes response shapes; PixelLab's
     API evolves. How do you avoid a second source of truth that goes stale? (Extend by data, not
     rewrite; or lean on schema/docs at runtime.)
   - **Security/trust surface.** Executable code that reads `PIXELLAB_SECRET`, hits the network, and
     writes files widens what audits (SkillSpector/ClawHub/VirusTotal/provenance) and users must trust,
     and it WILL produce by-design scanner findings that need dismissal rationales (as `bark.py` and
     `background_removal.py` do). Is the added surface justified?
   - **Regression risk.** A generic do-everything script is a single point of failure across ALL jobs —
     one mishandled response shape silently corrupts every job of that type. Worse than the agent doing
     it natively. Guard hard against this.
   - **Autonomy is harness-dependent, not script-provided.** A script can download in the background,
     but continuing create→animate without a manual resume needs the *harness* to re-invoke the agent
     on completion AND the agent to hold the workflow state. A script cannot manufacture that. Design
     for graceful behavior when the harness does NOT notify.

5. **The helper must ALWAYS fall back — never a hard dependency, never a dead end.** It must degrade
   gracefully every time a layer is unavailable. Which layer to *prefer* is a design decision from
   evidence — weigh this explicitly rather than defaulting either way:
   - **Strong argument for preferring the vetted helper whenever a runtime + shell ARE available — for
     EVERY agent, not just weak ones.** Agents routinely reinvent this: observed, one Antigravity run
     wrote ~a dozen throwaway scripts, each re-introducing the same bugs (wrong base64 shape, missing
     `quantized_image`, dropped job registration). And native chat-loop polling costs a tool round-trip
     + context tokens *per poll*, while a single vetted invocation loops locally at zero per-poll cost —
     cheaper (tokens/time), deterministic, encodes the traps once. This points to
     **script-first-when-available**, not script-as-last-resort. Take it seriously.
   - **The caveat that makes script-first safe (non-negotiable if you choose it):** preferring the
     script by default raises its correctness bar — one gap silently corrupts everyone's output. Only
     acceptable if the script **self-verifies what it saved** (real image, right place, expected count)
     and, on any case it cannot handle or any error, **cleanly DEFERS back to the agent** (clear signal
     + the info the agent needs) instead of failing silently or half-saving. Build the self-check and
     graceful defer in from the start.
   - **Native agent orchestration** (bounded in-turn poll via its own tools / MCP getters, or the
     harness's background-task mechanism) is the universal, zero-dependency layer — the fallback when
     there is no runtime/shell, and pure instruction that works everywhere.
   - **When neither finishes it** (no runtime, no shell, no notification), fall back to an honest,
     actionable handoff: "your asset is at job `<id>`, run `<X>` / ask me to resume to fetch it" — never
     a bare "check back later," never a silent abandon, never a crash.
   - Detect capability and auto-pick the best available layer; every gap has a fallback beneath it.

6. **Decide the design yourself and justify it.** You choose: one script or several; one job per
   invocation or a whole batch/chain; how jobs are discovered (auto-register at submit, derive from
   manifests, scan a run dir); how autonomy is achieved per harness; language/runtime and the
   no-runtime fallback. Write a short design rationale (what you chose, what you rejected, why) before
   coding, and re-challenge it after you've seen the API evidence.

7. **It must work for every case and cause no regressions.** Prove it against the real cases you found
   (sync, async, base64, URL, raw-RGBA, multi-output, chained, MCP-managed, REST, **review-status**).
   Idempotent and re-runnable: never re-spend credits, never clobber or mix existing outputs, never
   fabricate. Do not break anything the skill already does. Run `python dev-tools/qa.py` and keep it
   green.

## Known hard problems / caveats you MUST address or honestly scope out

- **Chained autonomy is the hardest part and may not be fully solvable by a download helper alone.**
  Downloading a completed result does not itself resume the agent to fire the *next* generation
  (animate after character). That needs harness re-invocation on completion **plus** the agent holding
  the workflow state. Treat "download the completed job" and "continue the chain" as separate problems;
  be explicit about which the helper actually solves on which harness, and don't claim end-to-end
  autonomy you haven't proven.
- **Review status.** Some jobs (e.g. objects) return `review` with candidate frames that need
  selection. The helper must NOT auto-select or silently pick one — surface it for the agent/user per
  `references/reviewable-candidates.md`. Downloading ≠ choosing.
- **Validation spends real credits.** Proving "every case" means live generation. Minimize it: reuse
  existing completed job/asset IDs from `pixellab-pip-generations/` and recorded manifests, poll those
  rather than re-generating; generate the minimum new jobs needed for a case; never batch-generate to
  test. State the credit cost of your validation.
- **No-Python / no-shell environments.** A robust "never abandon a paid job" guarantee must degrade
  when the runtime or shell is absent (see step 5's fallback ladder). Decide honestly whether
  "no runtime + short turn + async job" is supported or cleanly refused with an actionable handoff.
- **Rate limits & expiry.** Honor `429`/`529` + `Retry-After`; MCP download URLs and map objects can
  expire (map objects auto-delete after 8h) — retrieve promptly and re-fetch stale URLs via the getter,
  per `references/job-lifecycle.md`.
- **Implement it scanner-safe (if it ships in the skill).** A network+secret+file executable WILL be
  scanned (SkillSpector/ClawHub/VirusTotal/provenance). Build it to read as by-design, like the existing
  `assets/bark.py` / `assets/background_removal.py`: read `PIXELLAB_SECRET` only from the environment and
  never print/log it; no `eval`/`exec`/dynamic-code or obfuscation; no shell-out to untrusted input; a
  clear top-of-file docstring stating purpose and exact network scope (`api.pixellab.ai` + the returned
  asset URLs only); minimal, auditable dependencies (prefer stdlib). Then run the repo security scan and
  QA, expect a few by-design findings, and prepare a short per-finding dismissal rationale (as the repo
  already does). Getting flagged is fine; getting flagged for something avoidable is not.

## What is only ENCOURAGEMENT (weigh it, override it freely)

The goal and constraints in `todo.md` — agent-agnostic, generic/complete, flexible & intuitive,
safe/do-no-harm, autonomous-via-background-task-notifications, chained-workflow support, auto-register,
no-Python fallback — are *current thinking*, not requirements. They exist to seed your analysis. If your
research shows a better approach, take it and explain the divergence. The only non-negotiables are the
process above and the outcome: **every case works, nothing regresses, and the user is never left
babysitting a paid job the agent could have finished.**

## Suggested shape of your deliverable (also non-binding)

- A written design decision (challenged, evidence-based).
- The helper itself, wherever it best lives (a skill `assets/` helper if it should ship; a dev tool
  otherwise — you decide, and justify shipping vs not).
- A validation run across the real case types you enumerated, verified on disk, with credit cost stated.
- If it changes the skill's contract, the matching edit to `references/job-lifecycle.md` (kept lean,
  YAGNI, per `AGENTS.md`) and QA green.

Start by challenging this plan, then research, then design, then build, then prove it.
