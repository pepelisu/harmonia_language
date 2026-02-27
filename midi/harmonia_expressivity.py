"""
HARMONIA EXPRESSIVITY ENGINE — v2.1
Functions for adding expressive tone to any chord.

These functions modify HOW a chord sounds without changing
WHAT it says. They are the "tone of voice" of Harmonia.

Usage:
  from expressivity import expressive_chord
  
  expressive_chord(midi, track, channel, time,
      notes=[C4, E4, G4],
      duration=4.0,
      velocity=65,
      shape='rise',
      touch='legato',
      breath='rubato_pull',
      ornament={'note': E4, 'type': 'vibrato'},
      space='sustained'
  )
"""

import math
import random


def expressive_chord(
    midi, track, channel, time, notes, duration, velocity,
    shape='block',
    touch='legato',
    breath='steady',
    ornament=None,
    space='half_pedal',
    seed=None
):
    """
    Play a chord with expressive modifications.
    
    Parameters:
        midi:      MIDIFile object
        track:     track number
        channel:   MIDI channel
        time:      start time in beats
        notes:     list of MIDI note numbers
        duration:  total duration in beats
        velocity:  base velocity (0-127)
        shape:     how the chord unfolds (see SHAPES)
        touch:     how notes are attacked/released (see TOUCHES)
        breath:    temporal modification (see BREATHS)
        ornament:  dict with 'note' and 'type' keys, or list of dicts
        space:     acoustic environment (see SPACES)
        seed:      random seed for scatter/humanize
    """
    if seed is not None:
        random.seed(seed)
    
    # ── BREATH: modify timing ──────────────────────
    time_offset = 0.0
    duration_mod = 1.0
    
    if breath == 'rubato_pull':
        # Time stretches — play slightly late, hold slightly longer
        time_offset = 0.08
        duration_mod = 1.12
    elif breath == 'rubato_push':
        # Time compresses — play slightly early, hold slightly shorter
        time_offset = -0.06
        duration_mod = 0.9
    elif breath == 'fermata':
        # Time stops — hold much longer
        duration_mod = 1.8
    elif breath == 'hesitant':
        # Tiny pause before — delayed start
        time_offset = 0.15
    elif breath == 'agogic':
        # First note held slightly longer than others
        # Handled in shape section
        pass
    elif breath == 'sighing':
        # Two-note gesture handled in shape
        duration_mod = 0.85
    
    actual_time = time + time_offset
    actual_duration = duration * duration_mod
    
    # ── TOUCH: modify velocity and note duration ───
    vel_curve = []   # velocity for each note
    dur_curve = []   # duration multiplier for each note
    
    if touch == 'legato':
        vel_curve = [velocity] * len(notes)
        dur_curve = [1.0] * len(notes)  # full duration, overlapping
    elif touch == 'portato':
        vel_curve = [velocity] * len(notes)
        dur_curve = [0.85] * len(notes)  # slightly separated
    elif touch == 'staccato':
        vel_curve = [velocity + 5] * len(notes)  # slightly louder attack
        dur_curve = [0.35] * len(notes)  # short
    elif touch == 'tenuto':
        vel_curve = [velocity + 3] * len(notes)
        dur_curve = [1.0] * len(notes)  # absolutely full value
    elif touch == 'sforzando':
        vel_curve = [velocity + 30] + [velocity - 15] * (len(notes) - 1)
        dur_curve = [0.7] + [0.9] * (len(notes) - 1)
    elif touch == 'peso':
        vel_curve = [velocity + 10] * len(notes)
        dur_curve = [1.0] * len(notes)
    elif touch == 'leggiero':
        vel_curve = [max(velocity - 15, 20)] * len(notes)
        dur_curve = [0.6] * len(notes)
    elif touch == 'morendo':
        # Each successive note softer
        for i in range(len(notes)):
            fade = int(velocity * (1.0 - (i * 0.2)))
            vel_curve.append(max(fade, 15))
            dur_curve.append(1.0 - (i * 0.1))
    elif touch == 'bell':
        vel_curve = [velocity + 15] * len(notes)
        dur_curve = [1.3] * len(notes)  # ring beyond expected
    elif touch == 'crescendo':
        for i in range(len(notes)):
            grow = int(velocity * (0.6 + (i * 0.2)))
            vel_curve.append(min(grow, 127))
            dur_curve.append(1.0)
    else:
        vel_curve = [velocity] * len(notes)
        dur_curve = [1.0] * len(notes)
    
    # ── SPACE: modify pedaling and register ────────
    sustain = False
    
    if space == 'dry':
        sustain = False
    elif space == 'sustained':
        sustain = True
        midi.addControllerEvent(track, channel, actual_time, 64, 127)
    elif space == 'half_pedal':
        sustain = True
        midi.addControllerEvent(track, channel, actual_time, 64, 80)
    elif space == 'open':
        sustain = True
        midi.addControllerEvent(track, channel, actual_time, 64, 100)
        # Spread voicing — handled by caller providing wide-spaced notes
    elif space == 'close':
        sustain = False
        # Tight voicing — handled by caller providing close-spaced notes
    elif space == 'echoed':
        sustain = True
        midi.addControllerEvent(track, channel, actual_time, 64, 90)
        # Add echo notes — softer, delayed, octave displaced
        for n in notes:
            echo_note = n + 12 if n + 12 < 108 else n - 12
            echo_time = actual_time + actual_duration * 0.6
            echo_vel = max(vel_curve[0] - 30, 15)
            echo_dur = actual_duration * 0.5
            midi.addNote(track, channel, echo_note, echo_time, echo_dur, echo_vel)
    elif space == 'sparse':
        sustain = False
        # Extra silence after — handled by duration reduction
        dur_curve = [d * 0.6 for d in dur_curve]
    elif space == 'dense':
        sustain = True
        midi.addControllerEvent(track, channel, actual_time, 64, 127)
        # Add octave doublings
        for n in notes:
            if n - 12 >= 21:  # don't go below piano range
                midi.addNote(track, channel, n - 12,
                           actual_time, actual_duration * 0.8,
                           max(velocity - 20, 15))
    
    # ── SHAPE: determine note placement ────────────
    
    if shape == 'block':
        # All notes at once
        for i, n in enumerate(notes):
            midi.addNote(track, channel, n, actual_time,
                        actual_duration * dur_curve[i], vel_curve[i])
    
    elif shape == 'rise':
        # Notes arpeggiated upward, slow
        sorted_notes = sorted(notes)
        spacing = min(actual_duration * 0.15, 0.4)
        for i, n in enumerate(sorted_notes):
            note_time = actual_time + (i * spacing)
            remaining = actual_duration - (i * spacing)
            note_dur = max(remaining * dur_curve[min(i, len(dur_curve)-1)], 0.3)
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            if breath == 'agogic' and i == 0:
                note_dur *= 1.15  # first note held slightly longer
            midi.addNote(track, channel, n, note_time, note_dur, note_vel)
    
    elif shape == 'fall':
        # Notes arpeggiated downward, slow
        sorted_notes = sorted(notes, reverse=True)
        spacing = min(actual_duration * 0.15, 0.4)
        for i, n in enumerate(sorted_notes):
            note_time = actual_time + (i * spacing)
            remaining = actual_duration - (i * spacing)
            note_dur = max(remaining * dur_curve[min(i, len(dur_curve)-1)], 0.3)
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time, note_dur, note_vel)
    
    elif shape == 'bloom':
        # Center note first, then outer notes spread
        sorted_notes = sorted(notes)
        mid_idx = len(sorted_notes) // 2
        center = sorted_notes[mid_idx]
        spacing = min(actual_duration * 0.12, 0.3)
        
        # Center first
        midi.addNote(track, channel, center, actual_time,
                    actual_duration * dur_curve[0], vel_curve[0])
        
        # Then outward
        step = 1
        for i in range(len(sorted_notes)):
            if i == mid_idx:
                continue
            note_time = actual_time + (step * spacing)
            remaining = actual_duration - (step * spacing)
            note_dur = max(remaining * dur_curve[min(step, len(dur_curve)-1)], 0.3)
            note_vel = vel_curve[min(step, len(vel_curve)-1)]
            midi.addNote(track, channel, sorted_notes[i],
                        note_time, note_dur, note_vel)
            step += 1
    
    elif shape == 'gather':
        # Outer notes first, converging to center
        sorted_notes = sorted(notes)
        mid_idx = len(sorted_notes) // 2
        # Build order: outermost first, then inward
        order = []
        left = 0
        right = len(sorted_notes) - 1
        while left <= right:
            if left == right:
                order.append(sorted_notes[left])
            else:
                order.append(sorted_notes[right])
                order.append(sorted_notes[left])
            left += 1
            right -= 1
        
        spacing = min(actual_duration * 0.12, 0.3)
        for i, n in enumerate(order):
            note_time = actual_time + (i * spacing)
            remaining = actual_duration - (i * spacing)
            note_dur = max(remaining * dur_curve[min(i, len(dur_curve)-1)], 0.3)
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time, note_dur, note_vel)
    
    elif shape == 'wave':
        # Up then down
        sorted_notes = sorted(notes)
        wave_notes = sorted_notes + sorted_notes[-2:0:-1]  # up then down
        total_steps = len(wave_notes)
        spacing = actual_duration / (total_steps + 1)
        for i, n in enumerate(wave_notes):
            note_time = actual_time + (i * spacing)
            note_dur = spacing * 1.5 * dur_curve[min(i, len(dur_curve)-1)]
            note_vel = vel_curve[min(i % len(vel_curve), len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time,
                        max(note_dur, 0.2), note_vel)
    
    elif shape == 'pulse':
        # Repeated rhythmic pattern
        pulse_dur = min(actual_duration / 4, 0.5)
        repetitions = int(actual_duration / pulse_dur)
        for rep in range(repetitions):
            rep_time = actual_time + (rep * pulse_dur)
            for i, n in enumerate(notes):
                note_dur = pulse_dur * 0.8 * dur_curve[min(i, len(dur_curve)-1)]
                # Slight velocity variation — human feel
                v = vel_curve[min(i, len(vel_curve)-1)]
                v += random.randint(-5, 5)
                v = max(min(v, 127), 15)
                midi.addNote(track, channel, n, rep_time,
                            max(note_dur, 0.1), v)
    
    elif shape == 'scatter':
        # Notes placed irregularly
        for i, n in enumerate(notes):
            scatter_offset = random.uniform(0, actual_duration * 0.4)
            note_time = actual_time + scatter_offset
            note_dur = random.uniform(actual_duration * 0.3, actual_duration * 0.8)
            note_dur *= dur_curve[min(i, len(dur_curve)-1)]
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            note_vel += random.randint(-10, 10)
            note_vel = max(min(note_vel, 127), 15)
            midi.addNote(track, channel, n, note_time,
                        max(note_dur, 0.2), note_vel)
    
    elif shape == 'cascade':
        # Rapid waterfall downward
        sorted_notes = sorted(notes, reverse=True)
        spacing = 0.08  # very fast
        for i, n in enumerate(sorted_notes):
            note_time = actual_time + (i * spacing)
            note_dur = actual_duration * dur_curve[min(i, len(dur_curve)-1)]
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time,
                        max(note_dur, 0.3), note_vel)
    
    elif shape == 'climb':
        # Rapid upward run
        sorted_notes = sorted(notes)
        spacing = 0.08
        for i, n in enumerate(sorted_notes):
            note_time = actual_time + (i * spacing)
            note_dur = actual_duration * dur_curve[min(i, len(dur_curve)-1)]
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time,
                        max(note_dur, 0.3), note_vel)
    
    elif shape == 'pendulum':
        # Two outer notes alternating
        if len(notes) >= 2:
            sorted_notes = sorted(notes)
            low = sorted_notes[0]
            high = sorted_notes[-1]
            swing_dur = actual_duration / 6
            for i in range(6):
                n = low if i % 2 == 0 else high
                note_time = actual_time + (i * swing_dur)
                note_dur = swing_dur * 1.2 * dur_curve[0]
                note_vel = vel_curve[0] + ((-1)**i * 5)
                note_vel = max(min(note_vel, 127), 15)
                midi.addNote(track, channel, n, note_time,
                            max(note_dur, 0.15), note_vel)
            # Middle notes sustained throughout
            for n in sorted_notes[1:-1]:
                midi.addNote(track, channel, n, actual_time,
                            actual_duration, velocity - 10)
    
    elif shape == 'dissolve':
        # All notes start together, then fade one by one
        sorted_notes = sorted(notes, reverse=True)
        for i, n in enumerate(sorted_notes):
            note_dur = actual_duration * (1.0 - (i * 0.25))
            note_dur = max(note_dur, actual_duration * 0.3)
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            # Each subsequent note slightly softer
            note_vel = max(note_vel - (i * 8), 15)
            midi.addNote(track, channel, n, actual_time,
                        note_dur * dur_curve[min(i, len(dur_curve)-1)],
                        note_vel)
    
    elif shape == 'grow':
        # Notes entering one by one, each sustaining
        sorted_notes = sorted(notes)
        spacing = actual_duration / (len(sorted_notes) + 1)
        for i, n in enumerate(sorted_notes):
            note_time = actual_time + (i * spacing)
            remaining = actual_duration - (i * spacing)
            note_dur = remaining * dur_curve[min(i, len(dur_curve)-1)]
            note_vel = vel_curve[min(i, len(vel_curve)-1)]
            midi.addNote(track, channel, n, note_time,
                        max(note_dur, 0.3), note_vel)
    
    # ── ORNAMENT: add decorations ──────────────────
    
    if ornament is not None:
        if isinstance(ornament, dict):
            ornament = [ornament]
        
        for orn in ornament:
            orn_note = orn.get('note')
            orn_type = orn.get('type', 'grace_below')
            
            if orn_note is None:
                continue
            
            if orn_type == 'mordent':
                # Main-lower-main (quick bite)
                lower = orn_note - 1  # half step below
                midi.addNote(track, channel, orn_note, actual_time, 0.1, velocity)
                midi.addNote(track, channel, lower, actual_time + 0.1, 0.1, velocity - 10)
                midi.addNote(track, channel, orn_note, actual_time + 0.2, 0.3, velocity)
            
            elif orn_type == 'inverted_mordent':
                # Main-upper-main (quick flick up)
                upper = orn_note + 1 if orn_note + 1 <= 108 else orn_note
                midi.addNote(track, channel, orn_note, actual_time, 0.1, velocity)
                midi.addNote(track, channel, upper, actual_time + 0.1, 0.1, velocity - 10)
                midi.addNote(track, channel, orn_note, actual_time + 0.2, 0.3, velocity)
            
            elif orn_type == 'turn':
                # Upper-main-lower-main
                upper = orn_note + 2
                lower = orn_note - 1
                t_dur = 0.12
                midi.addNote(track, channel, upper, actual_time, t_dur, velocity - 5)
                midi.addNote(track, channel, orn_note, actual_time + t_dur, t_dur, velocity)
                midi.addNote(track, channel, lower, actual_time + t_dur*2, t_dur, velocity - 5)
                midi.addNote(track, channel, orn_note, actual_time + t_dur*3, t_dur*2, velocity)
            
            elif orn_type == 'trill':
                # Rapid alternation
                upper = orn_note + 2  # whole step trill
                trill_dur = min(actual_duration * 0.5, 2.0)
                t_step = 0.08
                t_count = int(trill_dur / t_step)
                for ti in range(t_count):
                    n = orn_note if ti % 2 == 0 else upper
                    t_time = actual_time + (ti * t_step)
                    t_vel = velocity - 5 + random.randint(-3, 3)
                    t_vel = max(min(t_vel, 127), 15)
                    midi.addNote(track, channel, n, t_time,
                                t_step * 1.2, t_vel)
            
            elif orn_type == 'grace_below':
                # Quick note from half step below
                grace = orn_note - 1
                midi.addNote(track, channel, grace, actual_time - 0.12,
                            0.12, velocity - 10)
            
            elif orn_type == 'grace_above':
                # Quick note from half step above
                grace = orn_note + 1
                midi.addNote(track, channel, grace, actual_time - 0.12,
                            0.12, velocity - 10)
            
            elif orn_type == 'acciaccatura':
                # Crushed note — almost simultaneous
                crush = orn_note - 1
                midi.addNote(track, channel, crush, actual_time - 0.05,
                            0.06, velocity - 5)
            
            elif orn_type == 'vibrato':
                # Simulated through pitch bend (simplified: 
                # rapid soft repetitions at slightly varying velocity)
                vib_dur = min(actual_duration * 0.6, 3.0)
                vib_start = actual_time + actual_duration * 0.2
                vib_step = 0.15
                vib_count = int(vib_dur / vib_step)
                for vi in range(vib_count):
                    v_variation = int(5 * math.sin(vi * 1.5))
                    v_time = vib_start + (vi * vib_step)
                    v_vel = max(min(velocity - 15 + v_variation, 127), 10)
                    midi.addNote(track, channel, orn_note, v_time,
                                vib_step * 0.8, v_vel)
            
            elif orn_type == 'harmonic':
                # Play the note an octave higher, very soft
                harm_note = orn_note + 12 if orn_note + 12 <= 108 else orn_note
                midi.addNote(track, channel, harm_note,
                            actual_time + actual_duration * 0.3,
                            actual_duration * 0.5,
                            max(velocity - 35, 10))
            
            elif orn_type == 'slide':
                # Chromatic approach from a third below
                slide_start = orn_note - 4
                slide_steps = 4
                s_dur = 0.1
                for si in range(slide_steps):
                    s_note = slide_start + si
                    s_time = actual_time - (slide_steps - si) * s_dur
                    if s_time < 0:
                        s_time = 0
                    s_vel = max(velocity - 25 + (si * 5), 10)
                    midi.addNote(track, channel, s_note, s_time,
                                s_dur * 1.2, s_vel)
            
            elif orn_type == 'tremolo':
                # Rapid soft repetitions
                trem_dur = min(actual_duration * 0.6, 2.0)
                trem_step = 0.06
                trem_count = int(trem_dur / trem_step)
                for tri in range(trem_count):
                    t_time = actual_time + (tri * trem_step)
                    t_vel = velocity - 10 + random.randint(-8, 8)
                    t_vel = max(min(t_vel, 127), 10)
                    midi.addNote(track, channel, orn_note, t_time,
                                trem_step * 0.9, t_vel)
    
    # ── SPACE: release pedal at end if needed ──────
    if sustain:
        release_time = actual_time + actual_duration
        if space == 'sustained':
            release_time += actual_duration * 0.3  # extra sustain
        midi.addControllerEvent(track, channel, release_time, 64, 0)
    
    return actual_time + actual_duration


# ══════════════════════════════════════════════════════
# PRE-BUILT EXPRESSIVE MODES
# ══════════════════════════════════════════════════════

MODES = {
    'tender': {
        'shape': 'rise', 'touch': 'legato',
        'breath': 'rubato_pull', 'space': 'half_pedal'
    },
    'resolute': {
        'shape': 'block', 'touch': 'peso',
        'breath': 'steady', 'space': 'dry'
    },
    'searching': {
        'shape': 'scatter', 'touch': 'portato',
        'breath': 'hesitant', 'space': 'sparse'
    },
    'ecstatic': {
        'shape': 'climb', 'touch': 'leggiero',
        'breath': 'rubato_push', 'space': 'open'
    },
    'grieving': {
        'shape': 'fall', 'touch': 'morendo',
        'breath': 'agogic', 'space': 'sustained'
    },
    'playful': {
        'shape': 'wave', 'touch': 'staccato',
        'breath': 'steady', 'space': 'dry'
    },
    'sacred': {
        'shape': 'grow', 'touch': 'tenuto',
        'breath': 'fermata', 'space': 'open'
    },
    'anxious': {
        'shape': 'pulse', 'touch': 'staccato',
        'breath': 'rubato_push', 'space': 'close'
    },
    'nostalgic': {
        'shape': 'dissolve', 'touch': 'morendo',
        'breath': 'rubato_pull', 'space': 'sustained'
    },
    'furious': {
        'shape': 'block', 'touch': 'sforzando',
        'breath': 'rubato_push', 'space': 'dense'
    },
    'dreaming': {
        'shape': 'bloom', 'touch': 'leggiero',
        'breath': 'fermata', 'space': 'sustained'
    },
    'confessing': {
        'shape': 'rise', 'touch': 'portato',
        'breath': 'hesitant', 'space': 'close'
    },
    'ironic': {
        'shape': 'wave', 'touch': 'leggiero',
        'breath': 'steady', 'space': 'dry'
    },
    'heroic': {
        'shape': 'climb', 'touch': 'peso',
        'breath': 'steady', 'space': 'open'
    },
}


def mode_chord(
    midi, track, channel, time, notes, duration, velocity,
    mode='tender', ornament=None
):
    """
    Play a chord using a pre-built expressive mode.
    Convenience wrapper around expressive_chord.
    """
    m = MODES.get(mode, MODES['tender'])
    return expressive_chord(
        midi, track, channel, time, notes, duration, velocity,
        shape=m['shape'],
        touch=m['touch'],
        breath=m['breath'],
        ornament=ornament,
        space=m['space']
    )