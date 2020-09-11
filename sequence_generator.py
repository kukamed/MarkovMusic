import pickle
import random
from EasyMIDI import EasyMIDI, Track, Note
import sys

init_symbols = pickle.load( open( sys.argv[1] + '/init_symbols.p', "rb" ) )
symbol_transition_count = pickle.load( open( sys.argv[1] + '/symbol_transition_count.p', "rb" ) )

initial_state = tuple(random.choice(init_symbols))
sequence = [initial_state]
for i in range( int(sys.argv[3])):
    if sequence[-1] not in symbol_transition_count:
        break

    transitions = symbol_transition_count[sequence[-1]]
    weights = list(transitions.values())
    states = list(transitions.keys())
    current_state = random.choices(states, weights = weights)[0]
    sequence.append(current_state)

n_tracks = len(sequence[0]) - 1
tracks = [[] for i in range(n_tracks)]
for state in sequence:
    for i in range(n_tracks):
        pitch = state[i]
        duration = state[-1]
        if pitch > 0:
            tracks[i].append([pitch, duration])
        else:
            tracks[i][-1][1] += duration

notes = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

easyMIDI = EasyMIDI()

for voice in tracks:
    track = Track("choir aahs")
    for note in voice:
        pitch = note[0]
        duration = note[1]
        midi_note = Note(notes[pitch%12], octave = pitch//12 - 1, duration = duration/4, volume = 100)
        track.addNote(midi_note)

    easyMIDI.addTrack(track)

easyMIDI.writeMIDI(sys.argv[2])