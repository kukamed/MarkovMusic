import glob
import os
import music21
import sys

def check_or_create_folder(name):
    if os.path.isdir(name):
        return
    os.makedirs(name + "/")

    
majors = dict([('A-', 4),('G#', 4),('A', 3),('A#', 2),('B-', 2),('B', 1),('C', 0),('C#', -1),('D-', -1),('D', -2),('D#', -3),('E-', -3),('E', -4),('F', -5),('F#', 6),('G-', 6),('G', 5)])
minors = dict([('G#', 1), ('A-', 1),('A', 0),('A#', -1),('B-', -1),('B', -2),('C', -3),('C#', -4),('D-', -4),('D', -5),('D#', 6),('E-', 6),('E', 5),('F', 4),('F#', 3),('G-', 3),('G', 2)])

keys = ['C', 'C#', 'D', 'E-', 'E', 'F', 'F#', 'G', 'A-', 'A', 'B-', 'B']
enarmonic = { 'D-' : 'C#', 'E-' : 'D#', 'G-': 'F#', 'G#' : 'A-', 'A#' : 'B-'}

check_or_create_folder(sys.argv[2])
for file in glob.glob(sys.argv[1] + "/*.mid"):
    

    score = music21.converter.parse(file)
    key = score.analyze('key')
    if key in enarmonic:
        key = enarmonic[key]

    print( f'{file} on {key.tonic.name} {key.mode}')
    key_index = keys.index(key.tonic.name)
    
    for i in range(-6, 6):
        newscore = score.transpose(i)
        new_key = keys[ (key_index + i) % 12]
        folder = f'{new_key} {key.mode}'
        check_or_create_folder( sys.argv[2] + '/' + folder)
        file_name = os.path.split(file)[-1]
        newFileName = f'{sys.argv[2]}/{folder}/{file_name}'
        newscore.write('midi',newFileName)