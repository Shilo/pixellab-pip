# PixelLab Pip installation measurement

Reviewed: 2026-10-15.

## Decision

Display two visual badges: **Downloads** and **Clones (14 days)**. Downloads is the sum of the download counters reported by ClawHub and currently published GitHub release assets. Clones uses GitHub's official rolling 14-day count, kept separate. Neither badge estimates installations or people. Both link to the definitions below; the README needs no explanatory paragraph.

An exact installation total across every agent, environment, and distribution is not recoverable from the available counters. One downloaded copy can be installed on many offline machines; one automated system can clone repeatedly without installing anything. Both cases are compatible with the same server-side totals. Neither a conversion factor nor an arithmetic sum resolves that uncertainty.

For a README that encourages adoption, lead with the useful workflows, examples, and security evidence already present. Use scoped activity figures as supporting evidence. A partial counter labelled as the whole audience would undermine that trust.

## What each measurement means

| Measurement | Unit | What it cannot establish |
|---|---|---|
| Download | A delivery service's counted retrieval | Successful installation, a new person, or subsequent use |
| Clone | A Git repository retrieval counted by GitHub | Whether the marketplace's plugin was installed or used |
| Installation transaction | One install operation reported by a participating installer | A unique person, an installation still present, or use |
| Activated installation | An observed first successful setup or invocation | Copies that were installed but never invoked |
| Active installation | A persistent installation identity with observed Pip use in a defined window | Distinct people or installations that do not report |
| Active account | An account with observed Pip use in a defined window | Every person using offline, shared, or unlinked environments |
| Stars, views, and command copies | Interest or discovery activity | Downloads, installations, or active use |

The [Agent Skills specification](https://agentskills.io/specification) defines a portable directory format, not a required installation registry or reporting protocol. Local copies can therefore work without any universal installation event.

## Observed counters

The public counters below were read live on 2026-10-15. The screenshot is a separate historical observation, not a fresh API result.

| Source | Observed figure | Safe public label |
|---|---:|---|
| [ClawHub skill API](https://clawhub.ai/api/v1/skills/pixellab-pip) | 1,360 downloads | ClawHub downloads |
| Same API | 3 installs | ClawHub recorded installs |
| [skills.sh skill page](https://skills.sh/shilo/pixellab-pip/pixellab-pip) | 22 installs | skills CLI reported installs |
| [GitHub releases API](https://api.github.com/repos/Shilo/pixellab-pip/releases?per_page=100) | 42 downloads across 17 current release assets | GitHub release asset downloads |
| Supplied GitHub Traffic screenshot, September 30 through October 13, 2026 | 1,232 clones; 389 unique cloners | GitHub clones and unique cloners for that stated period |
| [GitHub repository](https://github.com/Shilo/pixellab-pip) | 37 stars | GitHub stars |

The current clone API request returned HTTP 401 in the research environment. No live rolling clone badge can be populated from that request. Authentication and an approved source of publisher metrics remain prerequisites; a missing response is not zero.

### ClawHub

ClawHub's current [download metering specification](https://github.com/openclaw/clawhub/blob/main/specs/download-metering.md) records new counted downloads per target, identity, and UTC day, while preserving historical counts. It keeps skills.sh installs separate. These are service-defined download counts, not a raw count of every HTTP request or a lifetime count of unique people. The current source describes the implementation; it does not prove that every historical observation used that implementation.

Its [install telemetry contract](https://github.com/openclaw/clawhub/blob/main/docs/telemetry.md) requires a logged-in CLI and enabled reporting. Install events record presence. Uninstalling does not decrement the counters. Consequently, even a field named `installsCurrent` must not be presented as active users or currently installed copies. The three recorded installs are not three additional users to add to the download counter.

### skills CLI

[skills.sh documents](https://www.skills.sh/docs) installation telemetry, rather than ongoing skill usage. The CLI's [telemetry implementation](https://github.com/vercel-labs/skills/blob/main/src/telemetry.ts) supports opting out, flags CI, and treats reporting as best effort. Its [installation code](https://github.com/vercel-labs/skills/blob/main/src/add.ts) can send one event containing several target agents. The public number must not be interpreted as unique people or multiplied by a guessed agent count. The public backend's deduplication and CI treatment were not established by these client files.

The documented [catalog API](https://www.skills.sh/docs/api) currently requires authentication. Its official [public badge](https://skills.sh/b/shilo/pixellab-pip) is available without embedding a credential, but it covers only that installer.

### GitHub

GitHub [traffic documentation](https://docs.github.com/en/repositories/viewing-activity-and-data-for-your-repository/viewing-traffic-to-a-repository) distinguishes repository clones from fetches. Its [traffic API](https://docs.github.com/en/rest/metrics/traffic) exposes a rolling 14-day window with counts, unique counts, and date buckets. It does not attribute clone traffic to particular agents. Referring-site data describes page visits.

Release assets expose a separate [`download_count`](https://docs.github.com/en/rest/releases/assets). Neither that field nor the [Shields release-download badge](https://shields.io/badges/git-hub-downloads-all-assets-all-releases) includes repository cloning, raw-file retrieval, or manual copies. Summing the assets currently published also does not recover counters from deleted assets.

## Distribution counter audit

The 2026-10-15 audit checked the repository's [publishing inventory](publishing.md), [installation guide](../install.md), plugin manifests, release workflow, and additional publicly discoverable Pip listings. The publishing inventory's July status snapshot is not proof that every listing is still live. No additional independently reported download counter with a verified, supported public metrics API was found for the current aggregate.

| Distribution or listing | Evidence and treatment |
|---|---|
| ClawHub | Include the skill API's download counter once. Its native install counter and skills.sh installation telemetry are separate measurements. |
| GitHub release packages | Include published release asset downloads once, across versions. A directory linking to the same asset does not create another counter to add. |
| Claude Code, Codex, Copilot CLI, VS Code agent plugins, Cursor, Gemini CLI | Transport-dependent GitHub activity is already covered where GitHub counts it. No additional public Pip download counter was verified. Publisher-only installation analytics, where available, must retain their platform and time scope. |
| [skills.sh](https://skills.sh/shilo/pixellab-pip/pixellab-pip) | 22 reported installs. Suitable only for a separately labelled skills CLI installs badge; adding these to downloads would mix units and can overlap retrieval activity. |
| [SkillsMP](https://skillsmp.com/creators/shilo/pixellab-pip/skills-pixellab-pip) | The public [search API](https://skillsmp.com/api/v1/skills/search?q=pixellab-pip&limit=10) returns Pip's listing, GitHub URL, and stars, without a download counter. Download availability alone supplies no number to add. |
| [LLM Mart](https://llmmart.ai/artifacts/pixellab-pip) | Hosts a ZIP, but the visible metrics are views, listing impressions, and install-command copies. No public archive-download counter was verified. Its [Claude marketplace entry](https://llmmart.ai/marketplace.json) points to this GitHub repository, so marketplace installations are not an independent population to add. |
| [Skillget](https://skillget.dev/listings/shilo-pixellab-pip) | Displays Downloads: 0. The download-count semantics and a supported public metrics API were not established; do not build a scraper around this field or assume it measures completed installations. |
| [ClaudePluginHub](https://www.claudepluginhub.com/plugins/shilo-pixellab-pip), [Skills Directory](https://www.skillsdirectory.com/skills/shilo-pixellab-pip), [AgentSpec](https://agentspec.sh/rules/f0f440cd-d9bf-47a4-91cd-7fa176453777) | Listing, command-copy, or separately labelled installation activity does not supply a verified independent package-download count. Keep it outside Downloads. |
| [HOL](https://hol.org/registry/plugins/shilo%2Fpixellab-pip), awesomeskills.dev, LobeHub, Smithery skills, FindSkills, SkillsMD, claudemarketplaces.com, and awesome-lists | No additional verifiable public Pip download count was found. Some pages were inaccessible or not found during review; an unavailable measurement is not zero. Discovery links or mirrored upstream metrics must not be counted again. |
| npm, PyPI, VS Code Marketplace, Open VSX | The reviewed publishing configuration does not ship Pip as an npm package, Python package, or VSIX. Downloads of `skills`, an agent CLI, or other installer dependencies belong to those products, not Pip. |

The badge therefore measures **reported downloads from the included sources**, not all deliveries through every directory. Third-party hosted archives, bulk packs, private caches, and manual copies can remain unmeasured. To add another source later, verify that its counter measures Pip retrievals, is independent of the included upstream counters, and is available through a supported API with a known time scope. A mirror showing ClawHub's or GitHub's number adds no new downloads. None of these counters establishes active use.

## Coverage across installation methods

Grouping by delivery method covers the measurement problem more reliably than assuming every agent uses one fixed transport. Users can select different methods in the same agent.

| Method and examples | Observable evidence | Remaining gap |
|---|---|---|
| Git marketplace or repository install: Claude Code, Codex, Copilot CLI, VS Code, some Cursor flows | GitHub clone activity when that installation actually makes a new counted clone | Marketplace registration can precede installation; cache reuse and updates vary; no global completion signal |
| Gemini CLI extension | Git clone or release-archive retrieval, depending on the selected distribution | The same install command can use different transports |
| Cross-agent skills CLI | Participating installation telemetry; Git or HTTP retrieval depending on the source | Opt-outs, failures, multiple agents, and service aggregation prevent a universal total |
| Hosted registry archive, including ClawHub | Registry download count; participating install telemetry | A download does not confirm extraction, registration, or use |
| Raw-file or source-archive retrieval by an assistant | Usually no public author-facing counter for that operation | Release asset counts do not cover GitHub's automatically generated source archives or arbitrary raw-file reads |
| Manual installation: OpenCode, Deep Code, Antigravity, and other skills-compatible agents | The original retrieval, if any | Copying or linking an existing directory creates no new source-server event |
| Team marketplace, vendor cache, mirror, vendored repository, or prebuilt environment | The cache or mirror's upstream retrieval | Many downstream installations or users can share that retrieval |
| Containers, CI, remote sessions, WSL, and disposable cloud environments | Whatever retrieval or reporting those environments perform | One person can create many temporary identities; reused images can create no new retrieval |

Relevant primary evidence:

- [Claude Code marketplace hosting](https://code.claude.com/docs/en/plugins/host-marketplace): Git-hosted marketplace and plugin repositories are cloned. Pip's plugin uses a relative source in the same marketplace repository, so marketplace addition is not proof of a separate completed plugin installation.
- [Codex marketplace addition](https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/marketplace_add/install.rs) and [upgrade implementation](https://github.com/openai/codex/blob/main/codex-rs/core-plugins/src/marketplace_upgrade/git.rs): both contain Git clone paths. This establishes possible clone activity, not one clone per user or per successful install.
- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) and [VS Code agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins): marketplace and local installation are separate supported mechanisms. VS Code documents updating cloned marketplace repositories.
- [Gemini extension distribution](https://geminicli.com/docs/extensions/releasing/): GitHub Releases can avoid cloning, and installation metadata distinguishes release and Git installation types.
- [Cursor plugins](https://prod.cursor.com/docs/plugins): a team marketplace can be served from Cursor's synced copy, separating downstream installations from direct GitHub retrieval.
- [OpenCode skill discovery](https://opencode.ai/docs/skills/): existing local directories are discovered on demand.

## Publisher analytics and active use

For an approved directory listing, [Anthropic's publisher portal](https://claude.com/docs/connectors/building/after-publishing#track-published-plugin-usage) documents installs, active accounts, retention, and component usage, with daily updates and CSV export for a selected period up to 90 days. Sample values in Preview are not real activity. Its coverage of Pip's separate GitHub marketplace is not established, so exports must retain their declared scope.

[Claude Code's measurement guide](https://code.claude.com/docs/en/plugins/measure) separates publisher-directory reporting from organization administration and local usage. Organization analytics are not global third-party publisher analytics. They can also redact third-party plugin names.

Codex has [internal plugin analytics events](https://github.com/openai/codex/blob/main/codex-rs/analytics/src/tests/suite/plugins_tests.rs), but no supported author-facing global install or active-user query was established for this Git-distributed plugin. Platform telemetry existing is not equivalent to the publisher being able to retrieve it. [Gemini telemetry](https://geminicli.com/docs/cli/telemetry/) likewise describes operator-configured lifecycle reporting, not an all-user publisher count.

Custom reporting could measure participating installations going forward. It would need explicit disclosure and opt-in, a persistent random installation identity, a first activation event, and an actual Pip-use event. A 7-day or 30-day distinct installation count must be labelled as active reporting installations. Starting an agent with Pip merely available is not Pip use. Successful generation alone also misses questions, routing, and other supported uses.

Updates should preserve the identity. Reinstallation, duplicated images, shared state, offline operation, blocked networking, and missing reports still affect coverage. Linking several devices and agents to one person requires an optional shared account identity; a random installation ID is pseudonymous, not proof of a unique person. Do not estimate unobserved users by scaling opt-in participation without an independently measured sampling model.

[OpenAI's plugin guide](https://developers.openai.com/plugins/build/plugins) limits bundled lifecycle hooks to supported manual desktop installations, requires trust, and excludes hook-containing plugins from the public directory. The [portable skill format](https://agentskills.io/specification) supplies no universal hook. Therefore, neither session hooks nor an instruction asking the model to call a helper can guarantee reporting in every environment.

Adding an MCP proxy, mandatory account, wrapper installer, or network dependency solely to manufacture a popularity counter would change Pip's portable design without solving offline copies. Keep the existing direct PixelLab routing and secret boundaries. Runtime analytics would require a separate product decision and updates to the existing [security disclosures](../security.md).

## Combinations to reject

- **Clones plus downloads plus reported installs:** one installation can contribute to several terms, which also have different units and windows.
- **At least N installs based on downloads:** bots, inspection, failed installs, and repeat retrievals mean retrieval is not a lower bound on successful installations.
- **Unique cloners equals users:** the identifier and deduplication do not establish humans or actual use.
- **Subtract CI run count from clones:** jobs can skip checkout, retry, perform multiple retrievals, or reuse data; aggregate traffic does not provide exact attribution.
- **Daily unique cloners summed as lifetime users:** returning cloners appear on multiple dates.
- **Command copies, directory views, stars, or a README tracking image counted as installs:** they are discovery signals. Image proxies and caching further separate image requests from readers.
- **Redirect or custom archive requests counted as completed installs:** they observe a delivery step, not installation completion; cached and offline routes can bypass them.

GitHub's [webhook event reference](https://docs.github.com/en/webhooks/webhook-events-and-payloads) provides no repository clone event. [Enterprise organization audit logs](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization) can expose Git events with special access and retention, but they are not a universal clone log for this personal public repository and do not prove installations.

## What the badges count

**Downloads** sums ClawHub's `skill.stats.downloads` and the `download_count` of every asset on every currently published GitHub release, including prereleases. Draft releases are excluded, and the release list is paginated. This is an arithmetic sum of source-reported downloads with different metering rules, not deduplicated people, installations, or an exhaustive history of every delivery route. Updates, automated retrieval, and repeat activity can contribute. Deleted release assets, automatically generated source archives, raw files, manual copies, and third-party mirrors are outside the GitHub asset counter. Clones and skills CLI installation telemetry are never added to this sum.

**Clones (14 days)** uses the top-level `count` returned by GitHub's clone traffic endpoint. It does not sum daily unique cloners or attempt a lifetime estimate. The badge shows only the count; `metrics.json` records the UTC observation time. Marketplace additions, installation tools, and automation can contribute; a clone does not confirm a successful installation.

The [Distribution Badges workflow](../../.github/workflows/distribution-badges.yml) reads the official APIs directly and publishes two [Shields endpoint](https://shields.io/badges/endpoint-badge) JSON files plus a source breakdown to the dedicated `codex/badges` branch. It uses no repository checkout, hosted analytics service, or installed-skill telemetry. Updating that branch does not trigger the existing `main` push workflows. A repository guard prevents forks from mixing their own GitHub counts with Pip's ClawHub counter.

The badges link here, and the public `metrics.json` file on that branch records the component counts and UTC observation time. Transient connection and selected server errors receive up to three GET attempts with short increasing delays. Authentication failures, rate limits, and writes are not automatically retried. GitHub requests use the documented `2026-03-10` API version.

Source failures produce `unavailable`, never a partial download sum, guessed clone count, stale value copied from a previous run, or fabricated zero. The job publishes those honest states and then fails, making the problem visible in Actions and eligible for the maintainer's configured failure notifications. A successful response containing a real zero remains zero. If publishing itself fails or scheduling stops, the previous snapshot remains; inspect the `metrics.json` observation time to check its age. GitHub and Shields caching can delay changes.

## Activating the badges

1. Publish the workflow and README changes on `main`. The workflow runs when its file changes on `main`, on published or deleted releases, after the **Release New Version** workflow completes on `main`, daily, and on manual dispatch. The completion trigger covers releases made with the built-in token, which normally do not trigger another release-event workflow. It reads no triggering-run artifacts or code.
2. For clone access, create a fine-grained personal access token restricted to this repository with **Administration: read**. Save it as the repository Actions secret `TRAFFIC_TOKEN`; never paste it into chat, code, badge URLs, or saved responses. The traffic credential is used only for the GitHub clone request, never for ClawHub or writing badge data. The [traffic API](https://docs.github.com/en/rest/metrics/traffic) documents the required permission. Do not save a GitHub App installation token as this static secret: it expires after one hour. Automatic App-token generation would require a separately configured App and is not part of this implementation.
3. Run **Distribution Badges** from the Actions tab to verify access and initialize or refresh the data branch. The job's separate built-in token needs `contents: write` to publish aggregate JSON. If organization policy restricts that permission, resolve it in repository administration. A missing or invalid traffic secret makes only the clone badge unavailable and marks the refresh run as failed; Downloads can still update.

**Traffic credential renewal:** The current `TRAFFIC_TOKEN` was configured with a 90-day lifetime on 2026-10-15, giving an expected expiry of **2027-01-13**. Confirm the exact expiry in GitHub's token settings and renew by **2027-01-06**. Generate a replacement with the same repository restriction and Administration read permission, replace the Actions secret, and dispatch **Distribution Badges** to verify it. Update this renewal note when replacing the token; never record its value here.

To verify activation, check the latest **Distribution Badges** run, inspect the public `downloads.json`, `clones.json`, and `metrics.json` on `codex/badges`, and confirm both badge images render in the README after caches refresh. A local preview or a passing unit test alone does not establish that GitHub can read traffic, publish the data branch, or serve the live badge images.

## Preserving scope

The workflow publishes the latest snapshot only. It does not reconstruct all-time clones, scrape private endpoints, require users to register, or change the skill's runtime. Badges can be retained in Git history, but adding overlapping rolling clone totals would inflate any cumulative calculation. Directory publisher reports and any future opt-in activation reporting must remain separate from these download and clone badges.

Normal refreshes require no manual count edits. Zero future maintenance cannot be guaranteed: a personal token can expire or be revoked, API contracts can change, and GitHub can delay or drop scheduled runs. GitHub also documents disabling public-repository schedules after 60 days without repository activity; do not rely on automated data commits as a guaranteed exemption. If that happens, re-enable the workflow in Actions and dispatch it. Choose the traffic token's lifetime deliberately and renew it before expiry if applicable. These are [GitHub scheduling limits](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule), not an installation or usage gap that a larger number can solve.
