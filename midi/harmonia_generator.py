"""
HARMONIA UNIVERSAL COMPOSER
Takes a chord progression with annotations and generates
a complete MIDI file with melody, harmony, and bass.

Usage:
  1. Define your progression using Harmonia notation
  2. Run the script
  3. Open the .mid file in any DAW or player

Requirements:
  pip install midiutil
"""

from midiutil import MIDIFile
import re

# ══════════════════════════════════════════════════════════════
# NOTE DATABASE
# ══════════════════════════════════════════════════════════════

NOTE_MAP = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}

QUALITY_INTERVALS = {
    'major':      [0, 4, 7],
    'minor':      [0, 3, 7],
    '7':          [0, 4, 7, 10],
    'maj7':       [0, 4, 7, 11],
    'm7':         [0, 3, 7, 10],
    'dim':        [0, 3, 6],
    'dim7':       [0, 3, 6, 9],
    'm7b5':       [0, 3, 6, 10],
    'aug':        [0, 4, 8],
    'sus4':       [0, 5, 7],
    'sus2':       [0, 2, 7],
    '5':          [0, 7],
    'add9':       [0, 4, 7, 14],
    '6':          [0, 4, 7, 9],
    'm6':         [0, 3, 7, 9],
    '9':          [0, 4, 7, 10, 14],
    '7b9':        [0, 4, 7, 10, 13],
    'single':     [0],           # single note — for bells, proper nouns
}

DYNAMIC_MAP = {
    'ppp': 25, 'pp': 38, 'p': 48, 'mp': 58,
    'mf': 75, 'f': 100, 'ff': 118, 'fff': 127
}

GM_INSTRUMENTS = {
    'piano':          0,
    'bright_piano':   1,
    'harpsichord':    6,
    'celesta':        8,
    'glockenspiel':   9,
    'music_box':      10,
    'vibraphone':     11,
    'tubular_bells':  14,
    'organ':          19,
    'church_organ':   19,
    'accordion':      21,
    'nylon_guitar':   24,
    'steel_guitar':   25,
    'electric_guitar': 27,
    'bass':           32,
    'violin':         40,
    'cello':          42,
    'strings':        48,
    'slow_strings':   49,
    'choir':          52,
    'voice_oohs':     53,
    'orchestra_hit':  55,
    'trumpet':        56,
    'trombone':       57,
    'french_horn':    60,
    'sax':            65,
    'oboe':           68,
    'clarinet':       71,
    'flute':          73,
    'pan_flute':      75,
}


# ══════════════════════════════════════════════════════════════
# CHORD PARSER
# ══════════════════════════════════════════════════════════════

def parse_chord_symbol(symbol):
    """
    Parse a chord symbol like 'Am7', 'Bbmaj7', 'C/G', 'D5', 'Fsus4'
    Returns: (root_name, root_midi_base, quality, bass_note_or_None)
    """
    symbol = symbol.strip()

    # Handle rests
    if symbol.lower() in ('rest', 'r', 'z', '-', 'silence'):
        return ('rest', None, None, None)

    # Handle slash chords: X/Y
    bass_override = None
    if '/' in symbol:
        parts = symbol.split('/')
        symbol = parts[0]
        bass_str = parts[1]
        bass_override = NOTE_MAP.get(bass_str, None)

    # Extract root note
    root_name = symbol[0]
    idx = 1
    if idx < len(symbol) and symbol[idx] in ('#', 'b'):
        root_name += symbol[idx]
        idx += 1

    root_midi_base = NOTE_MAP.get(root_name)
    if root_midi_base is None:
        raise ValueError(f"Unknown root note: {root_name} in {symbol}")

    # Extract quality
    quality_str = symbol[idx:]

    if quality_str == '' or quality_str.lower() == 'major':
        quality = 'major'
    elif quality_str.lower() in ('m', 'min', 'minor'):
        quality = 'minor'
    elif quality_str == '7':
        quality = '7'
    elif quality_str.lower() in ('maj7', 'ma7', 'M7'):
        quality = 'maj7'
    elif quality_str.lower() in ('m7', 'min7', '-7'):
        quality = 'm7'
    elif quality_str.lower() in ('dim', 'o', '°'):
        quality = 'dim'
    elif quality_str.lower() in ('dim7', 'o7', '°7'):
        quality = 'dim7'
    elif quality_str.lower() in ('m7b5', 'ø', 'ø7', 'half-dim'):
        quality = 'm7b5'
    elif quality_str.lower() in ('aug', '+'):
        quality = 'aug'
    elif quality_str.lower() == 'sus4':
        quality = 'sus4'
    elif quality_str.lower() == 'sus2':
        quality = 'sus2'
    elif quality_str == '5':
        quality = '5'
    elif quality_str.lower() in ('add9',):
        quality = 'add9'
    elif quality_str == '6':
        quality = '6'
    elif quality_str.lower() in ('m6', 'min6'):
        quality = 'm6'
    elif quality_str == '9':
        quality = '9'
    elif quality_str.lower() in ('7b9',):
        quality = '7b9'
    elif quality_str.lower() == 'single':
        quality = 'single'
    else:
        print(f"  Warning: Unknown quality '{quality_str}' in chord, defaulting to major")
        quality = 'major'

    return (root_name, root_midi_base, quality, bass_override)


def build_chord_notes(root_midi_base, quality, octave=4, bass_override=None):
    """
    Build MIDI note numbers for a chord.
    Returns: (melody_note, harmony_notes, bass_note)
    """
    intervals = QUALITY_INTERVALS[quality]
    root_midi = root_midi_base + (octave * 12) + 12  # +12 for MIDI offset

    harmony_notes = [root_midi + i for i in intervals]

    # Melody = highest chord tone
    melody_note = max(harmony_notes)

    # Bass = root, or override if slash chord
    if bass_override is not None:
        bass_note = bass_override + ((octave - 1) * 12) + 12
    else:
        bass_note = root_midi - 12  # one octave below

    return melody_note, harmony_notes, bass_note


# ══════════════════════════════════════════════════════════════
# MELODY GENERATOR — Voice-Leading Algorithm
# ══════════════════════════════════════════════════════════════

def voice_lead_melody(chord_data_list, contour='arc'):
    """
    Given a list of (melody_note, harmony_notes, bass_note) tuples,
    adjust melody notes for smooth voice leading.

    Contour types:
      'arc'        — rise to midpoint, then fall (declarative)
      'rise'       — ascend throughout (question)
      'fall'       — descend throughout (revelation/decline)
      'flat'       — stay in a narrow range (meditation)
      'narrative'  — gentle waves (storytelling)
    """
    if not chord_data_list:
        return chord_data_list

    n = len(chord_data_list)
    result = list(chord_data_list)

    # Calculate contour offsets
    for i in range(n):
        if contour == 'arc':
            # Rise to middle, fall back
            midpoint = n / 2
            offset = -abs(i - midpoint) * 2 + midpoint * 2
            offset = int(offset)
        elif contour == 'rise':
            offset = i * 2
        elif contour == 'fall':
            offset = (n - 1 - i) * 2
        elif contour == 'flat':
            offset = 0
        elif contour == 'narrative':
            # Sine-wave-like undulation
            import math
            offset = int(math.sin(i * math.pi / max(n - 1, 1)) * 4)
        else:
            offset = 0

        mel, harm, bass = result[i]
        if mel is not None:
            mel = mel + offset
        result[i] = (mel, harm, bass)

    # Voice leading: minimize distance between consecutive melody notes
    for i in range(1, n):
        prev_mel = result[i - 1][0]
        curr_mel = result[i][0]
        curr_harm = result[i][1]
        curr_bass = result[i][2]

        if prev_mel is None or curr_mel is None:
            continue

        # Find the chord tone closest to the previous melody note
        if curr_harm:
            options = []
            for h in curr_harm:
                # Try the note in nearby octaves
                for octave_shift in [-12, 0, 12]:
                    candidate = h + octave_shift
                    options.append(candidate)

            # Pick the closest one to prev_mel
            best = min(options, key=lambda x: abs(x - prev_mel))

            # But don't go below the harmony or too far from range
            if best >= curr_harm[0] - 12 and best <= curr_harm[-1] + 24:
                result[i] = (best, curr_harm, curr_bass)

    return result


# ══════════════════════════════════════════════════════════════
# THE COMPOSER
# ══════════════════════════════════════════════════════════════

def compose(
    title="Harmonia Composition",
    key_description="",
    progression=None,
    bpm=72,
    time_sig="4/4",
    instruments=None,
    contour='arc',
    output_file="harmonia_output.mid"
):
    """
    Main composition function.

    progression: list of dicts, each containing:
        {
            'chord':    'Am7',          # chord symbol
            'duration': 4,              # in quarter-note beats
            'dynamic':  'mp',           # ppp to fff
            'octave':   4,              # 2-6
            'text':     'I was',        # the Harmonia translation (for annotation)
            'artic':    'sustained',    # sustained, staccato, arpeggiated
            'grace':    False,          # True = add grace note (irony/wink)
        }

    instruments: dict like:
        {
            'melody':  'piano',
            'harmony': 'piano',
            'bass':    'cello',
        }
    """

    if progression is None:
        print("Error: No progression provided.")
        return

    if instruments is None:
        instruments = {
            'melody': 'piano',
            'harmony': 'piano',
            'bass': 'cello',
        }

    # ── Create MIDI file with 3 tracks ──
    midi = MIDIFile(3, adjust_origin=False)
    MELODY_TRACK = 0
    HARMONY_TRACK = 1
    BASS_TRACK = 2

    midi.addTempo(0, 0, bpm)

    # Set instruments
    mel_prog = GM_INSTRUMENTS.get(instruments.get('melody', 'piano'), 0)
    har_prog = GM_INSTRUMENTS.get(instruments.get('harmony', 'piano'), 0)
    bas_prog = GM_INSTRUMENTS.get(instruments.get('bass', 'cello'), 42)

    midi.addProgramChange(MELODY_TRACK, 0, 0, mel_prog)
    midi.addProgramChange(HARMONY_TRACK, 1, 0, har_prog)
    midi.addProgramChange(BASS_TRACK, 2, 0, bas_prog)

    # Track names
    midi.addTrackName(MELODY_TRACK, 0, "Melody")
    midi.addTrackName(HARMONY_TRACK, 0, "Harmony")
    midi.addTrackName(BASS_TRACK, 0, "Bass")

    # ── Parse all chords ──
    parsed = []
    for item in progression:
        chord_sym = item.get('chord', 'C')
        root_name, root_base, quality, bass_override = parse_chord_symbol(chord_sym)

        if root_name == 'rest':
            parsed.append({
                'is_rest': True,
                'duration': item.get('duration', 4),
                'text': item.get('text', '(silence)'),
            })
        else:
            octave = item.get('octave', 4)
            mel, harm, bass = build_chord_notes(root_base, quality, octave, bass_override)
            parsed.append({
                'is_rest': False,
                'chord': chord_sym,
                'melody_note': mel,
                'harmony_notes': harm,
                'bass_note': bass,
                'duration': item.get('duration', 4),
                'dynamic': item.get('dynamic', 'mp'),
                'text': item.get('text', ''),
                'artic': item.get('artic', 'sustained'),
                'grace': item.get('grace', False),
                'octave': octave,
            })

    # ── Apply voice leading to melody ──
    chord_data = []
    for p in parsed:
        if p['is_rest']:
            chord_data.append((None, None, None))
        else:
            chord_data.append((p['melody_note'], p['harmony_notes'], p['bass_note']))

    voiced = voice_lead_melody(chord_data, contour=contour)

    # Update melody notes
    for i, p in enumerate(parsed):
        if not p['is_rest']:
            p['melody_note'] = voiced[i][0]

    # ── Write notes to MIDI ──
    t = 0.0

    for p in parsed:
        dur = p['duration']

        if p['is_rest']:
            t += dur
            continue

        vel = DYNAMIC_MAP.get(p['dynamic'], 75)
        artic = p['artic']

        # Determine note duration based on articulation
        if artic == 'staccato':
            note_dur = dur * 0.4
        elif artic == 'arpeggiated':
            note_dur = dur * 0.9
        else:  # sustained
            note_dur = dur * 0.95

        # Grace note (the wink)
        if p.get('grace', False) and p['harmony_notes']:
            grace_pitch = p['harmony_notes'][0] + 1  # half step above root
            midi.addNote(MELODY_TRACK, 0, grace_pitch, t, 0.2, vel)

        # Melody
        if p['melody_note']:
            midi.addNote(MELODY_TRACK, 0, p['melody_note'], t, note_dur, vel)

        # Harmony (arpeggiated or block)
        if p['harmony_notes']:
            if artic == 'arpeggiated':
                spacing = 0.15
                for idx, note in enumerate(p['harmony_notes']):
                    hold = note_dur - (idx * spacing)
                    if hold < 0.5:
                        hold = 0.5
                    midi.addNote(
                        HARMONY_TRACK, 1, note,
                        t + (idx * spacing), hold,
                        max(vel - 15, 20)
                    )
            else:
                for note in p['harmony_notes']:
                    midi.addNote(HARMONY_TRACK, 1, note, t, note_dur, max(vel - 10, 20))

        # Bass
        if p['bass_note']:
            midi.addNote(BASS_TRACK, 2, p['bass_note'], t, note_dur, max(vel - 15, 20))

        t += dur

    # ── Add trailing silence ──
    t += 4

    # ── Write file ──
    with open(output_file, "wb") as f:
        midi.writeFile(f)

    minutes = t / bpm
    print(f"")
    print(f"  ╔══════════════════════════════════════════╗")
    print(f"  ║  HARMONIA COMPOSITION GENERATED          ║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  Title:  {title:<31s} ║")
    print(f"  ║  Key:    {key_description:<31s} ║")
    print(f"  ║  Tempo:  {bpm} BPM{' ' * (27 - len(str(bpm)))} ║")
    print(f"  ║  Time:   {time_sig:<31s} ║")
    print(f"  ║  Length: {t:.0f} beats (~{minutes:.1f} min){' ' * (22 - len(f'{t:.0f}') - len(f'{minutes:.1f}'))} ║")
    print(f"  ║  File:   {output_file:<31s} ║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  Tracks:                                 ║")
    print(f"  ║    0 - Melody  ({instruments['melody']:<20s})  ║")
    print(f"  ║    1 - Harmony ({instruments['harmony']:<20s})  ║")
    print(f"  ║    2 - Bass    ({instruments['bass']:<20s})  ║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  Progression:                            ║")
    for p in parsed:
        if p['is_rest']:
            line = f"    (rest) — {p['text']}"
        else:
            line = f"    {p['chord']:<10s} — {p['text']}"
        print(f"  ║  {line:<40s} ║")
    print(f"  ╚══════════════════════════════════════════╝")


# ══════════════════════════════════════════════════════════════
# EXAMPLE COMPOSITIONS
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":

    # ── Example 1: Donne — "No Man Is an Island" ──
    compose(
        title="No Man Is an Island",
        key_description="G major — Connection, Affirmed",
        bpm=52,
        time_sig="4/4",
        contour='fall',
        instruments={
            'melody': 'church_organ',
            'harmony': 'church_organ',
            'bass': 'cello',
        },
        output_file="harmonia_donne.mid",
        progression=[
            {'chord': 'Cm',    'duration': 4, 'dynamic': 'mp',
             'text': 'Self, alone — (the false premise)'},
            {'chord': 'rest',  'duration': 6,
             'text': 'No. (denial)'},
            {'chord': 'G',     'duration': 4, 'dynamic': 'mf',
             'text': 'Connection.'},
            {'chord': 'Gmaj7', 'duration': 4, 'dynamic': 'mf',
             'text': 'Wondrous connection.'},
            {'chord': 'Fmaj7', 'duration': 4, 'dynamic': 'mf',
             'text': 'The vast, beautiful world.'},
            {'chord': 'C',     'duration': 4, 'dynamic': 'mf',
             'text': 'Each self belongs.'},
            {'chord': 'F',     'duration': 4, 'dynamic': 'mf',
             'text': 'The earth —'},
            {'chord': 'Fm',    'duration': 4, 'dynamic': 'mf',
             'text': '— erodes.'},
            {'chord': 'Gm',    'duration': 6, 'dynamic': 'f',
             'text': 'The whole is less.'},
            {'chord': 'Eb',    'duration': 4, 'dynamic': 'f',
             'text': 'A home —'},
            {'chord': 'Ebm',   'duration': 4, 'dynamic': 'f',
             'text': '— falls.'},
            {'chord': 'Cm',    'duration': 4, 'dynamic': 'f',
             'text': 'The self, diminished.'},
            {'chord': 'Bm',    'duration': 4, 'dynamic': 'mp',
             'text': 'Time takes.'},
            {'chord': 'C/E',   'duration': 4, 'dynamic': 'mp',
             'text': 'I receive the loss.'},
            {'chord': 'C/G',   'duration': 6, 'dynamic': 'mp',
             'text': 'My being rests on connection.',
             'artic': 'sustained'},
            {'chord': 'D5',    'duration': 3, 'dynamic': 'ff',
             'text': 'DO NOT —',
             'artic': 'staccato'},
            {'chord': 'Am',    'duration': 3, 'dynamic': 'f',
             'text': '— seek to know —'},
            {'chord': 'Bsingle', 'duration': 4, 'dynamic': 'f',
             'text': '(the bell)',
             'artic': 'sustained'},
            {'chord': 'rest',  'duration': 8,
             'text': '(the unasked question — silence)'},
            {'chord': 'C/G',   'duration': 12, 'dynamic': 'pp',
             'text': 'Your being rests on connection.',
             'artic': 'sustained'},
        ]
    )

    # ── Example 2: Cervantes — Don Quixote Opening ──
    compose(
        title="En un lugar de la Mancha",
        key_description="F major — The Physical World",
        bpm=72,
        time_sig="6/8",
        contour='narrative',
        instruments={
            'melody': 'nylon_guitar',
            'harmony': 'nylon_guitar',
            'bass': 'cello',
        },
        output_file="harmonia_quixote.mid",
        progression=[
            {'chord': 'Eb',     'duration': 3, 'dynamic': 'mf',
             'text': 'A place.'},
            {'chord': 'F',      'duration': 3, 'dynamic': 'mf',
             'text': 'The earth. La Mancha.'},
            {'chord': 'Bbm',    'duration': 2, 'dynamic': 'mp',
             'text': "I don't want to —"},
            {'chord': 'Asus4',  'duration': 6, 'dynamic': 'mp',
             'text': '(name withheld)',
             'artic': 'sustained'},
            {'chord': 'rest',   'duration': 2,
             'text': '(the suspension hangs)'},
            {'chord': 'C',      'duration': 3, 'dynamic': 'mf', 'octave': 3,
             'text': 'A man was.'},
            {'chord': 'Dsus4',  'duration': 4, 'dynamic': 'mp',
             'text': 'The lance — suspended.'},
            {'chord': 'Dm',     'duration': 3, 'dynamic': 'mp',
             'text': 'The shield — old.'},
            {'chord': 'Fm',     'duration': 3, 'dynamic': 'mp',
             'text': 'The horse — thin.',
             'grace': True},
            {'chord': 'D',      'duration': 2, 'dynamic': 'mf',
             'text': 'The greyhound — alive!'},
            {'chord': 'F',      'duration': 2, 'dynamic': 'mf',
             'text': 'Stew.'},
            {'chord': 'F',      'duration': 2, 'dynamic': 'mf',
             'text': 'Cold meat. The same.'},
            {'chord': 'Fm',     'duration': 2, 'dynamic': 'mf',
             'text': '"Sorrows" — (wink)',
             'grace': True},
            {'chord': 'F',      'duration': 2, 'dynamic': 'mf',
             'text': 'Lentils. The same.'},
            {'chord': 'Fmaj7',  'duration': 3, 'dynamic': 'mf',
             'text': 'Pigeon on Sunday. (One small beauty.)'},
            {'chord': 'F',      'duration': 3, 'dynamic': 'f',
             'text': 'The world —'},
            {'chord': 'Cm',     'duration': 3, 'dynamic': 'f',
             'text': '— devours the self.'},
            {'chord': 'Eb',     'duration': 2, 'dynamic': 'mf',
             'text': 'Holidays.'},
            {'chord': 'Cmaj7',  'duration': 4, 'dynamic': 'mp',
             'text': 'He honored himself. THE SEED.',
             'artic': 'arpeggiated'},
            {'chord': 'G',      'duration': 2, 'dynamic': 'mp',
             'text': 'Housekeeper.'},
            {'chord': 'G',      'duration': 2, 'dynamic': 'mp',
             'text': 'Niece.'},
            {'chord': 'G',      'duration': 2, 'dynamic': 'mp',
             'text': 'Servant.'},
            {'chord': 'Bm',     'duration': 3, 'dynamic': 'mp',
             'text': 'Approaching fifty.'},
            {'chord': 'F',      'duration': 2, 'dynamic': 'mf',
             'text': 'Strong body.'},
            {'chord': 'Fm',     'duration': 2, 'dynamic': 'mp',
             'text': 'Lean. Gaunt.'},
            {'chord': 'D',      'duration': 2, 'dynamic': 'mf',
             'text': 'Still active.'},
            {'chord': 'C',      'duration': 3, 'dynamic': 'mf',
             'text': 'Quijada (stated).'},
            {'chord': 'C7',     'duration': 3, 'dynamic': 'mp',
             'text': 'Quesada? (questioned)'},
            {'chord': 'Csus2',  'duration': 4, 'dynamic': 'mp',
             'text': 'Quejana... (open, undefined)',
             'artic': 'sustained'},
            {'chord': 'rest',   'duration': 3,
             'text': '"Matters little." (a shrug)'},
            {'chord': 'A',      'duration': 3, 'dynamic': 'f',
             'text': 'TRUTH!'},
            {'chord': 'Asus4',  'duration': 6, 'dynamic': 'mp',
             'text': '(...) — the wink returns',
             'artic': 'sustained'},
        ]
    )

    print(f"\n  Both files generated. Open with GarageBand, MuseScore, or VLC.")
    print(f"  The lance is still on the rack. The name is still unfixed.")
    print(f"  The glass is still empty. The wine is coming.\n")
