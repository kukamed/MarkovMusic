import mido
import os
import pandas as pd
import pickle
import sys

def midi_to_tracks(midi):
    tracks = []
    
    for track in midi.tracks:
        notes = []
        note_on = {}
        for msg in track:
            if msg.type == 'note_on':
                duration = msg.time
                pitch = msg.note
                note_on[pitch] = duration
            if msg.type == 'note_off' and msg.note in note_on:
                pitch = msg.note
                duration = note_on[pitch] + msg.time
                notes.append(pitch)
                slur_count = duration//min_duration - 1
                for i in range(slur_count):
                    notes.append(-pitch)
        tracks.append(notes)
    
    return tracks

def tracks_to_symbol_sequence(tracks):
    symbol_sequence = []

    n_tracks = len(tracks)
    sequence_length = len(tracks[0])
    for sequence_index in range(sequence_length):
        if is_slur(sequence_index, n_tracks):
            symbol_count = len(symbol_sequence) - 1
            symbol_sequence[symbol_count][4] += 1
        else:
            new_symbol = sequence_index_to_symbol(sequence_index, n_tracks)
            symbol_sequence.append( new_symbol )
    return symbol_sequence


def add_to_transition_matrix(symbol_sequence, symbol_transition_count, init_symbols):
    init_symbols.append( tuple(symbol_sequence[0]) )
    for symbol_index in range(1, len(symbol_sequence)):
        
        first_symbol = tuple(symbol_sequence[symbol_index-1])
        second_symbol = tuple(symbol_sequence[symbol_index])
        
        if first_symbol not in symbol_transition_count:
            symbol_transition_count[first_symbol] = {}
        
        if second_symbol not in symbol_transition_count[first_symbol]:
            symbol_transition_count[first_symbol][second_symbol] = 0
            
        symbol_transition_count[first_symbol][second_symbol] += 1


def sequence_index_to_symbol(sequence_index, n_tracks):
    symbol = []
    for track_id in range(n_tracks):
        symbol.append(tracks[track_id][sequence_index])
    symbol.append(1)
    return symbol

def is_slur(sequence_index, n_tracks):
    status = True
    for track_id in range(n_tracks):
        status = status and tracks[track_id][sequence_index] < 0
    return status

def check_track_length(tracks):
    length = len(tracks[0])
    for track in tracks:
        if len(track) != length:
            return False
    return True

os.chdir(sys.argv[1])

min_duration = 256

symbol_transition_count = {}
init_symbols = []

path = './.'
files = [os.path.join(root, name)
             for root, dirs, files in os.walk(path)
             for name in files
             if name.endswith(".mid")]

for file_name in files:
    if file_name.split('.')[-1] != 'mid':
        continue
        
    print(file_name)
    midi = mido.MidiFile(file_name)
    
    tracks = midi_to_tracks(midi)
    if check_track_length(tracks) == False or len(tracks) != 4:
        print('error on track')
        continue
    symbol_sequence = tracks_to_symbol_sequence(tracks)
    add_to_transition_matrix(symbol_sequence, symbol_transition_count, init_symbols)

pickle.dump( symbol_transition_count, open( "symbol_transition_count.p", "wb" ) )
pickle.dump( init_symbols, open( "init_symbols.p", "wb" ) )