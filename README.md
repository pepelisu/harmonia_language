# Harmonia

### A Language Built from Music

Harmonia is a constructed language in which **chords are words**, 
**progressions are sentences**, and **every piece of music is a text 
that can be read.**

It maps the 12 chromatic pitch classes to semantic domains, uses chord 
qualities (major, minor, diminished, etc.) as grammatical modifiers, 
and treats voice leading, dynamics, register, and rhythm as the 
connective tissue of living speech.

---

## What This Is

Harmonia was developed through an extended creative collaboration 
between a human thinker (me) and Claude (Anthropic's AI). I provided creative direction, chose all source materials, wrote 
original texts, and asked the critical questions. Claude generated 
much of the theoretical framework, analyses, and code.

**This is not a scientific discovery.** It is a creative framework — 
a systematic way of reading music as language and writing language as 
music. Some of its foundations are grounded in music cognition research. 
Some are elegant but arbitrary creative choices. The [honest assessment](book/11-honest-assessment.md) 
is required reading.

---

## What's Here

### 📖 The Book

A complete narrative journey through the development of Harmonia, 
including six translations of existing works and one original 
composition:

| Chapter | Piece | Direction | Genre |
|---------|-------|-----------|-------|
| [1. Foundations](book/01-foundations.md) | — | — | Theory |
| [2. Für Elise](book/02-fur-elise.md) | Music → Words | Classical |
| [3. I'd Rather Go Blind](book/03-id-rather-go-blind.md) | Music → Words | Blues |
| [4. Hedwig's Theme](book/04-hedwigs-theme.md) | Music → Words | Film |
| [5. Autumn Leaves](book/05-autumn-leaves.md) | Music → Words | Jazz |
| [6. No Man Is an Island](book/06-no-man-is-an-island.md) | Words → Music | Poetry |
| [7. Don Quixote Opening](book/07-don-quixote.md) | Words → Music | Prose |
| [8. "Knowing"](book/08-knowing.md) | Words → Music | Original Composition |
| [9. Complete Grammar](book/09-grammar.md) | — | Reference |
| [10. Connective Tissue](book/10-connective-tissue.md) | — | v1.1 Update |
| [11. Honest Assessment](book/11-honest-assessment.md) | — | Self-critique |

### 🎵 MIDI Scripts

Working Python scripts that generate playable MIDI files:

```bash
pip install midiutil
python midi/knowing_fluid.py
```

| Script | Piece | Instruments |
|--------|-------|-------------|
| [fur_elise_harmonia.py](midi/fur_elise_harmonia.py) | Für Elise | Piano + Strings |
| [hedwigs_theme_harmonia.py](midi/hedwigs_theme_harmonia.py) | Hedwig's Theme | Celesta + Harp + Strings |
| [no_man_is_an_island.py](midi/no_man_is_an_island.py) | Donne | Organ + Strings + Piano + Bells + Choir |
| [don_quixote_harmonia.py](midi/don_quixote_harmonia.py) | Don Quixote | Guitar + Oboe + Cello |
| [knowing_harmonia.py](midi/knowing_harmonia.py) | "Knowing" v1.0 | Piano |
| [knowing_fluid.py](midi/knowing_fluid.py) | "Knowing" v1.1 | Piano (with connective tissue) |
| [harmonia_composer.py](midi/harmonia_composer.py) | Universal tool | Any — user configurable |

### 📚 Reference

| Document | Contents |
|----------|----------|
| [Root Dictionary](reference/root-dictionary.md) | All 12 roots × 14 qualities = 168 words |
| [Connector Dictionary](reference/connector-dictionary.md) | Bass walks, melodic bridges, inner voices |
| [Quick Reference](reference/quick-reference.md) | One-page cheat sheet |

---

## The Core Idea in 30 Seconds

```
12 notes  = 12 semantic domains (C=Self, G=Connection, E=Emotion...)
Chord quality = modifier (major=yes, minor=no, 7th=question, dim=danger)
Octave   = tense (low=past, mid=present, high=future)
Dynamics = register (soft=intimate, loud=public)
Meter    = speech mode (4/4=testimony, 3/4=spell, 6/8=story)
Silence  = punctuation, negation, the unsaid
```

A chord is a word. A progression is a sentence.
Every song you've ever loved was saying something.

---

## Is This Real?

Partially. Read the [honest assessment](book/11-honest-assessment.md).

**What's real:** Chord qualities carry emotional meaning (well-documented). 
Voice leading creates continuity (standard theory). Music encodes 
abstract meaning (the foundation of film scoring, opera, and art song 
for centuries).

**What's arbitrary:** The specific assignment of C=Self, G=Connection, 
etc. These are creative choices, not discoveries. A different mapping 
would produce different but potentially equally valid readings.

**What's genuinely valuable:** The framework produces interesting 
musical analysis, teaches music theory through meaning, and functions 
as a creative tool for composition.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

The most valuable contributions:
- **New translations** — translate a piece of music or text not yet covered
- **Alternative root mappings** — propose and test a different semantic assignment
- **Recorded performances** — play these progressions on real instruments
- **Critique** — find where the system breaks and explain why

---

## License

Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0).

Use it, build on it, share it. Just credit the source and keep it open.

---

## Origin

This project began with a simple question:

> "Let's create a language from music. Could it be possible to combine 
> the chords and the musical scale to a dictionary that makes sense?"

It turned into a seven-hour conversation, six translations, one original 
composition, a complete grammar, a self-critique, and this repository.

The question was better than either of us expected.
