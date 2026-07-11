# PixelLab Top-Down House Generation Routing Spike

Last reviewed: 2026-07-10.

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
- The exact style-reference image, prompt, settings, and output should be captured in a future reproducible spike if the user wants this conclusion promoted into the runtime routing contract.
- Re-test after meaningful PixelLab model or endpoint changes; this document records behavior observed on 2026-07-10.

## Related Documentation

- [PixelLab Asset Routing](pixellab-asset-routing.md)
- [Style Reference Generation](../../skills/pixellab-pip/references/style-reference.md)
- [Image Input Roles](../../skills/pixellab-pip/references/image-input-roles.md)
- [Create Image Pro (`generate-image-v2`)](../../skills/pixellab-pip/references/create-image-pro.md)
