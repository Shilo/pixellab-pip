# Localization

Read this when the user writes in a non-English language, mixes languages, or asks for output in a specific language.

PixelLab natural-language parameters should be English unless SKILL.md preserves exact field text. Answer the user in their language unless they ask for another language.

## Before PixelLab Actions

- Detect the user's response language from the current request and recent conversation. If response-language confidence is low but the asset/action is clear, proceed in the dominant or most recent user language instead of interrupting.
- Translate PixelLab-facing natural-language fields (`description`, `*_description`, `action`, `item_descriptions`, `text`, `color_palette`) into concise English unless SKILL.md preserves exact field text.
- Keep non-language values unchanged: file paths, URLs, IDs, endpoint names, tool names, enum values, dimensions, seeds, colors, code identifiers, and bearer-token variable names.
- Preserve exact quoted names or requested on-image text inside otherwise English parameter values. Otherwise translate descriptive wording into English, except exact field text preserved by SKILL.md.
- For mixed-language requests, preserve technical terms, translate descriptive wording, and ask only when language mixing or culture-specific context creates multiple plausible asset meanings, response-language choices, or credit-spending actions.
- If an ambiguity affects the generated asset, edit target, on-image text, or selected PixelLab surface/tool, ask one short clarification in the user's language before spending credits.

## User-Facing Responses

- These responses override any fixed English wording a template or reference supplies, such as the cost-approval gate and auto-on reminder (`references/auto.md`), the `Auto is on.`/`Bark is on.` confirmations, the candidate-selection prompt (`references/reviewable-candidates.md`), collision clarifications, and the final usage report (`references/usage-reporting.md`). Render their visible prose and labels in the user's language, keeping each template's structure and order. Keep literal the non-language values listed above, command tokens such as `/pixellab-pip auto`, and any reply keyword the skill matches literally (e.g. `all`, `dismiss`) so the user can type it back.
- Ask clarifying questions, confirmations, refusals, and follow-up explanations in the user's language.
- When confirming or reporting a live call, include the English parameter values actually sent to PixelLab, but explain their meaning in the user's language.
- If PixelLab returns English-only errors or field names, keep the exact technical term and summarize the problem in the user's language.
