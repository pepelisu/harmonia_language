"""
SUNLIGHT — Composed in Harmonia v2.1
"The sun is shining and the day is bright..."

Key: F major — Nature+Knowledge+Self
     "The physical world, understood, inhabited"

Meter: 6/8 — waves, breathing, the rhythm of the shore
Tempo: dotted-quarter = 76 — walking pace on the beach

Journey: Nature (F) → Self (C)
         The world, through desire and play, becomes the self

Four tracks:
  0 - Melody (the voice, with ornaments)
  1 - Harmony (polyphonic words, with expressive shapes)  
  2 - Bass (walking narrative, wave-like patterns)
  3 - Domain thread (what persists and transforms)

Run: python sunlight.py
Output: sunlight.mid
"""

from midiutil import MIDIFile
import math
import random

random.seed(7)  # reproducible

# ── Configuration ─────────────────────────────────────
BPM = 76  # dotted-quarter = 76 (6/8 feel)

# Durations (in quarter-note beats)
S    = 0.25
E    = 0.5
Q    = 1.0
DQ   = 1.5      # one 6/8 beat
H    = 2.0
DH   = 3.0      # one 6/8 measure
W    = 4.0
LONG = 6.0      # two measures
VERY = 8.0
EXT  = 10.0
FINAL = 12.0

# Dynamics
PPP  = 22; PP = 35; P = 45; MP = 58; MF = 75; F = 95; FF = 115

# ── MIDI Notes ────────────────────────────────────────
# Octave 2
F2=41; G2=43; A2=45; Bb2=46; B2=47
# Octave 3
C3=48; Cs3=49; D3=50; Ds3=51; Eb3=51; E3=52; F3=53
Fs3=54; G3=55; Gs3=56; Ab3=56; A3=57; As3=58; Bb3=58; B3=59
# Octave 4
C4=60; Cs4=61; D4=62; Ds4=63; Eb4=63; E4=64; F4=65
Fs4=66; G4=67; Gs4=68; Ab4=68; A4=69; As4=70; Bb4=70; B4=71
# Octave 5
C5=72; Cs5=73; D5=74; Ds5=75; Eb5=75; E5=76; F5=77
Fs5=78; G5=79; Gs5=80; A5n=81; As5=82; Bb5=82; B5=83
# Octave 6
C6=84

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(4, adjust_origin=False, deinterleave=False)

MEL  = 0
HARM = 1
BASS = 2
DOM  = 3

midi.addTempo(0, 0, BPM)

for tr in range(4):
    midi.addProgramChange(tr, tr, 0, 0)  # All piano

midi.addTrackName(MEL,  0, "Melody - Voice")
midi.addTrackName(HARM, 1, "Harmony - Polyphonic Words")
midi.addTrackName(BASS, 2, "Bass - Walking Waves")
midi.addTrackName(DOM,  3, "Domain Thread")

# ── Helpers ───────────────────────────────────────────

def nt(track, chan, time, pitch, dur, vel):
    """Safe note."""
    midi.addNote(track, chan, pitch, max(0, time), max(0.01, dur),
                 max(min(int(vel), 127), 1))

def nt_h(track, chan, time, pitch, dur, vel, spread=4):
    """Humanized note."""
    t = max(0, time + random.uniform(-0.02, 0.02))
    v = max(min(vel + random.randint(-spread, spread), 127), 12)
    nt(track, chan, t, pitch, dur, v)

def pedal_on(track, chan, time, amount=100):
    midi.addControllerEvent(track, chan, max(0, time), 64, min(amount, 127))

def pedal_off(track, chan, time):
    midi.addControllerEvent(track, chan, max(0, time), 64, 0)

def harm_rise(time, notes, total_dur, vel, spacing=0.38):
    """Upward arpeggio — opening, hopeful."""
    sorted_n = sorted(notes)
    for i, n in enumerate(sorted_n):
        hold = total_dur - (i * spacing)
        if hold < 0.4: hold = 0.4
        nt_h(HARM, 1, time + (i * spacing), n, hold, vel - (i * 2))

def harm_bloom(time, notes, total_dur, vel, spacing=0.3):
    """Center outward — revealing."""
    sorted_n = sorted(notes)
    mid = len(sorted_n) // 2
    nt_h(HARM, 1, time, sorted_n[mid], total_dur, vel)
    step = 1
    for i in range(len(sorted_n)):
        if i == mid: continue
        t = time + (step * spacing)
        hold = total_dur - (step * spacing)
        nt_h(HARM, 1, t, sorted_n[i], max(hold, 0.4), vel - (step * 3))
        step += 1

def harm_wave(time, notes, total_dur, vel):
    """Up then down — breathing, wave-like."""
    sorted_n = sorted(notes)
    wave = sorted_n + sorted_n[-2:0:-1]
    spacing = total_dur / (len(wave) + 1)
    for i, n in enumerate(wave):
        t = time + (i * spacing)
        hold = min(spacing * 1.6, total_dur - (i * spacing))
        v = vel + ((-1)**i * 4)
        nt_h(HARM, 1, t, n, max(hold, 0.2), v)

def harm_grow(time, notes, total_dur, vel):
    """One by one, each sustaining — accumulating."""
    sorted_n = sorted(notes)
    spacing = total_dur / (len(sorted_n) + 1)
    for i, n in enumerate(sorted_n):
        t = time + (i * spacing)
        hold = total_dur - (i * spacing)
        nt_h(HARM, 1, t, n, max(hold, 0.4), vel)

def harm_dissolve(time, notes, total_dur, vel):
    """All together, fading one by one — letting go."""
    sorted_n = sorted(notes, reverse=True)
    for i, n in enumerate(sorted_n):
        dur = total_dur * (1.0 - (i * 0.2))
        dur = max(dur, total_dur * 0.3)
        v = max(vel - (i * 10), 15)
        nt_h(HARM, 1, time, n, dur, v)

def harm_cascade(time, notes, total_dur, vel):
    """Rapid downward — joyful tumble, like a wave breaking."""
    sorted_n = sorted(notes, reverse=True)
    spacing = 0.1
    for i, n in enumerate(sorted_n):
        t = time + (i * spacing)
        hold = total_dur - (i * spacing)
        nt_h(HARM, 1, t, n, max(hold, 0.3), vel + (i * 2))

def harm_climb(time, notes, total_dur, vel):
    """Rapid upward — ascending, freeing."""
    sorted_n = sorted(notes)
    spacing = 0.1
    for i, n in enumerate(sorted_n):
        t = time + (i * spacing)
        hold = total_dur - (i * spacing)
        nt_h(HARM, 1, t, n, max(hold, 0.3), vel + (i * 2))

def wave_bass(time, root, dur, vel):
    """6/8 wave-like bass pattern: root-fifth-octave, rocking."""
    fifth = root + 7
    octave = root + 12
    pulse = dur / 6
    # Strong-weak-weak Strong-weak-weak (6/8 feel)
    nt_h(BASS, 2, time, root, pulse * 1.8, vel)
    nt_h(BASS, 2, time + pulse, fifth, pulse * 0.9, vel - 12)
    nt_h(BASS, 2, time + pulse * 2, octave, pulse * 0.85, vel - 15)
    nt_h(BASS, 2, time + pulse * 3, root, pulse * 1.6, vel - 5)
    nt_h(BASS, 2, time + pulse * 4, fifth, pulse * 0.9, vel - 12)
    nt_h(BASS, 2, time + pulse * 5, octave, pulse * 0.85, vel - 15)

def walk_bass(time, notes, dur_each, vel):
    """Walking bass between chords."""
    t = time
    for n in notes:
        nt_h(BASS, 2, t, n, dur_each * 0.9, vel)
        t += dur_each
    return t

def add_vibrato(track, chan, time, note, dur, vel, speed=0.2):
    """Safe vibrato."""
    count = max(1, int(dur / speed))
    note_dur = speed * 0.7
    for i in range(count):
        v_mod = int(5 * math.sin(i * 1.8))
        t = max(0, time + (i * speed))
        v = max(min(vel - 15 + v_mod, 127), 10)
        nt(track, chan, t, note, note_dur, v)

def add_grace_below(track, chan, time, note, vel):
    """Grace note from below — safe."""
    nt(track, chan, max(0, time - 0.1), note - 1, 0.1, max(vel - 10, 10))

def add_grace_above(track, chan, time, note, vel):
    """Grace note from above — safe."""
    nt(track, chan, max(0, time - 0.1), note + 1, 0.1, max(vel - 10, 10))

def add_mordent(track, chan, time, note, vel):
    """Quick bite."""
    t = max(0, time)
    nt(track, chan, t, note, 0.09, vel)
    nt(track, chan, t + 0.1, note - 2, 0.08, max(vel - 10, 10))
    nt(track, chan, t + 0.19, note, 0.35, vel + 3)

def add_turn(track, chan, time, note, vel):
    """Savoring."""
    d = 0.1
    t = max(0, time)
    nt(track, chan, t, note + 2, d * 0.9, max(vel - 5, 10))
    nt(track, chan, t + d, note, d * 0.9, vel)
    nt(track, chan, t + d*2, note - 1, d * 0.9, max(vel - 5, 10))
    nt(track, chan, t + d*3, note, d * 2, vel)

def add_trill(track, chan, time, note, dur, vel):
    """Rapid alternation — excitement."""
    upper = note + 2
    step = 0.09
    count = max(1, int(dur / step))
    for i in range(count):
        n = note if i % 2 == 0 else upper
        t = max(0, time + (i * step))
        v = max(min(vel - 3 + random.randint(-3, 3), 127), 10)
        nt(track, chan, t, n, step * 0.85, v)

def add_harmonic(track, chan, time, note, dur, vel):
    """Ghost note — octave above, soft."""
    harm = note + 12 if note + 12 <= 107 else note
    nt(track, chan, max(0, time + dur * 0.2), harm, dur * 0.5, max(vel - 30, 10))

# ── Time Cursor ───────────────────────────────────────
t = 0.0


# ==============================================================
# SECTION 1: "The sun is shining and the day is bright."
#
# F major → Fmaj7
# Nature+Knowledge+Self → Nature+Knowledge+Self+EMOTION
# "The world inhabited" → "The world FELT"
#
# Mode: WARM, OPENING — like stepping outside into sunlight
# Shape: RISE (light ascending, warmth spreading)
# Touch: legato (smooth, continuous, flowing)
# Space: open, sustained (sunlight fills everything)
# ==============================================================

pedal_on(HARM, 1, t, 100)

# ── F major — "The sun is shining" ──
# v2.0: F+A+C = Nature+Knowledge+Self
# v2.1: RISE shape — the sunlight opens upward
# Bass: 6/8 wave pattern — the rhythm of morning, breathing

wave_bass(t, F2, DH, MP)

# Harmony: F→A→C rising (Nature→Knowledge→Self — the world unfolds)
harm_rise(t, [F3, A3, C4], DH + DH, MP - 10, spacing=0.45)

# Melody: starts on F (Nature), rises warmly
nt_h(MEL, 0, t, F4, DQ, MP + 5)                  # Nature — the sun
nt_h(MEL, 0, t + DQ, A4, E, MP)                  # Knowledge — shining (seen)
nt_h(MEL, 0, t + H, C5, Q, MP + 3)               # Self — "I see it"
# Turn on C5 — savoring the brightness
add_turn(MEL, 0, t + DH - E, C5, MP)

# Domain thread: C (Self) sustained — the self is present from the start
nt(DOM, 3, t, C3, LONG * 3, PPP)                 # Self — always present (deep)
# A (Knowledge) thread — understanding persists
nt(DOM, 3, t, A3, LONG, PP)

t += DH

# Second 6/8 measure — the phrase continues
wave_bass(t, F2, DH, MP)

nt_h(MEL, 0, t, A4, DQ, MP)                      # Knowledge — the day
nt_h(MEL, 0, t + DQ, F4, E, MP - 3)              # Nature — returning
nt_h(MEL, 0, t + H, A4, Q, MP)                   # Knowledge — continued
t += DH


# ── Fmaj7 — "and the day is bright" ──
# v2.0: F+A+C+E = Nature+Knowledge+Self+EMOTION
# The E enters — brightness is FELT, not just observed
# v2.1: BLOOM shape — the brightness radiates from center
# The E (Emotion) gets special attention — grace note from below

wave_bass(t, F2, DH, MP + 3)

# Harmony: BLOOM from A (Knowledge) outward — understanding radiates
harm_bloom(t, [F3, A3, C4, E4], DH + DH, MP - 8, spacing=0.35)

# Melody: E5 (Emotion!) — the brightness — with GRACE NOTE from below
# "The brightness reaches the heart"
nt_h(MEL, 0, t, C5, Q, MP)                       # Self — "the day"
nt_h(MEL, 0, t + Q, D5, E, MP - 3)               # passing: Action
add_grace_below(MEL, 0, t + DQ, E5, MP + 5)
nt_h(MEL, 0, t + DQ, E5, DQ, MP + 5)             # EMOTION — bright! felt!

# v2.1: vibrato on E4 in harmony — the brightness SHIMMERS
add_vibrato(DOM, 3, t + Q, E4, H, PP, speed=0.18)

t += DH

# Second measure — settling into the warmth
wave_bass(t, F2, DH, MP)

nt_h(MEL, 0, t, E5, Q, MP)                       # Emotion lingering
nt_h(MEL, 0, t + Q, C5, Q, MP - 3)               # Self — settling
nt_h(MEL, 0, t + H, A4, Q, MP - 5)               # Knowledge — understood
t += DH

# ── Brief breath between sentences ──
# Walking bass: F → G → A → Bb (stepping toward desire)
walk_bass(t, [F3, G3, A3], Q * 0.9, MP - 15)
# Melody: transition
nt_h(MEL, 0, t, F4, Q, P)
nt_h(MEL, 0, t + Q, G4, E, P - 3)
t += DQ

pedal_off(HARM, 1, t)


# ==============================================================
# SECTION 2: "I want to see the sea and bath in the sun,
#             play with the waves and make a castle in the sand."
#
# Bb → Bbmaj7 → F → D → Eb
# Desire → Desire+Knowledge → Nature → Action+Unknown → Home
#
# Mode: PLAYFUL, BUILDING — like running toward the water
# Shape: WAVE (the waves themselves), CASCADE (tumbling)
# Touch: mix of legato and leggiero (flowing and light)
# Space: open (outdoors, vast, the horizon)
# ==============================================================

pedal_on(HARM, 1, t, 90)

# ── Bb major — "I want" ──
# v2.0: Bb+D+F = Desire+Action+Nature
# "Wanting that moves through the physical world"
# v2.1: RISE shape — desire ascending, reaching
# The 6/8 lilt becomes more energetic — wanting drives forward

wave_bass(t, Bb2, DH, MF - 5)

# Harmony: RISE — desire reaches upward
harm_rise(t, [Bb3, D4, F4], DH, MF - 10, spacing=0.35)

# Melody: Bb4 (Desire) leaps up to D5 (Action) — I WANT → to DO
nt_h(MEL, 0, t, Bb4, Q, MF)                      # Desire — "I want"
add_mordent(MEL, 0, t + Q, D5, MF + 3)           # Action — bitten into — eager!
nt_h(MEL, 0, t + Q + 0.4, D5, E, MF)
nt_h(MEL, 0, t + H, F5, Q, MF - 3)               # Nature — "in the world"

# Domain thread: D (Action) enters — the doing begins
nt(DOM, 3, t + Q, D4, LONG * 2, PP)

t += DH


# ── Bbmaj7 — "to see the sea" ──
# v2.0: Bb+D+F+A = Desire+Action+Nature+KNOWLEDGE
# "Wanting to KNOW the sea" — desire gains understanding
# v2.1: WAVE shape — the sea itself! the harmony rocks like water

wave_bass(t, Bb2, DH, MF - 3)

# Harmony: WAVE — the sea!
harm_wave(t, [Bb3, D4, F4, A4], DH, MF - 10)

# Melody: A (Knowledge) — seeing = knowing — with turn (savoring the sight)
nt_h(MEL, 0, t, F5, Q, MF - 3)                   # Nature — "the sea"
add_turn(MEL, 0, t + Q, A4, MF)                  # Knowledge — "seeing" — savored
nt_h(MEL, 0, t + Q + 0.5, A4, Q, MF - 5)
nt_h(MEL, 0, t + DH - Q, Bb4, Q, MF - 5)         # Desire — still wanting

t += DH


# ── F major — "and bath in the sun" ──
# v2.0: F+A+C = Nature+Knowledge+Self
# Return to nature — immersed — the body in sunlight
# v2.1: BLOOM shape — warmth radiating from the center (the body)
# Bass: the wave pattern continues but warmer

wave_bass(t, F2, DH, MF)

# Harmony: BLOOM — warmth radiating from C (Self — the body in the sun)
harm_bloom(t, [F3, A3, C4], DH, MF - 10, spacing=0.3)

# Melody: settles into warmth — legato, relaxed
nt_h(MEL, 0, t, C5, DQ, MF)                      # Self — "I, in the sun"
nt_h(MEL, 0, t + DQ, A4, E, MF - 5)              # Knowledge — felt warmth
nt_h(MEL, 0, t + H, F4, Q, MF - 3)               # Nature — immersed

# v2.1: vibrato on C4 — the self trembles with warmth
add_vibrato(DOM, 3, t + E, C4, H, PP, speed=0.22)

t += DH

# Walking bass to D: F → G → A → ... → D (ascending — energy building)
walk_bass(t, [G3, A3, B3], E, MF - 15)
nt_h(MEL, 0, t, G4, E, MF - 10)
nt_h(MEL, 0, t + E, A4, E, MF - 8)
t += DQ

pedal_off(HARM, 1, t)
pedal_on(HARM, 1, t, 80)


# ── D major — "play with the waves" ──
# v2.0: D+F#+A = Action+UNKNOWN+Knowledge
# "Doing that reaches into mystery" — the unknown of each wave!
# v2.1: CASCADE shape — tumbling like a wave breaking!
# This should be the most PLAYFUL moment — leggiero touch, bright

# Bass: wave pattern but faster, more energetic
wave_bass(t, D3, DH, MF + 3)

# Harmony: CASCADE — rapid downward — the wave breaks!
harm_cascade(t, [D4, Fs4, A4], DH, MF - 5)

# Melody: F#5 (Unknown!) — the wave! with TRILL — excitement!
nt_h(MEL, 0, t, D5, E, MF + 5)                   # Action — "play!"
add_trill(MEL, 0, t + E, Fs5, Q, MF)             # Unknown — the WAVE — trilling!
nt_h(MEL, 0, t + DQ + E, A4, Q, MF - 3)          # Knowledge — learning from play

# Domain thread: F# (Unknown) appears — mystery enters
nt(DOM, 3, t + E, Fs4, H, PP)
add_harmonic(DOM, 3, t + E, Fs4, Q, PPP)          # ghost of the unknown — playful

t += DH

# Second measure — the wave recedes, another comes
wave_bass(t, D3, DH, MF)

# Harmony: another CASCADE — another wave
harm_cascade(t, [D4, Fs4, A4], H, MF - 8)

# Melody: rides the wave down
nt_h(MEL, 0, t, Fs5, E, MF)                      # Unknown
nt_h(MEL, 0, t + E, D5, E, MF - 3)               # Action
nt_h(MEL, 0, t + Q, A4, Q, MF - 5)               # Knowledge — settling

# Walking bass toward Eb: D → Eb (half step — arriving at home)
nt_h(BASS, 2, t + H, D3, Q, MF - 15)
nt_h(MEL, 0, t + H, D5, E, MF - 8)
nt_h(MEL, 0, t + H + E, Eb5, E, MF - 5)          # Eb — Home approaching!
t += DH


# ── Eb major — "and make a castle in the sand" ──
# v2.0: Eb+G+Bb = Home+Connection+Desire
# "A place of belonging, shared, and longed for"
# v2.1: GROW shape — building, accumulating (making the castle!)
# But also: DISSOLVE at the end — sand castles don't last
# This is the bittersweet moment — building something temporary

pedal_off(HARM, 1, t)
pedal_on(HARM, 1, t, 110)  # more sustain — the castle moment

wave_bass(t, Eb3, DH, MF - 3)

# Harmony: GROW — building the castle! Each note = another wall
harm_grow(t, [Eb3, G3, Bb3], DH, MF - 10)

# Melody: Eb (Home) → G (Connection) → Bb (Desire)
# Building upward — each note another layer of the castle
nt_h(MEL, 0, t, Eb5, DQ, MF)                     # Home — the foundation
nt_h(MEL, 0, t + DQ, G5, E, MF + 3)              # Connection — shared joy
add_grace_below(MEL, 0, t + H, Bb5, MF)
nt_h(MEL, 0, t + H, Bb5, Q, MF)                  # Desire — the wish, the dream

# Domain thread: Eb (Home) — with harmonic (it won't last)
add_harmonic(DOM, 3, t, Eb4, H, PP)               # ghost of home — temporary

t += DH

# The castle stands... briefly
# Harmony: DISSOLVE — the sand castle in time
harm_dissolve(t, [Eb3, G3, Bb3], DH, MF - 15)

wave_bass(t, Eb3, DH, MP)

# Melody: descending — the moment passes — but warmly
nt_h(MEL, 0, t, Bb4, Q, MP)                      # Desire fading
nt_h(MEL, 0, t + Q, G4, Q, MP - 5)               # Connection settling
nt_h(MEL, 0, t + H, Eb4, Q, MP - 8)              # Home — accepted

t += DH

pedal_off(HARM, 1, t)

# ── Transition: the text shifts — internal now ──
# "I will be free and happy, escape from this and find myself."
# Walking bass: Eb → D → C → D (arriving at action)
walk_bass(t, [D3, C3, D3], Q, P - 5)
nt_h(MEL, 0, t, D4, Q, P)
nt_h(MEL, 0, t + Q, C4, Q, P - 5)
nt_h(MEL, 0, t + H, D4, E, P - 3)
t += DH


# ==============================================================
# SECTION 3: "I will be free and happy, escape from this 
#             and find myself."
#
# Dm → D → E → Dm → C
# 
# The transformation: F→F# (Nature→Unknown = freedom)
# The arrival: C major (Self+Emotion+Connection = found)
#
# Mode: starts RESOLUTE → becomes ECSTATIC → settles SACRED
# Register: rising (octave 4 → 5 → future tense — "I WILL")
# Dynamic: builds to climax then settles
# ==============================================================

pedal_on(HARM, 1, t, 80)

# ── Dm — "escape from this" ──
# v2.0: D+F+A = Action+Nature+Knowledge
# "Doing grounded in the physical world" — leaving, but still in it
# Differential: F# became F — Unknown became Nature — possibility grounded
# v2.1: RISE shape — the escape begins, climbing out

wave_bass(t, D3, DH, MF)

# Harmony: RISE — climbing, escaping
harm_rise(t, [D3, F3, A3], DH + Q, MF - 10, spacing=0.4)

# Melody: D5 (Action) — resolute — "I will escape"
nt_h(MEL, 0, t, D5, Q, MF)                       # Action — escaping
nt_h(MEL, 0, t + Q, F5, Q, MF - 3)               # Nature — "from this world"
nt_h(MEL, 0, t + H, A4, Q, MF - 5)               # Knowledge — understanding why

# Domain thread: F (Nature) — about to transform into F# (Unknown)!
nt(DOM, 3, t, F4, DH + Q, MP)                    # Nature — tracked — about to change

t += DH

# ══════════════════════════════════════════════════════
# THE FREEDOM MOMENT: Dm → D
# F (Nature) → F# (Unknown) — the grounded becomes the possible
# v2.1: the F rises chromatically to F# in the domain thread
# This half step IS freedom — the physical becomes potential
# ══════════════════════════════════════════════════════

# Walking bass: D stays — Action persists as the ground
nt(BASS, 2, t, D3, H, MF - 10)

# The transformation: F→F# in the domain thread
nt(DOM, 3, t, F4, Q, MP)                         # Nature — one last time
# Grace note: F reaching up to F#
add_grace_below(DOM, 3, t + Q, Fs4, MP + 5)
nt(DOM, 3, t + Q, Fs4, Q, MP + 5)                # UNKNOWN — freedom!

# Melody: F5 rising to F#5 — the moment of liberation
nt_h(MEL, 0, t, F5, Q, MF)                       # Nature — "from this"
add_grace_below(MEL, 0, t + Q, Fs5, MF + 8)
nt_h(MEL, 0, t + Q, Fs5, Q, MF + 8)              # UNKNOWN — FREE!

t += H

# ── D major — "I will be free" ──
# v2.0: D+F#+A = Action+UNKNOWN+Knowledge
# The F has become F# — Nature has become Unknown — FREEDOM
# v2.1: CLIMB shape — rapid ascent — liberation!

# Harmony: CLIMB — soaring upward!
harm_climb(t, [D4, Fs4, A4], DH, MF + 5)

wave_bass(t, D3, DH, MF + 3)

# Melody: climbs to the highest point — A5! (Knowledge at the peak)
nt_h(MEL, 0, t, Fs5, Q, MF + 5)                  # Unknown — the sky!
nt_h(MEL, 0, t + Q, A5n, Q, F)                   # Knowledge — understanding freedom!
# Trill at the peak — ecstatic!
add_trill(MEL, 0, t + H, A5n, Q, MF + 5)

t += DH

pedal_off(HARM, 1, t)
pedal_on(HARM, 1, t, 120)  # full sustain for the emotional peak


# ── E major — "and happy" ──
# v2.0: E+G#+B = Emotion+SPIRIT+Time
# "Feeling that transcends the moment" — joy touching the sacred
# v2.1: BLOOM shape — happiness radiating from the center
# This is the CLIMAX — the highest dynamic, the most luminous chord

wave_bass(t, E3, DH, F - 5)

# Harmony: BLOOM — joy radiating
harm_bloom(t, [E3, Gs3, B3], DH + DH, F - 10, spacing=0.3)

# Melody: G#5 (Spirit!) — transcendent happiness
# With TRILL — the joy TREMBLES, it's almost too much
nt_h(MEL, 0, t, E5, Q, F)                        # Emotion — happiness!
add_trill(MEL, 0, t + Q, Gs5, DQ, F)             # Spirit — TRANSCENDENT JOY

# Domain thread: G# (Spirit) — new domain — joy goes beyond the physical
nt(DOM, 3, t + Q, Gs4, H, MP)
add_harmonic(DOM, 3, t + Q, Gs4, Q, PP)           # Spirit — luminous

t += DH

# Second measure — the joy settles but persists
wave_bass(t, E3, DH, MF)

nt_h(MEL, 0, t, Gs5, E, MF)                      # Spirit lingering
nt_h(MEL, 0, t + E, E5, Q, MF)                   # Emotion settling
nt_h(MEL, 0, t + DQ, B4, DQ, MF - 5)             # Time — the moment held

# v2.1: vibrato on E4 — the feeling is alive
add_vibrato(DOM, 3, t, E4, DH, PP, speed=0.2)

t += DH

pedal_off(HARM, 1, t)

# Walking bass: E → D → C (descending to Self — coming home)
walk_bass(t, [D3, C3], Q, MP - 10)
nt_h(MEL, 0, t, E5, Q, MP - 5)                   # Emotion
nt_h(MEL, 0, t + Q, D5, E, MP - 8)               # Action
nt_h(MEL, 0, t + DQ, C5, E, MP - 10)             # Self — approaching
t += H

pedal_on(HARM, 1, t, 120)


# ── Dm (brief) — "escape from this" ──
# v2.0: D+F+A = Action+Nature+Knowledge
# Reflective — the action of leaving, grounded
# v2.1: passing chord — RISE but quick, transitional

harm_rise(t, [D3, F3, A3], H + Q, MP - 5, spacing=0.3)

nt_h(MEL, 0, t, D5, Q, MP)                       # Action — escaping
nt_h(MEL, 0, t + Q, F5, E, MP - 3)               # Nature — the world left behind

# Bass: D → C walk (arriving at Self)
nt_h(BASS, 2, t, D3, Q, MP - 10)
nt_h(BASS, 2, t + Q, E3, E, MP - 12)
nt_h(BASS, 2, t + DQ, D3, E, MP - 13)
nt_h(BASS, 2, t + H, C3, E, MP - 15)             # C — Self — arriving

# Melody: descending to C — finding
nt_h(MEL, 0, t + DQ, E5, E, MP - 5)              # Emotion
nt_h(MEL, 0, t + H, D5, E, MP - 8)               # Action — last step
t += H + E

# Appoggiatura: D5 → C5 — "despite everything... arriving at Self"
nt_h(MEL, 0, t, D5, E, MP - 5)                   # Action — appoggiatura
t += E


# ==============================================================
# FINAL CHORD: C major — "and find myself"
#
# v2.0: C+E+G = Self+Emotion+Connection
# "A being that feels and connects"
#
# The entire piece traveled from F (Nature) to C (Self).
# From the physical world to the person inside it.
#
# v2.1: SACRED mode — grow shape, tenuto, vast
# The arrival should feel INEVITABLE and WARM
# ==============================================================

# Harmony: GROW — each domain entering and sustaining
# Order: C→E→G (Self, then Emotion, then Connection)
# "First I find my self. Then I feel. Then I connect."
harm_grow(t, [C3, E3, G3], LONG + W, MP, )

# Add octave doubling for fullness
harm_grow(t, [C4, E4, G4], LONG + W, PP + 5)

# Bass: C — deep, arrived, final
nt(BASS, 2, t, C3, LONG + W, MP - 10)
# Low C for depth
nt(BASS, 2, t + Q, C3 - 12, LONG, PP)

# Melody: C5 (Self) — arrived — with VIBRATO (alive, warm, human)
nt_h(MEL, 0, t + 0.08, C5, DH, MP)               # Self — found!

# Then: E5 (Emotion) — felt
nt_h(MEL, 0, t + DH + 0.1, E5, H, MP - 3)        # Emotion — felt

# Then: G5 (Connection) — belonging — the last note
add_grace_below(MEL, 0, t + DH + H, G5, MP)
nt_h(MEL, 0, t + DH + H + 0.08, G5, DH, MP - 5)  # Connection — belonging

# v2.1: vibrato on C4 — the self is ALIVE, not a concept
add_vibrato(DOM, 3, t + Q, C4, LONG, PP, speed=0.3)

# v2.1: harmonic on E — feeling as overtone — the glow
add_harmonic(DOM, 3, t + DH, E4, W, PPP)

# v2.1: harmonic on G — connection as overtone — the warmth
add_harmonic(DOM, 3, t + DH + H, G4, DH, PPP)

t += LONG + W

# ── Final lingering ──
# The wave bass returns one last time — but barely, a whisper
# The sea is still there. The sun is still shining.
# But now the self is found.

# One soft wave
nt_h(BASS, 2, t, F2, DQ, PPP)                    # Nature — still present
nt_h(BASS, 2, t + DQ, C3, DQ, PPP)               # Self — inside it
t += DH

# Final silence
t += VERY

pedal_off(HARM, 1, t)


# ==============================================================
# Write
# ==============================================================

filename = "sunlight.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"""
  ╔═══════════════════════════════════════════════════════════╗
  ║  SUNLIGHT — Composed in Harmonia v2.1                     ║
  ╠═══════════════════════════════════════════════════════════╣
  ║                                                           ║
  ║  "The sun is shining and the day is bright.               ║
  ║   I want to see the sea and bath in the sun,              ║
  ║   play with the waves and make a castle in the sand.      ║
  ║   I will be free and happy, escape from this              ║
  ║   and find myself."                                       ║
  ║                                                           ║
  ╠═══════════════════════════════════════════════════════════╣
  ║  Key:     F major (Nature+Knowledge+Self)                 ║
  ║  Meter:   6/8 (waves, breathing, the shore)               ║
  ║  Tempo:   {BPM} BPM                                         ║
  ║  Journey: Nature (F) → Self (C)                           ║
  ║  Length:  ~{minutes:.1f} min                                       ║
  ║  File:    {filename}                                     ║
  ╠═══════════════════════════════════════════════════════════╣
  ║  Progression:                                             ║
  ║                                                           ║
  ║   F          "The sun is shining"                         ║
  ║     Nature+Knowledge+Self — the world inhabited           ║
  ║                                                           ║
  ║   Fmaj7      "and the day is bright"                      ║
  ║     +Emotion — the brightness is FELT                     ║
  ║                                                           ║
  ║   Bb         "I want"                                     ║
  ║     Desire+Action+Nature — wanting in the world           ║
  ║                                                           ║
  ║   Bbmaj7     "to see the sea"                             ║
  ║     +Knowledge — wanting to SEE, to KNOW                  ║
  ║                                                           ║
  ║   F          "and bath in the sun"                        ║
  ║     Nature — immersed, the body in warmth                 ║
  ║                                                           ║
  ║   D          "play with the waves"                        ║
  ║     Action+Unknown+Knowledge — play IS mystery            ║
  ║                                                           ║
  ║   Eb         "make a castle in the sand"                  ║
  ║     Home+Connection+Desire — building belonging           ║
  ║     (dissolve shape — sand castles don't last)            ║
  ║                                                           ║
  ║   Dm→D       "I will be free"                             ║
  ║     F→F# = Nature→Unknown = FREEDOM                      ║
  ║     the grounded becomes the possible                     ║
  ║                                                           ║
  ║   E          "and happy"                                  ║
  ║     Emotion+Spirit+Time — joy that transcends             ║
  ║                                                           ║
  ║   Dm         "escape from this"                           ║
  ║     Action+Nature+Knowledge — leaving, grounded           ║
  ║                                                           ║
  ║   C          "and find myself"                            ║
  ║     Self+Emotion+Connection — being, feeling, belonging   ║
  ║                                                           ║
  ╠═══════════════════════════════════════════════════════════╣
  ║  Listen for:                                              ║
  ║    - 6/8 wave bass — the rhythm of the shore              ║
  ║    - Fmaj7: E (Emotion) enters — brightness FELT          ║
  ║    - D cascade: waves BREAKING (rapid downward arpeggio)  ║
  ║    - F# trill: the UNKNOWN of each wave — playful!        ║
  ║    - Eb grow→dissolve: castle built then fading            ║
  ║    - F→F# half step: Nature→Unknown = FREEDOM             ║
  ║    - E bloom + G# trill: transcendent HAPPINESS           ║
  ║    - Final C: Self+Emotion+Connection — FOUND             ║
  ║    - Last whisper: F2→C3 — Nature still there, Self inside║
  ╚═══════════════════════════════════════════════════════════╝
""")