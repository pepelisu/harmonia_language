"""
KNOWING v2.0 — Polyphonic Recomposition
"Life is a story that we tell to ourselves..."

WHAT'S DIFFERENT FROM v1.1:
  - Every chord is read through ALL its constituent notes
  - Arpeggiation order = internal syntax of each polyphonic word
  - G major replaces G→D (Connection+Time+Action in one chord)
  - Inner voice tracking: specific domain-notes are sustained 
    across chord changes to show what persists and what transforms
  - The Am→A transformation explicitly voices C→C# in an 
    isolated inner line
  - Four tracks instead of three: Melody, Harmony (arpeggiated 
    polyphonic words), Bass, and Domain Tracking (the thread)

Compare with:
  - knowing_harmonia.mid (v1.0 — telegraphic)
  - knowing_fluid.mid   (v1.1 — with connective tissue)
  - knowing_v2.mid      (v2.0 — polyphonic, THIS FILE)

Run: python knowing_v2.py
Output: knowing_v2.mid
"""

from midiutil import MIDIFile

# ── Configuration ─────────────────────────────────────
BPM = 63    # Slightly slower than v1.1 — each note in the 
            # arpeggio needs space to speak as its own domain

# Durations
S    = 0.25     # sixteenth
E    = 0.5      # eighth
Q    = 1.0      # quarter
DQ   = 1.5      # dotted quarter
H    = 2.0      # half
DH   = 3.0      # dotted half
W    = 4.0      # whole
LONG = 6.0
VERY = 8.0
EXT  = 10.0     # extended
FINAL = 14.0

# Dynamics
PPP  = 22
PP   = 35
P    = 45
MP   = 58
MF   = 75
F    = 95

# ── MIDI Notes ────────────────────────────────────────
A2=45; As2=46; Bb2=46; B2=47
C3=48; Cs3=49; D3=50; Ds3=51; Eb3=51; E3=52; F3=53
Fs3=54; G3=55; Gs3=56; Ab3=56; A3=57; As3=58; Bb3=58; B3=59
C4=60; Cs4=61; D4=62; Ds4=63; Eb4=63; E4=64; F4=65
Fs4=66; G4=67; Gs4=68; Ab4=68; A4=69; As4=70; Bb4=70; B4=71
C5=72; Cs5=73; D5=74; Ds5=75; Eb5=75; E5=76; F5=77
Fs5=78; G5=79; Gs5=80; A5n=81; As5=82; Bb5=82; B5=83

# ── Track Setup ───────────────────────────────────────
midi = MIDIFile(4, adjust_origin=False)

MEL   = 0    # Melody — the speaking voice (top line)
HARM  = 1    # Harmony — arpeggiated polyphonic words
BASS  = 2    # Bass — narrative spine, walking between roots
TRACK = 3    # Domain Tracking — sustained notes showing 
             # what persists across chord changes (the thread)

midi.addTempo(0, 0, BPM)

# All piano — the self speaking to itself
for tr in range(4):
    midi.addProgramChange(tr, tr, 0, 0)  # Acoustic Grand

midi.addTrackName(MEL,   0, "Melody - The Voice")
midi.addTrackName(HARM,  1, "Harmony - Polyphonic Words")
midi.addTrackName(BASS,  2, "Bass - Narrative Spine")
midi.addTrackName(TRACK, 3, "Domain Thread - What Persists")

# ── Helpers ───────────────────────────────────────────
def nt(track, chan, time, pitch, dur, vel):
    midi.addNote(track, chan, pitch, time, dur, vel)

def ch(track, chan, time, notes, dur, vel):
    for n in notes:
        midi.addNote(track, chan, n, time, dur, vel)

def domain_arp(time, notes, note_dur, vel, spacing=None):
    """
    v2.0 DELIBERATE ARPEGGIATION
    Each note is given space to speak as its own domain.
    The order of notes = the internal syntax of the polyphonic word.
    
    Unlike v1.1's decorative arpeggiation, this is SEMANTIC:
    the first note is the subject, the last is the predicate.
    """
    if spacing is None:
        spacing = note_dur
    t = time
    for n in notes:
        nt(HARM, 1, t, n, note_dur + (len(notes) - 1) * spacing - (t - time), vel)
        t += spacing
    return time + len(notes) * spacing

def walk(time, notes, dur_each, vel):
    """Walking bass — each note a preposition."""
    t = time
    for n in notes:
        nt(BASS, 2, t, n, dur_each, vel)
        t += dur_each
    return t

def sustain_on(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 127)

def sustain_off(track, chan, time):
    midi.addControllerEvent(track, chan, time, 64, 0)

# ── Time Cursor ───────────────────────────────────────
t = 0.0

# ==============================================================
# PICKUP: E4 — "Feel."
#
# v2.0 note: E = Emotion. But in the polyphonic view,
# this single note is a DOMAIN, not a word. It is the 
# first semantic atom. The chord will add the other atoms.
# A single note is a domain waiting for context.
# ==============================================================

sustain_on(BASS, 2, t)
sustain_on(TRACK, 3, t)

nt(MEL, 0, t, E4, DQ, PP)

# Bass: A barely audible — the key, the ground of knowing
nt(BASS, 2, t, A2, DQ, PPP)

# Domain thread: E3 sustained from the very beginning
# E (Emotion) will persist across the ENTIRE piece
# It is the thread that never breaks
nt(TRACK, 3, t, E3, VERY * 4, PPP)  # held for a very long time

t += DQ + S

# ==============================================================
# SECTION 1: "Life is a story that we tell to ourselves"
#
# v2.0 CHANGES:
#   - C major arpeggiated as C→E→G (Self→Emotion→Connection)
#   - Cmaj7 arpeggiated with B (Time) given its own moment
#   - G major REPLACES G→D: Connection+Time+Action in ONE chord
#     (arpeggiated G→B→D = "Connection across Time through Action")
#   - C/E arpeggiated E→G→C (Emotion→Connection→Self = 
#     "to ourselves, arriving through feeling and connection")
#
# 6/8 lilt — narrative
# ==============================================================

# ── C major — "Life..." ──
# v2.0: C+E+G = Self + Emotion + Connection
# "A being that feels and connects"
# Arpeggio order: C→E→G (Self first, then Emotion, then Connection)
# "A self... that feels... and connects"

# Deliberate arpeggiation — each note gets a full beat
nt(HARM, 1, t, C3, DH + H, MP - 15)       # C = Self (first, foundation)
nt(HARM, 1, t + Q, E3, DH, MP - 15)        # E = Emotion (second, felt)
nt(HARM, 1, t + H, G3, DH - H, MP - 15)    # G = Connection (third, reaching out)

# Melody: rises through the chord's own domains
nt(MEL, 0, t, C4, Q, MP)                    # Self
nt(MEL, 0, t + Q, E4, Q, MP)               # Emotion  
nt(MEL, 0, t + H, G4, Q, MP)               # Connection
# The melody and harmony speak the same three words simultaneously

# Bass: C (Self) — the ground
nt(BASS, 2, t, C3, DH, MP - 15)

t += DH

# ── Cmaj7 — "...is a wondrous story" ──
# v2.0: C+E+G+B = Self + Emotion + Connection + TIME
# "The complete human situation — being becomes biography"
# The B (Time) is the NEW element — it transforms being into story
# Arpeggio: C→E→G→B (Self→Emotion→Connection→Time)

nt(HARM, 1, t, C3, W, MP - 15)             # C = Self (persists)
nt(HARM, 1, t + E, E3, W - E, MP - 15)     # E = Emotion (persists)
nt(HARM, 1, t + Q, G3, DH, MP - 15)        # G = Connection (persists)
nt(HARM, 1, t + DQ, B3, DH - E, MP)        # B = TIME — the new arrival!
# B is played slightly louder — it is the revelation

# Melody: the B (Time) gets the highest, most prominent position
nt(MEL, 0, t, G4, Q, MP)                    # Connection (continuing)
nt(MEL, 0, t + Q, A4, E, MP - 5)           # passing: Knowledge (approached)
nt(MEL, 0, t + DQ, B4, DQ, MP)             # TIME — the revelation note
# "Connection... touching knowledge... arriving at TIME"
# "Being acquires time. The story begins."

# Bass: C held — Self persists as foundation
nt(BASS, 2, t, C3, W, MP - 15)

# Domain thread: E persists (emotion continues)
# G enters the thread (connection joins)
nt(TRACK, 3, t, G3, W * 3, PP)             # Connection will persist far

t += W

# ── Walking bass: C → D → ... to G ──
# v2.0: each walk note is a domain-preposition
# C (Self) → D (Action) → stepping toward G (Connection)
# "Self, through action, arriving at connection"

nt(BASS, 2, t, D3, Q, MP - 15)             # D = Action — "through doing"
nt(MEL, 0, t, A4, E, MP - 10)              # passing: Knowledge
nt(MEL, 0, t + E, B4, E, MP - 10)          # passing: Time
t += Q

# ── G major — "We tell" ──
# v2.0 KEY CHANGE: G major = G+B+D = Connection + Time + Action
# "Togetherness across time, expressed through doing"
# 
# In v1.1, this was TWO chords: G ("we") then D ("tell")
# In v2.0, G major ALREADY CONTAINS Action (D is its fifth)
# "We tell" lives in ONE chord. The combination IS the meaning.
#
# Arpeggio: G→B→D (Connection→Time→Action = "together, across time, doing")

nt(HARM, 1, t, G3, DH + Q, MP - 10)       # G = Connection ("we...")
nt(HARM, 1, t + E, B3, DH, MP - 10)        # B = Time ("...across time...")
nt(HARM, 1, t + Q, D4, DH - E, MP - 5)     # D = Action ("...TELL")
# D played slightly louder — Action is the verb, the emphasis

# Melody: leaps to D5 — Action gets the high note
nt(MEL, 0, t, G4, Q, MP)                    # Connection
nt(MEL, 0, t + Q, D5, H, MP)               # Action — the leap = emphasis
# "Connection... TELL" — the leap IS the act of telling

# Bass: G
nt(BASS, 2, t, G3, DH, MP - 15)

t += DH

# ── Walking bass: G → F → E → to C/E ──
# v2.0: G (Connection) → F (Nature/World) → E (Emotion)
# "Connection, through the world, arriving at feeling"
# The bass literally walks from others through the world to feeling

nt(BASS, 2, t, F3, Q, MP - 15)             # F = Nature — "through the world"
nt(MEL, 0, t, D5, E, MP - 10)              # melody begins descent
nt(MEL, 0, t + E, C5, E, MP - 10)          # stepping down: Self
t += Q

nt(BASS, 2, t, E3, E, MP - 15)             # E = Emotion — arriving
nt(MEL, 0, t, B4, E, MP - 10)              # Time (passing)
t += E

# Melody: appoggiatura before arriving — "despite, arriving"
nt(MEL, 0, t, F4, E, MP - 10)              # F = Nature — appoggiatura
                                             # "despite the world..."
t += E

# ── C/E — "...to ourselves" ──
# v2.0: C major in first inversion = E in bass
# Content: Self + Emotion + Connection (same as C major)
# But with Emotion as the FOUNDATION (E in bass)
# "To ourselves — received through feeling"
#
# Arpeggio: E→G→C (Emotion→Connection→Self)
# Reversed order from the opening C chord!
# Opening: C→E→G = "Self, feeling, connecting" (subject speaks)
# Closing: E→G→C = "Feeling, connecting, self" (subject receives)
# The SAME chord, reversed — the speaker becomes the listener

nt(HARM, 1, t, E3, DH, MP - 10)            # E = Emotion (now the foundation!)
nt(HARM, 1, t + E, G3, DH - E, MP - 10)    # G = Connection
nt(HARM, 1, t + Q, C4, DH - Q, MP - 10)    # C = Self (now arrives LAST)

# Melody: arrives at E4 — Emotion — the self rests on feeling
nt(MEL, 0, t, E4, H, MP)                    # Emotion — home
nt(MEL, 0, t + H, C4, Q, P)                # Self — whispered, last

# Bass: E (Emotion as ground)
nt(BASS, 2, t, E3, DH, MP - 15)

# The circle closes: C→E→G (opening) → E→G→C (closing)
# The arpeggio reversed. The speaker became the audience.
# "Life speaks to itself."

t += DH

sustain_off(BASS, 2, t)
sustain_off(TRACK, 3, t)

# ── Transition breath ──
# Bass walks from E down to A (Emotion → Knowledge)
# "From feeling... descending toward knowing"
nt(BASS, 2, t, D3, Q, P - 10)              # D = Action
nt(BASS, 2, t + Q, C3, Q, P - 10)          # C = Self
nt(BASS, 2, t + H, B2, Q, P - 10)          # B = Time
# Melody: echoes the descent
nt(MEL, 0, t + Q, B3, Q, PP)               # Time...
nt(MEL, 0, t + H, A3, Q, PP)               # Knowledge (arriving)
t += DH


# ==============================================================
# SECTION 2a: "You don't know what you still have to learn"
#
# v2.0 CHANGES:
#   - Am arpeggiated as A→C→E (Knowledge→Self→Emotion)
#     "understanding through personal experience and feeling"
#   - F#m arpeggiated as F#→A→C# (Unknown→Knowledge→Boundary)
#     "mystery partially understood at a threshold"
#   - Dsus4 = D+G+A: the Unknown (F#) replaced by Connection (G)
#     "doing through others toward understanding — WITHOUT mystery"
#     The suspension is specifically: mystery replaced by the familiar
#   - A7 polyphonic: Knowledge+Boundary+Emotion+Connection
#     "understanding through confrontation, felt and shared"
# ==============================================================

sustain_on(BASS, 2, t)
sustain_on(TRACK, 3, t)

# ── Am — "You don't know" ──
# v2.0: A+C+E = Knowledge + Self + Emotion
# "Understanding through personal experience and feeling"
# This is INTIMATE not-knowing — known through the self, felt
# Arpeggio: A→C→E (Knowledge→Self→Emotion)

nt(HARM, 1, t, A3, DH + H, P)              # A = Knowledge
nt(HARM, 1, t + E, C4, DH, P)              # C = Self — the personal
nt(HARM, 1, t + Q, E4, DH - E, P)          # E = Emotion — the felt

# Domain thread: C (Self) enters — track it, it will transform
nt(TRACK, 3, t, C4, VERY, PP)              # C = Self — THE NOTE THAT WILL CHANGE

# Melody: starts high, descends — the realization falls
nt(MEL, 0, t, E5, DQ, P)                    # Emotion (high — the feeling)
nt(MEL, 0, t + DQ, C5, Q, P)               # Self (descending — personal)
nt(MEL, 0, t + DQ + Q, A4, E, P)           # Knowledge (arrived — but minor)

# Bass: A
nt(BASS, 2, t, A2, DH, P - 10)

t += DH

# ── Walking bass: A → G# → G → F# ──
# v2.0: Knowledge → Spirit → Connection → Unknown
# "Understanding, through the sacred, through others, to mystery"
# CHROMATIC descent — inevitability
nt(BASS, 2, t, Gs3, E, P - 10)             # G# = Spirit
nt(BASS, 2, t + E, G3, E, P - 10)          # G = Connection
nt(BASS, 2, t + Q, Fs3, E, P - 10)         # F# = Unknown (arriving)

# Melody: descending toward the unknown
nt(MEL, 0, t, B4, E, P - 5)                # Time
nt(MEL, 0, t + E, A4, E, P - 5)            # Knowledge
nt(MEL, 0, t + Q, Gs4, E, P - 5)           # Spirit (chromatic)
t += DQ

# ── F#m — "the unknown is felt" ──
# v2.0: F#+A+C# = Unknown + Knowledge + Boundary
# "Mystery partially understood at a threshold"
# Arpeggio: F#→A→C# (Unknown→Knowledge→Boundary)

nt(HARM, 1, t, Fs3, DH, P)                 # F# = Unknown
nt(HARM, 1, t + E, A3, DH - E, P)          # A = Knowledge
nt(HARM, 1, t + Q, Cs4, DH - Q, P)         # C# = Boundary

# Domain thread: C (Self) is NO LONGER in this chord
# C# (Boundary) has appeared — foreshadowing the transformation
# But C is still sustaining from Am... the old self persists in memory
# while the new chord contains Boundary instead

# Melody: C# gets prominence — the boundary is felt
nt(MEL, 0, t, Fs4, Q, P)                    # Unknown
nt(MEL, 0, t + Q, Cs5, Q, P)               # Boundary — reaching
nt(MEL, 0, t + H, A4, Q, P)                # Knowledge — settling

# Bass: F#
nt(BASS, 2, t, Fs3, DH, P - 10)

t += DH

# ── Walking bass: F# → E → D ──
# Unknown → Emotion → Action
nt(BASS, 2, t, E3, Q, P - 10)              # Emotion
nt(BASS, 2, t + Q, D3, Q, P - 10)          # Action (arriving)
nt(MEL, 0, t, A4, Q, P - 5)                # held
nt(MEL, 0, t + Q, G4, Q, P - 5)            # step down
t += H

# ── Dsus4 — "action waits" ──
# v2.0: D+G+A = Action + Connection + Knowledge
# Missing: F# (Unknown) — replaced by G (Connection)
# "Doing through others toward understanding — WITHOUT MYSTERY"
# The suspension is SPECIFIC: mystery has been replaced by the familiar
# You're learning from others, not from the void

nt(HARM, 1, t, D3, H + Q, P)               # D = Action
nt(HARM, 1, t + E, G3, H, P)               # G = Connection (replacing F#!)
nt(HARM, 1, t + Q, A3, H - E, P)           # A = Knowledge

# Melody: G (Connection) — the sus4 note — what replaced mystery
nt(MEL, 0, t, G4, Q, P)                     # Connection — the substitute
nt(MEL, 0, t + Q, A4, Q, P)                # Knowledge — reaching

# Bass: D
nt(BASS, 2, t, D3, H, P - 10)

t += H

# ── Chromatic approach to A7 ──
nt(BASS, 2, t, Gs3, E, P - 10)             # pressing toward A
nt(MEL, 0, t, Gs4, E, P - 5)               # mirror
t += E

# ── A7 — "What?" ──
# v2.0: A+C#+E+G = Knowledge + Boundary + Emotion + Connection
# "Understanding through confrontation, felt and shared"
# The question contains confrontation (C#) AND sharing (G)
# "Do you understand what we've been through together?"

nt(HARM, 1, t, A3, W + H, P)               # A = Knowledge
nt(HARM, 1, t + E, Cs4, W, P)              # C# = Boundary — confrontation!
nt(HARM, 1, t + Q, E4, W - E, P)           # E = Emotion
nt(HARM, 1, t + DQ, G4, DH, P)             # G = Connection — shared!

# Melody: the question unfolds — confrontation then feeling
nt(MEL, 0, t, E5, Q, P)                     # Emotion — high
nt(MEL, 0, t + Q, Cs5, Q, P)               # Boundary — the confrontation
nt(MEL, 0, t + H, G4, Q, P)                # Connection — the sharing
nt(MEL, 0, t + DH, E4, Q, P)               # Emotion — settling, waiting

# Bass: A
nt(BASS, 2, t, A2, LONG, P - 10)

t += LONG

sustain_off(BASS, 2, t)
sustain_off(TRACK, 3, t)

# ── Transition ──
nt(BASS, 2, t, E3, Q, PPP)                 # E lingers
nt(BASS, 2, t + Q, Gs3, Q, PPP)            # chromatic approach
t += H


# ==============================================================
# SECTION 2b: "because knowledge is infinite"
#
# v2.0 CHANGES:
#   - A = Knowledge + Boundary + Emotion (battle-won truth)
#   - Amaj7 = Knowledge + Boundary + Emotion + SPIRIT
#     (understanding touching the transcendent)
#   - Aaug = Knowledge + Boundary + Nature  
#     ("the physical world understood at its limits" = infinity)
#   - E = Emotion + Spirit + Time (feeling that transcends)
#   - B = Time + Home + Unknown (belonging at mystery's edge)
#   - F# = Unknown + Desire + Boundary (mystery longed for)
#
# Each expansion chord is richer — three/four domains at once
# ==============================================================

sustain_on(BASS, 2, t)
sustain_on(TRACK, 3, t)

# ── A major — "Knowledge." ──
# v2.0: A+C#+E = Knowledge + Boundary + Emotion
# "Understanding won through confrontation, felt deeply"
# Arpeggio: A→C#→E (Know→Boundary→Feel)
# This is HARDER knowledge than Am's personal knowing

nt(HARM, 1, t, A3, W, MF - 10)             # A = Knowledge
nt(HARM, 1, t + Q, Cs4, DH, MF - 5)        # C# = BOUNDARY — emphasized
nt(HARM, 1, t + H, E4, H, MF - 10)         # E = Emotion

# Domain thread: C# appears! The Boundary has entered
# Compare: Am had C (Self), A has C# (Boundary)
# The thread should show C# NOW (Self has transformed into Boundary)
nt(TRACK, 3, t, Cs4, W * 2, MP)            # C# tracked — Boundary present

# Melody: confident, rising
nt(MEL, 0, t, A4, Q, MF)                    # Knowledge
nt(MEL, 0, t + Q, Cs5, Q, MF)              # Boundary — clear, confrontational
nt(MEL, 0, t + H, E5, H, MF)               # Emotion — opening

# Bass: A
nt(BASS, 2, t, A2, W, MF - 15)

t += W

# ── Amaj7 — "is beautiful" ──
# v2.0: A+C#+E+G# = Knowledge + Boundary + Emotion + SPIRIT
# "Understanding through confrontation, felt, touching the transcendent"
# The G# (Spirit) is NEW — knowledge reaches toward the sacred

nt(HARM, 1, t, A3, W, MF - 10)             # Knowledge
nt(HARM, 1, t + E, Cs4, W - E, MF - 10)    # Boundary
nt(HARM, 1, t + Q, E4, DH, MF - 10)        # Emotion
nt(HARM, 1, t + DQ, Gs4, DH - E, MF)       # G# = SPIRIT — the new arrival!

# Melody: the G# (Spirit) gets attention — the turn toward wonder
nt(MEL, 0, t, E5, E, MF)                    # Emotion
nt(MEL, 0, t + E, Gs5, Q, MF)              # SPIRIT — the reach toward transcendence
nt(MEL, 0, t + E + Q, A5n, E, MF)          # Knowledge — at the heights
nt(MEL, 0, t + H + E, Cs5, DQ, MF)         # Boundary — even here

# Bass: A
nt(BASS, 2, t, A2, W, MF - 15)

t += W

# ── Aaug — "is INFINITE" ──
# v2.0: A+C#+F = Knowledge + Boundary + NATURE
# "The physical world understood at its absolute limits"
# The augmented chord is SYMMETRICAL — no center, no resolution
# F (Nature) replaces E#/F enharmonically — 
# the world ITSELF enters the chord of knowledge
#
# Three domains in equal, centerless expansion

nt(HARM, 1, t, A3, LONG, MF - 10)          # Knowledge
nt(HARM, 1, t + E, Cs4, LONG - E, MF - 10) # Boundary
nt(HARM, 1, t + Q, F4, LONG - Q, MF - 5)   # NATURE — the #5 — the world breaks in!

# Melody: F5 — Nature — oscillating with E5 (Emotion)
# The boundary between understanding and feeling and the world SHAKES
nt(MEL, 0, t, Cs5, Q, MF)                   # Boundary
nt(MEL, 0, t + Q, E5, Q, MF)               # Emotion
nt(MEL, 0, t + H, F5, Q, MF)               # NATURE — the break!
nt(MEL, 0, t + DH, E5, Q, MF)              # Emotion (oscillating)
nt(MEL, 0, t + W, F5, H, MF)               # Nature holds — infinity

# Bass: A
nt(BASS, 2, t, A2, LONG, MF - 15)

t += LONG

sustain_off(BASS, 2, t)
sustain_off(TRACK, 3, t)
t += S

# ── The Expansion: E → B → F# ──
# v2.0: each chord is now THREE domains, not one
# The expansion reaches further because each chord carries more

sustain_on(BASS, 2, t)
sustain_on(TRACK, 3, t)

# ── E major — "it touches feeling" ──
# v2.0: E+G#+B = Emotion + Spirit + Time
# "Feeling that transcends the moment"
# Three domains: feeling + the sacred + duration

nt(HARM, 1, t, E3, DH + Q, MF - 10)        # Emotion
nt(HARM, 1, t + E, Gs3, DH, MF - 10)       # Spirit — transcendence!
nt(HARM, 1, t + Q, B3, DH - E, MF - 10)    # Time

# Melody: Spirit (G#) gets the high note — transcendence
nt(MEL, 0, t, E5, Q, MF)                    # Emotion
nt(MEL, 0, t + Q, Gs5, H, MF)              # Spirit — reaching high
nt(MEL, 0, t + DH, B4, Q, MP)              # Time — settling

# Bass: E
nt(BASS, 2, t, E3, DH, MF - 15)

t += DH

# Walking: E → D# → D → C# → B
# Emotion → Home → Action → Boundary → Time
nt(BASS, 2, t, Ds3, E, MP - 10)            # Home (briefly)
nt(BASS, 2, t + E, D3, E, MP - 10)         # Action
nt(BASS, 2, t + Q, Cs3, E, MP - 10)        # Boundary
nt(MEL, 0, t, Gs5, E, MP - 5)              # Spirit descending
nt(MEL, 0, t + E, Fs5, Q, MP - 5)          # Unknown (approaching)
t += DQ

# ── B major — "spans time" ──
# v2.0: B+D#+F# = Time + HOME + Unknown
# "A moment of belonging at the edge of the unknowable"
# HOME (D#) appears inside a chord for the first time in the piece!

nt(HARM, 1, t, B3, DH, MP - 10)            # Time
nt(HARM, 1, t + E, Ds4, DH - E, MP - 5)    # HOME — D#! First appearance!
nt(HARM, 1, t + Q, Fs4, DH - Q, MP - 10)   # Unknown

# Domain thread: D# (Home) appears — track it
nt(TRACK, 3, t, Ds4, DH, P)                # Home enters the thread — briefly

# Melody: Home (D#) gets prominence
nt(MEL, 0, t, Ds5, DQ, MP)                  # HOME — the note that wasn't there before
nt(MEL, 0, t + DQ, Fs5, DQ, MP - 5)        # Unknown

# Bass: B
nt(BASS, 2, t, B2, DH, MP - 10)

t += DH

# Walking: B → A# → A → G# → F#
nt(BASS, 2, t, As3, E, P - 10)             # Desire (Bb/A#)
nt(BASS, 2, t + E, A3, E, P - 10)          # Knowledge
nt(BASS, 2, t + Q, Gs3, E, P - 10)         # Spirit
nt(MEL, 0, t, Cs5, DQ, P - 5)              # Boundary (descending)
t += DQ

# ── F# major — "reaches the unknown" ──
# v2.0: F#+A#+C# = Unknown + DESIRE + Boundary
# "Mystery longed for at the edge of the known"
# DESIRE (A#/Bb) appears — the unknown is not just encountered, it is WANTED

nt(HARM, 1, t, Fs3, DH, P - 10)            # Unknown
nt(HARM, 1, t + E, As3, DH - E, P - 10)    # DESIRE — Bb! Wanting the mystery!
nt(HARM, 1, t + Q, Cs4, DH - Q, P - 10)    # Boundary — the edge

# Melody: fading into the distance
nt(MEL, 0, t, Cs5, Q, P)                    # Boundary
nt(MEL, 0, t + Q, As4, Q, P - 5)           # Desire — wanting
nt(MEL, 0, t + H, Fs4, Q, P - 10)          # Unknown — the farthest reach

# Bass: F#
nt(BASS, 2, t, Fs3, DH, P - 10)

t += DH

sustain_off(BASS, 2, t)
sustain_off(TRACK, 3, t)

# ── The Silence of Infinity ──
# v2.0: not fully empty — E (Emotion) persists
# AND: fragments of domain-notes echo — the expansion reverberates

nt(TRACK, 3, t, E3, VERY, PPP)             # Emotion — the eternal thread

# Echoes of the expansion — fragments of what was touched
nt(MEL, 0, t + H, Gs4, E, PPP)             # Spirit (echo)
nt(MEL, 0, t + DH, Ds4, E, PPP)            # Home (echo)
nt(MEL, 0, t + W, A4, Q, PPP)              # Knowledge (echo)
nt(MEL, 0, t + W + DQ, E4, Q, PPP)         # Emotion (echo — the thread)

t += VERY


# ==============================================================
# SECTION 2c: "knowing what is missing = knowing it all"
#
# v2.0 THE TRANSFORMATION — now read polyphonically
#
# Am = Knowledge + SELF + Emotion (C is the third — personal)
# A  = Knowledge + BOUNDARY + Emotion (C# is the third — confrontational)
# A5 = Knowledge + Emotion (both Self and Boundary removed)
#
# The v2.0 insight: C→C# is not just "minor→major"
# It is Self→Boundary — "internal experience becomes external confrontation"
# And then BOTH are removed — neither the personal nor the confrontational
# survives. What remains is the irreducible pair.
#
# The domain thread will EXPLICITLY voice C→C# and then silence both.
# ==============================================================

sustain_on(BASS, 2, t)
sustain_on(MEL, 0, t)
sustain_on(HARM, 1, t)
sustain_on(TRACK, 3, t)

# ── Am — "knowing what is missing" ──
# v2.0: A+C+E = Knowledge + SELF + Emotion
# Arpeggio: A→C→E (Knowledge→Self→Emotion)
# "I know this through who I am and what I feel"

# Deliberate arpeggiation — each domain speaks
nt(HARM, 1, t, A3, LONG, PP)               # A = Knowledge
nt(HARM, 1, t + Q, C4, LONG - Q, PP)       # C = SELF — the personal third
nt(HARM, 1, t + H, E4, LONG - H, PP)       # E = Emotion

# Domain thread: C (Self) — ISOLATED, PROMINENT
# This is THE NOTE that will transform
nt(TRACK, 3, t, C4, LONG + H, PP)          # C = Self — held, tracked

# Melody: mirrors the arpeggio
nt(MEL, 0, t, E5, Q, PP)                    # Emotion
nt(MEL, 0, t + Q, C5, Q, PP)               # Self
nt(MEL, 0, t + H, A4, H, PP)               # Knowledge

# Bass: A — Knowledge persists as ground
nt(BASS, 2, t, A2, LONG, PP - 10)
nt(BASS, 2, t, A3, LONG, PPP)              # octave reinforcement

t += LONG

# ══════════════════════════════════════════════════════════
# THE v2.0 BRIDGE — The Transformation in Slow Motion
#
# What happens polyphonically:
# Am chord: A + C  + E = Knowledge + SELF + Emotion
# A  chord: A + C# + E = Knowledge + BOUNDARY + Emotion
#
# The transformation: C (Self) → C# (Boundary)
# "Internal experience becomes external confrontation"
# "The personal becomes the tested"
# "Who I am becomes what I've faced"
#
# A and E do NOT change. Knowledge and Emotion persist.
# Only the THIRD changes — and it changes by one half step.
#
# In v1.1, this was "minor becomes major."
# In v2.0, this is "Self becomes Boundary."
# ══════════════════════════════════════════════════════════

# Bass: A pedal — "throughout this, Knowledge persists"
nt(BASS, 2, t, A2, W + H, PP)
nt(BASS, 2, t, A3, W + H, PPP)

# E (Emotion) persists — unchanged
nt(HARM, 1, t, E4, W + H, PP)              # Emotion: constant

# A (Knowledge) persists — unchanged
nt(HARM, 1, t, A3, W + H, PP)              # Knowledge: constant

# NOW — the transformation of the third
# C (Self) is still sounding from the domain thread...
# It begins to rise

# Phase 1: C holds — "the self, still present"
nt(TRACK, 3, t, C4, H, PP)                 # Self — holding
nt(MEL, 0, t, C5, H, PP)                   # melody mirrors: Self

t += H

# Phase 2: the half step — C moves to C#
# "The self presses against its boundary"
# This is the moment of transformation

# Melody: B (Time) as appoggiatura before C#
# "Through time... the boundary appears"
nt(MEL, 0, t, B4, Q, PP)                    # B = Time — appoggiatura
                                             # "through time..."

# Domain thread: C begins to waver
nt(TRACK, 3, t, C4, E, PP)                 # C still — barely
# Then: the SHIFT
nt(TRACK, 3, t + E, Cs4, DQ, PP)           # C# APPEARS
                                             # Self → Boundary
                                             # The personal becomes the confrontational
                                             # One half step. The transformation.

# Melody: mirrors the shift
nt(MEL, 0, t + Q, Cs5, Q, PP)              # C# — "becoming..."
                                             # The melody has crossed

t += H

# ── A major — "knowing it all" ──
# v2.0: A+C#+E = Knowledge + BOUNDARY + Emotion
# Arpeggio: A→C#→E (Knowledge→Boundary→Emotion)
# "I know this through what I've confronted and what I feel"

# Same arpeggio as Am, but with C# instead of C
# EVERYTHING ELSE IS IDENTICAL — same A, same E, same rhythm
nt(HARM, 1, t, A3, LONG, PP)               # A = Knowledge (same)
nt(HARM, 1, t + Q, Cs4, LONG - Q, PP)      # C# = BOUNDARY (changed!)
nt(HARM, 1, t + H, E4, LONG - H, PP)       # E = Emotion (same)

# Domain thread: C# now established
nt(TRACK, 3, t, Cs4, LONG, PP)             # Boundary — the new third

# Melody: IDENTICAL rhythm to the Am melody — same pattern, one note different
nt(MEL, 0, t, E5, Q, PP)                    # Emotion (same)
nt(MEL, 0, t + Q, Cs5, Q, PP)              # BOUNDARY (was Self — only change)
nt(MEL, 0, t + H, A4, H, PP)               # Knowledge (same)

# Bass: A — unchanged
nt(BASS, 2, t, A2, LONG, PP - 10)

t += LONG

# ══════════════════════════════════════════════════════════
# THE DISSOLUTION — v2.0 version
#
# What happens:
# A major contains A + C# + E = Knowledge + Boundary + Emotion
# A5 contains A + E = Knowledge + Emotion
#
# BOTH C (Self) and C# (Boundary) are removed.
# Neither the personal nor the confrontational survives.
# The distinction between internal and external knowing dissolves.
#
# v2.0 tracks this explicitly: the domain thread fades C# to silence
# while A and E strengthen. The POLYPHONIC content simplifies.
# From three domains to two. From a word to a pair.
# ══════════════════════════════════════════════════════════

# Phase 1: C# begins to fade — "the boundary weakens"
nt(BASS, 2, t, A2, W, PP)
nt(BASS, 2, t, E3, W, PP)                   # A and E in bass — strengthening

nt(HARM, 1, t, A3, W, PP)                   # Knowledge — persistent
nt(HARM, 1, t, E4, W, PP)                   # Emotion — persistent
nt(TRACK, 3, t, Cs4, W, P - 15)            # Boundary — fading...

nt(MEL, 0, t, A4, H, PP)                    # Knowledge
nt(MEL, 0, t + H, E5, H, PP)               # Emotion — the pair establishing
t += W

# Phase 2: C# barely audible — "the distinction dissolving"
nt(BASS, 2, t, A2, W, PPP)                  # Knowledge — deep
nt(BASS, 2, t, E3, W, PP)                   # Emotion — warmer

nt(HARM, 1, t, A3, W, PP)                   # Knowledge
nt(HARM, 1, t, E4, W, PP)                   # Emotion
nt(TRACK, 3, t, Cs4, W, PPP)               # Boundary — almost gone

nt(MEL, 0, t, E5, W, PP)                    # Emotion holds
t += W

# Phase 3: A5 — only Knowledge and Emotion remain
# C and C# are BOTH gone — neither Self nor Boundary
# The distinction between personal and confrontational has dissolved
# What remains: the irreducible pair — knowing and feeling

# Three octaves of A and E only
nt(BASS, 2, t, A2, FINAL, PPP)             # Knowledge — deepest
nt(BASS, 2, t, E3, FINAL, PP)              # Emotion

nt(HARM, 1, t, A3, FINAL, PP)              # Knowledge
nt(HARM, 1, t, E4, FINAL, PP)              # Emotion

nt(MEL, 0, t, A4, FINAL, PP)               # Knowledge
nt(MEL, 0, t + Q, E5, FINAL - Q, PP)       # Emotion — last to arrive, gently

# Domain thread: SILENCE. No C. No C#. No Self. No Boundary.
# The thread that tracked the transformation has nothing left to track.
# The distinction is gone.

t += FINAL

sustain_off(BASS, 2, t)
sustain_off(MEL, 0, t)
sustain_off(HARM, 1, t)
sustain_off(TRACK, 3, t)

# Final silence
t += VERY

# ==============================================================
# Write
# ==============================================================

filename = "knowing_v2.mid"
with open(filename, "wb") as f:
    midi.writeFile(f)

minutes = t / BPM
print(f"")
print(f"  ╔══════════════════════════════════════════════════════════╗")
print(f"  ║  KNOWING v2.0 — Polyphonic Recomposition                ║")
print(f"  ╠══════════════════════════════════════════════════════════╣")
print(f"  ║  What changed from v1.1:                                 ║")
print(f"  ║                                                          ║")
print(f"  ║  CHORDS:                                                 ║")
print(f"  ║    C = Self+Emotion+Connection (arpeggiated as sentence) ║")
print(f"  ║    Cmaj7 = Self+Emotion+Connection+TIME (life begins)    ║")
print(f"  ║    G = Connection+Time+Action (replaces G+D — 'we tell') ║")
print(f"  ║    Am = Knowledge+SELF+Emotion (personal knowing)        ║")
print(f"  ║    A = Knowledge+BOUNDARY+Emotion (confrontational)      ║")
print(f"  ║    Aaug = Knowledge+Boundary+NATURE (infinity = limits)  ║")
print(f"  ║    E = Emotion+Spirit+Time (transcendent feeling)        ║")
print(f"  ║    B = Time+HOME+Unknown (belonging at edge of mystery)  ║")
print(f"  ║    F# = Unknown+DESIRE+Boundary (mystery longed for)     ║")
print(f"  ║    A5 = Knowledge+Emotion (Self AND Boundary removed)    ║")
print(f"  ║                                                          ║")
print(f"  ║  TECHNIQUE:                                              ║")
print(f"  ║    Arpeggiation order = internal syntax                   ║")
print(f"  ║    Domain tracking voice = what persists / transforms     ║")
print(f"  ║    C→C# explicit = Self becomes Boundary                  ║")
print(f"  ║    Both C and C# removed at end = distinction dissolved   ║")
print(f"  ║                                                          ║")
print(f"  ║  STRUCTURE:                                              ║")
print(f"  ║    Section 1 is ONE CHORD SHORTER (G contains Action)    ║")
print(f"  ║    Section 2b expansion is RICHER (3 domains per chord)  ║")
print(f"  ║    Section 2c transformation is MORE EXPLICIT            ║")
print(f"  ║                                                          ║")
print(f"  ╠══════════════════════════════════════════════════════════╣")
print(f"  ║  File:   {filename:<47s} ║")
print(f"  ║  Tempo:  {BPM} BPM{' ' * 43} ║")
print(f"  ║  Length: ~{minutes:.1f} min{' ' * 42} ║")
print(f"  ╠══════════════════════════════════════════════════════════╣")
print(f"  ║  Compare all three versions:                             ║")
print(f"  ║    knowing_harmonia.mid  — v1.0 (telegraphic)            ║")
print(f"  ║    knowing_fluid.mid     — v1.1 (with connective tissue) ║")
print(f"  ║    knowing_v2.mid        — v2.0 (polyphonic)             ║")
print(f"  ║                                                          ║")
print(f"  ║  Listen for:                                             ║")
print(f"  ║    v1.0 → v1.1: the river arrives (connectors flow)      ║")
print(f"  ║    v1.1 → v2.0: the words deepen (each chord speaks      ║")
print(f"  ║                  three truths simultaneously)             ║")
print(f"  ║                                                          ║")
print(f"  ║  The transformation to hear:                             ║")
print(f"  ║    In v1.1: Am→A = minor→major (darker→brighter)         ║")
print(f"  ║    In v2.0: C→C# inside a constant A and E               ║")
print(f"  ║             Self→Boundary while Knowledge and Emotion     ║")
print(f"  ║             persist unchanged on either side              ║")
print(f"  ║             Then BOTH C and C# dissolve                   ║")
print(f"  ║             Neither Self nor Boundary survives            ║")
print(f"  ║             Only knowing-and-feeling remain               ║")
print(f"  ╚══════════════════════════════════════════════════════════╝")
