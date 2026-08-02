# Pixen Character Prompt

Use this prompt before the subject description:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet. <subject description>.
```

Use `view: "low top-down"` and `direction: "south"`. Omit `small` and other optional settings unless requested. Set `no_background: true` when transparency is required.

Pixen/v3/new may underweight user instructions such as `view`/`direction` and has isometric bias; prefer Pro when the user's instructions or static south-facing view matter and higher cost and different character style are acceptable.

Reject results that are not full-body, front/south-facing, idle, and low top-down, or that are isometric, rear-facing, portrait-like, or action-like.
