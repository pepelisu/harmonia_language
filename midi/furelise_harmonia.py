"""
FÜR ELISE — Harmonia Translation MIDI
Ludwig van Beethoven (1810)

Key: A minor — "Understanding absent — I don't know"
Meter: 3/8 — intimate, turning, trapped
Voice: Piano — human, personal

Sections:
  A  — Whispered Confession (pp)
      Am ↔ E = "not-knowing ↔ love"
  B  — Open Declaration (mf)
      C → G → Am → E = "I exist — with you — lost — feeling"
  C  — The Storm (ff)
      F → C → Bb → A = "LIFE! SELF! I WANTED TO KNOW!"
  A' — Resignation (pp)
      The same words, carrying new weight

Run: python fur_elise_harmonia.py
Output: fur_elise_harmonia.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────
BPM = 72

# Durations (in quarter-note beats)
S    = 0.5     # eighth note
Q    = 1.0     # quarter note
DQ   = 1.5     # dotted quarter
H    = 2.0     # half note
DH   = 3.0     # dotted half
W    = 4.0     # whole note

# Dynamics (MIDI velocity 0–127)
PP   = 38
P    = 48
MP   = 58
MF   = 75
F    = 100
FF   = 118

# ── MIDI Note Definitions (COMPLETE) ─────────────────
# Octave 2
C2   = 36;  Cs2  = 37;  Db2  = 37;  D2   = 38;  Ds2  = 39
Eb2  = 39;  E2   = 40;  F2   = 41;  Fs2  = 42;  Gb2  = 42
G2   = 43;  Gs2  = 44;  Ab2  = 44;  A2   = 45;  As2  = 46
Bb2  = 46;  B2   = 47

# Octave 3
C3   = 48;  Cs3  = 49;  Db3  = 49;  D3   = 50;  Ds3  = 51
Eb3  = 51;  E3   = 52;  F3   = 53;  Fs3  = 54;  Gb3  = 54
G3   = 55;  Gs3  = 56;  Ab3  = 56;  A3   = 57;  As3  = 58
Bb3  = 58;  B3   = 59

# Octave 4 (middle C = C4 = 60)
C4   = 60;  Cs4  = 61;  Db4  = 61;  D4   = 62;  Ds4  = 63
Eb4  = 63;  E4   = 64;  F4   = 65;  Fs4  = 66;  Gb4  = 66
G4   = 67;  Gs4  = 68;  Ab4  = 68;  A4   = 69;  As4  = 70
Bb4  = 70;  B4   = 71

# Octave 5
C5   = 72;  Cs5  = 73;  Db5  = 73;  D5   = 74;  Ds5  = 75
Eb5  = 75;  E5   = 76;  F5   = 77;  Fs5  = 78;  Gb5  = 78
G5   = 79;  Gs5  = 80;  Ab5  = 80;  A5   = 81;  As5  = 82
Bb5  = 82;  B5   = 83

# Octave 6
C6   = 84

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(3, adjust_origin=False)

MELODY  = 0    # Piano right hand — the human voice
HARMONY = 1    # Piano left hand — the harmonic frame
STRINGS = 2    # String Ensemble — the emotional community

midi.addTempo(0, 0, BPM)

midi.addProgramChange(MELODY,  0, 0, 0)     # Acoustic Grand Piano
midi.addProgramChange(HARMONY, 1, 0, 0)     # Acoustic Grand Piano
midi.addProgramChange(STRINGS, 2, 0, 48)    # String Ensemble 1

# ── Helpers ───────────────────────────────────────────
def ch(track, channel, time, notes, duration, velocity):
    """Add a chord."""
    for n in notes:
        midi.addNote(track, channel, n, time, duration, velocity)

def nt(track, channel, time, pitch, duration, velocity):
    """Add a single note."""
    midi.addNote(track, channel, pitch, time, duration, velocity)

def melody_run(time, notes, dur, vel):
    """Play a sequence of notes, returning the new time position."""
    t = time
    for n in notes:
        nt(MELODY, 0, t, n, dur, vel)
        t += dur
    return t

def sustain_on(track, channel, time):
    midi.addControllerEvent(track, channel, time, 64, 127)

def sustain_off(track, channel, time):
    midi.addControllerEvent(track, channel, time, 64, 0)

# ── Time Cursor ───────────────────────────────────────
t = 0.0

# ==============================================================
# SECTION A — WHISPERED CONFESSION
# Piano alone, pp → mp
# Am ↔ E = "I don't understand ↔ this love"
#
# The famous E-D# oscillation:
# "Feeling... home... feeling... home... feeling...
#  time... action... self... I don't understand."
# ==============================================================

sustain_on(HARMONY, 1, t)

# ── Phrase A1: First yearning ──────────────────────
# Melody: E-D#-E-D#-E-B-D-C → landing on A (Am)
t = melody_run(t, [E5, Ds5, E5, Ds5, E5, B4, D5, C5], S, PP)

# Am — "I don't understand"
nt(MELODY, 0, t, A4, DQ, PP)
ch(HARMONY, 1, t, [A2, E3, A3], DQ, PP)
t += DQ

# Answer: ascending through E chord — "this love"
t = melody_run(t, [E4, Gs4, B4], S, PP)

# E major — "this love"
nt(MELODY, 0, t, C5, DQ, PP)
ch(HARMONY, 1, t, [E3, Gs3, B3], DQ, PP)
t += DQ

# ── Phrase A2: Second yearning (identical — the loop) ──
t = melody_run(t, [E5, Ds5, E5, Ds5, E5, B4, D5, C5], S, PP)

# Am — "I don't understand"
nt(MELODY, 0, t, A4, DQ, PP)
ch(HARMONY, 1, t, [A2, E3, A3], DQ, PP)
t += DQ

# Answer through E
t = melody_run(t, [E4, Gs4, B4], S, PP)

# E — → Am resolution
nt(MELODY, 0, t, A4, DQ, PP)
ch(HARMONY, 1, t, [E3, Gs3, B3], Q, PP)
t += Q
ch(HARMONY, 1, t, [A2, E3, A3], S, PP)
t += S

# ── Phrase A3: Third yearning, then the C–G passage ──
t = melody_run(t, [E5, Ds5, E5, Ds5, E5, B4, D5, C5], S, MP)

# Am — "I am searching"
nt(MELODY, 0, t, A4, DQ, MP)
ch(HARMONY, 1, t, [A2, E3, A3], DQ, MP)
t += DQ

# ── The ascending passage: "I exist — beside you" ──

# C major — "I exist"
nt(MELODY, 0, t, C5, Q, MP)
ch(HARMONY, 1, t, [C3, E3, G3], Q, MP)
t += Q

nt(MELODY, 0, t, D5, Q, MP)
t += Q

# G major — "beside you"
nt(MELODY, 0, t, E5, Q, MP)
ch(HARMONY, 1, t, [G3, B3, D4], Q, MP)
t += Q

# Descending: back toward not-knowing
nt(MELODY, 0, t, D5, S, MP)
nt(MELODY, 0, t + S, C5, S, MP)
t += Q

# Am — "yet I don't understand"
nt(MELODY, 0, t, A4, DQ, MP)
ch(HARMONY, 1, t, [A2, E3, A3], DQ, MP)
t += DQ

# E — "this feeling"
nt(MELODY, 0, t, Gs4, DQ, MP)
ch(HARMONY, 1, t, [E3, Gs3, B3], DQ, MP)
t += DQ

# Am — "I don't know..." (held, fading)
nt(MELODY, 0, t, A4, H, P)
ch(HARMONY, 1, t, [A2, E3, A3], H, P)
t += H

sustain_off(HARMONY, 1, t)

# ── Breath between sections ──
t += Q

# ==============================================================
# SECTION B — OPEN DECLARATION
# Piano + Strings, mp → mf
# C → G → Am → E
# "I am here, with you, and I don't understand
#  why I feel this way."
# ==============================================================

sustain_on(HARMONY, 1, t)

# ── First statement ──

# C — "I am here"
nt(MELODY, 0, t, E5, Q, MF)
ch(HARMONY, 1, t, [C3, G3, C4, E4], H, MF)
ch(STRINGS, 2, t, [C3, G3], H, MP)
nt(MELODY, 0, t + Q, G5, Q, MF)
t += H

# G — "with you"
nt(MELODY, 0, t, D5, H, MF)
ch(HARMONY, 1, t, [G2, D3, G3, B3], H, MF)
ch(STRINGS, 2, t, [G3, D4], H, MP)
t += H

# Am — "and I don't understand"
nt(MELODY, 0, t, C5, Q, MF)
ch(HARMONY, 1, t, [A2, E3, A3, C4], H, MF)
ch(STRINGS, 2, t, [A3, E4], H, MP)
nt(MELODY, 0, t + Q, A4, Q, MF)
t += H

# E — "why I feel this way"
nt(MELODY, 0, t, Gs4, Q, MF)
ch(HARMONY, 1, t, [E3, Gs3, B3], H, MF)
ch(STRINGS, 2, t, [E3, B3], H, MP)
nt(MELODY, 0, t + Q, B4, Q, MF)
t += H

# ── Second statement (variation) ──

# C — "I am real"
nt(MELODY, 0, t, G5, H, MF)
ch(HARMONY, 1, t, [C3, G3, C4, E4], H, MF)
ch(STRINGS, 2, t, [C4, E4, G4], H, MF)
t += H

# G — "We are real"
nt(MELODY, 0, t, D5, H, MF)
ch(HARMONY, 1, t, [G2, D3, G3, B3], H, MF)
ch(STRINGS, 2, t, [G3, B3, D4], H, MF)
t += H

# Am — "But I cannot grasp it"
nt(MELODY, 0, t, E5, Q, MF)
ch(HARMONY, 1, t, [A2, E3, A3, C4], H, MF)
ch(STRINGS, 2, t, [A3, C4, E4], H, MF)
nt(MELODY, 0, t + Q, C5, Q, MF)
t += H

# E → Am — "Love dissolves into questions"
nt(MELODY, 0, t, B4, Q, MF)
ch(HARMONY, 1, t, [E3, Gs3, B3], Q, MF)
ch(STRINGS, 2, t, [E3, B3], Q, MF)
t += Q

nt(MELODY, 0, t, A4, DH, MP)
ch(HARMONY, 1, t, [A2, E3, A3, C4], DH, MP)
ch(STRINGS, 2, t, [A3, C4, E4], DH, MP)
t += DH

sustain_off(HARMONY, 1, t)

# ── Breath ──
t += Q

# ==============================================================
# SECTION C — THE STORM
# Piano ff + Strings f, low register (past tense)
#
# F → C = "LIFE! SELF!" (hammering)
# Bb → A = "I WANTED TO KNOW!"
# Dm → Am → E → Am = collapse, exhaustion
# ==============================================================

sustain_on(HARMONY, 1, t)

# ── F → C hammering: "Life! Self! The world! Who I was!" ──

# F — "Life!"
nt(MELODY, 0, t, F5, Q, FF)
ch(HARMONY, 1, t, [F2, C3, F3, A3], Q, FF)
ch(STRINGS, 2, t, [F3, A3, C4], Q, F)
t += Q

# C — "Self!"
nt(MELODY, 0, t, E5, Q, FF)
ch(HARMONY, 1, t, [C3, G3, C4, E4], Q, FF)
ch(STRINGS, 2, t, [C4, E4, G4], Q, F)
t += Q

# F — "The world!"
nt(MELODY, 0, t, F5, Q, FF)
ch(HARMONY, 1, t, [F2, C3, F3, A3], Q, FF)
ch(STRINGS, 2, t, [F3, A3, C4], Q, F)
t += Q

# C — "Who I was!"
nt(MELODY, 0, t, G5, Q, FF)
ch(HARMONY, 1, t, [C3, G3, C4, E4], Q, FF)
ch(STRINGS, 2, t, [C4, E4, G4], Q, F)
t += Q

# F — "Life—"
nt(MELODY, 0, t, A5, Q, FF)
ch(HARMONY, 1, t, [F2, C3, F3, A3], Q, FF)
ch(STRINGS, 2, t, [F3, A3, C4], Q, F)
t += Q

# C — "—and being, colliding!"
nt(MELODY, 0, t, G5, Q, FF)
ch(HARMONY, 1, t, [C3, G3, C4, E4], Q, FF)
ch(STRINGS, 2, t, [C4, E4, G4], Q, F)
t += Q

# ── Bb → A: "I WANTED — TO KNOW!" ──

# Bb — "I WANTED—"
nt(MELODY, 0, t, F5, H, FF)
ch(HARMONY, 1, t, [Bb2, F3, Bb3, D4], H, FF)
ch(STRINGS, 2, t, [Bb3, D4, F4], H, F)
t += H

# A major — "—TO KNOW!"
nt(MELODY, 0, t, E5, H, F)
ch(HARMONY, 1, t, [A2, E3, A3, Cs4], H, F)
ch(STRINGS, 2, t, [A3, Cs4, E4], H, F)
t += H

# ── Collapse: Dm → Am → E → Am ──
# "I was still. I was lost. I felt. And did not understand."

# Dm — "I was still"
nt(MELODY, 0, t, D5, H, MF)
ch(HARMONY, 1, t, [D3, F3, A3], H, MF)
ch(STRINGS, 2, t, [D3, A3], H, MF)
t += H

# Am — "I was lost"
nt(MELODY, 0, t, C5, H, MF)
ch(HARMONY, 1, t, [A2, E3, A3, C4], H, MF)
ch(STRINGS, 2, t, [A3, E4], H, MP)
t += H

# E — "I felt"
nt(MELODY, 0, t, B4, H, MP)
ch(HARMONY, 1, t, [E3, Gs3, B3], H, MP)
ch(STRINGS, 2, t, [E3, B3], H, MP)
t += H

# Am — "And did not understand"
nt(MELODY, 0, t, A4, H, MP)
ch(HARMONY, 1, t, [A2, E3, A3, C4], H, MP)
ch(STRINGS, 2, t, [A3, C4, E4], H, MP)
t += H

sustain_off(HARMONY, 1, t)

# ── Long breath — the storm exhausts itself ──
t += H

# ==============================================================
# RETURN TO A — RESIGNATION
# Piano alone again, pp
# The same words, now carrying the weight of the storm
#
# "Feeling... home... feeling... home... feeling...
#  I don't understand this love.
#  I exist beside you.
#  I still don't know."
# ==============================================================

sustain_on(HARMONY, 1, t)

# ── The yearning returns ──
t = melody_run(t, [E5, Ds5, E5, Ds5, E5, B4, D5, C5], S, PP)

# Am
nt(MELODY, 0, t, A4, DQ, PP)
ch(HARMONY, 1, t, [A2, E3, A3], DQ, PP)
t += DQ

# Through E
t = melody_run(t, [E4, Gs4, B4], S, PP)

# E
nt(MELODY, 0, t, C5, DQ, PP)
ch(HARMONY, 1, t, [E3, Gs3, B3], DQ, PP)
t += DQ

# ── Final oscillation ──
t = melody_run(t, [E5, Ds5, E5, Ds5, E5, B4, D5, C5], S, PP)

# ── Final Am — the question that never receives its answer ──
nt(MELODY, 0, t, A4, W, PP)
ch(HARMONY, 1, t, [A2, E3, A3, C4], W, PP)
t += W

sustain_off(HARMONY, 1, t)

# ── Silence ──
t += W

# ==============================================================
# Write
# ==============================================================

filename = "fur_elise_harmonia.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  Created: {filename}")
print(f"  Tempo:   {BPM} BPM")
print(f"  Length:  {t:.0f} beats (~{minutes:.1f} minutes)")
print(f"")
print(f"  Tracks:")
print(f"    0 - Piano melody   (the human voice)")
print(f"    1 - Piano harmony  (the harmonic frame)")
print(f"    2 - Strings        (the emotional community)")
print(f"")
print(f"  Sections:")
print(f"    A  — Whispered Confession (pp)  Am ↔ E")
print(f"    B  — Open Declaration (mf)      C → G → Am → E")
print(f"    C  — The Storm (ff)             F → C → Bb → A")
print(f"    A' — Resignation (pp)           Am... unresolved")
print(f"")
print(f"  Listen for:")
print(f"    - The E-D# oscillation (feeling ↔ home, yearning)")
print(f"    - Am ↔ E (not-knowing ↔ love)")
print(f"    - The C → G moment (I exist — beside you)")
print(f"    - The F-C hammering (LIFE! SELF!)")
print(f"    - Bb → A (I WANTED TO KNOW)")
print(f"    - The final Am, held, unresolved")
print(f"    - The piece ends on a question that is never answered")
