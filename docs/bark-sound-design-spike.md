# Bark Sound Design Spike

Last reviewed: 2026-07-16.

Purpose: record how the bundled `skills/pixellab-pip/assets/bark.wav` is actually built, the auditory-display and bioacoustics research behind a possible replacement, the candidate sounds generated from that research, and the measurement methodology used to compare them. This is a research spike for sound design and evidence. It is not a canonical agent instruction contract — the bark routing/config/playback contract stays in [`../skills/pixellab-pip/references/bark.md`](../skills/pixellab-pip/references/bark.md).

No asset was replaced. `bark.wav` is unchanged; the candidates are local-only pending an audition decision. Mascot identity context lives in [`pip-mascot.md`](pip-mascot.md).

## Why This Matters

The bark fires after every live PixelLab generation, edit, and animation job. That is a high-frequency, low-priority confirmation cue, played at a moment of relief rather than urgency. Material Design's own guidance is that the more often an interaction happens, the less intrusive its sound should be, and Google has publicly described dialing every sound up to maximum personality as coming "at the expense of the user experience" ([Google Design](https://design.google/library/ux-sound-haptic-material-design)). Any bark redesign is therefore constrained more by repetition tolerance than by first-play charm.

## The Current Asset, Reverse-Engineered

Nothing in the repository generated `bark.wav`. The commit that introduced it added the binary with no synthesis script, so the file itself is the only record. The structure below was recovered by fitting a parametric model to the samples with `scipy.optimize.curve_fit`.

Container: mono, 16-bit PCM, **22050 Hz**, 4629 frames, **210 ms**. Peak `0.6048`, true peak `-4.36` dBTP, `-17.2` LUFS.

Layout: burst 1 from 0–60 ms, roughly 20 ms of silence, burst 2 from 80–170 ms, then trailing silence to 210 ms. Onset-to-onset, that is an **inter-bark interval of 79 ms** (measured with a Schmitt-triggered envelope detector, validated against a known 500 ms gap and a known single beat).

Each burst is **three partials at `f0 x [1, 2.1, 3.4]`** with relative amplitudes `[1, 0.385, 0.154]` under a single shared exponential decay, and an instant onset (no attack ramp).

| Burst | f0 | Partials (Hz) | Relative amps | Decay tau |
| --- | --- | --- | --- | --- |
| 1 | **220.00 Hz** | 220.0 / 462.2 / 748.3 | 1.000 / 0.380 / 0.157 | ~46 ms |
| 2 | **165.00 Hz** | 165.0 / 346.5 / 561.0 | 1.000 / 0.385 / 0.153 | ~52 ms |

Free-parameter fit residuals: **-16.7 dB** (burst 1) and **-20.8 dB** (burst 2). Both bursts recover the same partial ratios (`2.101`/`3.402` and `2.100`/`3.400`) and the same relative amplitudes, so this is one synthesis function called twice with a different `f0`. The residual that remains is consistent with the onset shape not being a pure exponential from `t=0`.

Three structural facts follow:

- **`220.00 -> 165.00 Hz` is exactly `4:3`, a descending perfect fourth.** The interval is deliberate, not incidental.
- **`1 : 2.1 : 3.4` is inharmonic.** A harmonic series would be `1 : 2 : 3`.
- **The 79 ms inter-bark interval sits in the measured most-annoying band.** The 2019 study tested inter-bark interval directly: **0.5 s scored least annoying and happiest, 0.1 s scored most annoying**. The current asset is at 0.079 s — at or below the worst interval the study tested.

The inharmonicity is measurable, not cosmetic. A harmonic replica of the same sound (same `f0`, same amplitudes, same decay, same sample rate) measures **40 dB** harmonic-to-noise ratio; the real file measures **13.6 dB**. Three independent literatures treat that direction as a cost: Brewster lists "irregular harmonics" among the properties that make a sound attention-grabbing, Edworthy found irregular harmonic frequencies raise perceived urgency, and Pongracz found low harmonic-to-noise ratio is the strongest acoustic predictor of a bark being rated angry. The current sound is mild enough (only three partials, all low) that this is a small effect, but it points the wrong way.

So the current asset carries **two independent defects that both point toward annoyance**: inharmonic partials, and a near-worst-case inter-bark interval. Neither is severe on its own — the sound is quiet, dark, and short, which covers for a lot — but both are cheap to correct, and `c0-heritage-harmonic` exists to test exactly that (it fixes the ratios and the onset, and widens the interval to 300 ms, while keeping the 220->165 identity).

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

Seven candidates were rendered to `.local/bark-candidates/` (local-only, gitignored), each with a 12x repetition file under `.local/bark-candidates/loop-test/` for the Berlyne check. `dsp.py` and `synth.py` in that folder regenerate everything.

| Candidate | Concept |
| --- | --- |
| `c0-heritage-harmonic` | The current file, minimally repaired: partial ratios `1:2.1:3.4` -> `1:2:3`, plus a 12 ms raised-cosine attack. Same 220->165 descending fourth, same amplitudes, same taus. |
| `c1-spec-rising` | The psychoacoustic spec taken literally. Strictly harmonic stack, energy peak on harmonic 2, F0 415 -> 523 (rising major third), no formant filter. |
| `c2-boof-falling` | Full source-filter dog: glottal pulse source, three-stage formant "wah" morph, per-bark pitch drop, breath onset. Falling major third (523 -> 415 sense). |
| `c3-chime-dog` | Bark voice layered under a prominent Chowning FM marimba/bell tone. Rising major third. The "chime with a bark vibe" reading. |
| `c4-pip-single` | One soft boof, 200 ms, with a quiet tonal underlayer. Minimal and least intrusive. |
| `c5-yip-playful` | Higher F0 band (620/740 Hz), brightest, shortest gap. Included to audition the 2006 "high and tonal reads friendly" reading against the 2019 annoyance finding. |
| `c6-heritage-body` | The heritage 220/165 pitch identity given formants and a body. |

### Measurements

All candidates are loudness-matched to **-18.5 LUFS** with true peak at or below **-1.0 dBTP**. Matching matters: comparing candidates at unequal loudness is not a fair test, because louder simply reads as better. `-18.5` is the loudest level every candidate reaches without breaching the peak ceiling — percussive sounds have a high crest factor, and several hit `-1 dBTP` while still 2–3 dB short of `-16 LUFS`. Absolute ship level is a separate decision once one is chosen.

| Candidate | Beats | IBI | Duration | True peak | LUFS | Centroid | Sharpness | HNR |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `c0-heritage-harmonic` | 2 | 300 ms | 550 ms | -5.86 dBTP | -18.5 | 267 Hz | 0.46 acum | 40.0 dB |
| `c1-spec-rising` | 2 | **450 ms** | 660 ms | -1.00 dBTP | -18.7 | 1216 Hz | 1.14 acum | 17.0 dB |
| `c2-boof-falling` | 2 | **430 ms** | 640 ms | -1.50 dBTP | -18.5 | 995 Hz | 1.14 acum | 14.3 dB |
| `c3-chime-dog` | 2 | **450 ms** | 770 ms | -5.28 dBTP | -18.5 | 1319 Hz | 1.28 acum | 23.7 dB |
| `c4-pip-single` | 1 | — | 200 ms | -4.66 dBTP | -18.5 | 1118 Hz | 1.07 acum | 18.3 dB |
| `c5-yip-playful` | 2 | 250 ms | 420 ms | -2.63 dBTP | -18.5 | 1305 Hz | 1.26 acum | 14.0 dB |
| `c6-heritage-body` | 2 | 300 ms | 530 ms | -2.03 dBTP | -18.5 | 514 Hz | 0.71 acum | 15.8 dB |
| *(current `bark.wav`)* | *2* | ***79 ms*** | *210 ms* | *-4.36 dBTP* | *-17.2* | *251 Hz* | *0.40 acum* | *13.6 dB* |

Bold IBI values sit in the 2019 study's least-annoying band (~0.5 s). Every candidate clears the sharpness threshold (`< 1.75 acum`) and keeps its centroid well under 2 kHz. All except `c5` sit inside or above the 2019 study's tonal band (HNR 11.6–35.4 dB).

`c0`, `c5`, and `c6` occupy an unhappy middle at 250–300 ms: too wide to read as a fast double-tap, too narrow to earn the measured happy interval. If any of them survives an audition, its interval should move to ~450 ms.

### On Beat Count

Two beats is not an arbitrary inheritance from the current asset. Real barks come in bouts, and once the bright formants are rolled off for the sharpness and accessibility constraints, the two-event rhythm is the cheapest remaining cue that says "dog" rather than "blip". Two also stays clear of the IEC 60601-1-8 alarm patterns, which are 3-pulse and 5-pulse.

The direct evidence favours two: the 2019 study tested bark **bouts** and found long-interval bouts least annoying and happiest. There is no single-bark condition in it to compare against, so it cannot settle 1 vs 2 — it can only say that *if* you use a bout, use a wide interval.

One conflation to avoid: Farago's "shorter calls rated more positive" refers to the individual vocalization, not the bout. Every candidate already uses short individual barks (~150 ms), so that finding does not discriminate between one beat and two.

The real cost of two beats is total duration — a happy interval forces ~640 ms versus 200 ms for a single. **The trap: do not resolve "too long" by tightening the interval.** That moves toward the measured most-annoying condition, which is precisely the mistake the current asset makes. Shorten the individual barks, or drop to one beat.

### Provisional Ranking

Ranked on measurements and literature only. **The sounds were not auditioned before ranking**, so this ordering is a prior, not a verdict, and the loop test is expected to reorder the top three.

1. **`c2-boof-falling`** — most convincingly canine while staying inside the safe psychoacoustic envelope (centroid 995 Hz, sharpness 1.14, HNR 14.3). Falling interval reads resolved and final, which suits a completion cue.
2. **`c4-pip-single`** — 200 ms, single event, least fatiguing under repetition. Best aligned with the frequency-of-use constraint, which is this asset's dominant one.
3. **`c3-chime-dog`** — most charming and closest to the chime-meets-bark brief; highest tonality (HNR 23.7). At 770 ms it is the longest, against the "shorter reads more positive" finding.
4. `c1-spec-rising` — safest numbers, but with no formant filter it reads closer to a synth blip than a dog.
5. `c0-heritage-harmonic` — excellent measurements and the smallest possible change, but barely reads as a bark. The strongest option if the goal is to fix the current sound rather than replace it.
6. `c6-heritage-body` — heritage pitch with a body; F0 220/165 is large-dog territory under the motivation-structural rules.
7. `c5-yip-playful` — brightest; the 2019 data places this direction toward annoyance. Included to hear the axis.

Unresolved by the literature: **rising versus falling interval.** Rising correlates with higher arousal and positive/open affect; falling reads final, and Material's Guided Frame precedent resolves to the tonic at completion because it "feels like home". Both are represented in the candidate set because the sources do not settle it.

## Measurement Methodology

Measurement code is `dsp.py` in the candidate folder; `python dsp.py` runs a self-check that validates every metric against signals with known answers (calibrated harmonic-plus-noise mixes, pure tones, band-limited noise, a decaying tone, and the int16 round-trip).

Three metrics were wrong on the first attempt, and each failure is worth recording:

1. **Spectral analysis over an amplitude-thresholded selection.** Gathering "the loud samples" with `x[abs(x) > threshold]` concatenates non-contiguous regions. Each join is a step discontinuity that smears broadband energy across the spectrum. This inflated centroid and sharpness for every candidate. Fix: analyze one contiguous window from the voiced body of the loudest event.
2. **Moving-average HNR with the window narrower than the spectral peaks.** A 10-bin moving average over a 2.7 Hz/bin spectrum spans 27 Hz, but a 50 ms Hann window produces peaks ~80 Hz wide, so the "noise floor" tracked the peaks themselves and the difference collapsed. The metric reported HNR near 0 dB for provably noise-free signals.
3. **Autocorrelation HNR without envelope flattening.** Autocorrelation assumes stationarity. A percussive exponential decay depresses the correlation on its own, which the metric reports as noise that is not present. Fix: divide out the analytic (Hilbert) amplitude envelope before correlating, with the smoothing window longer than the pitch period.

The decisive diagnostic in each case was the same: **measure a signal whose answer is already known.** The current `bark.wav` has a numerically verified noise floor near -114 dB, so any metric reporting it as noisy was broken. Synthesizing a provably clean replica at the same sample rate and pitch (which read 40 dB) separated "the metric is biased" from "the file really does contain something aperiodic" — and it was the latter, which is how the inharmonicity was found.

Final metric definitions:

- **HNR**: Boersma (1993) autocorrelation method (Praat's), on the envelope-flattened signal, over a 50 ms window from the voiced body.
- **Sharpness**: Aures / DIN 45692-style, from a Bark-band specific-loudness approximation.
- **LUFS**: ITU-R BS.1770 K-weighting, ungated — short-form sounds defeat the gate, so integrated loudness is unreliable under ~400 ms.
- **True peak**: 4x oversampled peak.

### Reproduction Note

Writing 16-bit WAV from numpy has a trap the self-check covers: `+1.0 * 32768` overflows int16 and wraps to `-32768`, turning a full-scale positive peak into a full-scale negative one, and `.astype(np.int16)` wraps silently rather than clipping. Always `np.clip(x, -1, 1)` first and scale by **32767**.

## Open / Untested

- **Nothing has been auditioned.** The ranking is a measurement prior. The loop test at `.local/bark-candidates/loop-test/` is the decisive check and has not been run.
- Rising versus falling interval is unresolved by the sources and needs an ear.
- No candidate was tested on laptop speakers or phone speakers, where the sub-500 Hz content that carries `c0`/`c6` will largely disappear. Small-speaker reproduction may be the deciding constraint, and it favours the harmonic-2 energy peak.
- Sample rate for a replacement is undecided. Candidates render at 44100 Hz (~40–70 KB); the current asset is 22050 Hz (9 KB). `winsound` and the POSIX players in `assets/bark.py` accept both.
- Roughness (asper) is argued to be near zero by construction — strictly harmonic partials, no modulation in the 15–300 Hz band — but was not measured. Only sharpness has an implemented metric.
- The measured `1 : 2.1 : 3.4` ratio set was not traced to a known synthesis recipe or preset. Whether it was hand-picked or inherited from a tool is unknown.
- Candidate synthesis depends on numpy and scipy. The runtime helper `assets/bark.py` is deliberately dependency-free; if a generator is ever committed it belongs in `dev-tools/`, not in the skill payload.
- Third-party summaries circulate Material Design LUFS figures (-18/-14/-12) and a "sound never lasts more than 0.3 s longer than its animation" rule. Neither could be verified against Material's own documentation, which is JavaScript-rendered. They are excluded from the spec above. Slack's "Knock Brush" has no design rationale that could be located; do not cite one.
