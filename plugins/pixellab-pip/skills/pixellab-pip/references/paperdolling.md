# Paperdolling

Read this for layered characters, outfit variants, equipment swaps, or animation-consistent paperdoll workflows.

Treat paperdolling as a workflow contract, not a separate PixelLab surface.

Ask or infer:

- Base character identity.
- Direction count.
- Sprite and canvas size.
- Animation list.
- Layers such as body, hair, outfit, armor, weapon, accessory, shadow, and VFX.
- Whether outputs must be isolated transparent layers or composited previews.

Preserve:

- Canvas size.
- Frame count.
- Frame order.
- Direction names/order.
- Origin/pivot.
- Transparency/background.
- Palette/style reference where consistency matters.

Route MCP-managed characters through character/state/animation tools. Use REST v2 raw animation, edit-animation, interpolation, and outfit-transfer routes only when exact file-level control matters. Warn that text-only paperdolling drifts without a base frame, seed, or reference.

