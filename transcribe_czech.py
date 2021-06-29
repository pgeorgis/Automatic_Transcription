#AUTOMATIC GRAPHEME-TO-PHONEME (G2P) TRANSCRIPTION: CZECH
#Written by Philip Georgis (2021)

import re

#Mapping of Czech orthographic characters to IPA symbols
#Any characters not included here have identical IPA representation,
#or else must be kept in orthographic form until later on in order to 
#apply phonological rules properly (e.g. <ř>, <y>, <ý>)
czech_ipa = {'á':'aː',
             'e':'ɛ',
             'é':'ɛː',
             'i':'ɪ',
             'í':'iː',
             'ó':'oː',
             'ú':'uː',
             'ů':'uː',
             'c':'ʦ',
             'č':'ʧ',
             'ď':'ɟ',
             'g':'ɡ',
             'h':'ɦ',
             'ň':'ɲ',
             'š':'ʃ',
             'ť':'c',
             'w':'v',
             'x':'ks',
             'ž':'ʒ'}

#Two-character IPA correspondences
cz_digraphs = {'au':'au̯',
               'eu':'ɛu̯',
               'ou':'ou̯',
               'ch':'X', #needs to be kept separate from <x> at first
               #'dz':'ʣ',
               'dž':'ʤ',
               'ng':'ŋɡ',
               'nk':'ŋk',
               'qu':'kv'}

#Characters which undergo palatalization before <i>, <í>, <ě>
cz_palatal_dict = {'d':'ɟ',
                   't':'c',
                   'n':'ɲ'} 

#Designate IPA characters as respective sound types 
#(vowels, consonants, obstruents, voiceless sounds, etc.)
cz_obstruents = ['b', 'c', 'd', 'f', 'ɡ', 'k', 'p', 's', 't', 'v', 'x', 'z',
                 'ɟ', 'ɦ', 'ʃ', 'ʒ', 'ʦ', 'ʧ', 'ř', 'ʣ', 'ʤ', 'ɣ']

cz_consonants = cz_obstruents + ['m', 'n', 'ɲ', 'ŋ', 'r', 'l', 'j']

#Consonants which can be syllabic in Czech
syllabics = ['r', 'l', 'm', 'n'] 

#Dictionary of voiced sounds with their devoiced equivalents
cz_devoicing_dict = {'b':'p',
                     'd':'t',
                     'ɡ':'k',
                     'v':'f',
                     'z':'s',
                     'ɦ':'x',
                     'ɟ':'c',
                     'ʒ':'ʃ',
                     'ʣ':'ʦ',
                     'ʤ':'ʧ',
                     'ř':'ř̊' #hard to see, but includes voiceless diacritic above for ř
                     }

cz_voicing_dict = {cz_devoicing_dict[phone]:phone for phone in cz_devoicing_dict}
cz_voicing_dict['x'] = 'ɣ'

cz_voiceless = list(cz_voicing_dict.keys())

cz_vowels = ['a', 'i', 'ɛ', 'ɪ', 'o', 'u']

#Characters (spaces, punctuation, etc.) which mark the end of a word
ending = [' ', '.', ',', ';', ':', '!', '?', '[', ']', '(', ')', "'", '"']


def cz_g2p(text):
    """Converts an orthographic text to a basic IPA representation"""
    
    #Lowercase the text and split it into a list of words
    text = text.lower().split()

    #Iterate through words in the text and store their basic transcriptions in a list
    tr = []
    for word in text:
        tr_word = word[:]
        
        #Convert two-character sequences to IPA first
        for digraph in cz_digraphs:
            tr_word = re.sub(digraph, cz_digraphs[digraph], tr_word)
        
        #Then convert remaining single characters to IPA
        for ch in czech_ipa:
            tr_word = re.sub(ch, czech_ipa[ch], tr_word)
        
        #Treat digraph <ch> /x/ separately
        #If initially converted to /x/, it would be mistaken for orthographic <x>
        #and be transcribed as /ks/ in second step
        #Convert at first to <X> with cz_digraphs, then convert <X> to /x/
        #<ch> --> <X> --> /x/
        tr_word = re.sub('X', 'x', tr_word)
        
        #Add transcribed word to list of transcribed words
        tr.append(tr_word)
        
    return ' '.join(tr)



def palatalize_cz(text):
    """Carries out palatalization of consonants in the relevant context"""
    tr = []
    
    #Iterate through characters in the text
    for i in range(len(text)):
        ch = text[i]
        
        #Do nothing if the character cannot be palatalized
        if ch not in cz_palatal_dict:
            tr.append(ch)
            
        #If the character can be palatalized, check its following context
        else:
            
            #Check what the next character is
            try:
                
                #Palatalize the consonant if the following character is one of
                #the palatalizing vowels
                nxt = text[i+1]
                if nxt in ['ě', 'i', 'ɪ']:
                    tr.append(cz_palatal_dict[ch])
                    
                #Otherwise change nothing
                else:
                    tr.append(ch)
                    
            #If there is no next character (i.e., it is the final character of the text),
            #change nothing
            except IndexError:
                tr.append(ch)
    
    tr = ''.join(tr)        
    
    #Now that palatalization has been applied, orthographic <y> and <ý> can 
    #be transcribed to IPA
    #(If done prior to this point, they would mistakenly trigger palatalization;
    #<y> and <i> have same phonetic realization as [ɪ], except that the latter triggers
    #palatalization of the preceding consonant, while the former does not; 
    #same for <ý> and <í> as [iː])
    
    #Similarly, carry out special palatalization of labial consonants /m, b, p, f, v/,
    #only when followed by orthographic <ě>
    palatalization2 = {'y':'ɪ',
                       'ý':'iː',
                       'mě':'mɲɛ'}
    labials = ['b', 'p', 'f', 'v']
    for labial in labials:
        palatalization2[f'{labial}ě'] = f'{labial}jɛ'
    
    #Replace all relevant sequences
    for seq in palatalization2:
        tr = re.sub(seq, palatalization2[seq], tr)
    
    #Replace all remaining instances of <ě> with /ɛ/
    #(preceding consonants palatalized in first palatalization step)
    tr = re.sub('ě', 'ɛ', tr)
         
    return tr



def final_devoicing(text):
    """Carries out word-final devoicing"""
    
    #Store transcriptions in list
    tr = []
    
    #Split text into words
    text = text.split()

    #Iterate through words in text
    for word in text:
        
        #Start from end of word and iterate backwards, 
        #to find index j of final non-punctuation character
        i = 0
        w = []
        j = len(word) - 1
        while word[j] in ending:
            j -= 1
            
        #Iterate forward through characters until character at index j
        while i < len(word):
            ch = word[i]
            if i != j:
                w.append(ch)
            
            #Devoice only character at index j, if applicable
            else:
                w.append(cz_devoicing_dict.get(ch, ch))
                
            i += 1
        
        #Add transcribed word to list of transcribed words
        tr.append(''.join(w))        
        
    return ' '.join(tr)    



def syllabify(text):
    """Adds syllabic diacritics to /r, l, m, n/ if one of the following conditions is met:
        (1) at beginning of word and next character is a consonant
        (2) at end of word and previous character is a consonant
        (3) surrounded by consonants"""
    
    #Store transcriptions in list
    tr = []
    
    #Split text into words
    text = text.split()

    #Iterate through words in text
    for word in text:
        
        #Iterate through characters in word
        w = []
        for i in range(len(word)):
            ch = word[i]
            w.append(ch)
            
            #Examine context if character is possibly syllabic; otherwise do nothing
            if ch in syllabics:
                
                #(1) Check whether the character is at the beginning of the word
                if i == 0:
                    
                    #If so, check for next character
                    try:
                        nxt = word[i+1]
                        
                        #Check whether the next character is a consonant
                        if nxt in cz_consonants:
                            
                            #Don't add syllabic diacritic to /m, n/ if followed
                            #by /m, n, ɲ, l, r/
                            if ((ch in ['m', 'n']) and (nxt in ['m', 'n', 'ɲ', 'l', 'r'])):
                                continue
                            
                            #Otherwise, condition (1) is met, add syllabic diacritc
                            else:
                                w.append('̩') #syllabic diacritic
                        else:
                            continue
                    
                    #In case of words consisting of a single possibly-syllabic 
                    #consonant, add the syllabic diacritic
                    except IndexError:
                        w.append('̩')
                
                #If not at the beginning of the word, check for conditions (2) and (3)
                else:
                    
                    #Check if preceding character is a consonant
                    if word[i-1] in cz_consonants:
                        
                        #If so, check whether the following character is also a consonant (3)
                        #or if it is at the end of the word (2)
                        try:
                            nxt = word[i+1]
                            
                            #Check whether the following character is a consonant
                            if nxt in cz_consonants:
                                
                                #Don't add syllabic diacritic to /m, n/ if followed
                                #by /m, n, ɲ, l, r/
                                if ((ch in ['m', 'n']) and (nxt in ['m', 'n', 'ɲ', 'l', 'r'])):
                                    continue
                                
                                #Otherwise, condition (3) is met, add syllabic diacritc
                                else:
                                    w.append('̩')
                            else:
                                continue
                        
                        #If there is no following character, it is at the end of the word
                        #Fulfills condition (2), add syllabic diacritic
                        except IndexError:
                            w.append('̩')
                    
                    #If the next character is not a consonant, do nothing
                    else:
                        continue
        
        #Add transcribed word to list of transcribed words
        tr.append(''.join(w))
        
    return ' '.join(tr)



def cz_voice_assim(text):
    "Performs forward and backward voicing assimilation of obstruents"

    tr = []
    
    #Backward voicing assimilation (from following to preceding consonant)
    #Iterate backwards through characters in the text
    for i in range(len(text)-1,-1,-1):
    
        ch = text[i]
        
        #Perform voicing assimilation if the character is an obstruent
        #(and if the following character is also an obstruent)
        if ch in cz_obstruents:
            
            #Check for a following character, which will be the first character 
            #of the transcribed list constructed in reverse order
            try:
                nxt = tr[0]
                
                #Exception to regressive voicing assimilation is sequence <sh>
                #Underlyingly /sɦ/, but pronounced /sx/ rather than /zɦ/ (Bohemia, not Moravia)
                #Note: some words do use /zɦ/, e.g. <shora>, <shluk> but this detail is ignored here
                #No need to mark the case where /ɦ/ has been devoiced to /x/ word-finally
                #as no voicing assimilation will occur in that case
                if (ch, nxt) == ('s', 'ɦ'):
                    tr[0] = 'x'
                    tr.insert(0, ch)
                    continue
                
                #Check if the following character is an obstruent
                if nxt in cz_obstruents:
                    
                    #<v, ř> /v, r̝/ do not trigger voicing assimilation of preceding consonant
                    if nxt not in ['v', 'ř']:
                        
                        #Check whether the following segment is voiced or voiceless
                        voice = nxt not in cz_voiceless
                        
                        #Devoice or voice the present segment according to 
                        #the voicing of the following segment
                        if voice == False:
                            tr.insert(0, cz_devoicing_dict.get(ch, ch))
                        else:
                            tr.insert(0, cz_voicing_dict.get(ch, ch))
                    
                    #Change nothing if the following consonant was one of <v, ř> /v, r̝/
                    else:
                        tr.insert(0, ch)
                else:
                    tr.insert(0, ch)
                    
            #Do not change anything if it is the final character of the text
            except IndexError:
                tr.insert(0, ch)
        
        #Otherwise change nothing
        else:
            tr.insert(0, ch)
 
    #Forward voicing assimilation: only affects <ř> (from preceding to following consonant)
    new_tr = [tr[0]]
    for i in range(1, len(tr)):
        ch = tr[i]
        if ch == 'ř':
            
            #Check what the preceding segment was
            prev = tr[i-1]
            
            #If the preceding segment was voiceless, devoice <ř> to <ř̊>
            if prev in cz_voiceless:
                new_tr.append(cz_devoicing_dict[ch])
            
            #Otherwise leave <ř> as is
            else:
                new_tr.append(ch)
        
        #Don't change segments other than <ř>
        else:
            new_tr.append(ch)
            
            
    return ''.join(new_tr)



def add_stress(text):
    """Adds stress marking to the first syllabic segment of each word in the text"""
    #Store transcriptions in list
    tr = []
    
    #Split text into words
    text = text.split()
    
    #Iterate through words in text
    for word in text:
        w = []
        
        #Search for the first syllabic segment, either a vowel or a syllabic,
        #and add stress diacritic to it
        i = 0
        while i < len(word):
            ch = word[i]
            
            #Check if the character is a vowel
            #If so, add syllabic diacritic and stop search
            if ch in cz_vowels:
                w.append('ˈ')
                break
            
            #Check whether the character is a syllabic consonant
            elif ch in syllabics:
                
                #Add syllabic diacritic if syllabic and stop search
                if word[i+1] == '̩': #syllabic diacritic
                    w.append('ˈ')
                    break
                
                #Do nothing if not syllabic
                else:
                    w.append(ch)
                    i += 1
            
            #Do nothing if neither a vowel nor a syllabic consonant
            else:
                w.append(ch)
                i += 1
        
        #Once the first syllabic segment is found, add the remaining characters
        w.extend(word[i:])
        
        #Add transcribed word to list of transcribed words
        tr.append(''.join(w))
        
    return ' '.join(tr)
            
            

def transcribe_cz(text, stress=True):
    #Get basic IPA transcription
    step1 = cz_g2p(text)
    
    #Perform palatalization
    step2 = palatalize_cz(step1)
    
    #Perform final devoicing
    step3 = final_devoicing(step2)
    
    #Perform voicing assimilation
    step4 = cz_voice_assim(step3)
    
    #Add syllabic diacritics, if applicable
    step5 = syllabify(step4)
    
    #Fix specific characters and sequences
    step6 = re.sub('ř', 'r̝', step5)
    step6 = re.sub('tʦ', 'ʦ', step6)
    step6 = re.sub('tʧ', 'ʧ', step6)
    
    #Add stress annotation if specified to do so
    if stress == True:
        step7 = add_stress(step6)
        return step7
    
    #Otherwise return transcribed word without stress annotation
    else:
        return step6

