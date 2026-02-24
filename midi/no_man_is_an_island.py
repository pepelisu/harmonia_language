"""
NO MAN IS AN ISLAND — Composed in Harmonia
John Donne, Meditation XVII (1624)
Translated to music via the Harmonia chord-language system

Instruments:
  - Church Organ:    Sections I & II (the institution, the sermon)
  - String Ensemble: Section II (humanity gathering)
  - Piano:           Sections III & IV (the individual, vulnerable)
  - Tubular Bells:   The bell (time itself striking)
  - Choir Aahs:      Final chord (all of humanity answering)

Run: python no_man_is_an_island.py
Output: no_man_is_an_island_harmonia.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────────────
BPM = 52  # Slow. Deliberate. Each chord is a sentence.

# Durations (in quarter-note beats)
WHOLE  = 4    # one measure
DOUBLE = 8    # two measures (sustained chords)
TRIPLE = 12   # three measures
QUAD   = 16   # four measures (final chord)

# Dynamics (MIDI velocity, 0-127)
PP  = 38   # pianissimo  — the choir whisper
MP  = 62   # mezzo piano — private speech
MF  = 80   # mezzo forte — confident declaration
F   = 100  # forte       — urgency
FF  = 120  # fortissimo  — the command

# MIDI note numbers
# Octave 2
C2  = 36
# Octave 3
C3  = 48;  D3 = 50;  Eb3 = 51;  E3 = 52;  F3 = 53
Gb3 = 54;  G3 = 55;  Ab3 = 56;  A3 = 57;  Bb3 = 58;  B3 = 59
# Octave 4 (middle C = C4 = 60)
C4  = 60;  D4 = 62;  Eb4 = 63;  E4 = 64;  F4 = 65
Fs4 = 66;  G4 = 67;  Ab4 = 68;  A4 = 69;  Bb4 = 70;  B4 = 71
# Octave 5
C5  = 72;  E5 = 76;  G5 = 79

# ── Track Setup ───────────────────────────────────────────────
midi = MIDIFile(5, adjust_origin=False)

ORGAN   = 0
STRINGS = 1
PIANO   = 2
CHOIR   = 3
BELLS   = 4

midi.addTempo(0, 0, BPM)

# General MIDI program numbers
midi.addProgramChange(ORGAN,   0, 0, 19)  # Church Organ
midi.addProgramChange(STRINGS, 1, 0, 48)  # String Ensemble 1
midi.addProgramChange(PIANO,   2, 0, 0)   # Acoustic Grand Piano
midi.addProgramChange(CHOIR,   3, 0, 52)  # Choir Aahs
midi.addProgramChange(BELLS,   4, 0, 14)  # Tubular Bells

# ── Helpers ───────────────────────────────────────────────────
def chord(track, channel, time, notes, duration, velocity):
    """Add multiple simultaneous notes (a chord)."""
    for note in notes:
        midi.addNote(track, channel, note, time, duration, velocity)

def sustain_on(track, channel, time):
    """Press sustain pedal."""
    midi.addControllerEvent(track, channel, time, 64, 127)

def sustain_off(track, channel, time):
    """Release sustain pedal."""
    midi.addControllerEvent(track, channel, time, 64, 0)

# ── Time Cursor ───────────────────────────────────────────────
t = 0.0

# ==============================================================
# SECTION I: THESIS — "The Truth of Connection"
# Voice: Organ alone
# Dynamic: mp → mf
#
# "No man is an island, entire of itself,
#  Every man is a piece of the continent,
#  A part of the main."
# ==============================================================

# ── Cm — "A self, alone—" (the false premise, struck and denied)
chord(ORGAN, 0, t, [C4, Eb4, G4], WHOLE, MP)
t += WHOLE                                           # beat 4

# ── Silence — "No." Two measures. The denial.
t += DOUBLE                                          # beat 12

# ── G — "Connection."
chord(ORGAN, 0, t, [G3, B3, D4], WHOLE, MF)
t += WHOLE                                           # beat 16

# ── Gmaj7 — "Wondrous connection."
chord(ORGAN, 0, t, [G3, B3, D4, Fs4], WHOLE, MF)
t += WHOLE                                           # beat 20

# ── Fmaj7 — "The vast, beautiful world."
chord(ORGAN, 0, t, [F3, A3, C4, E4], WHOLE, MF)
t += WHOLE                                           # beat 24

# ── C major — "Each self belongs."
chord(ORGAN, 0, t, [C4, E4, G4], WHOLE, MF)
t += WHOLE                                           # beat 28

# ==============================================================
# SECTION II: EVIDENCE — "The Erosion"
# Voice: Organ + Strings (humanity gathers)
# Dynamic: mf → f
#
# "If a clod be washed away by the sea,
#  Europe is the less.
#  As well as if a promontory were.
#  As well as if a manor of thy friend's
#  Or of thine own were."
# ==============================================================

# ── F major — "The earth—"
chord(ORGAN,   0, t, [F3, A3, C4], WHOLE, MF)
chord(STRINGS, 1, t, [F3, A3, C4], WHOLE, MF - 10)  # strings slightly softer
t += WHOLE                                           # beat 32

# ── F minor — "—erodes." (A natural drops to Ab — one half step — one clod)
chord(ORGAN,   0, t, [F3, Ab3, C4], WHOLE, MF)
chord(STRINGS, 1, t, [F3, Ab3, C4], WHOLE, MF - 10)
t += WHOLE                                           # beat 36

# ── G minor — "The whole is less." (sustained — let the shadow settle)
chord(ORGAN,   0, t, [G3, Bb3, D4], DOUBLE, F)
chord(STRINGS, 1, t, [G3, Bb3, D4], DOUBLE, F - 10)
t += DOUBLE                                         # beat 44

# ── Eb major — "A home—"
chord(ORGAN,   0, t, [Eb3, G3, Bb3], WHOLE, F)
chord(STRINGS, 1, t, [Eb3, G3, Bb3], WHOLE, F - 10)
t += WHOLE                                           # beat 48

# ── Eb minor — "—falls." (G natural drops to Gb — one half step — one home)
chord(ORGAN,   0, t, [Eb3, Gb3, Bb3], WHOLE, F)
chord(STRINGS, 1, t, [Eb3, Gb3, Bb3], WHOLE, F - 10)
t += WHOLE                                           # beat 52

# ── C minor (low) — "Your self, diminished."
chord(ORGAN,   0, t, [C3, Eb3, G3], WHOLE, F)
chord(STRINGS, 1, t, [C3, Eb3, G3], WHOLE, F - 10)
t += WHOLE                                           # beat 56

# ==============================================================
# SECTION III: THE TURN — "This Means Me"
# Voice: Piano alone (organ and strings withdraw)
# Dynamic: mp — suddenly intimate, one person speaking
#
# "Any man's death diminishes me,
#  Because I am involved in mankind."
# ==============================================================

sustain_on(PIANO, 2, t)

# ── Bm — "Time takes."
chord(PIANO, 2, t, [B3, D4, Fs4], WHOLE, MP)
t += WHOLE                                           # beat 60

# ── C/E — "I receive the loss." (first inversion — self as receiver)
chord(PIANO, 2, t, [E3, C4, E4, G4], WHOLE, MP)
t += WHOLE                                           # beat 64

# ── C/G — "Because my being rests on connection." (sustained)
chord(PIANO, 2, t, [G3, C4, E4, G4], DOUBLE, MP)
t += DOUBLE                                          # beat 72

sustain_off(PIANO, 2, t)

# ==============================================================
# SECTION IV: THE IMPERATIVE — "And This Means You"
# Voice: Piano → Bell → Silence → Choir
# Dynamic: ff → f → (nothing) → pp
#
# "And therefore never send to know
#  for whom the bell tolls;
#  It tolls for thee."
# ==============================================================

# ── D5 power chord — "DO NOT." (fortissimo — the command)
chord(PIANO, 2, t, [D4, A4], WHOLE, FF)
t += WHOLE                                           # beat 76

# ── Am — "—seek to know—"
chord(PIANO, 2, t, [A3, C4, E4], WHOLE, F)
t += WHOLE                                           # beat 80

# ── B (single bell note) — The bell. Time itself.
midi.addNote(BELLS, 4, B3, t, DOUBLE, F)             # rings and decays
t += WHOLE                                           # beat 84

# ── Silence — The unasked question. "For whom?"
# (The bell is still decaying during beats 84-88)
# (True silence from 88-96)
t += TRIPLE                                          # beat 96
# (3 measures of space — the bell fades — silence holds — )

# ── C/G — "It tolls for thee." (Choir, pp — all of humanity, whispering)
chord(CHOIR, 3, t, [G3, C4, E4, G4], QUAD, PP)       # lower voicing
chord(CHOIR, 3, t, [C5, E5, G5],     QUAD, PP - 5)   # upper voicing
t += QUAD                                            # beat 112

# ==============================================================
# Write the file
# ==============================================================

filename = "no_man_is_an_island_harmonia.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  Created: {filename}")
print(f"  Tempo:   {BPM} BPM")
print(f"  Length:  {t:.0f} beats (~{minutes:.1f} minutes)")
print(f"")
print(f"  Tracks:")
print(f"    0 - Church Organ    (Sections I & II)")
print(f"    1 - String Ensemble (Section II)")
print(f"    2 - Piano           (Sections III & IV)")
print(f"    3 - Choir Aahs      (Final chord)")
print(f"    4 - Tubular Bells   (The bell)")
print(f"")
print(f"  Open with:")
print(f"    - GarageBand (Mac/iOS)")
print(f"    - MuseScore  (free, all platforms)")
print(f"    - Logic Pro / FL Studio / Ableton")
print(f"    - VLC or any media player")
print(f"")
print(f"  The silence between the bell and the choir")
print(f"  is where the continent forms.")
