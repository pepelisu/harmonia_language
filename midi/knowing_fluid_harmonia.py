"""
KNOWING (FLUID VERSION) — Harmonia v1.1
"Life is a story that we tell to ourselves..."

This version adds the connective tissue:
  - Walking bass between chords (prepositions)
  - Melodic bridges (conjunctions)
  - Common tone sustains (continuity)
  - Pickup notes (anticipation)
  - Appoggiaturas (subtext)
  - Continuous rhythmic pulse (heartbeat)

Compare with knowing_harmonia.mid (v1.0) to hear the difference.

Run: python knowing_fluid.py
Output: knowing_fluid.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────
BPM = 66

# Durations
S    = 0.25     # sixteenth
E    = 0.5      # eighth
DE   = 0.75     # dotted eighth
Q    = 1.0      # quarter
DQ   = 1.5      # dotted quarter
H    = 2.0      # half
DH   = 3.0      # dotted half
W    = 4.0      # whole
LONG = 6.0
VERY = 8.0
FINAL = 14.0

# Dynamics
PPP  = 22; PP = 35; P = 45; MP = 58; MF = 75; F = 95

# ── MIDI Notes ────────────────────────────────────────
A2=45; B2=47
C3=48; Cs3=49; D3=50; Ds3=51; E3=52; F3=53; Fs3=54
G3=55; Gs3=56; A3=57; As3=58; Bb3=58; B3=59
C4=60; Cs4=61; D4=62; Ds4=63; E4=64; F4=65; Fs4=66
G4=67; Gs4=68; A4=69; As4=70; Bb4=70; B4=71
C5=72; Cs5=73; D5=74; Ds5=75; E5=76; F5=77; Fs5=78
G5=79; Gs5=80; A5n=81; B5=83

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(4, adjust_origin=False)

MEL  = 0    # Melody (right hand upper)
HAR  = 1    # Harmony (right hand lower / inner voices)
LH   = 2    # Left hand (bass + lower harmony)
PED  = 3    # Pedal / sustained tones (inner voice continuity)

midi.addTempo(0, 0, BPM)

for track in range(4):
    midi.addProgramChange(track, track, 0, 0)  # All piano

midi.addTrackName(MEL, 0, "Melody - The Voice")
midi.addTrackName(HAR, 0, "Harmony - Inner Voices")
midi.addTrackName(LH,  0, "Left Hand - Bass & Foundation")
midi.addTrackName(PED, 0, "Sustained Tones - Continuity")

# ── Helpers ───────────────────────────────────────────
def nt(track, chan, time, pitch, dur, vel):
    midi.addNote(track, chan, pitch, time, dur, vel)

def ch(track, chan, time, notes, dur, vel):
    for n in notes:
        midi.addNote(track, chan, n, time, dur, vel)

def arp_up(track, chan, time, notes, total_dur, vel, spacing=0.18):
    for i, n in enumerate(notes):
        hold = total_dur - (i * spacing)
        if hold < 0.3: hold = 0.3
        nt(track, chan, time + (i * spacing), n, hold, vel)

def walk(track, chan, start_time, notes, note_dur, vel):
    """Play a series of bass notes (walking bass line)."""
    t = start_time
    for n in notes:
        nt(track, chan, t, n, note_dur, vel)
        t += note_dur
    return t

def sustain_on(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 127)

def sustain_off(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 0)

# ── Time Cursor ───────────────────────────────────────
t = 0.0

# ==============================================================
# PICKUP: E4 — "Feel."
# But now with a gentle bass note establishing the ground
# ==============================================================

sustain_on(LH, 2, t)
sustain_on(PED, 3, t)

# E4 melody — feeling
nt(MEL, 0, t, E4, DQ, PP)

# Soft bass A — the key, barely heard, the ground
nt(LH, 2, t, A2, DQ, PPP)

# Already establishing the continuous E as inner voice
nt(PED, 3, t, E3, DQ, PPP)  # E sustained from the very start

t += DQ


# ==============================================================
# SECTION 1: "Life is a story that we tell to ourselves"
# 6/8 lilt — NOW WITH FLOWING CONNECTIONS
#
# C → Cmaj7 → G → D → C/E
#
# Connectors added:
#   - Arpeggiated left hand (continuous pulse)
#   - Walking bass between roots
#   - Melodic bridges (step-wise, with pickups)
#   - E sustained as common tone (emotion persists)
# ==============================================================

# ── C major — "Life..." ──
# Arpeggiated left hand creates pulse (the heartbeat begins)
arp_up(LH, 2, t, [C3, G3, C4], DH, MP - 15)
# Inner voice: E sustained (common tone with Am that will come later)
nt(PED, 3, t, E3, DH * 2, PP)  # E held across C and Cmaj7

# Melody: E4 rises through G4
nt(MEL, 0, t, E4, DQ, MP)
nt(MEL, 0, t + DQ, F4, E, MP - 5)    # passing tone — "and" — step up
nt(MEL, 0, t + DQ + E, G4, Q, MP)    # arrives at G (connection)
t += DH

# ── Walking bass: C → D → E → ... (approaching Cmaj7) ──
# The walk from C to C is... C stays! But the inner voice moves.
# Bass pulses: the left hand arpeggiates continuously

# ── Cmaj7 — "...is a wondrous story" ──
arp_up(LH, 2, t, [C3, G3, B3], DH, MP - 15)  # B appears (Time enters!)

# Melody: G4 → A4 → B4 (ascending — the story opens upward)
nt(MEL, 0, t, A4, E, MP)              # step up — "and"
nt(MEL, 0, t + E, B4, Q, MP)          # arrives at B (Time — the 7th)
nt(MEL, 0, t + E + Q, A4, DQ, MP)     # settles back — "then"
t += DH

# ── Walking bass: C → D → ... to G ──
# Bass walks from C up to G (the next root)
nt(LH, 2, t, D3, DQ, MP - 15)        # D (Action) — "stepping toward"
nt(LH, 2, t + DQ, E3, E, MP - 15)    # E (Emotion) — "through feeling"
# Melody: pickup into G chord
nt(MEL, 0, t + DQ, D5, E, MP - 5)    # pickup — "which then—"
nt(MEL, 0, t + DQ + E, E5, E, MP - 5) # pickup — "leads to—"
t += H

# ── G major — "We..." ──
arp_up(LH, 2, t, [G3, B3, D4], DH, MP - 15)
nt(PED, 3, t, D4, DH, PP)            # D sustained (action — the common tone with D chord)

# Melody: arrives on G4, leaps to D5
nt(MEL, 0, t, G4, DQ, MP)             # G — connection — "We"
nt(MEL, 0, t + DQ, B4, E, MP)         # passing B (Time) — "through time"
nt(MEL, 0, t + DQ + E, D5, Q, MP)     # arrives D (Action) — "tell"
t += DH

# ── Walking bass: G → F# → E → ... to C/E ──
nt(LH, 2, t, Fs3, E, MP - 15)        # F# (Unknown) — "through the unknown"
nt(MEL, 0, t, D5, E, MP - 5)          # melody holds on D — "still telling"
t += E
nt(LH, 2, t, E3, E, MP - 15)         # E (Emotion) — "through feeling"
nt(MEL, 0, t, C5, E, MP - 5)          # melody steps down — "and"
t += E
# Pickup notes into C/E
nt(MEL, 0, t, B4, E, MP - 10)         # passing B — "and then"
t += E

# ── D major (brief) — "tell" ──
ch(LH, 2, t, [D3, A3], DQ, MP - 15)
nt(MEL, 0, t, A4, DQ, MP)             # A — knowledge — "telling is knowing"
# Passing notes down
nt(MEL, 0, t + DQ, G4, E, MP - 10)    # step down — "which settles"
nt(MEL, 0, t + DQ + E, F4, E, MP - 10) # step down — "gently into"
t += H

# ── C/E — "to ourselves" ──
arp_up(LH, 2, t, [E3, G3, C4], DH, MP - 15)
nt(PED, 3, t, E3, DH, PP)             # E in bass — feeling is the ground

# Melody: arrives on E4, settles
nt(MEL, 0, t, E4, H, MP)              # E — feeling — home
# Appoggiatura! The melody touches F4 (nature/world) before settling on E4
# "Before I could rest in feeling, I first felt the world"
nt(MEL, 0, t + H, F4, E, MP - 10)     # appoggiatura — "despite"
nt(MEL, 0, t + H + E, E4, Q, MP - 5)  # resolution — "arriving"
# Final note: C4 (self) — the circle closes
nt(MEL, 0, t + DH - E, C4, E, P)      # "self" — whispered
t += DH

# ── Transition: bass walks down from E3 to A2 ──
# "From feeling... descending toward knowledge..."
sustain_off(LH, 2, t)
sustain_off(PED, 3, t)

nt(LH, 2, t, D3, Q, P - 10)          # D — "through action"
nt(LH, 2, t + Q, C3, Q, P - 10)      # C — "through self"
nt(LH, 2, t + Q * 2, B2, Q, P - 10)  # B — "through time"
nt(MEL, 0, t + Q, B3, Q, PP)          # echo — "time..." (the sigh)
nt(MEL, 0, t + Q * 2, A3, Q, PP)      # "...settling"
t += DH


# ==============================================================
# SECTION 2a: "You don't know what you still have to learn"
# FLOWING VERSION with chromatic inner line
# Am → F#m → Dsus4 → A7
# ==============================================================

sustain_on(LH, 2, t)
sustain_on(PED, 3, t)

# ── Am — "You don't know" ──
arp_up(LH, 2, t, [A2, E3, A3], DH, P - 5)
ch(HAR, 1, t, [C4, E4], DH, P)        # inner voices: C and E (Being and Emotion)
nt(PED, 3, t, E4, DH * 2, PP)         # E sustained — feeling persists

# Melody: starts high, descends — the realization falls
nt(MEL, 0, t, E5, DQ, P)              # E — "the feeling of not-knowing"
nt(MEL, 0, t + DQ, D5, E, P)          # step down — "and"
nt(MEL, 0, t + DQ + E, C5, Q, P)      # C — "the self doesn't"
t += DH

# ── Chromatic inner line begins: C4 → B3 ──
# (Being begins to descend — the self is shifting beneath the surface)
# Walking bass: A → G# → G → F# (chromatic descent — "inevitably...")
nt(LH, 2, t, Gs3, E, P - 10)         # G# — chromatic — "inevitably"
nt(LH, 2, t + E, G3, E, P - 10)      # G — connection — "through others"
nt(LH, 2, t + Q, Fs3, E, P - 10)     # F# — "toward the unknown"

# Melody pickup into F#m
nt(MEL, 0, t, B4, E, P - 5)           # step down — "which"
nt(MEL, 0, t + E, A4, E, P - 5)       # step down — "leads to"
t += DQ

# ── F#m — "the unknown is felt" ──
arp_up(LH, 2, t, [Fs3, Cs4, Fs4], DH, P - 5)
nt(HAR, 1, t, Cs4, DH, P)             # inner voice: C# (the boundary)
# Inner chromatic line: C → B (previous) → now Cs (it shifted!)
# The inner voice JUMPED from natural territory to sharp territory
# "The self crossed a boundary"

nt(MEL, 0, t, Cs5, DQ, P)             # C# — boundary, edge
nt(MEL, 0, t + DQ, A4, DQ, P)         # descends to A — knowledge
t += DH

# ── Walking bass: F# → E → D (descending — "falling toward...") ──
nt(LH, 2, t, E3, Q, P - 10)           # E — "through feeling"
nt(LH, 2, t + Q, D3, Q, P - 10)       # D — "arriving at action"
# Melody connector
nt(MEL, 0, t, A4, Q, P - 5)           # held — "still"
nt(MEL, 0, t + Q, G4, Q, P - 5)       # step down — "settling"
t += H

# ── Dsus4 — "action waits" ──
ch(LH, 2, t, [D3, A3], H, P - 5)
ch(HAR, 1, t, [G4, A4], H, P)         # sus4 voicing — G and A together — waiting
nt(MEL, 0, t, G4, Q, P)               # G — the sus4 note — "waiting"
# The melody DOESN'T resolve the sus4 — it holds
nt(MEL, 0, t + Q, A4, Q, P)           # steps to A — but doesn't go to F# (no resolution)
t += H

# ── Into A7: chromatic approach from below ──
nt(LH, 2, t, Gs3, E, P - 10)         # G# — chromatic approach — "inevitably leading to"
nt(MEL, 0, t, Gs4, E, P - 5)          # melody mirrors bass — "pressing toward"
t += E

# ── A7 — "What?" ──
arp_up(LH, 2, t, [A2, E3, A3], W, P - 5)
ch(HAR, 1, t, [Cs4, G4], W, P)        # the 7th chord — C# and G — boundary and connection
nt(MEL, 0, t, E5, Q, P)               # E — feeling the question
nt(MEL, 0, t + Q, G4, Q, P)           # G — the 7th — the question itself
nt(MEL, 0, t + H, E4, H, P)           # settling on E — feeling — waiting

# Inner sustained E
nt(PED, 3, t, E4, W + H, PP)          # E — "feeling persists even through the question"
t += W

sustain_off(LH, 2, t)
sustain_off(PED, 3, t)

# ── Transitional silence — but NOT empty ──
# A single bass note walks the bridge
nt(LH, 2, t, E3, Q, PPP)             # E lingers — "the feeling remains"
nt(LH, 2, t + Q, Gs3, Q, PPP)        # G# — chromatic — "shifting toward"
t += H


# ==============================================================
# SECTION 2b: "because knowledge is infinite"
# NOW with expansion and continuous motion
# A → Amaj7 → Aaug → E → B → F# → (silence)
# ==============================================================

sustain_on(LH, 2, t)
sustain_on(PED, 3, t)

# ── A major — "Knowledge." ──
arp_up(LH, 2, t, [A2, E3, A3, Cs4], W, MF - 10)
nt(PED, 3, t, E3, W * 2, MP)          # E sustained — ALWAYS present

# Melody: confident, rising
nt(MEL, 0, t, A4, Q, MF)              # A — "Knowledge"
nt(MEL, 0, t + Q, B4, E, MF)          # step up — "and"
nt(MEL, 0, t + Q + E, Cs5, Q, MF)     # C# — "clarity"
nt(MEL, 0, t + H + E, E5, DQ, MF)     # leap to E — "opening into feeling"
t += W

# ── Amaj7 — "is beautiful" ──
# The G# (major 7th) appears — wonder enters
arp_up(LH, 2, t, [A2, E3, A3, Cs4], W, MF - 10)
nt(HAR, 1, t, Gs4, W, MF - 10)        # the maj7 — wonder — shimmering

# Melody: turns around the G# — savoring the wonder
nt(MEL, 0, t, E5, E, MF)
nt(MEL, 0, t + E, Gs4, Q, MF)         # the maj7 — "wonder"
nt(MEL, 0, t + E + Q, A4, E, MF)      # turn — "savoring"
nt(MEL, 0, t + Q * 2, Cs5, H, MF)     # rises — "beauty"
t += W

# ── Aaug — "is INFINITE" ──
# A - C# - E#(F) — the boundary breaks
ch(LH, 2, t, [A2, E3], LONG, MF - 10)
ch(HAR, 1, t, [Cs4, F4], LONG, MF - 5)  # the augmented — F natural! — the 5th BREAKS

# Melody: the F5 — the boundary breaking — repeated, oscillating
nt(MEL, 0, t, Cs5, Q, MF)             # C# — boundary
nt(MEL, 0, t + Q, E5, Q, MF)          # E — feeling
nt(MEL, 0, t + H, F5, Q, MF)          # F! — the break — nature INTRUDES
nt(MEL, 0, t + DH, E5, Q, MF)         # back to E — oscillating
nt(MEL, 0, t + W, F5, H, MF)          # F holds — the expansion is real
t += LONG

sustain_off(LH, 2, t)
sustain_off(PED, 3, t)

# ── The Expansion: E → B → F# (connected by walking bass) ──

sustain_on(LH, 2, t)
sustain_on(PED, 3, t)

# Walking bass descends chromatically: A → G# → G → F# → F → E
# "Through boundary, connection, the unknown, nature, arriving at feeling"
# This chromatic descent IS the experience of infinity — passing through 
# every domain on the way out to the edge of the knowable

# E major — "it touches feeling"
arp_up(LH, 2, t, [E3, Gs3, B3], DH, MF - 10)
nt(MEL, 0, t, E5, DQ, MF)
nt(MEL, 0, t + DQ, Gs5, DQ, MP)       # rising to G# — "toward wonder"
nt(PED, 3, t, B3, DH, MP)             # B — time — sustained
t += DH

# Walking bass: E → D# → D → C# → B
nt(LH, 2, t, Ds3, E, MP - 10)         # "homeward" — Eb=Home
nt(LH, 2, t + E, D3, E, MP - 10)      # "through action"
nt(LH, 2, t + Q, Cs3, E, MP - 10)     # "through boundary"
nt(MEL, 0, t, Fs5, DQ, MP)            # melody descends from heights
t += DQ

# B major — "spans time"
arp_up(LH, 2, t, [B2, Ds3, Fs3], DH, MP - 10)
nt(MEL, 0, t, Ds5, DQ, MP)            # D# — home echoing
nt(MEL, 0, t + DQ, Fs5, DQ, MP - 5)   # F# — the unknown
nt(PED, 3, t, Fs3, DH, P)             # F# sustained — the unknown persists
t += DH

# Walking bass: B → A# → A → G# → G → F#
nt(LH, 2, t, As3, E, P - 10)          # "through desire"
nt(LH, 2, t + E, A3, E, P - 10)       # "through knowledge"
nt(LH, 2, t + Q, Gs3, E, P - 10)      # "through spirit"
nt(MEL, 0, t, Cs5, DQ, P - 5)         # melody fading — further out
t += DQ

# F# major — "reaches the unknown"
arp_up(LH, 2, t, [Fs3, As3, Cs4], DH, P - 10)
nt(MEL, 0, t, Cs5, Q, P)
nt(MEL, 0, t + Q, As4, Q, P - 5)
nt(MEL, 0, t + H, Fs4, Q, P - 10)     # melody descends into the unknown
nt(PED, 3, t, Cs4, DH, PP)            # the boundary — far, distant
t += DH

sustain_off(LH, 2, t)
sustain_off(PED, 3, t)

# ── The Silence of Infinity ──
# Not fully empty — a single E holds, ppp, the thread that never breaks
nt(PED, 3, t, E3, VERY, PPP)          # E — feeling — the only note that persists
                                        # through infinity — because feeling has no limit
# Faint echoes in the melody — fragments of what was heard
nt(MEL, 0, t + H, A4, Q, PPP)         # whisper: "knowledge"
nt(MEL, 0, t + W, E4, Q, PPP)         # whisper: "feeling"
t += VERY


# ==============================================================
# SECTION 2c: "knowing what is missing = knowing it all"
# THE TRANSFORMATION — now with the connective tissue
# that makes the half-step FEEL like a journey
# Am → A → A5
# ==============================================================

sustain_on(LH, 2, t)
sustain_on(MEL, 0, t)
sustain_on(HAR, 1, t)
sustain_on(PED, 3, t)

# ── Am — "knowing what is missing" ──
# Full, rich, arpeggiated — every note of the chord unfolded
arp_up(LH, 2, t, [A2, E3, A3], LONG, PP)
nt(HAR, 1, t, C4, LONG, PP)           # C — the minor third — BEING — the note that will change

# Melody: simple, clear, arriving
nt(MEL, 0, t, E5, Q, PP)              # E — feeling
nt(MEL, 0, t + Q, C5, Q, PP)          # C — being (the minor third)
nt(MEL, 0, t + H, A4, H, PP)          # A — knowledge
# Sustained
nt(PED, 3, t, E4, LONG, PPP)          # E — always present

t += LONG

# ══════════════════════════════════════════════════════════
# THE BRIDGE — the connective tissue that IS the transformation
#
# Instead of silence between Am and A, we now have:
# A CHROMATIC ASCENT in the inner voice: C → C#
# While the bass HOLDS (pedal A — "knowledge persists")
# And the melody TRACES the transformation
#
# This is the half-step made into a journey.
# ══════════════════════════════════════════════════════════

# Bass: A pedal — "throughout this, knowledge persists"
nt(LH, 2, t, A2, W, PP)
nt(LH, 2, t, A3, W, PP)

# Inner voice: C4 begins to rise
# This is the transformation in slow motion:
# The minor third (C) ascending to the major third (C#)
# "Being... pressing toward the boundary..."

nt(HAR, 1, t, C4, H, PP)              # C held — "being, still"
# Melody echoes the held C
nt(MEL, 0, t, C5, H, PP)              # C — "still here"

t += H

# The chromatic moment — C starts moving to C#
# But first — an appoggiatura-like gesture:
# The melody touches B4 (Time) before arriving at C#
# "Through time... the boundary shifts..."

nt(MEL, 0, t, B4, Q, PP)              # B — time — "through time"
# Inner voice: C... wavering... about to shift
nt(HAR, 1, t, C4, E, PP)              # still C
nt(HAR, 1, t + E, Cs4, DQ, PP)        # C# APPEARS — the transformation!
                                        # "The self reaches the boundary"
                                        # "Being becomes... something else"
                                        # One half step. The entire truth.

nt(MEL, 0, t + Q, Cs5, Q, PP)         # Melody mirrors: C# — "becoming"
t += H

# ── A major — "knowing it all" ──
# Now fully major — but arrived at through JOURNEY, not jump
arp_up(LH, 2, t, [A2, E3, A3], LONG, PP)
nt(HAR, 1, t, Cs4, LONG, PP)          # C# sustained — "the boundary crossed"
nt(PED, 3, t, E4, LONG, PPP)          # E — feeling — "still here"

# Melody: mirrors the Am melody exactly — same rhythm — different note
nt(MEL, 0, t, E5, Q, PP)              # same E — feeling hasn't changed
nt(MEL, 0, t + Q, Cs5, Q, PP)         # C# instead of C — the only difference
nt(MEL, 0, t + H, A4, H, PP)          # same A — knowledge hasn't changed

# Only the third changed. Everything else is identical.
# "Knowing what is missing" and "knowing it all" are
# the SAME melody, the SAME rhythm, the SAME feeling —
# one note apart.

t += LONG

# ══════════════════════════════════════════════════════════
# THE DISSOLUTION — the third fades, leaving A5
#
# Connected by: the C# gradually fading in velocity
# While A and E strengthen
# A slow crossfade from three notes to two
# ══════════════════════════════════════════════════════════

# Phase 1: C# begins to fade (the distinction weakening)
nt(LH, 2, t, A2, W, PP)
nt(LH, 2, t, E3, W, PP)               # A and E in bass — strengthening
nt(HAR, 1, t, Cs4, W, P - 10)         # C# — still present but quieter
nt(MEL, 0, t, A4, H, PP)              # A
nt(MEL, 0, t + H, E5, H, PP)          # E — the pair establishing
nt(PED, 3, t, E4, W, PP)              # E sustained
t += W

# Phase 2: C# barely audible (the distinction dissolving)
nt(LH, 2, t, A2, W, PPP)
nt(LH, 2, t, E3, W, PP)
nt(HAR, 1, t, Cs4, W, PPP)            # C# — almost gone
nt(MEL, 0, t, E5, W, PP)              # E — holding
nt(PED, 3, t, A4, W, PP)              # A — in the middle — knowledge
t += W

# Phase 3: A5 — only A and E remain
# Three octaves of the same two notes
# Knowledge and Feeling, everywhere, all at once
nt(LH, 2, t, A2, FINAL, PPP)          # deep A
nt(LH, 2, t, E3, FINAL, PP)           # E
nt(HAR, 1, t, A3, FINAL, PP)          # A
nt(PED, 3, t, E4, FINAL, PP)          # E
nt(MEL, 0, t, A4, FINAL, PP)          # A
nt(MEL, 0, t + Q, E5, FINAL - Q, PP)  # E — the last note to enter
                                        # (it arrives gently, joins the A)
                                        # (they sound together)
                                        # (they always have)

t += FINAL

sustain_off(LH, 2, t)
sustain_off(MEL, 0, t)
sustain_off(HAR, 1, t)
sustain_off(PED, 3, t)

# Final silence
t += VERY

# ==============================================================
# Write
# ==============================================================

filename = "knowing_fluid.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  ╔═══════════════════════════════════════════════════╗")
print(f"  ║  KNOWING (FLUID) — Harmonia v1.1                 ║")
print(f"  ╠═══════════════════════════════════════════════════╣")
print(f"  ║  Now with connective tissue:                      ║")
print(f"  ║    • Walking bass (prepositions)                  ║")
print(f"  ║    • Melodic bridges (conjunctions)               ║")
print(f"  ║    • Sustained common tones (continuity)          ║")
print(f"  ║    • Pickup notes (anticipation)                  ║")
print(f"  ║    • Appoggiaturas (subtext)                      ║")
print(f"  ║    • Chromatic inner line (slow transformation)   ║")
print(f"  ║    • Continuous pulse (heartbeat)                 ║")
print(f"  ╠═══════════════════════════════════════════════════╣")
print(f"  ║  File:   {filename:<40s} ║")
print(f"  ║  Tempo:  {BPM} BPM{' ' * 36} ║")
print(f"  ║  Length: ~{minutes:.1f} min{' ' * 35} ║")
print(f"  ╠═══════════════════════════════════════════════════╣")
print(f"  ║  Compare with knowing_harmonia.mid (v1.0)         ║")
print(f"  ║  to hear the difference between:                  ║")
print(f"  ║    v1.0: 'Word. Silence. Word.' (telegraphic)     ║")
print(f"  ║    v1.1: 'Word flowing into word' (speech)        ║")
print(f"  ╠═══════════════════════════════════════════════════╣")
print(f"  ║  The key connector to listen for:                 ║")
print(f"  ║                                                    ║")
print(f"  ║  In v1.0, Am→A was a jump (minor→major).          ║")
print(f"  ║  In v1.1, the C inside Am gradually rises to C#   ║")
print(f"  ║  while A and E hold steady around it.             ║")
print(f"  ║  The transformation is no longer an event.         ║")
print(f"  ║  It is a journey.                                  ║")
print(f"  ║  One half step, taken slowly, with feeling.        ║")
print(f"  ╚═══════════════════════════════════════════════════╝")
