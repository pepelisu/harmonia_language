"""
HEDWIG'S THEME — Harmonia Translation MIDI
John Williams (2001)

Key: E minor — "The feeling of something missing"
Meter: 3/4 — incantation, enchantment, spellcasting
Voice: Celesta — the otherworld, whispering

Sections:
  1st Statement — Celesta alone (pp)
      "A voice not quite human, whispering a spell"
  2nd Statement — Celesta + Strings (pp → mp)
      "Other voices join — the spell widens"

Run: python hedwigs_theme_harmonia.py
Output: hedwigs_theme_harmonia.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────
BPM = 60    # Slow, magical, unhurried

# Durations (quarter-note beats, in 3/4 time)
E    = 0.5     # eighth note
Q    = 1.0     # quarter note
DQ   = 1.5     # dotted quarter
H    = 2.0     # half note
DH   = 3.0     # dotted half (full measure of 3/4)
W    = 4.0     # whole (sustained beyond the measure)
LONG = 6.0     # two measures sustained

# Dynamics (MIDI velocity 0–127)
PP   = 35
P    = 45
MP   = 58
MF   = 72
F    = 95

# ── MIDI Note Definitions (COMPLETE) ─────────────────
# Octave 2
C2   = 36;  D2   = 38;  E2   = 40;  F2   = 41
Fs2  = 42;  Gb2  = 42;  G2   = 43;  Ab2  = 44
A2   = 45;  Bb2  = 46;  B2   = 47

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
G5   = 79;  Gs5  = 80;  Ab5  = 80;  A5   = 81;  Bb5  = 82
B5   = 83

# Octave 6
C6   = 84;  D6   = 86;  E6   = 88

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(4, adjust_origin=False)

CELESTA = 0    # The otherworldly voice — magic itself
HARP    = 1    # Harmonic support — the shimmer beneath
STRINGS = 2    # The emotional community (enters 2nd statement)
BASS    = 3    # Low anchor — the roots of each chord

midi.addTempo(0, 0, BPM)

# General MIDI program numbers
midi.addProgramChange(CELESTA, 0, 0, 8)     # Celesta
midi.addProgramChange(HARP,    1, 0, 46)    # Orchestral Harp
midi.addProgramChange(STRINGS, 2, 0, 48)    # String Ensemble 1
midi.addProgramChange(BASS,    3, 0, 42)    # Cello

# ── Helpers ───────────────────────────────────────────
def ch(track, channel, time, notes, duration, velocity):
    """Add a chord."""
    for n in notes:
        midi.addNote(track, channel, n, time, duration, velocity)

def nt(track, channel, time, pitch, duration, velocity):
    """Add a single note."""
    midi.addNote(track, channel, pitch, time, duration, velocity)

def harp_arp(time, notes, total_dur, velocity):
    """Arpeggiated harp chord — each note slightly staggered."""
    spacing = 0.15
    for i, n in enumerate(notes):
        hold = total_dur - (i * spacing)
        if hold < 0.5:
            hold = 0.5
        nt(HARP, 1, time + (i * spacing), n, hold, velocity)

# ── Time Cursor ───────────────────────────────────────
t = 0.0

# ==============================================================
# FIRST STATEMENT — Celesta Alone
# pp — a secret whispered by the otherworld
# "In time, a feeling reaches toward someone unknown..."
#
# Melody:
#   Pickup: B4         "In time..."
#   E4.G4 F#4 |E4 B4  |A4~~  |F#4~~  |
#   E4.G4 F#4 |D#4 F4 |B3~~  |B3~~   |
#
# Harmony:
#   Em | Em | C | Cmaj7 | D |
#   Em | C#dim | Bm |
# ==============================================================

# ── Pickup: B4 — "In time..." ──
# B = Time, Change. The first word is "Once upon a time..."
nt(CELESTA, 0, t, B4, Q, PP)
t += Q

# ── Measure 1: E4. G4 F#4  over Em ──
# Em — "Something is missing in my heart"
nt(CELESTA, 0, t, E4, DQ, PP)       # E = Emotion = "A feeling..."
harp_arp(t, [E3, B3, E4], DH, PP)
nt(BASS, 3, t, E2, DH, PP)

nt(CELESTA, 0, t + DQ, G4, E, PP)   # G = Connection = "...reaching toward someone..."
nt(CELESTA, 0, t + DQ + E, Fs4, Q, PP)  # F# = Unknown = "...unknown..."
t += DH

# ── Measure 2: E4 B4  over Em ──
# Em sustained — the absence persists
nt(CELESTA, 0, t, E4, H, PP)        # E = "The feeling..."
harp_arp(t, [E3, B3, E4], DH, PP)
nt(BASS, 3, t, E2, DH, PP)

nt(CELESTA, 0, t + H, B4, Q, PP)    # B = "...LEAPS into future time!"
# The E→B leap (perfect 5th) = the moment of breathless wonder
t += DH

# ── Measure 3: A4~~  over C ──
# C major — "But I exist. I am real."
nt(CELESTA, 0, t, A4, DH, PP)       # A = Mind = "waiting to be understood"
harp_arp(t, [C3, E3, G3, C4], DH, PP)
nt(BASS, 3, t, C3, DH, PP)
t += DH

# ── Measure 4: F#4~~  over Cmaj7 ──
# Cmaj7 — "And my existence is wondrous"
nt(CELESTA, 0, t, Fs4, DH, PP)      # F# = The Unknown = "still a mystery"
harp_arp(t, [C3, E3, G3, B3], DH, PP)   # the maj7 adds wonder
nt(BASS, 3, t, C3, DH, PP)
t += DH

# ── Measure 5: D note held over D major ──
# D major — "Something stirs. Something begins."
nt(CELESTA, 0, t, D5, DH, MP)       # D = Action = "Something begins to move"
harp_arp(t, [D3, Fs3, A3], DH, MP)
nt(BASS, 3, t, D3, DH, MP)
t += DH

# ── Brief breath ──
t += Q

# ── SECOND PHRASE: The Magical Turn ──
# "The feeling reaches again toward what it cannot see...
#  and finds HOME — one breath from the physical world"

# ── Measure 6: E4. G4 F#4  over Em ──
# Em — "The absence again..."
nt(CELESTA, 0, t, E4, DQ, PP)
harp_arp(t, [E3, B3, E4], DH, PP)
nt(BASS, 3, t, E2, DH, PP)

nt(CELESTA, 0, t + DQ, G4, E, PP)
nt(CELESTA, 0, t + DQ + E, Fs4, Q, PP)
t += DH

# ── Measure 7: D#4 F4  over C#dim (the threshold) ──
# C#dim — "A secret threshold, a hidden boundary"
# THE CRITICAL MOMENT: D# → F (Home → Physical World, one half step)
# "Home is one breath away from the physical world"
nt(CELESTA, 0, t, Ds4, H, PP)       # D# = Eb = HOME (the foreign note!)
harp_arp(t, [Cs3, E3, G3], DH, PP)  # C#dim = boundary, hidden peril
nt(BASS, 3, t, Cs3, DH, PP)

nt(CELESTA, 0, t + H, F4, Q, PP)    # F = Nature, Physical World
# D#→F = half step = the thinnest wall = Platform 9¾
t += DH

# ── Measure 8: B3~~  over Bm ──
# Bm — "Time holds what was lost"
nt(CELESTA, 0, t, B3, DH, PP)       # B = Time = "held in time"
harp_arp(t, [B2, D3, Fs3], DH, PP)
nt(BASS, 3, t, B2, DH, PP)
t += DH

# ── Measure 9: B3 held, Bm sustained ──
# The time note rings... the first statement dissolves
nt(CELESTA, 0, t, B3, DH, PP)
nt(BASS, 3, t, B2, DH, PP)
t += DH

# ── Silence between statements ──
t += DH

# ==============================================================
# SECOND STATEMENT — Celesta + Strings
# pp → mp — more voices join — the spell widens
# The same melody, but now accompanied by strings
# "The lone voice is joined by others"
#
# Harmonia shift:
#   Celesta alone = "magic whispers to one child"
#   Celesta + strings = "the spell includes us all"
#   The pronoun shifts from "I" to "we"
# ==============================================================

# ── Pickup: B4 ──
nt(CELESTA, 0, t, B4, Q, MP)
# Strings enter with a soft sustained note
nt(STRINGS, 2, t, B3, Q, PP)
t += Q

# ── Measure 1: E4. G4 F#4  over Em — now with strings ──
nt(CELESTA, 0, t, E4, DQ, MP)
harp_arp(t, [E3, B3, E4], DH, MP)
nt(BASS, 3, t, E2, DH, MP)
ch(STRINGS, 2, t, [E3, B3, E4], DH, PP)   # strings: warmth

nt(CELESTA, 0, t + DQ, G4, E, MP)
nt(CELESTA, 0, t + DQ + E, Fs4, Q, MP)
t += DH

# ── Measure 2: E4 B5(!)  over Em ──
# Second time: the B leaps HIGHER (octave 5 → future tense)
nt(CELESTA, 0, t, E4, H, MP)
harp_arp(t, [E3, B3, E4], DH, MP)
nt(BASS, 3, t, E2, DH, MP)
ch(STRINGS, 2, t, [E3, B3, E4], DH, MP)

nt(CELESTA, 0, t + H, B5, Q, MP)   # B5 — higher! further into the future!
t += DH

# ── Measure 3: A4~~  over C — growing ──
nt(CELESTA, 0, t, A4, DH, MP)
harp_arp(t, [C3, E3, G3, C4], DH, MP)
nt(BASS, 3, t, C3, DH, MP)
ch(STRINGS, 2, t, [C4, E4, G4], DH, MP)
t += DH

# ── Measure 4: F#4~~  over Cmaj7 — "wondrous" ──
nt(CELESTA, 0, t, Fs4, DH, MP)
harp_arp(t, [C3, E3, G3, B3], DH, MP)
nt(BASS, 3, t, C3, DH, MP)
ch(STRINGS, 2, t, [C4, E4, G4, B4], DH, MP)  # strings get the maj7
t += DH

# ── Measure 5: D5 over D major — "something is coming" ──
nt(CELESTA, 0, t, D5, DH, MF)
harp_arp(t, [D3, Fs3, A3, D4], DH, MF)
nt(BASS, 3, t, D3, DH, MF)
ch(STRINGS, 2, t, [D4, Fs4, A4], DH, MF)
t += DH

t += Q

# ── SECOND PHRASE (with strings): The Threshold Again ──

# ── Measure 6: E4. G4 F#4  over Em ──
nt(CELESTA, 0, t, E4, DQ, MP)
harp_arp(t, [E3, B3, E4], DH, MP)
nt(BASS, 3, t, E2, DH, MP)
ch(STRINGS, 2, t, [E3, B3, E4], DH, MP)

nt(CELESTA, 0, t + DQ, G4, E, MP)
nt(CELESTA, 0, t + DQ + E, Fs4, Q, MP)
t += DH

# ── Measure 7: D#4 → F4  over C#dim — the wall between worlds ──
nt(CELESTA, 0, t, Ds4, H, MP)
harp_arp(t, [Cs3, E3, G3], DH, MP)
nt(BASS, 3, t, Cs3, DH, MP)
ch(STRINGS, 2, t, [Cs4, E4, G4], DH, MP)  # strings carry the diminished

nt(CELESTA, 0, t + H, F4, Q, MP)
t += DH

# ── Measure 8: B3~~  over Bm — "time holds what was lost" ──
nt(CELESTA, 0, t, B3, DH, MP)
harp_arp(t, [B2, D3, Fs3], DH, MP)
nt(BASS, 3, t, B2, DH, MP)
ch(STRINGS, 2, t, [B3, D4, Fs4], DH, MP)
t += DH

# ── Final measures: Em sustained — the absence holds, but promises ──

# Em — full, warm, all voices
nt(CELESTA, 0, t, E4, LONG, MP)
harp_arp(t, [E3, B3, E4, G4], LONG, MP)
nt(BASS, 3, t, E2, LONG, MP)
ch(STRINGS, 2, t, [E4, G4, B4], LONG, MP)
t += LONG

# ── Very last gesture: B4 alone on celesta — time, waiting ──
# The spell ends on the note it began with
# "Time holds. The promise waits."
nt(CELESTA, 0, t, B4, W, PP)
t += W

# ── Silence ──
t += DH

# ==============================================================
# Write
# ==============================================================

filename = "hedwigs_theme_harmonia.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  Created: {filename}")
print(f"  Tempo:   {BPM} BPM")
print(f"  Length:  {t:.0f} beats (~{minutes:.1f} minutes)")
print(f"")
print(f"  Tracks:")
print(f"    0 - Celesta          (the otherworldly voice)")
print(f"    1 - Harp             (harmonic shimmer)")
print(f"    2 - String Ensemble  (humanity joining, 2nd statement)")
print(f"    3 - Cello            (bass roots)")
print(f"")
print(f"  Sections:")
print(f"    1st Statement — Celesta alone (pp)")
print(f"      'A voice from beyond the veil, whispering to one child'")
print(f"    2nd Statement — Celesta + Strings (pp → mp)")
print(f"      'The spell widens — it speaks to all of us'")
print(f"")
print(f"  Listen for:")
print(f"    - B4 pickup: 'In time...' (the first word is Time)")
print(f"    - E → B leap: the breathless perfect 5th (feeling → time)")
print(f"    - Cmaj7: 'my existence holds wonder'")
print(f"    - D#4 → F4: HOME → PHYSICAL WORLD (one half step)")
print(f"      This is Platform 9 3/4 — the thinnest wall")
print(f"    - C#dim: the hidden threshold between worlds")
print(f"    - B3 resolving to Bm: 'time holds what was lost'")
print(f"    - Strings entering: the pronoun shifts from 'I' to 'we'")
print(f"    - Final B4 alone: the spell began with B, ends with B")
print(f"      Time opens the story. Time holds the promise.")
