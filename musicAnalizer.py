import os, glob
import re
from progress.bar import Bar
import numpy as np
import codecs, json
import pprint
import re

'''
    Retorna um vetor de subsequencias a partir de uma sequencia primaria de acordes
    params:
        sequ: sequencia de acordes
        result: vetor que armazena os resultados
'''
def discSubseq ( sequ, result ) :

    # transforma a sequencia de acordes em uma unica string
    st = "".join( sequ )
    ch = ''
    '''
        Cria o padrao regex para capturar o vetor de acordes, os matchs sao da seguinte categoria:
        o \w[CDEFGAB]{1,10} captura uma sequencia de 1 a 10 notas que se encaixem na descricao
        a partir desse valor, ele procura uma parte da sequencia em que a primeira captura se repete depois
        de dois caracteres, ou seja, numa sequencia "CDEEEEECDE", a primeira captura referenciada por
        \1 e a string "CDE"
    '''
    pattern = re.compile(r'(\w[CDEFGAB]{1,10})\w\w*\1')
    # vetor de notas maiores
    major = ['C','D','E','F','G','A','B']
    # captura os matches de strings repetidas no vetor found    
    found = re.findall(pattern, st)
    # condicao de parada da funcao recursiva, ou seja, se nao for encontrado nada a funcao retorna
    if (found == [] or len(st) < 10) :
        ''' 
            Resultado recebe a propria sequencia, pois como nao foi encontrado nada a propria sequencia e uma
            subsequencia
        '''
        result.append(st)
        
        return result
    # exauri a sequencia para evitar que existam subsequencias na sequencia encontrada
    while len(found) > 0 :
        # para cada subsequencia em found
        for i in found :
            # contador de acordes encontrados na sequencia definida
            val = 0
            # string para guardar a subsequencia
            ch = i            
            # para cada caracter na string
            for j in i :
                # se o caracter estivem em major
                if j in major :
                    # contador incrementado
                    val+=1    
            # condicao de iniciacao
            if val>0 :
                ch = i
        # procura subsequencias na sequencia
        found = re.findall(pattern, ch)        
    # novo vetor com a sequencia antiga excluindo a subsequencia encontrada
    nw = st.split(ch)
    # o vetor de resultados finais recebem a ultima subsequencia encontrada
    result.append(ch)
    # limpa o nw de valores vazios
    nw = [i for i in nw if i!='']    
    val = 0
    # para cada sequencia em nw
    for i in nw :
        for j in i:
            if j in major :
                val+=1
        # se ainda tiverem notas em nw
        if val > 0 :
            # executa uma recursao
            discSubseq ( i, result )
    # retorna se todas as recursoes forem resolvidas
    return result

def processing_notes( searchpath = '/' , group = 'major', artist = 'all', musicalStyle = 'all' ) :

    # inicializa os objetos que guardaraoas notas
    error = []
    notes = {'C':0}
    finalNotes = {'D':0}
    notes['C'] = {'D':[0,1,0]}
    totalChords = []
    i = 0

    # inicializa o diretorio searchpath para busca
    os.chdir( searchpath )

    # cria o iterador para os arquivos JSON da pasta 
    bar = Bar('Processing', max=len(glob.glob("*.json")))
    print ('Numeros de arquivos a serem processados: ' + str(len(glob.glob("*.json"))))

    major           = ['C','D','E','F','G','A','B']
    minor           = ['Cm','Dm','Em','Fm','Gm','Am','Bm']
    sustenido       = ['C#','D#','F#','G#','A#']
    minorSustenido  = ['C#m','D#m','F#m','G#m','A#m']

    note_group      = []
    name_groups = group.split(' ')
    if ('major' in name_groups) :
        note_group = note_group + major
    if ('minor' in name_groups) :
        note_group = note_group + minor
    if ('sustenido' in name_groups) :
        note_group = note_group + sustenido
    if ('minorSustenido' in name_groups) :
        note_group = note_group + minorSustenido

    # passando por todos os arquivos
    for file in glob.glob("*.json"):

        print ('Processando o arquivo: ' + file)
        # comeca a processar
        try :
            # abre o arquivo em modo de leitura
            fp = open(file, "r")
            # le todo o conteudo do json
            text = fp.read()
            # da um split para deixar apenas as notas
            chords = text.split('":"')
            # regex para achar os campos
            songnamepattern = re.compile(r'"Songname":"([a-zA-Z\d\s]*)"')
            songname = re.findall(songnamepattern, text)
            artistpattern = re.compile(r'"Artist":"([a-zA-Z\d\s]*)"')
            artistname = re.findall(artistpattern, text)
            genrepattern = re.compile(r'"Genre":"([a-zA-Z\d\s]*)"')
            genre = re.findall(genrepattern, text)
            chordspattern = re.compile(r'"Chords":\["([a-zA-Z\d\s",#]*)"]}')
            chords = re.findall(chordspattern, text)
            success = 0
            try :
                chords = chords[0].split('","')
                songname = songname[0]
                genre = genre[0]
                artistname = artistname[0]
                success = 1
            except :
                success = 0
                error.append(ValueError)
                print(ValueError)

            if success is 1 :
                print('Songname: '+str(songname))
                print('Genre: '+str(genre))
                print('Artist Name: '+str(artistname))
                print('Chords: '+str(chords))

            if ((genre == musicalStyle) or (musicalStyle == 'all')) :
                print ('Genre: ' + str(genre) + '\nSongname: ' + str(songname))            
                # print('Sequencia de notas encontradas :' + str(chords))
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

    return finalNotes

'''
    Dados os arquivos json em search path, cria um arquivo em resultpath de distancias de acordes dados
    os parametros
'''
def create_json( searchpath = '/' ,resultpath = '/home/dev_pitel', group = 'major', artist = 'all', musicalStyle = 'all') :
    
    finalNotes = processing_notes( searchpath, group, artist, musicalStyle )

    '''
        Montando a tabela
    '''

    major           = ['C','D','E','F','G','A','B']
    minor           = ['Cm','Dm','Em','Fm','Gm','Am','Bm']
    sustenido       = ['C#','D#','F#','G#','A#']
    minorSustenido  = ['C#m','D#m','F#m','G#m','A#m']

    note_group      = []
    name_groups = group.split(' ')
    if ('major' in name_groups) :
        note_group = note_group + major
    if ('minor' in name_groups) :
        note_group = note_group + minor
    if ('sustenido' in name_groups) :
        note_group = note_group + sustenido
    if ('minorSustenido' in name_groups) :
        note_group = note_group + minorSustenido
    if ('all' in name_groups) :
        note_group = major + minor + sustenido + minorSustenido
    table = np.zeros((len(note_group), len(note_group)))

    k = 0
    p = 0

    for i in finalNotes :
        if i in (note_group) :
            print (finalNotes[i])
    #print ('MAJOR: ', major)
    for i in (note_group) :
        for j in (note_group) :
            try :
                if (i in finalNotes) :
                    if (j in finalNotes[i]) :
                        #print (i, j)
                        table[k][p] = finalNotes[i][j]
                    else :
                        table[k][p] = float('nan')

                else :
                    table[k][p] = float('nan')
            except ValueError :
                print (ValueError)
            p+=1
        k+=1
        p=0

    b = table.tolist()
    k = 0
    for i in (note_group) :
        print ('"',i, '": ', b[k], ',')
        k+=1
    file_path = resultpath + "table.json"
    json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4)

create_json( searchpath='data/', resultpath='/home/dev_pitel/Documents/trabalho/python/chordsCrawler/results/', group='all', musicalStyle='all')