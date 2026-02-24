"""
EN UN LUGAR DE LA MANCHA... — Composed in Harmonia
Miguel de Cervantes, Don Quijote, Chapter 1 Opening (1605)

Instruments:
  - Classical Guitar (nylon): The Narrator
  - Oboe:                     The Hidalgo (the man himself)
  - Cello:                    The Physical World (meals, body, weight)

Run: python don_quixote_harmonia.py
Output: don_quixote_harmonia.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────────────
BPM = 72  # Moderato — unhurried storytelling

# Durations (in beats — using 6/8 feel, but MIDI is in quarter notes)
SHORT   = 2    # half measure feel
BEAT    = 3    # one full 6/8 measure
WHOLE   = 4    # slightly sustained
LONG    = 6    # sustained chord
HELD    = 8    # deeply sustained (suspensions)

# Dynamics
PP  = 35
MP  = 58
MF  = 75
F   = 100
FF  = 118

# MIDI notes
# Octave 2
F2  = 41; G2  = 43; Ab2 = 44; A2  = 45; B2  = 47
# Octave 3
C3  = 48; D3  = 50; Eb3 = 51; E3  = 52; F3  = 53
Fs3 = 54; Gb3 = 54; G3  = 55; Ab3 = 56; A3  = 57; Bb3 = 58; B3  = 59
# Octave 4 (middle C = C4 = 60)
C4  = 60; Cs4 = 61; Db4 = 61; D4  = 62; Eb4 = 63; E4  = 64; F4  = 65
Fs4 = 66; G4  = 67; Ab4 = 68; A4  = 69; Bb4 = 70; B4  = 71
# Octave 5
C5  = 72; D5  = 74; E5  = 76

# ── Track Setup ───────────────────────────────────────────────
midi = MIDIFile(3, adjust_origin=False)

GUITAR = 0   # The Narrator
OBOE   = 1   # The Hidalgo
CELLO  = 2   # The Physical World

midi.addTempo(0, 0, BPM)

# GM Program numbers
midi.addProgramChange(GUITAR, 0, 0, 24)   # Nylon Guitar
midi.addProgramChange(OBOE,   1, 0, 68)   # Oboe
midi.addProgramChange(CELLO,  2, 0, 42)   # Cello

# ── Helpers ───────────────────────────────────────────────────
def chord(track, channel, time, notes, duration, velocity):
    for note in notes:
        midi.addNote(track, channel, note, time, duration, velocity)

def grace_note(track, channel, time, note, velocity):
    """Acciaccatura — the narrator's wink."""
    midi.addNote(track, channel, note, time, 0.25, velocity)

# ── Time Cursor ───────────────────────────────────────────────
t = 0.0

# ==============================================================
# SECTION I: THE SETTING — "En un lugar de la Mancha..."
# Guitar alone (narrator speaking)
# ==============================================================

# ── Eb major — "A place. Here."
chord(GUITAR, 0, t, [Eb3, G3, Bb3], WHOLE, MF)
t += WHOLE

# ── F major — "The earth. La Mancha."
chord(GUITAR, 0, t, [F3, A3, C4], WHOLE, MF)
t += WHOLE

# ── Bbm — "I don't want to—" (desire, negated)
chord(GUITAR, 0, t, [Bb3, Db4, F4], BEAT, MP)
t += BEAT

# ── Asus4 — "(name withheld)" — unresolved, hanging
chord(GUITAR, 0, t, [A3, D4, E4], HELD, MP)
t += HELD

# ── Brief silence (the suspension hangs in the air)
t += SHORT

# ==============================================================
# SECTION II: THE MAN AND HIS ARMS
# Guitar + Oboe (narrator introduces the character)
# ==============================================================

# ── B (low) — "Time past—" (not long ago)
chord(GUITAR, 0, t, [B2, Fs4], BEAT, MP)
t += BEAT

# ── C major — "A man was."
chord(GUITAR, 0, t, [C3, E3, G3, C4], WHOLE, MF)
# Oboe enters here — the hidalgo appears
midi.addNote(OBOE, 1, E4, t, WHOLE, MP)
t += WHOLE

# ── Dsus4 — "The lance — on the rack — suspended"
chord(OBOE,   1, t, [D4, G4], LONG, MP)
chord(GUITAR, 0, t, [D3, G3, A3], LONG, MP)
t += LONG

# ── Dm — "The shield — old, worn"
chord(OBOE,   1, t, [D4, F4], WHOLE, MP)
chord(GUITAR, 0, t, [D3, F3, A3], WHOLE, MP)
t += WHOLE

# ── Fm — "The horse — thin" (nature diminished)
# Oboe plays slightly too high — mock-heroic register mismatch
chord(OBOE,   1, t, [F4, Ab4], WHOLE, MP)
chord(GUITAR, 0, t, [F3, Ab3, C4], WHOLE, MP)
t += WHOLE

# ── D major — "The greyhound — alive!" (one spark)
chord(OBOE,   1, t, [D4, Fs4, A4], BEAT, MF)
chord(GUITAR, 0, t, [D3, Fs4, A4], BEAT, MF)
t += BEAT

t += SHORT  # breath

# ==============================================================
# SECTION III: THE MENU — "The week turns"
# Cello enters (the weight of the physical world)
# Guitar maintains the 6/8 lilt
# ==============================================================

# ── F — "Stew" (the physical world, plain)
chord(CELLO,  2, t, [F2, C3, F3], BEAT, MF)
chord(GUITAR, 0, t, [F3, A3, C4], BEAT, MF)
t += BEAT

# ── F — "Cold meat, most nights" (the same)
chord(CELLO,  2, t, [F2, C3, F3], BEAT, MF)
chord(GUITAR, 0, t, [F3, A3, C4], BEAT, MF)
t += BEAT

# ── Fm — "Duelos y quebrantos" (sorrows! — wink!)
# Grace note = the narrator's wink (acciaccatura)
grace_note(GUITAR, 0, t, A3, MF)  # the A natural flickers before Ab
chord(CELLO,  2, t, [F2, C3, F3], BEAT, MF)
chord(GUITAR, 0, t, [F3, Ab3, C4], BEAT, MF)
t += BEAT

# ── F — "Lentils, Friday" (the same, again)
chord(CELLO,  2, t, [F2, C3, F3], BEAT, MF)
chord(GUITAR, 0, t, [F3, A3, C4], BEAT, MF)
t += BEAT

# ── Fmaj7 — "Pigeon on Sundays" (one small beauty)
chord(CELLO,  2, t, [F2, C3, F3], BEAT, MF)
chord(GUITAR, 0, t, [F3, A3, C4, E4], BEAT, MF)
t += BEAT

# ── F — "The world—"
chord(CELLO,  2, t, [F2, C3, F3], WHOLE, F)
chord(GUITAR, 0, t, [F3, A3, C4], WHOLE, F)
t += WHOLE

# ── Cm — "—devours the self"
chord(CELLO,  2, t, [C3, G3], WHOLE, F)
chord(GUITAR, 0, t, [C3, Eb3, G3], WHOLE, F)
t += WHOLE

t += SHORT  # breath

# ==============================================================
# SECTION IV: THE WARDROBE — "Se honraba"
# Guitar — narrator noting the seed of transformation
# ==============================================================

# ── Eb — "Holidays — belonging"
chord(GUITAR, 0, t, [Eb3, G3, Bb3], BEAT, MF)
t += BEAT

# ── F — "Velvet — the physical world"
chord(GUITAR, 0, t, [F3, A3, C4], BEAT, MF)
t += BEAT

# ── F — "Weekdays — the same"
chord(GUITAR, 0, t, [F3, A3, C4], BEAT, MP)
t += BEAT

# ── Cmaj7 — "He honored himself — with wool" (THE SEED)
# Played warmly, lovingly — the narrator sees what we don't yet
chord(GUITAR, 0, t, [C3, E3, G3, B3], LONG, MP)
midi.addNote(OBOE, 1, B4, t, LONG, PP)  # oboe adds the maj7 high — aspiration
t += LONG

# ==============================================================
# SECTION V: THE HOUSEHOLD — "Three people"
# Guitar — plain, unadorned
# ==============================================================

# ── G — "Housekeeper"
chord(GUITAR, 0, t, [G3, B3, D4], BEAT, MP)
t += BEAT

# ── G — "Niece"
chord(GUITAR, 0, t, [G3, B3, D4], BEAT, MP)
t += BEAT

# ── G — "Servant"
chord(GUITAR, 0, t, [G3, B3, D4], BEAT, MP)
t += BEAT

t += SHORT  # breath

# ==============================================================
# SECTION VI: THE BODY — same shape as the possessions
# Oboe (the man's voice) + Cello (body weight)
# ==============================================================

# ── Bm — "Approaching fifty — time aging"
chord(OBOE,  1, t, [B3, D4, Fs4], WHOLE, MP)
chord(CELLO, 2, t, [B2, Fs3], WHOLE, MP)
t += WHOLE

# ── F — "Strong constitution — the body stands"
chord(OBOE,  1, t, [F4, A4], BEAT, MF)
chord(CELLO, 2, t, [F2, C3, F3], BEAT, MF)
t += BEAT

# ── Fm — "Lean, gaunt — the body thins"
chord(OBOE,  1, t, [F4, Ab4], BEAT, MP)
chord(CELLO, 2, t, [F2, Ab2, C3], BEAT, MP)
t += BEAT

# ── D — "Early riser, hunter — still active"
chord(OBOE,  1, t, [D4, Fs4, A4], BEAT, MF)
chord(CELLO, 2, t, [D3, A3], BEAT, MF)
t += BEAT

t += SHORT  # breath

# ==============================================================
# SECTION VII: THE NAME — three attempts, none resolving
# Guitar alone — searching
# ==============================================================

# ── C — "Quijada" (stated)
chord(GUITAR, 0, t, [C3, E3, G3, C4], WHOLE, MF)
t += WHOLE

# ── C7 — "Quesada?" (questioned)
chord(GUITAR, 0, t, [C3, E3, G3, Bb3], WHOLE, MP)
t += WHOLE

# ── Csus2 — "Quejana..." (open, undefined)
chord(GUITAR, 0, t, [C3, D3, G3, C4], LONG, MP)
t += LONG

t += SHORT  # the name doesn't settle

# ==============================================================
# SECTION VIII: THE TRUTH CLAIM — the frame closes
# Guitar alone — silence — declaration — suspension
# ==============================================================

# ── Rest — "Pero esto importa poco" (matters little — a shrug)
t += WHOLE

# ── A major — "LA VERDAD!" (Truth! — too loud)
chord(GUITAR, 0, t, [A3, Cs4, E4, A4], WHOLE, F)
t += WHOLE

# ── Asus4 — "(...)" (the wink — the frame closes — same as opening)
chord(GUITAR, 0, t, [A3, D4, E4], HELD, MP)
t += HELD

# ── Final silence — the suspensions hang
t += LONG

# ==============================================================
# Write the file
# ==============================================================

filename = "don_quixote_harmonia.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

beats = t
minutes = t / BPM
print(f"")
print(f"  Created: {filename}")
print(f"  Tempo:   {BPM} BPM")
print(f"  Length:  {beats:.0f} beats (~{minutes:.1f} minutes)")
print(f"")
print(f"  Tracks:")
print(f"    0 - Classical Guitar  (The Narrator)")
print(f"    1 - Oboe              (The Hidalgo)")
print(f"    2 - Cello             (The Physical World)")
print(f"")
print(f"  Listen for:")
print(f"    - The Asus4 that opens and closes (the narrator's signature)")
print(f"    - The grace note on 'duelos y quebrantos' (the wink)")
print(f"    - The Cmaj7 on the wool (the seed of everything)")
print(f"    - The three G chords (three people, plain as furniture)")
print(f"    - The Csus2 (a name that will not settle)")
print(f"    - The silence where Emotion should be")
print(f"")
print(f"  The lance is still on the rack.")
print(f"  The Dsus4 has not resolved.")
print(f"  The novel has not yet begun.")
