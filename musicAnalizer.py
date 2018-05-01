
import os, glob
import re
from progress.bar import Bar
import numpy as np
import codecs, json

def discSubseq ( sequ ) :
    chord = []
    if (len(sequ) > 2) :             
        ch = sequ[1]
        chord.append(ch)
        i = 2
        chcomp = sequ[2]
        while ((chcomp != ch) and (i < len(sequ))) :
            if (len(sequ) > (i)) :
                chord.append(sequ[i])
                chcomp = sequ[i]
            i = i + 1

    sequ = set(chord)
    subset = list(sequ)
    return subset

error = []
path = "/home/dev_pitel/Documents/trabalho/python/chordsCrawler"
os.chdir( path )

notes = {'C':0}
finalNotes = {'C':0}
finalNotes = {'D':0}
notes['C'] = {'D':[0,1,0]}
# print (notes)
totalChords = []

bar = Bar('Processing', max=len(glob.glob("*.json")))

for file in glob.glob("*.json"):
    #print (file)
    try :
        fp = open(file, "r")
        text = fp.read()
        chords = text.split('":"')
        if len(chords) > 2 :
            chords = chords[2].split('","')
            if len(chords[1].split('":["')) > 1 :
                chords[1] = chords[1].split('":["')[1]
            chords[len(chords) - 1] = chords[len(chords) - 1].split('"]}')[0]

        chord = []
        # print(chords)
        chord = discSubseq(chords)
        # print(chord)

        for i in range(0, len(chord)):
            for j in (0, len(chord)):
                if (len(chord) > j and len(chord) > i and abs(i - j) < 10) :
                    if (chord[i] in notes and chord[i] in finalNotes):
                        if (chord[j] in notes[chord[i]]):
                            notes[chord[i]][chord[j]][0] += abs(i-j)
                            notes[chord[i]][chord[j]][1] += 1
                            finalNotes[chord[i]][chord[j]] = notes[chord[i]][chord[j]][0] / notes[chord[i]][chord[j]][1] 
                        else :
                            notes[chord[i]][chord[j]] = [abs(i-j),1,abs(i-j)]
                            finalNotes[chord[i]][chord[j]] = abs(i-j)
                    else :
                        notes[chord[i]] = {chord[j]:[0,1,0]}
                        finalNotes[chord[i]] = {chord[j]:1}
                        if (chord[j] in notes[chord[i]]):
                            notes[chord[i]][chord[j]][0] += abs(i-j)                            
                            notes[chord[i]][chord[j]][1] += 1
                            finalNotes[chord[i]][chord[j]] = notes[chord[i]][chord[j]][0] / notes[chord[i]][chord[j]][1] 
                        else :
                            notes[chord[i]][chord[j]] = [abs(i-j),1,abs(i-j)]
                            finalNotes[chord[i]][chord[j]] = abs(i-j)

        # print (totalChords)

    except ValueError :
        error.append(ValueError)
        #print (ValueError)
    

    #bar.next()

#bar.finish()

'''
    Montando a tabela
'''

major           = ['C','D','E','F','G','A','B']
minor           = ['Cm','Dm','Em','Fm','Gm','Am','Bm']
sustenido       = ['C#','D#','F#','G#','A#']
minorSustenido  = ['C#m','D#m','F#m','G#m','A#m']

group = major + minor + sustenido + minorSustenido
table = np.zeros((len(group), len(group)))

k = 0
p = 0

for i in finalNotes :
    if i in (group) :
        print (finalNotes[i])
#print ('MAJOR: ', major)
for i in (group) :
    for j in (group) :
        try :
            if (i in finalNotes) :
                if (j in finalNotes[i]) :
                    #print (i, j)
                    table[k][p] = finalNotes[i][j]
                else :
                    table[k][p] = -1
                    print (j,"not in final notes",i)
            else :
                print (i,"not in final notes")
                table[k][p] = -1
        except ValueError :
            print (ValueError)
        p+=1
    k+=1
    p=0

b = table.tolist()
k = 0
for i in (group) :
    print ('"',i, '": ', b[k], ',')
    k+=1
file_path = path + "table.json"
json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)
