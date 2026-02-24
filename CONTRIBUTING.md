```markdown
# Contributing to Harmonia

## How to Add a Translation

### Music → Words (Analyzing a piece)

1. **State the key.** What is the primary key of the piece? 
   What does that mean in Harmonia?
2. **Map the chord progression.** List every chord, in order.
3. **Translate each chord** using the [root dictionary](reference/root-dictionary.md).
4. **Note the dynamics, meter, register, and instrumentation.**
5. **Read the connectors** — what do the bass movements, melodic 
   intervals, and common tones say?
6. **Assemble the translation.** Write it as a poem or prose passage.
7. **Be honest about what's interpretation vs. what's structural.**

### Words → Music (Composing from a text)

1. **Identify the domain.** What is the text about? → Choose a key.
2. **Map key concepts to roots.** What are the main ideas? 
   Which roots correspond?
3. **Choose chord qualities.** Is each concept affirmed, denied, 
   questioned, wondrous, dangerous?
4. **Set dynamics and meter.** How is this text spoken? 
   To whom? With what urgency?
5. **Apply melodic templates.** Use the connective tissue system 
   (v1.1) to make it flow.
6. **Generate a MIDI file** using the universal composer or 
   a custom script.

### What Makes a Good Contribution

- **Transparency.** Say what you chose and why. Say where you 
  were uncertain.
- **Honesty.** If a chord doesn't quite fit, say so. If you forced 
  a reading, admit it.
- **Musical sensitivity.** Listen to the piece many times before 
  translating. The analysis should honor the music.
- **A different perspective.** The existing translations are Western 
  classical, blues, jazz, film, and Spanish literature. Translations 
  of Indian classical music, Chinese opera, electronic music, hip-hop, 
  or non-Western poetry would be especially valuable.

## How to Propose Alternative Root Mappings

The current mapping (C=Self, G=Connection, etc.) is acknowledged 
as a creative choice. If you believe a different mapping produces 
better or more consistent results:

1. State your alternative mapping clearly.
2. Translate at least TWO existing pieces using your mapping.
3. Compare the results with the existing translations.
4. Explain where your mapping is stronger and where it is weaker.

Submit as a pull request with a new folder: 
`alternative-mappings/your-mapping-name/`

## Disagreements and Debates

Use GitHub Issues or Discussions. Tag with:
- `[theory]` — debates about the framework itself
- `[translation]` — discussions about specific chord readings
- `[code]` — bugs or improvements to the MIDI scripts
- `[critique]` — challenges to the system (these are welcome)
