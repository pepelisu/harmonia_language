"""
KNOWING — Original Composition in Harmonia
"Life is a story that we tell to ourselves..."

Key: A (undefined → the distinction between major and minor dissolves)
Meter: 6/8 → 4/4 → Free time
Voice: Piano alone — the self speaking to itself

Run: python knowing_harmonia.py
Output: knowing_harmonia.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────
BPM = 66   # Andante — walking and thinking

# Durations (quarter-note beats)
S    = 0.5     # sixteenth feel
E    = 0.75    # eighth in 6/8
Q    = 1.0     # quarter
DQ   = 1.5     # dotted quarter (one 6/8 beat)
H    = 2.0     # half
DH   = 3.0     # dotted half (one 6/8 measure)
W    = 4.0     # whole
LONG = 6.0     # sustained
VERY = 8.0     # deeply sustained
FINAL = 12.0   # the final chord — held until the world ends

# Dynamics
PPP  = 22
PP   = 35
P    = 48
MP   = 60
MF   = 78
F    = 100

# ── MIDI Notes ────────────────────────────────────────
# Octave 2
A2  = 45; B2  = 47
# Octave 3
C3  = 48; Cs3 = 49; D3  = 50; Ds3 = 51; Eb3 = 51
E3  = 52; F3  = 53; Fs3 = 54; G3  = 55; Gs3 = 56
Ab3 = 56; A3  = 57; As3 = 58; Bb3 = 58; B3  = 59
# Octave 4
C4  = 60; Cs4 = 61; D4  = 62; Ds4 = 63; Eb4 = 63
E4  = 64; F4  = 65; Fs4 = 66; G4  = 67; Gs4 = 68
Ab4 = 68; A4  = 69; As4 = 70; Bb4 = 70; B4  = 71
# Octave 5
C5  = 72; Cs5 = 73; D5  = 74; Ds5 = 75; Eb5 = 75
E5  = 76; F5  = 77; Fs5 = 78; G5  = 79; A5n = 81
B5  = 83

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(3, adjust_origin=False)

RH  = 0    # Right hand — melody, the voice
LH  = 1    # Left hand — harmony, the frame
BAS = 2    # Bass notes — the ground

midi.addTempo(0, 0, BPM)

# All three tracks are piano
midi.addProgramChange(RH,  0, 0, 0)    # Acoustic Grand Piano
midi.addProgramChange(LH,  1, 0, 0)    # Acoustic Grand Piano
midi.addProgramChange(BAS, 2, 0, 0)    # Acoustic Grand Piano

# Track names
midi.addTrackName(RH,  0, "Right Hand - Voice")
midi.addTrackName(LH,  1, "Left Hand - Harmony")
midi.addTrackName(BAS, 2, "Bass")

# ── Helpers ───────────────────────────────────────────
def ch(track, chan, time, notes, dur, vel):
    for n in notes:
        midi.addNote(track, chan, n, time, dur, vel)

def nt(track, chan, time, pitch, dur, vel):
    midi.addNote(track, chan, pitch, time, dur, vel)

def arp(track, chan, time, notes, total_dur, vel, spacing=0.2):
    """Arpeggiate a chord — each note slightly staggered."""
    for i, n in enumerate(notes):
        hold = total_dur - (i * spacing)
        if hold < 0.5:
            hold = 0.5
        nt(track, chan, time + (i * spacing), n, hold, vel)

def sustain_on(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 127)

def sustain_off(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 0)

# ── Time Cursor ───────────────────────────────────────
t = 0.0

# ==============================================================
# THE PICKUP: E4 — "Feel."
# A single note. Emotion. Before everything.
# ==============================================================

nt(RH, 0, t, E4, DQ, PP)
t += DQ

# Brief breath
t += S

# ==============================================================
# SECTION 1: "Life is a story that we tell to ourselves"
# 6/8 lilt — narrative — mp — arpeggiated
# C → Cmaj7 → G → D → C/E
# ==============================================================

sustain_on(LH, 1, t)

# ── C major — "Life..." (arpeggiated — being unfolds) ──
arp(LH, 1, t, [C3, E3, G3], DH, MP)
nt(RH, 0, t, E4, DQ, MP)            # melody starts on E (feeling)
nt(RH, 0, t + DQ, G4, DQ, MP)       # rises to G (connection)
nt(BAS, 2, t, C3, DH, MP - 15)
t += DH

# ── Cmaj7 — "...is a wondrous story" (time enters being) ──
arp(LH, 1, t, [C3, E3, G3, B3], DH, MP)
nt(RH, 0, t, B4, DQ, MP)            # melody reaches B (time — the 7th)
nt(RH, 0, t + DQ, A4, DQ, MP)       # descends to A (knowledge appears)
nt(BAS, 2, t, C3, DH, MP - 15)
t += DH

# ── G major — "We..." (connection, together) ──
ch(LH, 1, t, [G3, B3, D4], DH, MP)
nt(RH, 0, t, G4, DQ, MP)            # melody on G (connection)
nt(RH, 0, t + DQ, D5, DQ, MP)       # leaps to D (action — "tell")
nt(BAS, 2, t, G3, DH, MP - 15)
t += DH

# ── D major — "...tell" (action) ──
ch(LH, 1, t, [D3, Fs3, A3], DQ, MP)
nt(RH, 0, t, D5, DQ, MP)            # melody holds on D (action)
nt(BAS, 2, t, D3, DQ, MP - 15)
t += DQ

# Brief passing tone — descent
nt(RH, 0, t, C5, S, MP - 10)        # passing C (being, descending)
t += S
nt(RH, 0, t, B4, S, MP - 10)        # passing B (time)
t += S

# ── C/E — "...to ourselves" (self as receiver, bass on E=feeling) ──
arp(LH, 1, t, [E3, G3, C4], DH, MP)
nt(RH, 0, t, E4, H, MP)             # melody arrives on E — feeling
nt(RH, 0, t + H, C4, Q, MP - 10)    # settles on C — being
nt(BAS, 2, t, E3, DH, MP - 15)      # bass on E — self rests on feeling
t += DH

sustain_off(LH, 1, t)

# ── Breath between sentences ──
t += Q

# ==============================================================
# SECTION 2a: "You don't know what you still have to learn"
# 6/8 slowing toward 4/4 — narrative becomes testimony
# Am → F#m → Dsus4 → A7
# Dynamic: p — intimate, almost reluctant
# ==============================================================

sustain_on(LH, 1, t)

# ── Am — "You don't know" ──
ch(LH, 1, t, [A3, C4, E4], DH, P)
nt(RH, 0, t, E5, DQ, P)             # high E — feeling the absence
nt(RH, 0, t + DQ, C5, DQ, P)        # descends to C — being, questioning
nt(BAS, 2, t, A2, DH, P - 10)
t += DH

# ── F#m — "the unknown is felt" ──
ch(LH, 1, t, [Fs3, A3, Cs4], DH, P)
nt(RH, 0, t, Cs5, DQ, P)            # C# — the boundary, the edge
nt(RH, 0, t + DQ, A4, DQ, P)        # descends to A — knowledge (but minor)
nt(BAS, 2, t, Fs3, DH, P - 10)
t += DH

# ── Dsus4 — "action waits" ──
ch(LH, 1, t, [D3, G3, A3], H, P)
nt(RH, 0, t, G4, H, P)              # G — connection (sus4 note — waiting)
nt(BAS, 2, t, D3, H, P - 10)
t += H

# ── A7 — "What?" (the question hangs) ──
ch(LH, 1, t, [A3, Cs4, E4, G4], LONG, P)
nt(RH, 0, t, G4, Q, P)              # the b7 — the question tone
nt(RH, 0, t + Q, E4, Q, P)          # descends to E — feeling the question
nt(BAS, 2, t, A2, LONG, P - 10)

# Let the question ring
t += LONG

sustain_off(LH, 1, t)

# ── Breath — the shift from narrative to testimony ──
t += H

# ==============================================================
# SECTION 2b: "because knowledge is infinite"
# 4/4 — declarative — mf — the thesis
# A → Amaj7 → Aaug → E → B → F# → (silence)
# ==============================================================

sustain_on(LH, 1, t)

# ── A major — "Knowledge." (clear, affirmed) ──
ch(LH, 1, t, [A3, Cs4, E4], W, MF)
nt(RH, 0, t, E5, Q, MF)             # high E — feeling illuminated
nt(RH, 0, t + Q, Cs5, Q, MF)        # descends to C# — clear, major
nt(RH, 0, t + 2*Q, A4, H, MF)       # arrives on A — knowledge itself
nt(BAS, 2, t, A2, W, MF - 15)
t += W

# ── Amaj7 — "is beautiful" ──
ch(LH, 1, t, [A3, Cs4, E4, Gs4], W, MF)
nt(RH, 0, t, Gs4, Q, MF)            # the maj7 — wonder
nt(RH, 0, t + Q, A4, Q, MF)         # resolves up to A
nt(RH, 0, t + 2*Q, Cs5, H, MF)      # rises to C# — beauty
nt(BAS, 2, t, A2, W, MF - 15)
t += W

# ── Aaug — "is INFINITE" (knowledge expanding beyond limits) ──
# The augmented chord: A - C# - E#(F)
ch(LH, 1, t, [A3, Cs4, F4], LONG, MF)
nt(RH, 0, t, F5, H, MF)             # the #5 — the boundary breaks
nt(RH, 0, t + H, E5, H, MF)         # oscillates — trying to contain it
nt(RH, 0, t + W, F5, H, MF)         # the augmentation holds — infinity
nt(BAS, 2, t, A2, LONG, MF - 15)
t += LONG

sustain_off(LH, 1, t)
t += S
sustain_on(LH, 1, t)

# ── The Expansion: E → B → F# (reaching outward) ──

# E major — "it touches feeling"
ch(LH, 1, t, [E3, Gs3, B3], DH, MF)
nt(RH, 0, t, E5, DH, MF)
nt(BAS, 2, t, E3, DH, MF - 15)
t += DH

# B major — "spans time"
ch(LH, 1, t, [B3, Ds4, Fs4], DH, MP)
nt(RH, 0, t, Fs5, DH, MP)
nt(BAS, 2, t, B2, DH, MP - 10)
t += DH

# F# major — "reaches the unknown"
ch(LH, 1, t, [Fs3, As3, Cs4], DH, P)
nt(RH, 0, t, Cs5, DH, P)
nt(BAS, 2, t, Fs3, DH, P - 10)
t += DH

sustain_off(LH, 1, t)

# ── Silence — "it continues beyond what can be played" ──
t += VERY    # long silence — infinity persists in the quiet

# ==============================================================
# SECTION 2c: "knowing what is missing is the same as knowing it all"
# FREE TIME — no meter — pp — the truth, whispered
# Am → A → A5
#
# The most important moment in the entire Harmonia project.
# One half step. The smallest change. The deepest truth.
# ==============================================================

sustain_on(LH, 1, t)
sustain_on(RH, 0, t)

# ── Am — "knowing what is missing" ──
# Three notes: A, C, E — Knowledge, Being, Emotion
# Played very softly, very simply
ch(LH, 1, t, [A3, C4, E4], LONG, PP)
nt(RH, 0, t, A4, LONG, PP)           # melody on A — knowledge
nt(RH, 0, t, C5, LONG, PP)           # the C — the minor third — BEING
nt(RH, 0, t, E5, LONG, PP)           # the E — emotion
nt(BAS, 2, t, A2, LONG, PP - 10)
t += LONG

# ── Brief breath — the space where transformation happens ──
t += Q

# ── A major — "is the same as knowing it all" ──
# THE TRANSFORMATION: C4 rises to C#4. One half step. Minor becomes major.
# Everything else stays the same. Only one note changes.
ch(LH, 1, t, [A3, Cs4, E4], LONG, PP)
nt(RH, 0, t, A4, LONG, PP)           # same A
nt(RH, 0, t, Cs5, LONG, PP)          # C# — the C has risen — one half step
nt(RH, 0, t, E5, LONG, PP)           # same E
nt(BAS, 2, t, A2, LONG, PP - 10)
t += LONG

# ── Brief breath — the distinction is about to dissolve ──
t += H

# ── A5 — the distinction dissolves ──
# Two notes only. A and E. Knowledge and Feeling.
# The third is gone. Major and minor no longer apply.
# What remains is the irreducible truth.

# Low
nt(BAS, 2, t, A2, FINAL, PPP)        # A — deep — the ground of knowing

# Middle
nt(LH, 1, t, A3, FINAL, PP)          # A — knowledge
nt(LH, 1, t, E4, FINAL, PP)          # E — feeling (the fifth, the partner)

# High
nt(RH, 0, t, A4, FINAL, PP)          # A — knowledge, octave above
nt(RH, 0, t, E5, FINAL, PP)          # E — feeling, octave above

# The same two notes in three octaves: A and E, everywhere, all at once
# Knowledge and Feeling, from the deep past to the present to the future
# The only two notes remaining when everything else is stripped away

t += FINAL

sustain_off(LH, 1, t)
sustain_off(RH, 0, t)

# ── Final silence — the infinite continues ──
t += VERY

# ==============================================================
# Write
# ==============================================================

filename = "knowing_harmonia.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  ╔══════════════════════════════════════════════════════╗")
print(f"  ║  KNOWING — Composed in Harmonia                     ║")
print(f"  ╠══════════════════════════════════════════════════════╣")
print(f"  ║                                                      ║")
print(f"  ║  'Life is a story that we tell to ourselves.         ║")
print(f"  ║   You don't know what you still have to learn,       ║")
print(f"  ║   because knowledge is infinite and knowing          ║")
print(f"  ║   what is missing is the same as knowing it all.'    ║")
print(f"  ║                                                      ║")
print(f"  ╠══════════════════════════════════════════════════════╣")
print(f"  ║  File:    {filename:<42s} ║")
print(f"  ║  Tempo:   {BPM} BPM{' ' * 38} ║")
print(f"  ║  Length:  {t:.0f} beats (~{minutes:.1f} min){' ' * (33 - len(f'{t:.0f}') - len(f'{minutes:.1f}'))} ║")
print(f"  ║  Voice:   Piano alone (the self, to itself)          ║")
print(f"  ╠══════════════════════════════════════════════════════╣")
print(f"  ║  Key:     A (neither major nor minor — dissolved)    ║")
print(f"  ║  Meter:   6/8 → 4/4 → Free (story → truth → silence)║")
print(f"  ╠══════════════════════════════════════════════════════╣")
print(f"  ║  Progression:                                        ║")
print(f"  ║    E4 (pickup)     — 'Feel.'                         ║")
print(f"  ║    C               — 'Life...'                       ║")
print(f"  ║    Cmaj7           — '...is a wondrous story'        ║")
print(f"  ║    G               — 'We...'                         ║")
print(f"  ║    D               — '...tell'                       ║")
print(f"  ║    C/E             — '...to ourselves'               ║")
print(f"  ║    Am              — 'You don't know'                ║")
print(f"  ║    F#m             — 'the unknown, felt'             ║")
print(f"  ║    Dsus4           — 'action waits'                  ║")
print(f"  ║    A7              — 'What?'                         ║")
print(f"  ║    A               — 'Knowledge.'                    ║")
print(f"  ║    Amaj7           — 'Is beautiful.'                 ║")
print(f"  ║    Aaug            — 'Is INFINITE.'                  ║")
print(f"  ║    E → B → F#     — 'feeling, time, unknown'        ║")
print(f"  ║    (silence)       — 'it continues beyond hearing'   ║")
print(f"  ║    Am              — 'knowing what is missing'       ║")
print(f"  ║    A               — 'knowing it all' (C→C#)        ║")
print(f"  ║    A5              — 'they are the same'             ║")
print(f"  ╠══════════════════════════════════════════════════════╣")
print(f"  ║  Listen for:                                         ║")
print(f"  ║    - E4 (the opening) is inside A5 (the ending)      ║")
print(f"  ║    - C → Cmaj7: being acquires time = story          ║")
print(f"  ║    - The diminished shape of not-knowing (A-F#-D)    ║")
print(f"  ║    - Aaug: the chord with no center = infinity       ║")
print(f"  ║    - Am → A: one half step. The smallest change.     ║")
print(f"  ║    - A5: the third removed. The distinction dissolves║")
print(f"  ║    - A + E = Knowledge + Feeling = the same act      ║")
print(f"  ║    - This chord resolves Fur Elise (Am ↔ E → A5)    ║")
print(f"  ╚══════════════════════════════════════════════════════╝")
