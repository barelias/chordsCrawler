
import os, glob
import re
from progress.bar import Bar
import numpy as np
import codecs, json
import pprint
import re

def discSubseq ( sequ, result ) :

    
    st = "".join( sequ )
    print ('joined')
    ch = ''
    pattern = re.compile(r'(\w[CDEFGAB]{1,10})\w\w*\1')
    major = ['C','D','E','F','G','A','B']    
    found = re.findall(pattern, st)
    print ('founded')
    if (len(found) == 0 and len(st) < 10) :
        print ('return')    
        result.append(st)
        return result
    while len(found) > 0 :
        print ('found')    
        for i in found :
            val = 0
            ch = i            
            for j in i :
                if j in major :
                    val+=1    
            if val>0 :
                ch = i
        found = re.findall(pattern, ch)        
    print (ch)
    nw = st.split(ch)
    result.append(ch)
    nw = [i for i in nw if i!='']    
    print ('new ', nw)
    val = 0
    print ('result ', result)
    for i in nw :
        for j in i:
            if j in major :
                val+=1
        if val > 0 :
            print ('call', result, i)        
            discSubseq ( i, result )

    print ('return')
    return result

error = []
path = "/home/dev_pitel/Documents/trabalho/python/chordsCrawler"
os.chdir( path )

notes = {'C':0}
finalNotes = {'C':0}
finalNotes = {'D':0}
notes['C'] = {'D':[0,1,0]}
# print (notes)
totalChords = []
i = 0
bar = Bar('Processing', max=len(glob.glob("*.json")))
print (len(glob.glob("*.json")))
for file in glob.glob("*.json"):
    print (file)
    try :
        fp = open(file, "r")
        text = fp.read()
        chords = text.split('":"')
        if len(chords) > 2 :
            chords = chords[2].split('","')
            if len(chords[1].split('":["')) > 1 :
                chords[1] = chords[1].split('":["')[1]
            chords[len(chords) - 1] = chords[len(chords) - 1].split('"]}')[0]

        # print(chords)
        lis = []
        print (chords)
        chords = chords[2:]
        result = discSubseq(chords, [])
        print ('RESULTS: ', result)
        major = ['C','D','E','F','G','A','B']    

        for val in result :
            chord = []
            count = -1
            for i in val :
                if i in major :
                    count+=1
                    chord.append('')
                    chord[count] = i
                else :
                    chord.append('')                    
                    chord[count]+=i
            print ('CHORD', chord)
            for i in range(0, len(chord)):
                for j in (0, len(chord)):
                    if (len(chord) > j and len(chord) > i and abs(i - j) < 10) :
                        if (chord[i] in notes and chord[i] in finalNotes) and (chord[j] in notes and chord[j] in finalNotes):
                            if (chord[j] in notes[chord[i]] and chord[i] in notes[chord[j]]):
                                notes[chord[i]][chord[j]][0] += abs(i-j)
                                notes[chord[i]][chord[j]][1] += 1
                                finalNotes[chord[i]][chord[j]] = notes[chord[i]][chord[j]][0] / notes[chord[i]][chord[j]][1]
                                notes[chord[j]][chord[i]][0] += abs(i-j)
                                notes[chord[j]][chord[i]][1] += 1
                                finalNotes[chord[j]][chord[i]] = notes[chord[j]][chord[i]][0] / notes[chord[j]][chord[i]][1] 
    
                            else :
                                notes[chord[i]][chord[j]] = [abs(i-j),1,abs(i-j)]
                                finalNotes[chord[i]][chord[j]] = abs(i-j)
                                notes[chord[j]][chord[i]] = [abs(i-j),1,abs(i-j)]
                                finalNotes[chord[j]][chord[i]] = abs(i-j)

                        else :
                            notes[chord[i]] = {chord[j]:[0,1,0]}
                            notes[chord[j]] = {chord[i]:[0,1,0]}
                            finalNotes[chord[i]] = {chord[j]:1}
                            finalNotes[chord[j]] = {chord[i]:1}                        
                            if (chord[j] in notes[chord[i]] and chord[i] in notes[chord[j]]):
                                notes[chord[i]][chord[j]][0] += abs(i-j)                            
                                notes[chord[i]][chord[j]][1] += 1
                                notes[chord[j]][chord[i]][0] += abs(i-j)                            
                                notes[chord[j]][chord[i]][1] += 1

                                finalNotes[chord[i]][chord[j]] = notes[chord[i]][chord[j]][0] / notes[chord[i]][chord[j]][1] 
                                finalNotes[chord[j]][chord[i]] = notes[chord[j]][chord[i]][0] / notes[chord[j]][chord[i]][1]                             
                            else :
                                notes[chord[i]][chord[j]] = [abs(i-j),1,abs(i-j)]
                                finalNotes[chord[i]][chord[j]] = abs(i-j)
                                notes[chord[j]][chord[i]] = [abs(i-j),1,abs(i-j)]
                                finalNotes[chord[j]][chord[i]] = abs(i-j)

        print (totalChords)

    except ValueError :
        error.append(ValueError)
        print (ValueError)
    

    bar.next()

bar.finish()

'''
    Montando a tabela
'''

major           = ['C','D','E','F','G','A','B']
minor           = ['Cm','Dm','Em','Fm','Gm','Am','Bm']
sustenido       = ['C#','D#','F#','G#','A#']
minorSustenido  = ['C#m','D#m','F#m','G#m','A#m']

group = major#+ sustenido + minorSustenido
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
            else :
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
