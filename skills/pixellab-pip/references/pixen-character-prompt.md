# Pixen Character Prompt

For a requested full-body, south/front-facing neutral idle character in low top-down view, this tested prompt is a starting point before the subject description:

```text
full-body front-facing south-facing idle game character sprite, low top-down view. centered, neutral standing pose with arms at sides, full figure from head to feet. <subject description>.
```

For that composition, use `view: "low top-down"` and `direction: "south"`. Omit `small` and other optional settings unless requested. Set `no_background: true` when transparency is required.

For other requested facings, projections or poses, adapt the wording and supported `view`/`direction` controls to those requirements; do not add idle, south-facing or arms-at-sides constraints that conflict with the subject. Retain full-body framing only when requested. Validate the result against the actual request, not this example's pose or camera. The tested framing improves a scoped sample; weak view/direction controls still require visual review.
