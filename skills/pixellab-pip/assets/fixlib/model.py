"""The three things the animation doctor passes around: an animation, a finding about it, and a change made to it."""
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Anim:
    key: str                     # "<character>/<move>", e.g. "knight/attack"
    character: str
    move: str                    # idle|walk|run|attack|skill|cast|hurt|death|other
    kind: str                    # "loop" | "oneshot"
    kind_guessed: bool
    paths: list                  # input files in play order ([] for sheet/GIF input)
    frames: list                 # (H, W, 4) uint8 RGBA, all on one shared canvas
    offsets: list                # (x, y) of each original frame on the shared canvas
    sizes: list                  # (w, h) of each original frame
    scale: int                   # detected pixel size (1 = native)
    ref: np.ndarray = None       # reference sprite RGBA (its own size)
    ref_guessed: bool = True
    durations: list = None       # ms per frame when the input had them (GIF)
    bg: tuple = None             # the solid background colour the input had, keyed to transparent
    source: str = ''             # the sheet/GIF file, when frames came from one
    subdir: str = ''             # its folder under the input folder: written to the same place under the output


@dataclass
class Finding:
    check: str
    frames: list
    measured: float
    threshold: float
    severity: str                # "low" | "mid" | "high"
    region: str                  # "body" | "effect" | "whole"
    note: str


@dataclass
class Change:
    id: str                      # "c1", "c2" ... stable per run, used by --accept
    check: str
    frames: list
    action: str                  # plain words: "dropped frame 2, held frame 4"
    result: str                  # "fixed" | "still failing" | "proposed"
    data: dict = field(default_factory=dict, repr=False)
