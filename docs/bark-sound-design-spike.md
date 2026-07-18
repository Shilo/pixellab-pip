# Bark Sound Design Spike

Last reviewed: 2026-07-16.

Purpose: record how the original `skills/pixellab-pip/assets/bark.wav` was built, the auditory-display and bioacoustics research behind its replacement, the candidate sounds generated from that research, the adversarial verification that found real defects in them, and the measurement methodology — including the traps that produced three wrong answers along the way. This is a research spike for sound design and evidence. It is not a canonical agent instruction contract — the bark routing/config/playback contract stays in [`../skills/pixellab-pip/references/bark.md`](../skills/pixellab-pip/references/bark.md).

**Outcome: `bark.wav` was replaced** with the `woof-hush` candidate, chosen by ear from a ranked set of ten, then turned down ~9.85 dB after it proved too loud in use. See [Outcome](#outcome) and [Loudness](#loudness). Mascot identity context lives in [`pip-mascot.md`](pip-mascot.md).

## Why This Matters

The bark fires after every live PixelLab generation, edit, and animation job. That is a high-frequency, low-priority confirmation cue, played at a moment of relief rather than urgency. Material Design's own guidance is that the more often an interaction happens, the less intrusive its sound should be, and Google has publicly described dialing every sound up to maximum personality as coming "at the expense of the user experience" ([Google Design](https://design.google/library/ux-sound-haptic-material-design)). Any bark redesign is therefore constrained more by repetition tolerance than by first-play charm.

## The Original Asset, Reverse-Engineered

This section describes the asset as it stood before replacement. Nothing in the repository generated it: the commit that introduced it added the binary with no synthesis script, so the file itself was the only record. The structure below was recovered by fitting a parametric model to the samples with `scipy.optimize.curve_fit`.

Container: mono, 16-bit PCM, **22050 Hz**, 4629 frames, **210 ms**. Peak `0.6048`, true peak `-4.36` dBTP, `-17.2` LUFS.

Layout: burst 1 from 0–60 ms, roughly 20 ms of silence, burst 2 from 80–170 ms, then trailing silence to 210 ms. Onset-to-onset, that is an **inter-bark interval of 79 ms** (measured with a Schmitt-triggered envelope detector, validated against a known 500 ms gap and a known single beat).

Each burst is **three partials at `f0 x [1, 2.1, 3.4]`** with relative amplitudes `[1, 0.385, 0.154]` under a single shared exponential decay, and an instant onset (no attack ramp).

| Burst | f0 | Partials (Hz) | Relative amps | Decay tau |
| --- | --- | --- | --- | --- |
| 1 | **220.00 Hz** | 220.0 / 462.2 / 748.3 | 1.000 / 0.380 / 0.157 | see below |
| 2 | **165.00 Hz** | 165.0 / 346.5 / 561.0 | 1.000 / 0.385 / 0.153 | see below |

**The decay is not a clean exponential, and no single tau should be quoted for it.** A whole-waveform parametric fit returns ~46/52 ms; a log-envelope slope fit returns anywhere from 26 ms to 70 ms depending on which dB range is fitted; an independent adversarial re-measurement returned ~35/36 ms. The spread *is* the finding — the envelope departs from a single exponential, which is also the most likely source of the residual noted below. Any reconstruction should match the measured envelope rather than assume one time constant.

Free-parameter fit residuals: **-16.7 dB** (burst 1) and **-20.8 dB** (burst 2). Both bursts recover the same partial ratios (`2.101`/`3.402` and `2.100`/`3.400`) and the same relative amplitudes, so this is one synthesis function called twice with a different `f0`. The residual that remains is consistent with the onset shape not being a pure exponential from `t=0`.

Three structural facts follow:

- **`220.00 -> 165.00 Hz` is exactly `4:3`, a descending perfect fourth.** The interval is deliberate, not incidental.
- **`1 : 2.1 : 3.4` is inharmonic.** A harmonic series would be `1 : 2 : 3`.
- **The 79 ms interval is textbook for a notification gesture, and only looks wrong if you read the sound as a dog.** See [Beat Count And Spacing](#beat-count-and-spacing) — this was initially recorded here as a defect, and the shipped-sound corpus overturned that. It is *not* one of the defects, and was carried forward unchanged into two candidates.

The inharmonicity is measurable, not cosmetic. A harmonic replica of the same sound (same `f0`, same amplitudes, same decay, same sample rate) measures **40 dB** harmonic-to-noise ratio; the real file measures **13.6 dB**. Three independent literatures treat that direction as a cost: Brewster lists "irregular harmonics" among the properties that make a sound attention-grabbing, Edworthy found irregular harmonic frequencies raise perceived urgency, and Pongracz found low harmonic-to-noise ratio is the strongest acoustic predictor of a bark being rated angry. The effect is mild — only three partials, all low — but it points the wrong way.

Together with the **descending** interval — every shipped task-complete sound measured for this spike rises, see [Beat Count And Spacing](#beat-count-and-spacing) — the inharmonicity is one of exactly two properties of the original that survived scrutiny as a defect. Both are corrected in the shipped replacement; see [Outcome](#outcome).

### Analysis Caveat Worth Recording

The first pass at this analysis concluded the file was "a sine plus one octave harmonic" and reported harmonic 3 at `-57 dB`. That was wrong, and the reason is instructive: the probe assumed a harmonic series and sampled the spectrum at `3 x f0 = 513 Hz`, where the real partial sits at `561 Hz`. A 50 ms Hann window has a main lobe roughly 80 Hz wide, so the peak locations were also inside the error bars. Recovering the true structure required a high-resolution FFT with quadratic peak interpolation, followed by a curve fit. **Do not probe for harmonics at assumed harmonic positions when inharmonicity is the open question.**

## Research Findings

Two independent research passes were run: one on notification-sound standards and psychoacoustics, one on bark bioacoustics and synthesis DSP.

### The Central Conflict

The two passes returned contradictory headlines, both citing Pongracz:

- **[Pongracz et al. 2006](https://www.sciencedirect.com/science/article/abs/pii/S016815910500420X)**: low pitch scored aggressive; high and tonal scored non-aggressive.
- **[Jegh-Czinege, Farago & Pongracz 2019](https://real.mtak.hu/149699/1/Jegh-CzinegeFaragoPongracz-2019-Bioacoustics.pdf)**: low-pitched (401–531 Hz) and tonal barks were rated **least annoying and happiest**; high-pitched and harsh scored highest annoyance.

These reconcile once the measured quantity is separated. The 2019 annoyance study measured **F0**. [Yin 2002](https://cattledogpublishing.com/wp-content/uploads/2022/01/Yin2002Barking.pdf) — 4,672 barks — measured the **dominant frequency**, i.e. the loudest harmonic, reporting play barks at 840 Hz mean and 272 ms. Both are satisfied simultaneously by:

> **F0 around 415–520 Hz, with the spectral energy peak on harmonic 2 (roughly 830–1046 Hz).**

Putting the amplitude peak on harmonic 2 rather than the fundamental is the non-obvious move that buys a friendly F0 and a play-bark brightness at the same time.

The axis that survives both readings is **tonality**: harsh reads hostile regardless of pitch. This is Morton's motivation-structural rule ([Morton 1977](https://www.journals.uchicago.edu/doi/abs/10.1086/283219)), and humans apply the same rules to synthesized sounds ([Farago et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC3917336/), [Sci. Rep. 2024](https://www.nature.com/articles/s41598-024-68165-5)).

### Numeric Constraints

From [Brewster, Wright & Edwards (HCI'95)](https://www.dcs.gla.ac.uk/~stephen/papers/HCI95.pdf), experimentally derived earcon guidelines:

- Max pitch **5 kHz**; min pitch **125–150 Hz**.
- Min note length **82.5 ms**, or **30 ms** for a 1–2 note earcon.
- Use timbres with multiple harmonics; simple sine or square tones "are not effective".
- "Great care must be taken over the use of intensity because it is the main cause of annoyance due to sound."
- Attention-grabbing properties, to be avoided for routine cues: high pitch, wide pitch range, **rapid onset and offset times**, irregular harmonics, atonal or arrhythmic sounds.

Psychoacoustic thresholds:

- **Sharpness**: `S = 1.75 acum` is the threshold below which sharpness contributes nothing to Zwicker psychoacoustic annoyance. Design below it ([INTER-NOISE 2019](https://www.sea-acustica.es/INTERNOISE_2019/Fchrs/Proceedings/1503.pdf)).
- **Roughness**: peaks at **~70 Hz** modulation rate; the roughness band is **~15–300 Hz**. No amplitude modulation, vibrato, or tremolo anywhere in that band. A strictly harmonic series at F0 ~450 Hz is roughness-safe by construction, because adjacent partials are spaced far wider than a critical band below 2 kHz.
- **Ear sensitivity**: ear-canal resonance ~2.5 kHz amplifies by 10–15 dB; peak sensitivity 3.5–4 kHz. Energy in **2–5 kHz** buys perceived loudness and annoyance together.
- **Accessibility**: presbycusis and noise-induced loss hit hardest at **2–4 kHz**. Guidance is to keep meaningful tones under ~2.5 kHz and never rely on content above 8 kHz.

The anti-annoyance spec and the accessibility spec coincide: F0 ~450 Hz with harmonics through ~2.5 kHz satisfies both.

Alarm-mimicry avoidance: IEC 60601-1-8 medical alarms are pulse bursts of **3** (medium priority) or **5** (high priority) pulses, and the standard asks that non-medical sounds not resemble them ([Digi-Key](https://www.digikey.com/en/articles/iec-60601-1-8-guidance-for-designing-medical-equipment-alarms)). Use **2** barks — not 3, not 5 — and do not loop until acknowledged.

Level: true peak **at or below -1 dBTP**; **-16 LUFS** is the common mobile reference (AES). Brewster's narrow-intensity-range rule matters more than the absolute target.

### Bark Bioacoustics

- Single bark duration **38–137 ms** ([Yin & McCowan 2004](https://cattledogpublishing.com/wp-content/uploads/2022/01/YinMcCowan04.pdf)); a 2025 corpus normalizes to a **232 ms** median ([arXiv 2509.18375](https://arxiv.org/pdf/2509.18375)).
- Inter-bark interval: **0.5 s** rated least annoying / happiest; **0.1 s** most annoying (2019 study).
- **Formant dispersion (dF) is the size cue, and the main "dog not human" lever.** Small dogs: dF **2658 ± 232 Hz**; large dogs: dF **671 ± 253 Hz** ([PLOS ONE 2010](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0015175)). Vocal tract length correlates with body mass and inversely with dF ([Riede & Fitch 1999](https://journals.biologists.com/jeb/article/202/20/2859/8241/Vocal-tract-length-and-acoustics-of-vocalization)).
- Via the quarter-wave tube model (`dF = c/2L`, `F_n = (2n-1)·dF/2`, c = 35000 cm/s), a small-dog dF of 2658 Hz implies a 6.6 cm tract and formants at **1329 / 3987 / 6645 Hz**. A human male sits at roughly 500 / 1500 / 2500 Hz. **A small dog's F1 is above a human's F2** — formants at 500/1500/2500 synthesize a person; widening dF shrinks the animal.
- Nonlinear phenomena (deterministic chaos, subharmonics, biphonation) occur in real barks ([Riede et al. 2001, JASA](https://pubs.aip.org/asa/jasa/article/110/4/2191/547345/The-harmonic-to-noise-ratio-applied-to-dog-barks)) and read as aggressive. Omit them.

### The Design Tension

Dog-ness wants wide formant dispersion, which pushes F2/F3 into 2.7–6.6 kHz. Non-annoyance and accessibility want a hard roll-off above ~2.5 kHz. **These directly conflict**, and the conflict has no single correct answer — it is the axis the candidate set was built to explore. The candidates trade some dF away by keeping F2 present but attenuated (-8 to -12 dB) and rolling off above it.

### Repetition Tolerance

Berlyne's inverted-U (Wundt curve) is the governing model for the novelty-gag failure mode: hedonic value peaks at intermediate arousal potential and complexity. Positive habituation starts immediately, tedium starts later, and their sum produces an inverted-U against familiarity ([Chmiel & Schubert 2017](https://journals.sagepub.com/doi/full/10.1177/0305735617697507)). A gag is high-arousal, low-complexity: it front-loads its appeal and then decays.

The practical consequence is a required test rather than a guideline. Sonic-branding practice is to audition sounds as extended loops specifically to check they do not become annoying with exposure ([A-MNEMONIC](https://a-mnemonic.com/sonic-branding-frameworks/)). **First-play impression does not predict play #100, and play #100 is the operating condition for this asset.**

## Candidates

Two rounds were rendered, both local-only and gitignored, each candidate accompanied by a 12x repetition file for the Berlyne loop check.

### Round One: Exploration (`.local/bark-candidates/`, nine candidates)

Round one spanned the design space before the shipped-sound corpus was gathered. It is superseded, and is retained only for context. Its candidates ranged across the dog-to-chime axis (`c2-boof-falling` most canine, `c3-chime-dog` most tonal), tested descending against rising intervals, and used 250-450 ms inter-beat intervals derived from the dog-bout literature. The corpus survey later showed that 430-450 ms is wider than anything shipped, which retired most of the round.

Two round-one candidates survived into round two: `c7-gesture-rising` and `c8-heritage-rising`.

### Round Two: The Final Set (`.local/bark-final/`, ten candidates)

Round two applied every rule the research produced, with **surviving repetition as the primary objective**, since this asset fires after every generation. Candidates are prefixed with their recommended rank. `dsp.py`, `synth.py`, and `final.py` in that folder regenerate everything deterministically — verified by re-running and reproducing every WAV byte-for-byte.

| Candidate | Character | Concept |
| --- | --- | --- |
| `01-boof-third` | dog | Rising major third (415 -> 523) at Xbox's 85 ms spacing. |
| `02-woof-hush` | dog | **Shipped.** Softest attack, hard 2.2 kHz roll-off, minimal breath, rising minor third. |
| `03-heritage-rising` | chime | The original asset harmonised and inverted to rise. Cleanest spectrum of the set. |
| `04-boof-single-tail` | dog | One boof plus a legato tonal tail (the macOS single-strike position). |
| `05-pup-warm` | dog | Dark, warm, slowest attack. |
| `06-chime-pup-fourth` | hybrid | Voice under a marimba, rising perfect fourth. |
| `07-boof-minor-third` | dog | Gentlest rising interval. |
| `08-gesture-rising` | dog | Round-one survivor. Rising perfect fourth. |
| `09-boof-beats` | dog | Two distinct beats at AOSP's 125 ms rather than one gesture. |
| `10-marimba-pup-octave` | chime | Xbox's exact structure: rising octave, dog voice recessed to -13 dB. |

Design decisions specific to round two, each traceable to a finding:

- **Rising intervals throughout.** Every shipped task-complete sound rises.
- **Spacing 85-125 ms.** The shipped convergence, not the dog-bout 450 ms.
- **The interval is capped for a dog voice.** From F0 = 415 Hz, only a minor third (493 Hz) or major third (523 Hz) keeps the second beat inside Pongracz's 401-531 Hz friendly band. A perfect fourth reaches 553 Hz; an octave reaches 830 Hz, landing in the *most-annoying* band. Chime-forward candidates carry no F0-aggression semantics and may take the wider Xbox/Slack intervals, which is why `10` can use an octave safely while `08`'s fourth is marginal. **This reasoning was later partly refuted; see [Verification](#verification).**
- **Repetition levers applied set-wide:** attacks 16-22 ms nominal, breath noise -24 to -30 dB, centroids 650-1300 Hz, roll-off 2.2-2.9 kHz, no exaggerated sweeps, no gag gestures. Charm from timbre, never from a joke: a gag front-loads its appeal and then decays.
- **Brewster's closure rule:** beat 1 accented, beat 2 longer, so the pair reads as one closed unit.

### Measurements

| Candidate | Beats | IBI | Duration | True peak | Centroid | Sharpness | HNR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01-boof-third` | 2 | 86 ms | 340 ms | -4.51 dBTP | 791 Hz | 0.90 | 13.8 dB |
| `02-woof-hush` | 2 | 101 ms | 370 ms | -5.11 dBTP | 694 Hz | 0.86 | 14.9 dB |
| `03-heritage-rising` | fused | 79 ms | 349 ms | -7.61 dBTP | 268 Hz | 0.46 | 40.0 dB |
| `04-boof-single-tail` | 1 | — | 300 ms | -4.00 dBTP | 1074 Hz | 1.02 | 15.2 dB |
| `05-pup-warm` | 2 | 91 ms | 345 ms | -4.94 dBTP | 696 Hz | 0.85 | 14.5 dB |
| `06-chime-pup-fourth` | fused | 85 ms | 465 ms | -7.91 dBTP | 1296 Hz | 1.27 | 24.2 dB |
| `07-boof-minor-third` | 2 | 96 ms | 350 ms | -4.57 dBTP | 784 Hz | 0.89 | 13.8 dB |
| `08-gesture-rising` | 2 | 85 ms | 335 ms | -4.32 dBTP | 811 Hz | 0.92 | 13.3 dB |
| `09-boof-beats` | 2 | 126 ms | 385 ms | -4.02 dBTP | 796 Hz | 0.91 | 13.8 dB |
| `10-marimba-pup-octave` | fused | 85 ms | 485 ms | -8.44 dBTP | 653 Hz | 0.84 | 33.2 dB |
| *(original `bark.wav`)* | *2* | *79 ms* | *210 ms* | *-4.36 dBTP* | *251 Hz* | *0.40* | *13.6 dB* |

An automated gate reported all ten clearing every hard rule. **That gate was substantially wrong.** See [Verification](#verification).

## Verification

The final set was handed to an independent adversarial verifier, instructed to write its own measurement code from scratch (reusing this spike's `dsp.py` would inherit its bugs), to validate every metric against known-answer signals first, and to hunt for violations rather than confirm compliance. It found real defects. Everything below was independently reproduced before being accepted.

### The Compliance Gate Was Theatre

- **HNR cannot detect inharmonicity.** Demonstrated directly: an inharmonic `1 : 2.1 : 3.4` stack reads 12.7 dB and a harmonic `1 : 2 : 3` reads 39.6 dB, but a wide-lag autocorrelation search launders the difference away. The HNR gate was **blind to the exact defect it existed to catch**, which is how an inharmonic candidate passed it.
- **The self-check passed for the wrong reason.** `dsp.py`'s `demo()` used an HNR test signal mis-specified by 6.02 dB, with a tolerance of +/-6.0 dB — exactly wide enough to hide it. The validation built to prevent this class of error contained the same class of error.
- **Sharpness in acum is not absolutely testable on a file.** Acum is defined at a real SPL, and a WAV carries no SPL reference. The values are usable as *ordering only*; "< 1.75 acum" is not a test that can be run against an audio file.
- **"No AM in 15-300 Hz" is unsatisfiable.** A percussive envelope's broadband skirt puts energy across that band by construction: a 19.5 ms decay alone lands -18.7 dB at 70 Hz. The rule measures envelope bandwidth, not roughness.

### Real Defects Found

- **The loudness match was fake.** All ten reported -18.50 LUFS with a 0.01 dB spread. That is an artifact of measuring whole-file LUFS on sounds that are mostly trailing silence: 300 ms of padding alone shifts the number by 3 dB. Measured on the audible body, the spread is **4.95 dB**. Since intensity is the single documented annoyance driver, the A/B comparison was never fair, and louder candidates would have read as better for the wrong reason.
- **Two candidates were inharmonic — the exact defect under repair.** `pup()` sweeps f0 while `fm_tone()` is static, so voice and tail are in tune only at t=0; the ratio slides 1.56 -> 2.30 across the sound. `04-boof-single-tail` measures h2/h1 = **1.7679** (deviation 0.23) against the original asset's 2.1012 (deviation 0.10) — **2.3x worse than the sound it was replacing**. `06` is likewise inharmonic. Both were cut.
- **`decay_ms` is not a decay time.** `adsr()` computes `tau = decay_time / (40/8.686)`, so `decay_ms=90` yields **tau = 19.5 ms**. At 85 ms spacing, beat 1 is already 37.8 dB down. The claim that the beats "fuse into one gesture" is **false**: six of the ten are two discrete hits, and the rationale given for the 55-135 ms spacing did not apply to the sounds built on it. The spacing is still conventional — Discord at 95 ms and Skype at 100 ms are also discrete hits.
- **Beat 2 is outside the friendly band in every dog candidate** (539-613 Hz). The interval-cap reasoning above used *nominal* f0 and ignored the synth's own +28% contour overshoot, making the major-third argument arithmetic on a number the synth never produces. Nothing reached the 732-1833 Hz most-annoying band, so the error was not fatal.
- **The h2 energy peak — the headline design goal — is not achieved on 8/10.** h2 sits 7.1-11.5 dB *below* h1.
- **`finish()` waveshapes every candidate.** `softclip(x, 1.6)` maps 0.5 -> 0.72, which is compression, not a safety limiter. It brightens the spectrum and shortens attacks *after* formant levels are set precisely, so the shipped spectrum is not the one the formant spec describes.

### Why The h2 Miss Was Not Worth Fixing

The verifier attributed the h2 miss to `dog_stages` placing its t=0 formant at `f1*0.55`, landing on h1. **That diagnosis is incomplete.** Parking the formant on h2 for the entire sound was tested directly, and changes almost nothing: centroid 692 -> 696 Hz, sharpness 0.86 -> 0.86, h2 still 8.2 dB below h1.

The actual cause is the **source spectral tilt**. The glottal source uses 1/n rolloff plus -9 dB/oct of additional tilt, putting h2 roughly 15 dB below h1 before any filter is applied. No formant placement recovers that; only flattening the source tilt would, and that produces a brighter, buzzier sound.

That is the decisive point. **Brightness is the annoyance direction** — the 2-5 kHz sensitivity peak, sharpness, and Pongracz's high-F0 finding all point the same way. Achieving the h2 goal would move the sound *toward* the annoying end. The h2 peak was an instrumental goal whose purpose was to land the sound dark but bright enough; the outcome landed by another route. The miss serves the primary objective, so it was left alone.

### The Original Asset, Re-Adjudicated

The verifier independently confirmed the reverse-engineering **exactly**: partials at `1 : 2.1000 : 3.4000`, amplitudes `1 : 0.384 : 0.154`, f0 `220.01 -> 165.00`, ratio exactly `0.7500`, spacing `78.5 ms`, onset `0.41 ms`.

It refuted the decay figure, and re-measurement showed that neither party should assert one — see the decay note in [The Original Asset, Reverse-Engineered](#the-original-asset-reverse-engineered). The envelope is not a single exponential.

## Outcome

**`02-woof-hush` shipped**, chosen by ear from the ranked set. It replaced `bark.wav` as-is: no rebuild, no gain change.

| | original | `woof-hush` |
| --- | --- | --- |
| Partials | `1 : 2.1 : 3.4` (**inharmonic**) | strict harmonic series |
| Interval | descending perfect fourth | **rising minor third** |
| Attack | **0.41 ms** (instant) | 8.5 ms |
| Centroid | 251 Hz | 694 Hz |
| Format | 22050 Hz, 210 ms, 9,302 B | 44100 Hz, 370 ms, 32,678 B |
| Peak sample | 0.605 | 0.555 |
| Body loudness | -15.77 LUFS | -14.15 LUFS (**+1.62 dB**) |

Both defects that survived scrutiny — the inharmonic partials and the inverted interval — are corrected, and peak amplitude is *lower* than the original. Playback was verified through the bundled helper (`bark.py play` returns `played: true`; `winsound` handles 44.1 kHz), and `dev-tools/qa.py` passes. The repo's WAV gate only checks for a non-empty file, so the format change is safe.

Two decisions worth recording, both deliberate:

1. **Not rebuilt.** `woof-hush` carries the h2 miss, the non-fused beats, and the contour overshoot. None is an audible defect. The h2 miss makes it darker, which is the safe direction; the fusion claim was an error in prose rather than in the file; and the contour overshoot lands beat 2 at 539 Hz, 8 Hz past a band edge drawn from a study that tested a few discrete levels. That is 0.26 semitones, and not perceptible as a category change.
2. **Shipped +1.62 dB hotter than the original**, chosen by ear at that level. This was flagged as the one property to watch, and in real use it proved too loud — corrected in a follow-up pass; see [Loudness](#loudness).

The general lesson: **a human listening is a better instrument than any metric in this document.** The metrics exist to narrow the field to plausible candidates and to catch what an ear misses — inharmonicity, clipping, DC, loudness confounds. They do not decide.

## Loudness

After living with the shipped sound, it was reported **too loud** relative to subtle reference chimes (the Claude desktop notification was cited). The audition that selected `woof-hush` was run under an unfair loudness match (see [Verification](#verification)), so the level was never actually vetted — this closed that gap. Two independent lines of research were run and **converged on the same target**.

### The Level Was Objectively Hot

A survey measuring shipped notification sounds with a validated BS.1770 meter (Windows on-machine, macOS/iOS/Android from public mirrors) placed the sound near the loud end of the distribution:

- The **subtle, well-regarded cluster** — macOS Purr, Frog, Pop, Ping, Glass, Bottle, Basso, Sosumi, Submarine; iOS Chord, Note, Bamboo, Pulse — sits at **body median -23.0 LUFS** (range -27.5 to -21.2), RMS median -31.6 dBFS, true peaks -8 to -15 dBTP (never maximized).
- The shipped bark measured **body -14.15 LUFS** — **+8.8 dB above the subtle median**. Its nearest neighbours were Android TaDa, Android Ariel, and iOS sms-received4: deliberately attention-grabbing tones, not gentle ones.
- Android Material and Discord sounds form a separate loud tier (body -7 to -11, true peaks pinned at 0.0 dBTP, brick-wall limited) — engineered to cut through, the opposite of the goal here.

The one thing already right: true peak -5.11 dBTP left healthy headroom, so the sound was loud but clean, never clipped.

### Why -23/-24 And Not Higher

Standards research reached the same number by a different route, and every adjustment factor pointed the same way — quieter:

- **No published standard exists for "short UI success-sound loudness."** Integrated LUFS targets (-16 mobile, -23 EBU R128, -14 streaming) are *program-loudness* figures for long-form content measured over minutes; a 370 ms one-shot is a single event inside a mix, not a stream. The relevant question is how far *below* the app's notification reference the cue sits, which is qualitative in every HIG.
- **Apple HIG:** UI sound "has a much lower volume than a notification sound… keep it very quiet… a very subtle layer."
- **Material:** frequency-of-use scales intrusiveness *down*; a constantly-heard cue should be quieter and duller than a rare alert.
- **Percussive penalty:** an impulsive sound is rated as annoying as a steady tone **7.1 dB louder** ([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0360132319307516)). A two-beat bark is percussive, so it should sit *below* a smooth chime at equal meter reading, not level with it.
- **High-frequency = more annoying** at equal loudness — another reason to bias down.
- **Playback path.** Other apps' notification sounds are ducked by the OS notification system; part of why the Claude chime *feels* quiet is that management. The bundled helper plays through `winsound` (and `afplay`/`paplay`) **directly, at source level with no ducking**, so the authored level *is* the playback level. The file must therefore be authored conservatively quiet to match the perceived level of a sound that gets OS volume management for free.

The **under-signalling floor** is roughly -26 LUFS body: below that a 370 ms high-frequency cue starts disappearing under room noise on quiet speakers. The defensible window is **-23 to -26**; the two research lines centre it at -23, and the adjustment factors push toward the quiet end.

### Decision

**Shipped at body -24 LUFS** — a flat -9.85 dB gain on the selected sound. `-24` is the convergent -23 nudged 1 dB toward the quiet end (justified by the percussive penalty, the no-ducking playback path, and the user's clear "far too loud" signal), while staying 2 dB above the -26 floor.

| | before | after (-24) | subtle-cluster target |
| --- | --- | --- | --- |
| Body LUFS | -14.2 | **-24.0** | -23.0 median |
| Body RMS | -13.5 dBFS | -23.4 dBFS | -31.6 median |
| True peak | -5.1 dBTP | -15.0 dBTP | -8 to -15 |
| Peak sample | -5.1 dBFS | -15.0 dBFS | — |

Method notes, each a deliberate choice:

- **Flat gain, no limiter or compressor.** A limiter would squash the percussive transient — dulling the "bark" *and raising* perceived loudness relative to peak, the opposite of the goal. A linear multiply preserves the crest factor intact.
- **Measured on the audible body, not the whole file.** Integrated LUFS is gated in 400 ms blocks; at 370 ms the sound is shorter than one block, so the whole-file -18.5 figure is degenerate and was ignored. `ffmpeg loudnorm` is the wrong tool for the same reason.
- **One residual mismatch, left alone.** Even at body -24, the bark's body RMS (-23.4) sits far above the subtle cluster's (-31.6) because it is *more sustained* — RMS only ~1 dB under its body LUFS, where the cluster sounds are 8-9 dB under. Body LUFS is the perceptual-loudness match, so loudness is handled; the extra sustained energy reads as a fuller *character*, not more volume. Shortening the sound would close it, but that is a rebuild, not a level change.

A gain ladder from body -16 to -24 is in `.local/bark-volume/` for re-auditioning; moving the ship level is a one-line change of the target constant.

## Beat Count And Spacing

This section supersedes an earlier conclusion in this spike. The original reasoning applied the dog-bout literature directly and concluded the current asset's 79 ms interval was a defect, and that a replacement should use a ~450 ms interval. **A survey of shipped notification sounds overturned both claims.** The correction is recorded rather than quietly edited out, because the failure mode is reusable: bark bioacoustics and notification-sound convention give opposite answers, and which one applies depends on what the sound reads as.

### Does Beat Count Drive Annoyance? No.

**No rigorous evidence was found that multi-event sounds are more annoying than single hits.** This is a negative result and is recorded as one. The documented annoyance drivers are:

- **Intensity.** Brewster, citing Berglund: *"Great care must be taken over the use of intensity because it is the main cause of annoyance due to sound."*
- **Alert frequency and relevance.** The notification-fatigue literature is entirely about volume of alerts and usefulness, not acoustic structure.
- **Duration, via audio ducking.** Apple, [WWDC17 §803](https://developer.apple.com/videos/play/wwdc2017/803/): *"If your notification sound is too long, it ducks for a very long time, so it becomes annoying."* That penalises *long*, not *multi-onset* — two notes 85 ms apart are shorter than one note with a 1.5 s tail.

Note count is not on the list. The concern that "two beats is more annoying than one" is not supported by the evidence found.

### What Ships

Measured from actual shipped audio (Windows media folder on a Win11 26200 machine; AOSP `.ogg` from `android.googlesource.com`; Xbox's official master file; Slack's `slack_sfx` archive; macOS/iOS system sounds hash-verified across two independent archives):

| Sound | Events | Interval | Direction | Category |
| --- | --- | --- | --- | --- |
| **Xbox 360 achievement** | 2 | **85 ms** | D5 -> D6, rising octave | task complete |
| **Slack `complete_quest_requirement`** | 2 | **58 ms** | E6 -> A6, rising perfect fourth | task complete |
| **iOS Tri-tone** (origin: CD-burn complete) | 3 | ~115, ~100 ms | D4 -> A4 -> D5, rising 1-5-8 | task complete |
| Discord `message1` | 2 | 95 ms | G4 -> G5, rising octave | message |
| Skype message | 2 | 100 ms | — | message |
| Messenger "pop ding" | 2 | 100 ms | rising pop -> C7 ding | message |
| Teams chat | ~2 | ~110 ms | — | message |
| Google Chat | 2 | 125 ms | G3 -> G5, octave | message |
| Windows Notify Messaging | 3 | ~115, ~120 ms | C5 -> G4 -> C4, descending | message |
| Windows Notify Calendar | 3 | ~115, ~225 ms | C4 -> F4 -> C5, ascending | reminder |
| AOSP notification set (n=17) | **10 are 2 events, 7 are 1, none are 3+** | median 160 ms | — | notification |

Four findings converge:

1. **Two events is the modal choice**, and the standard one for task-complete specifically. Apple's own default alert went 3 (Tri-tone) -> 1 (Note) -> **2** (Rebound, iOS 17).
2. **The interval clusters at ~60–130 ms**, not 450 ms. This is the strongest convergence in the whole dataset, and it holds across vendors who did not coordinate. At that spacing the events overlap into **one gesture**, not two beats.
3. **Task-complete sounds rise.** Xbox (octave), Slack (perfect fourth), Tri-tone (1-5-8) all resolve upward. Rising broadly reads as arrive/complete, falling as leave/end.
4. **The motif is short; the tail is free.** Every onset lands in the first ~250–500 ms; file durations of 1–2 s are almost entirely decay. "How long is the sound" and "how long is the motif" are different questions.

### Why This Conflicts With The Bark Literature

The two bodies of evidence give **opposite answers to the same parameter**:

| | Says | Interval |
| --- | --- | --- |
| Dog bioacoustics (Pongracz 2019) | tight bouts read aggressive | **450–500 ms** |
| Shipped notification sounds | tight clusters read as one gesture | **60–130 ms** |

The resolution is that the bark finding is **conditional on the sound reading as a dog**. A chime motif at 100 ms carries no aggression semantics, because a chime is not an animal. Tight-bout-means-aggression only fires if the listener hears a bark bout in the first place.

That yields the design rule:

- **The more convincingly canine the timbre, the more the ~450 ms interval is required** — and the less the sound resembles anything that ships. Round one's `c2-boof-falling` sat at this extreme, with real formants and a ~640 ms total.
- **The more chime-like, the tighter the cluster can go**, up to the shipped 55-135 ms.
- **One beat sidesteps the conflict entirely**, since there is no interval to get wrong.

Round two resolved this by keeping real formants but rolling brightness off hard, then taking the shipped tight spacing anyway — betting that a *stylized* bark does not trigger the bark-bout reading that a recorded dog would. That bet is unverified: no study tests whether a synthetic, formant-light bark at 100 ms reads as aggressive. It is the largest untested assumption in the design.

**The original asset sat on the chime side of this line.** It had no formants, so it did not read as a dog, so the bark-bout finding did not apply to it — and its 79 ms interval is almost exactly Xbox's 85 ms and Slack's 58 ms. It was not misconfigured; it was a conventional two-note notification gesture that happened to be *called* a bark. Its questionable property was direction, not spacing.

One conflation avoided: Farago's "shorter calls rated more positive" refers to the individual vocalization, not the bout, so it does not discriminate between one beat and two.

Brewster, directly actionable for any two-beat design: *"the first note should be accented (played slightly louder) and the last note should be slightly longer"* — so it reads as one closed rhythmic unit.

### Counter-Evidence

Under-signalling is a real failure mode. Apple's move to the gentler two-note Rebound drew complaints that it was less noticeable, and **iOS 17.2 added customization so users could restore Tri-tone**. Quieter and smoother is not monotonically better.

### Final Ranking

Ranked on: survives repetition (dominant) > dog character > standards margin. This ordering is the filename prefix in `.local/bark-final/`. It was produced **before** any audition and after the adversarial verification, and it is a prior rather than a verdict.

| # | Candidate | Body LUFS | Attack | Why |
| --- | --- | --- | --- | --- |
| 1 | `woof-hush` | -14.2 | 8.5 ms | Best dog character that survives repetition. Softest attack of the paired set, beat 2 closest to the friendly band (539 Hz), centroid 694. |
| 2 | `heritage-rising` | -17.3 | 3.2 ms | Cleanest spectrum in the set (centroid 268, sharpness 0.46, harmonic to deviation 0.003). Demerits: 3.2 ms onset, barely reads as a dog, 165 Hz thins out on small speakers. |
| 3 | `pup-warm` | -14.2 | 8.8 ms | Slowest attack in the set; dark and low-arousal. |
| 4 | `boof-minor-third` | -13.7 | 8.2 ms | Gentlest rising interval. |
| 5 | `boof-third` | -13.6 | 8.2 ms | Beat 2 at 592 Hz, further out of band than 1-3, and runs hot. |
| 6 | `marimba-pup-octave` | -17.9 | 1.0 ms | Harmonic and dark, but the sharpest onset in the set — 1 ms is squarely Brewster's attention-grabber. |
| 7 | `boof-beats` | -13.0 | 8.1 ms | Loudest by body level; its -53 dB trough reads as two separate events rather than one. |
| 8 | `gesture-rising` | -13.5 | 7.1 ms | Hot, and the highest beat-2 F0 of any candidate (613 Hz). |
| — | `boof-single-tail` | -17.5 | 3.0 ms | **Cut: inharmonic** (h2/h1 = 1.77), worse than the asset being replaced. |
| — | `chime-pup-fourth` | -17.9 | 2.0 ms | **Cut: inharmonic**, brightest (1296 Hz), sharpest (1.27), 2 ms onset. |

**The Body LUFS column is the reason this ranking is weaker than it looks.** The set spans 4.95 dB in body loudness despite every file reporting -18.5 whole-file. Intensity is the documented annoyance driver, so an audition of this set partly measures that defect: the quiet candidates seem gentler than they are, and the hot ones more annoying. Ranks 1 and 2 sit ~3 dB apart and are not separated by these numbers.

**Attack times are all below the stated 12 ms rule.** This is definitional rather than a defect in the sounds: a raised-cosine attack's 10-90% rise is 0.5904x its nominal length, and `finish()`'s waveshaping shortens it further. The 12 ms figure was always an interpolation rather than a citation. For scale, the asset being replaced has a 0.41 ms attack.

The literature does **not** settle rising versus falling in general — rising correlates with higher arousal, and falling reads final. It is settled for *this* category: every measured task-complete sound rises, and rising to a consonant target (Xbox's octave, Slack's fourth) is both energetic and resolved, so finality is not traded away.

## Measurement Methodology

Measurement code is `dsp.py` in the candidate folder; `python dsp.py` runs a self-check that validates every metric against signals with known answers (calibrated harmonic-plus-noise mixes, pure tones, band-limited noise, a decaying tone, and the int16 round-trip).

**Six measurement errors were made across this spike.** Every one produced a confident wrong answer that survived until something forced a cross-check. They are recorded in full because the traps are generic, not specific to bark sounds.

1. **Spectral analysis over an amplitude-thresholded selection.** Gathering "the loud samples" with `x[abs(x) > threshold]` concatenates non-contiguous regions. Each join is a step discontinuity that smears broadband energy across the spectrum. This inflated centroid and sharpness for every candidate. Fix: analyze one contiguous window from the voiced body of the loudest event.
2. **Moving-average HNR with the window narrower than the spectral peaks.** A 10-bin moving average over a 2.7 Hz/bin spectrum spans 27 Hz, but a 50 ms Hann window produces peaks ~80 Hz wide, so the "noise floor" tracked the peaks themselves and the difference collapsed. The metric reported HNR near 0 dB for provably noise-free signals.
3. **Autocorrelation HNR without envelope flattening.** Autocorrelation assumes stationarity. A percussive exponential decay depresses the correlation on its own, which the metric reports as noise that is not present. Fix: divide out the analytic (Hilbert) amplitude envelope before correlating, with the smoothing window longer than the pitch period.
4. **Whole-file LUFS on short, padded sounds.** Trailing silence is averaged into the measurement, so 300 ms of padding alone shifts the value 3 dB. This produced a reported 0.01 dB loudness match across a set whose real body-level spread was 4.95 dB. Fix: measure loudness on the audible body, or on a fixed short-term window.
5. **A self-check whose tolerance was wider than its own error.** The HNR validation signal was mis-specified by 6.02 dB and checked with a +/-6.0 dB tolerance, so it passed for the wrong reason. A tolerance must be tighter than the error class it is meant to catch, or the test is decorative.
6. **Autocorrelation pitch tracking locking onto subharmonics.** Two candidates read as "falling" and "flat" when both in fact rise; the tracker had locked to half the true f0 (277 = 553/2, 416 = 830/2). The tell was the suspiciously exact ratios (0.667, 1.000). Fix: cross-check pitch with a spectral-peak method before believing a direction.

Three further errors were errors of *definition* rather than measurement, and are worth separating: HNR was used as a harmonicity gate although it cannot detect inharmonicity; sharpness was gated in absolute acum although acum requires an SPL reference a file does not carry; and "no AM in 15-300 Hz" was specified although a percussive envelope violates it by construction. See [Verification](#verification).

The decisive diagnostic in nearly every case was the same: **measure a signal whose answer is already known.** The original `bark.wav` had a numerically verified noise floor near -114 dB, so any metric reporting it as noisy was broken. Synthesizing a provably clean replica at the same sample rate and pitch (which read 40 dB) separated "the metric is biased" from "the file really does contain something aperiodic" — and it was the latter, which is how the inharmonicity was found.

Final metric definitions:

- **HNR**: Boersma (1993) autocorrelation method (Praat's), on the envelope-flattened signal, over a 50 ms window from the voiced body.
- **Sharpness**: Aures / DIN 45692-style, from a Bark-band specific-loudness approximation.
- **LUFS**: ITU-R BS.1770 K-weighting, ungated — short-form sounds defeat the gate, so integrated loudness is unreliable under ~400 ms.
- **True peak**: 4x oversampled peak.
- **Onset / IBI**: Schmitt-triggered envelope, armed only after the envelope falls below a low threshold, so a decaying tail cannot re-fire as a new onset. Counts *re-articulated* hits; legato notes inside a motif read as one.
- **Loudness for comparison**: body-window LUFS, not whole-file.

**Known-good caveat:** an amplitude-onset detector and a note counter answer different questions. 44 of 47 Windows notification sounds have exactly one re-articulated hit, yet most are 2-3 note legato motifs. Both statements are true of the same files. State which is being counted.

### Reproduction Note

Writing 16-bit WAV from numpy has a trap the self-check covers: `+1.0 * 32768` overflows int16 and wraps to `-32768`, turning a full-scale positive peak into a full-scale negative one, and `.astype(np.int16)` wraps silently rather than clipping. Always `np.clip(x, -1, 1)` first and scale by **32767**.

## Open / Untested

- **Loudness was corrected to body -24 LUFS** after the sound proved too loud in use; see [Loudness](#loudness). The residual: even at -24 the bark is more *sustained* than the subtle-cluster reference (body RMS -23.4 vs -31.6), which reads as fuller character rather than louder. Closing that is a rebuild (shorter sound), not a level change, and was not done.
- **Long-run repetition tolerance is unmeasured.** `woof-hush` was chosen from a first-listen audition. The loop files at `.local/bark-final/loop-test/` (12x at 1.2 s) exist for the Berlyne check, and the only real test is days of ordinary use. Nothing in this document predicts play #100.
- **The set was auditioned under an unfair loudness match** (4.95 dB body spread), so the *choice of candidate* may partly reflect which candidates were louder — the [Loudness](#loudness) pass fixed the level of the winner but not the possibility that a different candidate would have won under a fair match. A renormalized re-audition might pick a different sound.
- **Small-speaker reproduction was never tested.** Laptop and phone speakers lose most sub-500 Hz content. This matters most for `heritage-rising` (165/220 Hz), and it is the strongest surviving argument for the harmonic-2 energy peak that the set does not achieve.
- **The h2 energy peak is unachieved across the set** and would require flattening the glottal source tilt, not moving formants. That trade buys dog brightness at the cost of repetition safety; it was declined, not solved.
- Roughness (asper) was never implemented as a metric. The adversarial pass found no discrete AM lines and argued the candidates are clean, but on its reasoning rather than on a measurement.
- The `1 : 2.1 : 3.4` ratio set was not traced to a known synthesis recipe or preset. Whether it was hand-picked or inherited from a tool is unknown.
- Candidate synthesis depends on numpy and scipy. The runtime helper `assets/bark.py` is deliberately dependency-free; if a generator is ever committed it belongs in `dev-tools/`, not in the skill payload.
- Third-party summaries circulate Material Design LUFS figures (-18/-14/-12) and a "sound never lasts more than 0.3 s longer than its animation" rule. Neither could be verified against Material's own documentation, which is JavaScript-rendered. They are excluded from the spec above. Slack's "Knock Brush" has no design rationale that could be located; do not cite one.
- Discord, WhatsApp, Telegram, Messenger, Teams, Zoom and Google Chat sounds were measured from community-extracted copies rather than first-party assets, except Telegram (official source repos). Their identity is one tier below the Windows/AOSP/Xbox/Slack numbers.
