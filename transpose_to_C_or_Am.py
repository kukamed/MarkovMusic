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


check_or_create_folder(sys.argv[2])
for file in glob.glob(sys.argv[1] + "/*.mid"):
    print(file)
    score = music21.converter.parse(file)
    key = score.analyze('key')
   
    if key.mode == "major":
        halfSteps = majors[key.tonic.name]
        
    elif key.mode == "minor":
        halfSteps = minors[key.tonic.name]
    
    newscore = score.transpose(halfSteps)
    key = newscore.analyze('key')
    
    if key.mode == "minor":
        check_or_create_folder(sys.argv[2] + '/Am')
        newFileName = sys.argv[2] + "/Am/" + os.path.split(file)[-1]
        newscore.write('midi',newFileName)
    if key.mode == "major":
        check_or_create_folder(sys.argv[2] + '/C')
        newFileName = sys.argv[2] + "/C/" + os.path.split(file)[-1]
        newscore.write('midi',newFileName)