"""Every number a /pga-fix check flags at. Starting values from a 797-animation batch audit (references/animation.md
"Audit before you ship a batch"); calibrated values say so on their line."""
# Calibrated 2026-10 on 818 shipped, hand-approved animations (one game, 96-256 px heroes and champions): checks
# that lead to a paid re-roll (weapons, weird changes, detached, edge) flag about 2% of them; checks whose fix is free
# and harmless (brightness, specks, colour count, pinholes) flag 5-8%, so the known 15-20% bright poses are caught.
T = {
    'edge': 24,            # opaque px on one canvas side
    'detached': 400,       # px in a piece off the main body (a thrown weapon)
    'specks': 30,          # max size of a loose piece counted as a speck
    'specks_px': 100,      # loose body-coloured speck pixels in a frame before it's flagged (shipped art has hair strands, bits)
    'speck_gap': 2,        # a piece this close to the body is part of it (a staff tip after a 1 px gap)
    'ground': 4,           # px the feet sit above the ground line (grounded moves)
    'brightness': 0.20,    # mean brightness off the reference (ratio)
    'palette': 0.07,       # share of the body farther than palette_de from every reference colour
    'palette_de': 0.08,    # OKLab distance counted as "not a reference colour"
    'holes': 40,           # 1 px pinholes (all 8 neighbours opaque) allowed per frame
    'bg_leak': 0,          # px of the keyed background colour inside the body
    'effect_de': 0.15,     # OKLab distance from every reference colour beyond which a pixel is an effect candidate
    'jump_px': 6,          # a step must move at least this far (and 2.5x the median step) to be a jump
    'jump_x': 2.5,
    'mass_pop': 0.25,      # body mass change in one step that comes back within 2 steps
    'gap_x': 3.0,          # a step this many times the median, with calm neighbours = missing in-betweens
    'seam_x': 2.0,         # a loop's last->first step this many times the median
    'return_iou': 0.8,     # a one-shot's last frame vs the reference silhouette
    'flash_px': 20,        # an effect-coloured piece at least this big
    'cell_change': 0.71,  # colour-mix distance of a body cell from both neighbours (they agree with each other)
    'thin_lost': 0.89,     # share of a thin part (staff, blade) gone vs both neighbours = lost
    'thin_broken': 0.81,   # ... at least this share = broken
    'mixels': 0.05,        # share of k x k blocks (at the set's pixel size) that aren't one colour
    'soft_px': 8,          # half-transparent pixels in a frame
    'colour_ratio': 2.5,   # unique colours vs the reference's
    'size_lo': 0.9,        # body height vs the reference's
    'size_hi': 1.1,
    'repair_de': 0.25,     # pixels this close to a reference colour are body (recoloured); farther = effect, untouched
    'washed': 0.4,         # a frame this much brighter than the reference is washed out: not colour-matched
    'hurt_mass': 0.10,     # a hurt in-between with this much extra mass vs frames 0 and 4 is dirty (painted burst)
    'hurt_light': 0.12,    # ... or this much lightness change (darkened body)
    'head_band': 0.14,     # the top share of the reference's body core taken as its head
    'head_miss': 0.36,     # cost of a head pixel over transparency (a 0.6 OKLab miss, squared)
    'head_gap': 0.02,      # head match cost above its worse neighbour (mean squared OKLab), calibrated 2026-10-22:
    'head_x': 1.8,         # ... and this many times it; together they flag 1.0% of the 818 shipped animations
    'prop_side': 0.24,     # share of body width a prop may stray past its first/last-frame span (a warning: 5% of them)
}
