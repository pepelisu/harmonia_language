"""
KNOWING v2.1 — Complete Polyphonic + Expressive Composition
"Life is a story that we tell to ourselves..."

This is the MERGER of:
  v2.0 (polyphonic — four voices, walking bass, domain tracking,
        deliberate arpeggiation, full four-section structure)
  +
  v2.1 (expressivity — shapes, touch, breath, ornaments, space)

The v2.0 architecture is PRESERVED COMPLETELY.
The v2.1 expressivity is ADDED ON TOP — not replacing, enhancing.

Four tracks:
  0 - Melody     (the speaking voice — now with ornaments, breath)
  1 - Harmony    (polyphonic words — now with expressive shapes)
  2 - Bass       (walking narrative spine — now with touch variation)
  3 - Domain     (the thread — now with vibrato and harmonics)

Run: python knowing_v2_1_full.py
Output: knowing_v2_1_full.mid

Compare with:
  knowing_harmonia.mid   v1.0  (telegram)
  knowing_fluid.mid      v1.1  (connected)
  knowing_v2.mid         v2.0  (polyphonic)
  knowing_v2_1_full.mid  v2.1  (polyphonic + expressive) ← THIS
"""

from midiutil import MIDIFile
import math
import random

random.seed(42)  # reproducible humanization

# ── Configuration ─────────────────────────────────────
BPM = 60  # Slightly slower than v2.0 — breath needs room

# Durations
S    = 0.25
E    = 0.5
Q    = 1.0
DQ   = 1.5
H    = 2.0
DH   = 3.0
W    = 4.0
LONG = 6.0
VERY = 8.0
EXT  = 10.0
FINAL = 14.0

# Dynamics
PPP  = 22; PP = 35; P = 45; MP = 58; MF = 75; F = 95

# ── MIDI Notes ────────────────────────────────────────
A2=45; B2=47
C3=48; Cs3=49; D3=50; Ds3=51; E3=52; F3=53
Fs3=54; G3=55; Gs3=56; A3=57; As3=58; B3=59
C4=60; Cs4=61; D4=62; Ds4=63; E4=64; F4=65
Fs4=66; G4=67; Gs4=68; A4=69; As4=70; B4=71
C5=72; Cs5=73; D5=74; Ds5=75; E5=76; F5=77
Fs5=78; G5=79; Gs5=80; A5n=81; As5=82; B5=83

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(4, adjust_origin=False, deinterleave=False)


MEL   = 0    # Melody
HARM  = 1    # Harmony (polyphonic arpeggiated words)
BASS  = 2    # Bass (walking narrative)
DOM   = 3    # Domain tracking (the thread)

midi.addTempo(0, 0, BPM)

for tr in range(4):
    midi.addProgramChange(tr, tr, 0, 0)

midi.addTrackName(MEL,  0, "Melody - Voice + Ornaments")
midi.addTrackName(HARM, 1, "Harmony - Polyphonic + Expressive")
midi.addTrackName(BASS, 2, "Bass - Walking + Touch")
midi.addTrackName(DOM,  3, "Domain Thread + Vibrato")

# ══════════════════════════════════════════════════════
# EXPRESSIVITY HELPERS — v2.1 functions embedded
# ══════════════════════════════════════════════════════

def add_grace_below(track, chan, time, note, vel):
    """Grace note from half step below — safe timing."""
    grace_time = max(0, time - 0.12)
    nt(track, chan, grace_time, note - 1, 0.12, max(vel - 10, 10))

def add_grace_above(track, chan, time, note, vel):
    """Grace note from half step above — safe timing."""
    grace_time = max(0, time - 0.12)
    nt(track, chan, grace_time, note + 1, 0.12, max(vel - 10, 10))    

def nt(track, chan, time, pitch, dur, vel):
    """Basic note — enforces non-negative time and valid velocity."""
    midi.addNote(track, chan, pitch, max(0, time), max(0.01, dur), 
                 max(min(int(vel), 127), 1))

def humanize_vel(vel, spread=6):
    """Slight velocity randomization — human touch."""
    v = vel + random.randint(-spread, spread)
    return max(min(v, 127), 12)

def humanize_time(time, spread=0.03):
    """Slight timing randomization — never negative."""
    return max(0, time + random.uniform(-spread, spread))

def nt_h(track, chan, time, pitch, dur, vel, spread=5):
    """Humanized note — safe timing and velocity."""
    midi.addNote(track, chan, pitch,
                max(0, humanize_time(time)),
                max(0.01, dur),
                max(min(humanize_vel(vel, spread), 127), 1))

def pedal_on(track, chan, time, amount=100):
    midi.addControllerEvent(track, chan, max(0, time), 64, min(amount, 127))

def pedal_off(track, chan, time):
    midi.addControllerEvent(track, chan, max(0, time), 64, 0)

def pedal_off(track, chan, time):
    midi.addControllerEvent(track, chan, max(0, time), 64, 0)

def harm_rise(time, notes, total_dur, vel, spacing=None):
    """
    v2.0 deliberate arpeggiation + v2.1 RISE shape.
    Notes unfold upward. Each given space as its own domain.
    Humanized velocity and timing.
    """
    sorted_n = sorted(notes)
    if spacing is None:
        spacing = min(total_dur * 0.15, 0.45)
    for i, n in enumerate(sorted_n):
        hold = total_dur - (i * spacing)
        if hold < 0.4:
            hold = 0.4
        v = humanize_vel(vel - (i * 2))  # slightly softer each note
        t = humanize_time(time + (i * spacing))
        nt(HARM, 1, t, n, hold, v)

def harm_fall(time, notes, total_dur, vel, spacing=None):
    """Descending arpeggiation — settling, concluding."""
    sorted_n = sorted(notes, reverse=True)
    if spacing is None:
        spacing = min(total_dur * 0.15, 0.45)
    for i, n in enumerate(sorted_n):
        hold = total_dur - (i * spacing)
        if hold < 0.4:
            hold = 0.4
        v = humanize_vel(vel - (i * 2))
        t = humanize_time(time + (i * spacing))
        nt(HARM, 1, t, n, hold, v)

def harm_bloom(time, notes, total_dur, vel, spacing=None):
    """Center note first, then outward — revealing."""
    sorted_n = sorted(notes)
    if spacing is None:
        spacing = min(total_dur * 0.12, 0.35)
    mid = len(sorted_n) // 2
    # Center first
    nt_h(HARM, 1, time, sorted_n[mid], total_dur, vel)
    step = 1
    for i in range(len(sorted_n)):
        if i == mid:
            continue
        t = time + (step * spacing)
        hold = total_dur - (step * spacing)
        nt_h(HARM, 1, t, sorted_n[i], max(hold, 0.4), vel - (step * 3))
        step += 1

def harm_grow(time, notes, total_dur, vel):
    """Notes entering one by one, each sustaining — accumulating."""
    sorted_n = sorted(notes)
    spacing = total_dur / (len(sorted_n) + 1)
    for i, n in enumerate(sorted_n):
        t = time + (i * spacing)
        hold = total_dur - (i * spacing)
        nt_h(HARM, 1, t, n, max(hold, 0.4), humanize_vel(vel))

def harm_dissolve(time, notes, total_dur, vel):
    """All notes together, then fading one by one — letting go."""
    sorted_n = sorted(notes, reverse=True)
    for i, n in enumerate(sorted_n):
        dur = total_dur * (1.0 - (i * 0.22))
        dur = max(dur, total_dur * 0.3)
        v = max(vel - (i * 10), 15)
        nt_h(HARM, 1, time, n, dur, v)

def harm_wave(time, notes, total_dur, vel):
    """Up then down — breathing, contemplating."""
    sorted_n = sorted(notes)
    wave = sorted_n + sorted_n[-2:0:-1]
    spacing = total_dur / (len(wave) + 1)
    for i, n in enumerate(wave):
        t = time + (i * spacing)
        hold = spacing * 1.6
        v = humanize_vel(vel + ((-1)**i * 4))
        nt(HARM, 1, t, n, min(hold, total_dur - (i * spacing)), v)

def add_vibrato(track, chan, time, note, dur, vel, speed=0.18):
    """Simulated vibrato — non-overlapping repeated notes."""
    count = max(1, int(dur / speed))
    note_dur = speed * 0.72  # ends before next note starts
    for i in range(count):
        v_mod = int(6 * math.sin(i * 1.8))
        t = max(0, time + (i * speed))
        v = max(min(vel - 18 + v_mod, 127), 10)
        nt(track, chan, t, note, note_dur, v)

def add_harmonic(track, chan, time, note, dur, vel):
    """Harmonic — octave above, very soft."""
    harm = note + 12 if note + 12 <= 107 else note
    nt(track, chan, max(0, time + dur * 0.25), harm, 
       dur * 0.55, max(vel - 35, 10))

def add_mordent(track, chan, time, note, vel):
    """Quick bite — non-overlapping."""
    lower = note - 1
    safe_t = max(0, time)
    nt(track, chan, safe_t, note, 0.09, vel)
    nt(track, chan, safe_t + 0.1, lower, 0.08, max(vel - 10, 10))
    nt(track, chan, safe_t + 0.19, note, 0.35, vel + 3)

def add_turn(track, chan, time, note, vel):
    """Turn — savoring the note. Non-overlapping."""
    d = 0.11
    safe_t = max(0, time)
    nt(track, chan, safe_t, note + 2, d * 0.9, max(vel - 5, 10))
    nt(track, chan, safe_t + d, note, d * 0.9, vel)
    nt(track, chan, safe_t + d*2, note - 1, d * 0.9, max(vel - 5, 10))
    nt(track, chan, safe_t + d*3, note, d * 1.8, vel)

def walk_bass(time, notes, dur_each, vel):
    """Walking bass with humanized touch."""
    t = time
    for n in notes:
        nt_h(BASS, 2, t, n, dur_each * 0.92, vel, spread=4)
        t += dur_each
    return t

# ══════════════════════════════════════════════════════
# THE COMPOSITION — v2.0 structure + v2.1 expressivity
# ══════════════════════════════════════════════════════

t = 0.0

# ==============================================================
# PICKUP: E4 — "Feel."
# v2.1: with slight rubato pull (arrives slightly late)
# and harmonic on E (the ghost of feeling — foreshadowing the end)
# ==============================================================

pedal_on(HARM, 1, t, 80)  # half-pedal — warm room

# Melody: E4 — slightly late (hesitant breath)
nt(MEL, 0, t + 0.08, E4, DQ, PP)  # rubato pull — arriving gently

# v2.1: harmonic on E — the overtone foreshadows the ending
add_harmonic(DOM, 3, t + 0.08, E4, DQ, PPP)

# Bass: A barely present
nt_h(BASS, 2, t, A2, DQ, PPP)

# Domain thread: E3 — the thread begins
nt(DOM, 3, t, E3, VERY * 5, PPP)  # held across the entire piece

t += DQ + S + 0.08  # extra space from rubato


# ==============================================================
# SECTION 1: "Life is a story that we tell to ourselves"
# v2.0: C→Cmaj7→G→C/E (polyphonic architecture)
# v2.1: TENDER mode — rise shapes, legato, rubato pull, vibrato
# ==============================================================

pedal_off(HARM, 1, t)
pedal_on(HARM, 1, t, 90)  # sustained — warm, bleeding

# ── C major — "Life..." ──
# v2.0: C+E+G = Self+Emotion+Connection
# v2.1 shape: RISE (C→E→G, each note unfolding upward — tender)

harm_rise(t, [C3, E3, G3], DH + Q, MP - 15, spacing=0.4)

# Melody: rises through domains — with TURN on G (savoring connection)
nt_h(MEL, 0, t, C4, Q, MP)                      # Self
nt_h(MEL, 0, t + Q, E4, Q, MP)                  # Emotion
add_turn(MEL, 0, t + H, G4, MP)                 # Connection — SAVORED
nt_h(MEL, 0, t + H + 0.5, G4, Q, MP - 5)        # Connection settling

# Bass: C — with slight portato (each word weighed)
nt_h(BASS, 2, t, C3, DH * 0.9, MP - 15)

# Domain thread: G enters — Connection begins
nt(DOM, 3, t + H, G3, W * 4, PP)  # Connection sustained far

t += DH


# ── Cmaj7 — "...is a wondrous story" ──
# v2.0: C+E+G+B = Self+Emotion+Connection+TIME (life begins)
# v2.1 shape: BLOOM (E first — feeling — then Self and Time radiate outward)

harm_bloom(t, [C3, E3, G3, B3], W + Q, MP - 12, spacing=0.35)

# Melody: B (Time) gets emphasis — GRACE NOTE from below (reaching up to Time)
nt_h(MEL, 0, t, G4, Q, MP)                      # Connection continuing
nt_h(MEL, 0, t + Q, A4, E, MP - 5)              # passing: Knowledge
add_grace_below(MEL, 0, t + DQ, B4, MP)          # reaching UP to Time
nt_h(MEL, 0, t + DQ, B4, DQ, MP + 5)            # TIME — emphasized, arrived at

# Bass: C — held with slight agogic accent (longer than expected)
nt_h(BASS, 2, t, C3, W + Q, MP - 15)

t += W

# ── Bass walk: C → D to G ──
# v2.1: walking bass with humanized touch (slight portato)
nt_h(BASS, 2, t, D3, Q * 0.88, MP - 15)         # D = Action — portato
# Melody: passing notes toward G chord — with anticipation (reaching ahead)
nt_h(MEL, 0, t, A4, E, MP - 10)
nt_h(MEL, 0, t + E, B4, E, MP - 8)              # anticipation — already reaching
t += Q


# ── G major — "We tell" ──
# v2.0: G+B+D = Connection+Time+Action (one chord = "we tell")
# v2.1 shape: WAVE (up then down — the telling breathes, contemplates)

harm_wave(t, [G3, B3, D4], DH + E, MP - 10)

# Melody: D5 (Action) gets the high note — MORDENT (emphasis, biting into the verb)
nt_h(MEL, 0, t, G4, Q, MP)                      # Connection
add_mordent(MEL, 0, t + Q, D5, MP + 5)           # "TELL" — bitten into
nt_h(MEL, 0, t + Q + 0.4, D5, Q, MP)            # Action sustained

# Bass: G
nt_h(BASS, 2, t, G3, DH, MP - 15)

# v2.1: vibrato on B3 in the harmony — Time is alive, not mechanical
add_vibrato(DOM, 3, t + Q, B3, H, PP, speed=0.2)

t += DH

# ── Bass walk: G → F → E to C/E ──
# v2.1: chromatic-ish descent — each step a sigh (morendo touch)
nt_h(BASS, 2, t, F3, Q * 0.85, MP - 18)         # F — World (softer — fading)
nt_h(MEL, 0, t, D5, E, MP - 10)                 # melody descending
nt_h(MEL, 0, t + E, C5, E, MP - 12)
t += Q

nt_h(BASS, 2, t, E3, E * 0.9, MP - 20)          # E — Feeling (softest — arriving)
nt_h(MEL, 0, t, B4, E, MP - 12)
t += E

# Melody: appoggiatura F → E (despite the world, arriving at feeling)
nt_h(MEL, 0, t, F4, E * 0.7, MP - 14)           # F — appoggiatura (the world)
t += E


# ── C/E — "...to ourselves" ──
# v2.0: E→G→C (reversed from opening — speaker becomes listener)
# v2.1 shape: FALL (descending — settling into, concluding, arriving home)
# v2.1 breath: rubato pull (time stretches at the end of the sentence)

harm_fall(t, [E3, G3, C4], DH + S, MP - 10, spacing=0.38)

# Melody: E4 (Emotion) — with VIBRATO (humanized, warm, alive)
nt_h(MEL, 0, t + 0.06, E4, H, MP)               # Emotion — rubato (late)
add_vibrato(DOM, 3, t + Q, E4, DQ, PP - 5, speed=0.22)
nt_h(MEL, 0, t + H + 0.1, C4, Q, P)             # Self — whispered, arriving

# Bass: E — feeling as ground (with harmonic — ghost of emotion)
nt_h(BASS, 2, t, E3, DH, MP - 15)
add_harmonic(BASS, 2, t, E3, H, PPP)

t += DH

pedal_off(HARM, 1, t)

# ── Transition ──
# v2.1: sighing breath — two-note figure, softer second note
nt_h(BASS, 2, t, D3, Q * 0.9, P - 10)
nt_h(BASS, 2, t + Q, C3, Q * 0.85, P - 15)      # softer — the sigh
nt_h(BASS, 2, t + H, B2, Q * 0.8, P - 18)       # softest — settling

nt_h(MEL, 0, t + Q, B3, Q, PP)                  # Time (echoing)
nt_h(MEL, 0, t + H, A3, Q * 0.8, PP - 5)        # Knowledge (sighed)
t += DH


# ==============================================================
# SECTION 2a: "You don't know what you still have to learn"
# v2.0: Am→F#m→Dsus4→A7 (polyphonic architecture)
# v2.1: SEARCHING mode — scatter shapes, portato, hesitant breath
# ==============================================================

pedal_on(HARM, 1, t, 70)  # half-pedal — slightly dry, searching

# ── Am — "You don't know" ──
# v2.0: A+C+E = Knowledge+Self+Emotion (personal knowing)
# v2.1 shape: RISE (A→C→E — but with HESITANT breath — each note preceded by silence)

# v2.1: slight hesitation before the chord (breath before speaking)
t += 0.12  # hesitation

harm_rise(t, [A3, C4, E4], DH + H, P, spacing=0.5)

# Domain thread: C4 (Self) — track it explicitly with slight tremolo
# The note that will transform — make it alive, trembling
add_vibrato(DOM, 3, t + E, C4, DH, PP, speed=0.25)

# Melody: descending — PORTATO touch (each word weighed separately)
nt_h(MEL, 0, t + 0.05, E5, DQ * 0.85, P)        # Emotion — separated
nt_h(MEL, 0, t + DQ + 0.08, C5, Q * 0.88, P)    # Self — separated
nt_h(MEL, 0, t + DQ + Q + 0.05, A4, E, P - 3)   # Knowledge — fading

# Bass: A — portato
nt_h(BASS, 2, t, A2, DH * 0.88, P - 10)

t += DH

# ── Walking bass: A → G# → G → F# (chromatic — inevitable) ──
# v2.1: each step slightly softer (morendo walk — dissolving downward)
nt_h(BASS, 2, t, Gs3, E * 0.9, P - 12)
nt_h(BASS, 2, t + E, G3, E * 0.9, P - 15)
nt_h(BASS, 2, t + Q, Fs3, E * 0.85, P - 18)

# Melody: descending with grace notes (reaching, uncertain)
add_grace_below(MEL, 0, t, B4, P - 8)
nt_h(MEL, 0, t, B4, E, P - 5)
nt_h(MEL, 0, t + E, A4, E, P - 8)
add_grace_below(MEL, 0, t + Q, Gs4, P - 10)
nt_h(MEL, 0, t + Q, Gs4, E, P - 10)
t += DQ


# ── F#m — "the unknown is felt" ──
# v2.0: F#+A+C# = Unknown+Knowledge+Boundary
# v2.1 shape: SCATTER (notes placed irregularly — searching, uncertain)

# Scatter: irregular placement
nt_h(HARM, 1, t + 0.15, Fs3, DH - 0.2, P)       # Unknown (delayed)
nt_h(HARM, 1, t + 0.0, A3, DH * 0.9, P - 3)     # Knowledge (on time)
nt_h(HARM, 1, t + 0.3, Cs4, DH * 0.8, P - 5)    # Boundary (late)

# Melody: C# (Boundary) gets prominence with grace note from below
nt_h(MEL, 0, t + 0.05, Fs4, Q, P)
add_grace_below(MEL, 0, t + Q, Cs5, P + 3)
nt_h(MEL, 0, t + Q, Cs5, Q, P + 3)               # Boundary — reaching
nt_h(MEL, 0, t + H + 0.06, A4, Q * 0.9, P - 3)

# Bass: F#
nt_h(BASS, 2, t, Fs3, DH * 0.88, P - 10)

t += DH

# ── Bass walk: F# → E → D ──
nt_h(BASS, 2, t, E3, Q * 0.9, P - 12)
nt_h(BASS, 2, t + Q, D3, Q * 0.88, P - 15)
nt_h(MEL, 0, t, A4, Q * 0.85, P - 8)
nt_h(MEL, 0, t + Q, G4, Q * 0.82, P - 10)
t += H


# ── Dsus4 — "action waits" ──
# v2.0: D+G+A = Action+Connection+Knowledge (mystery replaced by familiar)
# v2.1 shape: GROW (notes entering one by one — building, waiting)
# v2.1 touch: tenuto (each held to full value — refusing to release)

harm_grow(t, [D3, G3, A3], H + Q, P)

# Melody: G (the sus note) with TURN — savoring the suspension, dwelling in it
add_turn(MEL, 0, t, G4, P)
nt_h(MEL, 0, t + 0.5, G4, E, P)
nt_h(MEL, 0, t + Q + 0.06, A4, Q * 0.9, P - 3)

# Bass: D — tenuto (held fully)
nt_h(BASS, 2, t, D3, H * 0.95, P - 10)

t += H

# ── Chromatic approach to A7 ──
# v2.1: with hesitation before (the question is hard to ask)
t += 0.1  # hesitation
nt_h(BASS, 2, t, Gs3, E * 0.8, P - 12)
nt_h(MEL, 0, t, Gs4, E * 0.7, P - 8)
t += E


# ── A7 — "What?" ──
# v2.0: A+C#+E+G = Knowledge+Boundary+Emotion+Connection
# v2.1 shape: BLOOM (the question opens from its center — Emotion first)
# v2.1 breath: fermata (time stops on the question)

harm_bloom(t, [A3, Cs4, E4, G4], W + H + Q, P, spacing=0.35)  # fermata — held longer

# Melody: the question unfolds with SIGH at the end
nt_h(MEL, 0, t, E5, Q, P)                       # Emotion
nt_h(MEL, 0, t + Q + 0.05, Cs5, Q, P - 3)       # Boundary
nt_h(MEL, 0, t + H + 0.08, G4, Q, P - 5)        # Connection
# Sigh: two notes, second softer (sighing breath)
nt_h(MEL, 0, t + DH, E4, Q, P - 5)              # first
nt_h(MEL, 0, t + W, D4, Q * 0.7, P - 12)        # sigh — softer, shorter

# Bass: A — with harmonic (the question echoes upward)
nt_h(BASS, 2, t, A2, LONG, P - 10)
add_harmonic(BASS, 2, t + Q, A2, W, PPP)

# v2.1: vibrato on E4 in the question — the emotional core trembles
add_vibrato(DOM, 3, t + H, E4, H, PP - 5, speed=0.2)

t += LONG

pedal_off(HARM, 1, t)

# ── Transition ──
nt_h(BASS, 2, t, E3, Q * 0.85, PPP)
nt_h(BASS, 2, t + Q + 0.06, Gs3, Q * 0.8, PPP - 3)
t += H + S


# ==============================================================
# SECTION 2b: "because knowledge is infinite"
# v2.0: A→Amaj7→Aaug→E→B→F# (expansion outward)
# v2.1: starts RESOLUTE, becomes ECSTATIC, then SACRED on expansion
# ==============================================================

pedal_on(HARM, 1, t, 100)  # more sustain — opening up

# ── A major — "Knowledge." ──
# v2.0: A+C#+E = Knowledge+Boundary+Emotion
# v2.1 shape: RISE (confident — ascending toward understanding)
# v2.1 touch: resolute (firm, certain)

harm_rise(t, [A3, Cs4, E4], W, MF - 10, spacing=0.35)

# Domain thread: C# (Boundary) — tracked, with MORDENT (bitten into — earned)
add_mordent(DOM, 3, t + E, Cs4, MP - 10)
nt(DOM, 3, t + 0.5, Cs4, W * 2, MP - 15)  # sustained

# Melody: confident, rising — BLOCK touch (resolute)
nt_h(MEL, 0, t, A4, Q * 0.95, MF)
nt_h(MEL, 0, t + Q, Cs5, Q * 0.95, MF + 3)  # Boundary — clear
nt_h(MEL, 0, t + H, E5, H * 0.93, MF)        # Emotion — opening

# Bass: A — peso (heavy, weighted)
nt(BASS, 2, t, A2, W * 0.95, MF - 15)

t += W


# ── Amaj7 — "is beautiful" ──
# v2.0: A+C#+E+G# = Knowledge+Boundary+Emotion+SPIRIT
# v2.1 shape: BLOOM (Spirit radiates from the center — wondrous)

harm_bloom(t, [A3, Cs4, E4, Gs4], W, MF - 8, spacing=0.3)

# Melody: G# (Spirit) with TURN — savoring the wonder
nt_h(MEL, 0, t, E5, E, MF)
add_turn(MEL, 0, t + E, Gs5, MF + 3)       # SPIRIT — savored, turned over
nt_h(MEL, 0, t + E + 0.5, A5n, E, MF)      # Knowledge at the heights
nt_h(MEL, 0, t + H + E, Cs5, DQ, MF - 3)

# Bass: A
nt_h(BASS, 2, t, A2, W * 0.93, MF - 15)

t += W


# ── Aaug — "is INFINITE" ──
# v2.0: A+C#+F = Knowledge+Boundary+NATURE (world breaks in)
# v2.1 shape: first RISE then WAVE (oscillating — infinity has no resolution)
# v2.1: TRILL on F (Nature — the boundary shakes, reality vibrates)

# First: the chord establishes
harm_rise(t, [A3, Cs4, F4], H, MF - 5, spacing=0.25)

# Then: WAVE oscillation (the augmented chord has no center — it WAVES)
harm_wave(t + H, [A3, Cs4, F4], W, MF - 8)

# Melody: F5 (Nature) oscillating with E5 (Emotion) — reality vibrating
nt_h(MEL, 0, t, Cs5, Q, MF)
nt_h(MEL, 0, t + Q, E5, Q, MF)
nt_h(MEL, 0, t + H, F5, Q, MF + 5)          # Nature BREAKS IN
nt_h(MEL, 0, t + DH, E5, E, MF)             # oscillating
nt_h(MEL, 0, t + DH + E, F5, E, MF + 3)     # oscillating
nt_h(MEL, 0, t + W, F5, H, MF + 5)          # Nature HOLDS — infinite

# v2.1: TRILL on F4 in harmony — the boundary vibrates
add_vibrato(DOM, 3, t + H, F4, W, MP - 10, speed=0.12)  # fast = trill-like

# Bass: A — unmoved (knowledge persists beneath the shaking)
nt(BASS, 2, t, A2, LONG * 0.95, MF - 15)

t += LONG

pedal_off(HARM, 1, t)
t += S


# ── Expansion: E → B → F# ──
# v2.1: each chord in a different mode — the expansion CHANGES CHARACTER
# E = ECSTATIC (climbing, soaring)
# B = SACRED (growing, vast)  
# F# = NOSTALGIC (dissolving, fading into mystery)

pedal_on(HARM, 1, t, 110)  # full sustain — vast

# ── E major — Emotion+Spirit+Time ──
# v2.1 mode: ECSTATIC (climb shape, light touch)
# Shape: CLIMB (rapid upward — soaring)

sorted_e = sorted([E3, Gs3, B3])
spacing = 0.1  # rapid — ecstatic
for i, n in enumerate(sorted_e):
    hold = DH + Q - (i * spacing)
    nt_h(HARM, 1, t + (i * spacing), n, hold, MF - 10 + (i * 3))

# Melody: Spirit (G#) soars HIGH — with TRILL (ecstatic trembling)
nt_h(MEL, 0, t, E5, Q, MF)
# Trill on G#5 — ecstatic
trill_dur = DQ
trill_step = 0.09
for ti in range(int(trill_dur / trill_step)):
    n = Gs5 if ti % 2 == 0 else A5n
    nt(MEL, 0, t + Q + (ti * trill_step), n, trill_step * 1.1,
       humanize_vel(MF - 3))
nt_h(MEL, 0, t + Q + trill_dur + 0.05, B4, Q, MP)

# Bass: E
nt_h(BASS, 2, t, E3, DH * 0.92, MF - 15)

t += DH

# Walk: E → D# → D → C# → approaching B
nt_h(BASS, 2, t, Ds3, E * 0.9, MP - 12)
nt_h(BASS, 2, t + E, D3, E * 0.88, MP - 14)
nt_h(BASS, 2, t + Q, Cs3, E * 0.85, MP - 16)
nt_h(MEL, 0, t, Gs5, E, MP - 5)
nt_h(MEL, 0, t + E, Fs5, Q * 0.9, MP - 8)
t += DQ


# ── B major — Time+HOME+Unknown ──
# v2.1 mode: SACRED (grow shape — each note entering and sustaining)
# D# (Home) appears for the first time — treat it with REVERENCE

harm_grow(t, [B3, Ds4, Fs4], DH, MP - 5)

# v2.1: D# (Home) with HARMONIC — the ghost of home, barely there
add_harmonic(DOM, 3, t + E, Ds4, DH * 0.6, PP)

# Melody: D# gets GRACE NOTE from below (reaching up to Home)
add_grace_below(MEL, 0, t, Ds5, MP)
nt_h(MEL, 0, t, Ds5, DQ, MP)                    # HOME — arrived at with effort
nt_h(MEL, 0, t + DQ + 0.05, Fs5, DQ * 0.9, MP - 5)

# Bass: B — with harmonic
nt_h(BASS, 2, t, B2, DH * 0.9, MP - 12)
add_harmonic(BASS, 2, t, B2, H, PPP)

t += DH

# Walk: B → A# → A → G# → toward F#
nt_h(BASS, 2, t, As3, E * 0.88, P - 10)
nt_h(BASS, 2, t + E, A3, E * 0.85, P - 13)
nt_h(BASS, 2, t + Q, Gs3, E * 0.82, P - 16)
nt_h(MEL, 0, t, Cs5, DQ * 0.9, P - 8)
t += DQ


# ── F# major — Unknown+DESIRE+Boundary ──
# v2.1 mode: NOSTALGIC (dissolve shape — fading into the distance)

harm_dissolve(t, [Fs3, As3, Cs4], DH, P - 5)

# Melody: fading, each note softer — morendo
nt_h(MEL, 0, t, Cs5, Q * 0.9, P)
nt_h(MEL, 0, t + Q, As4, Q * 0.85, P - 5)
nt_h(MEL, 0, t + H, Fs4, Q * 0.8, P - 10)     # the farthest reach

# Bass: F# — morendo
nt_h(BASS, 2, t, Fs3, DH * 0.85, P - 12)

t += DH

pedal_off(HARM, 1, t)

# ── Silence of infinity ──
# v2.1: NOT EMPTY — the domain thread persists (E = Emotion)
# Plus echoes: harmonics of what was touched during expansion

nt(DOM, 3, t, E3, VERY, PPP)  # Emotion — always

# Echoes — harmonics (ghosts of the expansion)
add_harmonic(MEL, 0, t + Q, Gs4, Q, PPP)        # Spirit (ghost)
add_harmonic(MEL, 0, t + DH, Ds4, Q, PPP)       # Home (ghost)
nt_h(MEL, 0, t + W + 0.1, A4, Q, PPP)           # Knowledge (barely)
nt_h(MEL, 0, t + W + DQ + 0.15, E4, Q, PPP)     # Emotion (the thread)

t += VERY


# ==============================================================
# SECTION 2c: "knowing what is missing = knowing it all"
# v2.0: Am → bridge → A → dissolution → A5
# v2.1: TENDER → CONFESSING → SACRED → NOSTALGIC → DREAMING
#
# Each phase gets its own expressive character.
# The v2.0 architecture (four voices, domain tracking, 
# C→C# transformation) is COMPLETELY PRESERVED.
# ==============================================================

pedal_on(HARM, 1, t, 110)
pedal_on(BASS, 2, t, 80)

# ── Am — "knowing what is missing" ──
# v2.0: A+C+E = Knowledge+Self+Emotion
# v2.1 mode: TENDER (rise, legato, rubato pull)
# v2.1 ornament: vibrato on E4 (feeling is alive, warm)

# Harmony: RISE — tender, unfolding
harm_rise(t, [A3, C4, E4], LONG, PP, spacing=0.5)

# Domain thread: C4 (Self) — vibrato (alive, trembling)
add_vibrato(DOM, 3, t + Q, C4, LONG - Q, PP, speed=0.25)

# Melody: mirrors arpeggio — RUBATO (arrives slightly late each time)
nt_h(MEL, 0, t + 0.06, E5, Q, PP)               # Emotion (rubato)
nt_h(MEL, 0, t + Q + 0.08, C5, Q, PP)            # Self (rubato)
nt_h(MEL, 0, t + H + 0.1, A4, H, PP - 3)         # Knowledge (rubato — latest)

# v2.1: vibrato on E4 in harmony (feeling LIVES)
add_vibrato(HARM, 1, t + DH, E4, H, PP - 5, speed=0.22)

# Bass: A — deep, warm
nt_h(BASS, 2, t, A2, LONG, PP - 10)
nt_h(BASS, 2, t, A3, LONG, PPP)

t += LONG


# ═══════════════════════════════════════════════════════
# THE BRIDGE: C → C# (Self → Boundary)
# v2.0: explicit transformation tracked in domain voice
# v2.1: CONFESSING mode (portato, hesitant, close)
# v2.1: the C holds with TENUTO then yields with a SIGH
# ═══════════════════════════════════════════════════════

# Bass + E: pedal (Knowledge and Emotion persist)
nt(BASS, 2, t, A2, W + H, PP)
nt(BASS, 2, t, A3, W + H, PPP)
nt(HARM, 1, t, E4, W + H, PP)                   # Emotion: constant
nt(HARM, 1, t, A3, W + H, PP)                   # Knowledge: constant

# Phase 1: C holds — TENUTO — the self refuses to let go
nt(DOM, 3, t, C4, H + Q, PP)                    # Self — held to the last
# Melody: C5 — same tenuto
nt_h(MEL, 0, t + 0.05, C5, H, PP)               # Self — held

t += H

# Phase 2: the shift — HESITATION then GRACE NOTE
# v2.1: hesitation (tiny silence before the C#)
t += 0.12  # the hesitation — finding the courage

# Melody: B4 (Time) as appoggiatura — "through time..."
nt_h(MEL, 0, t, B4, Q * 0.9, PP)                # Time — appoggiatura

# Domain thread: C wavers... then C# enters with GRACE NOTE from below
# The grace note IS C natural — the self reaching up to become boundary
nt(DOM, 3, t + E, C4, 0.12, PP)                 # C — one last time
add_grace_below(DOM, 3, t + Q, Cs4, PP + 3)
nt(DOM, 3, t + Q, Cs4, DQ, PP + 3)              # C# — Boundary arrives

# Melody mirrors:
nt_h(MEL, 0, t + Q + 0.04, Cs5, Q, PP)          # C# — the shift

t += H


# ── A major — "knowing it all" ──
# v2.0: A+C#+E = Knowledge+Boundary+Emotion
# v2.1 mode: SACRED (grow, tenuto, fermata, open)
# v2.1 ornament: mordent on C# (boundary bitten into — this is EARNED)

# Harmony: GROW — sacred, accumulating
harm_grow(t, [A3, Cs4, E4], LONG + Q, PP)  # fermata — held longer

# Domain thread: C# sustained — with MORDENT then sustain
add_mordent(DOM, 3, t + E, Cs4, PP + 5)
nt(DOM, 3, t + 0.5, Cs4, LONG, PP)

# Melody: IDENTICAL rhythm to Am — same pattern, one note different
# v2.1: same rubato offsets as Am — the SAMENESS is the point
nt_h(MEL, 0, t + 0.06, E5, Q, PP)               # Emotion (same)
nt_h(MEL, 0, t + Q + 0.08, Cs5, Q, PP)           # BOUNDARY (was Self!)
nt_h(MEL, 0, t + H + 0.1, A4, H, PP - 3)         # Knowledge (same)

# Bass: A
nt(BASS, 2, t, A2, LONG + Q, PP - 10)

# v2.1: vibrato on E4 AGAIN — same as Am — feeling unchanged
add_vibrato(HARM, 1, t + DH, E4, H, PP - 5, speed=0.22)

t += LONG + Q


# ═══════════════════════════════════════════════════════
# DISSOLUTION: A → A5
# v2.0: C# fades while A and E strengthen
# v2.1: NOSTALGIC → DREAMING
# v2.1: C# gets HARMONIC (becomes a ghost) then SILENCE
# ═══════════════════════════════════════════════════════

# Phase 1: NOSTALGIC — dissolve shape, morendo, C# becoming ghost
pedal_off(HARM, 1, t)
pedal_on(HARM, 1, t, 120)  # full sustain — everything bleeds

harm_dissolve(t, [A3, Cs4, E4], W, PP - 5)

# C# as HARMONIC — it's becoming a ghost
add_harmonic(DOM, 3, t, Cs4, W * 0.7, PPP)

# A and E strengthen (bass)
nt(BASS, 2, t, A2, W, PP)
nt(BASS, 2, t, E3, W, PP + 5)                   # E slightly louder — strengthening

# Melody: A and E only — the pair establishing
nt_h(MEL, 0, t, A4, H, PP)
nt_h(MEL, 0, t + H, E5, H, PP + 3)

t += W

# Phase 2: DREAMING — the final chord (A5 = Knowledge + Emotion)
# v2.1 shape: BLOOM — the pair radiating from center
# v2.1 touch: leggiero — barely touching, weightless
# v2.1 space: open + sustained — infinite, vast
# v2.1 ornament: harmonic on E (feeling as overtone — the ultimate ghost)

# The A5 — Knowledge and Emotion — three octaves
# Deep
nt(BASS, 2, t, A2, FINAL, PPP)                  # Knowledge — deepest
nt(BASS, 2, t, E3, FINAL, PP)                   # Emotion

# Middle: BLOOM — E4 first (feeling = center), then A radiates
nt_h(HARM, 1, t, E4, FINAL, PP)                 # Emotion (center, first)
nt_h(HARM, 1, t + 0.4, A3, FINAL - 0.4, PP)     # Knowledge (radiates)

# High: arrives late — gently
nt_h(MEL, 0, t + 0.8, A4, FINAL - 0.8, PP)      # Knowledge — arriving
nt_h(MEL, 0, t + 1.2, E5, FINAL - 1.2, PP - 3)  # Emotion — last to arrive

# v2.1: HARMONIC on E — feeling as overtone — the ghost of all feeling
add_harmonic(MEL, 0, t + 2.0, E5, LONG, PPP)

# v2.1: very slow vibrato on E4 — warmth, life, humanity
# This is the last sign that the sound is ALIVE, not mechanical
add_vibrato(DOM, 3, t + DH, E4, VERY, PPP, speed=0.35)

# Domain thread: SILENCE on C and C#. 
# Neither Self nor Boundary. Nothing to track.
# The thread voice goes quiet. Its work is done.

t += FINAL

pedal_off(HARM, 1, t)
pedal_off(BASS, 2, t)

# Final silence
t += VERY


# ==============================================================
# Write
# ==============================================================

filename = "knowing_v2_1_full.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"""
  ╔══════════════════════════════════════════════════════════╗
  ║  KNOWING v2.1 FULL — Polyphonic + Expressive            ║
  ╠══════════════════════════════════════════════════════════╣
  ║  This is the MERGER of v2.0 and v2.1:                    ║
  ║                                                          ║
  ║  FROM v2.0 (preserved):                                  ║
  ║    ✓ Four independent voices (melody, harmony, bass, dom)║
  ║    ✓ Walking bass between roots                          ║
  ║    ✓ Independent melody with passing tones               ║
  ║    ✓ Domain tracking voice (C→C# transformation)         ║
  ║    ✓ Deliberate arpeggiation (polyphonic syntax)          ║
  ║    ✓ Full four-section structure                          ║
  ║    ✓ Connective tissue throughout                        ║
  ║                                                          ║
  ║  FROM v2.1 (added):                                      ║
  ║    + Expressive SHAPES on harmony                        ║
  ║      (rise, bloom, wave, grow, dissolve, scatter, climb) ║
  ║    + ORNAMENTS on melody and domain notes                ║
  ║      (mordent, turn, grace notes, trill, vibrato)        ║
  ║    + BREATH modifications (rubato, fermata, hesitation)  ║
  ║    + TOUCH variation (portato, tenuto, morendo, leggiero)║
  ║    + SPACE variation (half-pedal, sustained, open)       ║
  ║    + HUMANIZATION (velocity and timing micro-variation)  ║
  ║    + HARMONICS (ghost notes — the memory of domains)     ║
  ║                                                          ║
  ╠══════════════════════════════════════════════════════════╣
  ║  File:   {filename:<47s} ║
  ║  Tempo:  {BPM} BPM{' ' * 43} ║
  ║  Length: ~{minutes:.1f} min{' ' * 42} ║
  ╠══════════════════════════════════════════════════════════╣
  ║  Compare all FOUR versions:                              ║
  ║    knowing_harmonia.mid      v1.0 (telegram)             ║
  ║    knowing_fluid.mid         v1.1 (connected)            ║
  ║    knowing_v2.mid            v2.0 (polyphonic)           ║
  ║    knowing_v2_1_full.mid     v2.1 (polyphonic+expressive)║
  ║                                                          ║
  ║  What to listen for (v2.0 → v2.1):                      ║
  ║    - The arpeggios now BREATHE (shapes vary per chord)   ║
  ║    - Ornaments on key notes (turns, mordents, trills)    ║
  ║    - Rubato on melody (slightly late = human timing)     ║
  ║    - Vibrato on sustained E notes (feeling is ALIVE)     ║
  ║    - Harmonics (ghost notes — memories of domains)       ║
  ║    - Walking bass with morendo (each step slightly dying)║
  ║    - Hesitation before difficult moments                 ║
  ║    - The Aaug section WAVES (infinity has no center)     ║
  ║    - The E expansion TRILLS (ecstatic trembling)         ║
  ║    - The B chord treats D# (Home) with reverence         ║
  ║    - The F# chord DISSOLVES (fading into mystery)        ║
  ║    - C→C# bridge has GRACE NOTE (self reaching up)       ║
  ║    - Final A5 BLOOMS from E (feeling is the center)      ║
  ║    - Harmonic on final E (feeling becomes an overtone)   ║
  ║    - Slow vibrato on last E4 (the final sign of life)    ║
  ╚══════════════════════════════════════════════════════════╝
""")