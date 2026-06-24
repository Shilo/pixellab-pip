# Localization

Read this when the user writes in a non-English language, mixes languages, or asks for output in a specific language.

PixelLab natural-language parameters must be English even when the conversation is not. Answer the user in their language unless they ask for another language.

## Before PixelLab Actions

- Detect the user's response language from the current request and recent conversation.
- Before MCP, REST, website/editor, Aseprite, or Pixelorama actions, translate or rewrite every PixelLab natural-language input into concise English, including `description`, `style_description`, `negative_description`, `edit_description`, `action`, `action_description`, `animation_description`, `item_descriptions`, `text`, and `color_palette`.
- Keep non-language values unchanged: file paths, URLs, IDs, endpoint names, tool names, enum values, dimensions, seeds, colors, code identifiers, and bearer-token variable names.
- Preserve exact quoted names or requested on-image text only when the user explicitly wants that literal text rendered, and keep it inside an otherwise English parameter value. Otherwise translate descriptive wording into English.
- If a phrase is ambiguous after translation or depends on culture-specific context that affects the generated asset, ask one short clarification in the user's language before spending credits.

## User-Facing Responses

- Ask clarifying questions, confirmations, refusals, and follow-up explanations in the user's language.
- When confirming or reporting a live call, include the English parameter values actually sent to PixelLab, but explain their meaning in the user's language.
- If PixelLab returns English-only errors or field names, keep the exact technical term and summarize the problem in the user's language.
