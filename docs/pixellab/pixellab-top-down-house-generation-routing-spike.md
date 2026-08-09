# PixelLab Top-Down House Generation Routing Spike

Last reviewed: 2026-08-08.

Purpose: record observed failures and the successful fallback when generating a south-facing, top-down house asset. This is a focused routing study, not a claim that every subject or future PixelLab model behaves the same way.

## Target

The requested asset was a `128x128` rustic ancient village house for a top-down game. The required composition was an overhead or orthographic top-down view with the entrance facing south. Tests also requested selective outlines and high detail. Later tests used a transparent background.

The critical acceptance criterion was structural: the house had to read as a top-down game asset rather than an isometric or three-quarter building illustration.

## Observed Results

### Text-only Create Image (New) / Pixen (`create-image-pixen`)

Twenty-four REST outputs from Create Image (New) / Pixen (`create-image-pixen`) were visually reviewed during the investigation across several prompt strategies. The user initially referred to this workflow as v3/new, but the documented route tested here is Create Image (New) / Pixen (`create-image-pixen`); this document does not equate `new` with a documented v3 endpoint. An additional API-completed output was observed but not retained after an earlier batch timeout. It also failed the structural review.

The tests varied:

- `high top-down` and `low top-down` view fields;
- explicit `south` direction;
- `selective outline` and `highly detailed` fields;
- positive descriptions of a direct overhead, map, satellite, floor-plan, or tactical view;
- descriptions with explicit anti-isometric constraints;
- descriptions without negative constraints;
- detailed architectural prompts;
- minimal prompts, including `house.`;
- `no_background: false` and `no_background: true`.

All 24 reviewed outputs failed the structural acceptance criterion. They remained isometric-like, axonometric, or three-quarter building views. Shortening the prompt and removing negative wording changed styling and framing but did not reliably change the underlying projection. Transparent-background generation isolated the asset but did not correct its view.

Conclusion: for this subject and tested route state, prompt wording, the documented view/direction fields, and background removal did not overcome the route's observed tendency to produce angled house illustrations. Repeating prompt-only retries after this pattern was established spent credits without finding a compliant result.

### Init-image guidance

User-run tests with an initial image produced two recurring failure modes:

1. The output followed the supplied house shape too literally and looked uncanny or derivative.
2. The output departed from the supplied geometry and reverted to an isometric-like house.

This made init-image guidance a poor fit for the desired balance: preserve the top-down projection while retaining freedom to redesign the house.

This observation is qualitative because the exact init-image requests and outputs are not stored in this repository. Treat it as a reported workflow result, not a controlled API benchmark.

### Create Image Pro (`generate-image-v2`)

User-run Create Image Pro (`generate-image-v2`) tests failed in the same practical way as the text-only Create Image (New) / Pixen (`create-image-pixen`) route: the outputs did not preserve the required top-down house projection.

The Pro quality tier did not, by itself, solve the structural view problem. Do not recommend upgrading from text-only Create Image (New) / Pixen (`create-image-pixen`) to Create Image Pro (`generate-image-v2`) solely to correct this failure mode.

This observation is also qualitative because the exact Pro requests and outputs are not stored in this repository.

### Create Image from Style Reference (Pro) (`generate-with-style-v2`)

The successful route was **Create Image from Style Reference (Pro)** (`generate-with-style-v2`) using a top-down house as the style reference.

Observed behavior:

- the reference anchored the required top-down house projection;
- the prompt could still vary the generated house rather than merely reproducing the reference;
- different house styles remained possible while preserving the useful view;
- the result avoided the uncanny shape-copying behavior seen with init-image guidance.

This was the only tested workflow reported to satisfy both structural fidelity and prompt-driven variation.

The successful style-reference inputs and outputs are not stored in this repository, so the conclusion should be treated as strong user-observed routing evidence rather than a reproducible checked-in benchmark.

## Routing Recommendation

For a top-down house asset where a specific projection is a hard requirement:

1. A text-only Create Image (New) / Pixen (`create-image-pixen`) attempt is reasonable as a cheap probe.
2. Verify projection before judging style, detail, palette, or background.
3. If the first candidate has the wrong projection, avoid a long sequence of prompt-only retries. One materially different retry can test whether the failure is incidental; repeated isometric reversion indicates a route mismatch.
4. Do not assume Create Image Pro (`generate-image-v2`) will repair structural view adherence merely because it is Pro.
5. Do not use an init image when the user wants freedom from the reference's exact geometry unless they accept the risk of literal shape transfer.
6. Treat Create Image from Style Reference (Pro) (`generate-with-style-v2`), with a reference that clearly demonstrates the required top-down projection, as the leading candidate for the next attempt pending a checked-in reproduction.
7. Describe the reference as a view/style anchor rather than the identity of the desired house. Use the prompt for architecture, materials, age, palette, and other variations.
8. Verify that the generated house preserves the reference's projection without copying its distinctive subject geometry too closely.

This provisional recommendation applies to the tested house failure mode when view adherence is more important than minimizing cost. Extending it to other architecture is an untested hypothesis. Create Image from Style Reference (Pro) (`generate-with-style-v2`) is a paid route, so confirm the reference role and batch scope before generation.

## Why Style Reference Fits Better

The tested problem was not lack of descriptive detail. The model repeatedly recognized "house" but selected the wrong projection. A top-down style reference supplied a visual example of the structural convention that text and broad camera fields did not enforce reliably.

Init-image and style-reference workflows should not be treated as interchangeable:

- An init image can act as source geometry and encourage literal structural transfer.
- A style reference can anchor visual conventions, including the observed projection, while leaving more room for a new subject design.

That distinction explains the reported outcome, but it remains an inference from the tests rather than a documented guarantee of the underlying models.

## Verification Checklist

For future top-down architecture tests, judge candidates in this order:

1. Projection: does the asset read as top-down rather than isometric or three-quarter?
2. Direction: is the south-facing entrance readable in the intended game orientation?
3. Independence: does the result avoid copying distinctive geometry from a style-only reference?
4. Variation: did prompt-requested materials and architecture change while the view stayed stable?
5. Output integrity: are size, transparency, outline treatment, and detail level correct?

Stop or change routes when projection fails. Polishing a structurally unusable candidate does not make it production-ready.

## Evidence Limits and Follow-up

- The 24 reviewed Create Image (New) / Pixen (`create-image-pixen`) outputs are not checked-in documentation fixtures.
- The init-image, Create Image Pro (`generate-image-v2`), and successful Create Image from Style Reference (Pro) (`generate-with-style-v2`) tests were performed by the user outside the checked-in corpus.
- No seed-controlled comparison was performed across routes.
- The earlier 2026-07-10 style-reference test did not retain its exact fixture, prompt, settings, or output; the 2026-08-08 follow-up below captures a separate reproducible control and request.
- Re-test after meaningful PixelLab model or endpoint changes; this document records historical behavior observed on 2026-07-10 and the follow-up observed on 2026-08-08.

## Reproducible MVP follow-up (2026-08-08)

The planned follow-up captured the previously missing fixture, request, seeds, outputs, and
candidate-level review in
[the top-down south-facing building MVP plan](../plans/pixellab-top-down-south-facing-building-prompt-plan.md)
and its gitignored
[run review](../../pixellab-pip-generations/top-down-south-building-mvp-20260808/review.md).

The controlled test used a locally authored neutral 128x128 transparent projection guide at
style-reference/projection-guide.png. The guide showed a simple screen-aligned shallow top-down
building with a south/bottom front facade and entrance. It was sent as a style reference, not an
init/source image, so its exact geometry was not meant to be copied.

The exact REST request used for both independent calls was:

    POST /v2/generate-with-style-v2
    style_images: one 128x128 image from style-reference/projection-guide.png
    description: one new town-house sprite with a different roof, windows, and facade materials; preserve the reference's shallow top-down, screen-aligned game-map projection, with the front facade and entrance on the south/bottom edge facing the camera/player; do not copy the reference's exact building geometry.
    style_description: simple flat pixel-art reference with a screen-aligned shallow top-down building, rectangular footprint, visible roof, and south-facing front facade; match the projection and compact sprite framing, not the exact geometry.
    no_background: true
    image_size: omitted; output size was derived from the 128x128 reference

Each call returned four 128x128 transparent candidates. All eight candidates passed the hard
projection, south-facing front, screen-alignment, single-whole-asset, and output-integrity gates.
Their roof shapes, windows, and facade materials varied from the guide, so the route preserved
the projection without simply cloning the reference geometry.

The same run also tested one Pixen sentinel and a 3x3 PixFlux prompt ladder. The sentinel failed,
and all nine PixFlux candidates failed the projection/screen-alignment gates despite explicit
low top-down, south, anti-isometric wording, and isometric: false. The prompt-only route should
therefore remain a cheap probe rather than the reliable path for this building class.

Routing conclusion for the current model state: for a hard screen-aligned top-down/south-facing
building sprite, use REST generate-with-style-v2 with a neutral projection/style anchor and a
short variation prompt, then reject any candidate that fails the structural gates. The result is
strong operational evidence, not a guarantee across future model versions or arbitrary style
references.

## Minimal-prompt and surface follow-up (2026-08-08)

A second controlled run separated the reference from prompt wording. With the same neutral
128x128 projection guide:

- The full canonical description with style_description omitted passed 4/4.
- A shorter description with style_description passed 4/4.
- A still shorter description with style_description passed 4/4.
- The minimal description
  a new traditional 2D town-house sprite with a south-facing entrance and different geometry.
  with style_description omitted passed 4/4.

This identifies the smallest tested prompt for the current route. The exact replay recipe and all
candidate outputs are in the
[follow-up run review](../../pixellab-pip-generations/top-down-south-building-mvp-followup-20260808/review.md).

The follow-up also tested reference specificity. Replacing the neutral guide with a previously
generated successful house preserved the top-down/south-facing structure but caused all four
outputs to converge visually on that reference-specific architecture. The reference must
therefore be generic when the requested building geometry must change.

Finally, MCP create_image_pro with the neutral guide as style_image_base64 and all four style_copy
aspects passed 4/4 structural gates in one call. It was a viable MCP fallback in this first
comparison, but the native Pro route needed a broader text-only check before changing the default.

## Native Pro follow-up (2026-08-08)

A bounded native MCP `create_image_pro` comparison tested three text-only prompts and two calls
with the same neutral guide. The shortest text-only prompt passed 4/4 candidates; longer structural
wording passed 2/4 and handheld-RPG wording passed 3/4. The guide-assisted calls held the required
projection across 8/8 candidates, but their building-shaped guide encouraged convergence on its
architecture.

For an MCP-first agent generating a new town-house-like sprite, start with `create_image_pro` and
the shortest prompt in the style-reference contract. Use the neutral guide only when projection
needs visual anchoring or the user supplies it. Keep REST `generate-image-v2` for MCP unavailability
with one guide, and use `generate-with-style-v2` only for REST-only multi-reference control. Its
earlier 11/12 repeat result remains the stronger reliability sample, so this Pro finding is not a
guarantee across model state or building categories.

## Reliability suite and category boundary (2026-08-08)

A bounded repeat suite ran 10 independent REST style-reference calls and retained 40 candidates.
The base neutral projection guide with the minimal town-house prompt passed 11/12 hard gates
across three new seeds. An alternate neutral guide passed 2/4, confirming that the guide itself
materially affects reliability.

Category probes showed a boundary rather than a universal building recipe:

- shop: 2/4 with minimal wording, then 3/4 with explicit front-facade wording and 3/4 with
  stricter side-wall exclusions;
- inn: 2/4 with minimal wording, then 0/4 with either targeted prompt, because sign-like text
  persisted and failed the output-integrity gate.

The current operational conclusion is to keep the neutral guide plus minimal prompt as the MVP for
town-house-like forms, but require a separate category-specific prompt/reference test for shops,
inns, and other named building types. More adjectives and repeated negative wording did not
produce a reliable rescue. The full [reliability review](../../pixellab-pip-generations/top-down-south-building-mvp-reliability-20260808/review.md)
and [run manifest](../../pixellab-pip-generations/top-down-south-building-mvp-reliability-20260808/run-manifest.json)
are preserved with the generated candidates.

## Reference scope decision

The neutral guide is a building projection control, not a universal south-facing reference. Do not
combine it with character guidance or create a shared building/character fixture: the building
guide's roof, facade, and entrance encode architecture and can bias character silhouettes or poses.
No separate character guide is justified by this building-only evidence; create one only after a
character-specific test demonstrates a projection problem that needs visual anchoring.

## Related Documentation

- [PixelLab Asset Routing](pixellab-asset-routing.md)
- [Style Reference Generation](../../skills/pixellab-pip/references/style-reference.md)
- [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md)
- [Create Image Pro (`generate-image-v2`)](../../skills/pixellab-pip/references/create-image-pro.md)
- [Traditional Top-Down South-Facing Building MVP Prompt Test Plan](../plans/pixellab-top-down-south-facing-building-prompt-plan.md)
