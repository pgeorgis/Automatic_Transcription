#SLOVAK G2P
#Written by Philip Georgis (2020-21)

import re

#Dictionary of Slovak orthographic characters and their IPA equivalents
slovak_ipa = {'á':'aː',
             'ä':'æ',
             'e':'ɛ',
             'é':'ɛː',
             'í':'iː',
             'o':'ɔ',
             'ó':'ɔː',
             'ô':'ʊ̯ɔ',
             'ú':'uː',
             'c':'ʦ',
             'č':'ʧ',
             'ď':'ɟ',
             'g':'ɡ',
             'h':'ɦ',
             'l':'ɫ',
             'ĺ':'ɫ̩ː', #always syllabic
             'ľ':'ʎ',
             'ň':'ɲ',
             'ŕ':'r̩ː', #always syllabic
             'š':'ʃ',
             'ť':'c',
             'w':'v',
             'x':'ks',
             'ž':'ʒ'}

#Slovak two-character combinations with special transcriptions
sk_digraphs = {'ia':'ɪ̯a',
               'ie':'ɪ̯ɛ',
               'iu':'ɪ̯u',
               'au':'au̯',
               'eu':'ɛu̯',
               'ou':'ɔʊ̯',
               'ch':'X', #needs to be distinct from <x> at first
               'dz':'ʣ',
               'dž':'ʤ',
               'qu':'kv',
               'nk':'ŋk',
               'ng':'ŋɡ'
               #'mf':'ɱf',
               #'mv':'ɱv'
               }

#Dictionary of consonants with their palatalized forms
sk_palatal_dict = {'d':'ɟ',
                   't':'c',
                   'n':'ɲ', 
                   'l':'ʎ'}

#Lists of Slovak obstruents and consonants
sk_obstruents = ['b', 'c', 'd', 'f', 'ɡ', 'k', 'p', 's', 't', 'v', 
                 'x', 'z', 'ɟ', 'ɦ', 'ʃ', 'ʒ', 'ʦ', 'ʧ', 'ʣ', 'ʤ']

sk_consonants = sk_obstruents + ['m', 'n', 'ɲ', 'ŋ', 'r', 'ɫ', 'ʎ', 'j', 'ʋ']


#Dictionary of voiced consonants and their devoiced equivalents
sk_devoicing_dict = {'b':'p',
                     'd':'t',
                     'ɡ':'k',
                     'v':'f',
                     'z':'s',
                     'ɦ':'x',
                     'ɟ':'c',
                     'ʒ':'ʃ',
                     'ʣ':'ʦ',
                     'ʤ':'ʧ'}

#Dictionary of voiceless consonants and their voiced equivalents
sk_voicing_dict = {sk_devoicing_dict[phone]:phone for phone in sk_devoicing_dict}

#List of voiceless segments
sk_voiceless = list(sk_voicing_dict.keys())

#List of Slovak vowels
sk_vowels = ['a', 'i', 'ɛ', 'æ', 'ɔ', 'u', 'ʊ', 'ɪ']

#List of characters to consider as punctuation marking the end of a word
ending = [' ', '.', ',', ';', ':', '!', '?', '[', ']', '(', ')', "'", '"']


def sk_g2p(text):
    """Converts an orthographic text into basic IPA"""
    
    #Lowercase the text
    text = text.lower()
    
    #Convert digraphs to IPA
    for digr in sk_digraphs:
        text = re.sub(digr, sk_digraphs[digr], text)
    
    #Convert remaining single characters to IPA
    for ch in slovak_ipa:
        text = re.sub(ch, slovak_ipa[ch], text)
    
    #Lowercase the text again (<ch> --> /X/ --> /x/)
    text = text.lower()

    return text


def palatalize_sk(text, 
                  exceptions = ['jɛdɛn', 'tɛn', 'tɛlɛfɔːn']):
    """Performs palatalization on broad IPA transcribed text
    text : string
    exceptions : list of strings, words which don't follow palatalization rule"""
    
    #Split the text into words, and palatalize each word individually, skipping exceptions 
    tr = []
    text = text.split()
    for word in text:
        if word not in exceptions: #what about inflections of these words?
        
            #Palatalize all palatalizable consonants before all front vowels
            for ch in sk_palatal_dict:
                for front_vowel in ['ɛ', 'i', 'ɪ']:
                    word = re.sub(f'{ch}{front_vowel}', f'{sk_palatal_dict[ch]}{front_vowel}', word)
            tr.append(word)
        
        #Skip words which are known not to undergo palatalization
        else:
            tr.append(word)
    
    #Rejoin the text and convert orthographic <y> and <ý> to IPA
    #(which would have otherwise triggered palatalization if done previously)
    tr = ' '.join(tr)
    tr = re.sub('y', 'i', tr)
    tr = re.sub('ý', 'iː', tr)
    
    return tr


def final_devoicing(text):
    """Devoices word-final obstruents"""
    
    #Split the text into words and process each word individually
    tr = []
    text = text.split()
    for word in text:
        
        #Search for last segment of word, which might be masked by punctuation
        #Last segment is at index j
        j = len(word) - 1
        while word[j] in ending:
            j -= 1
        word = list(word)
        
        #If the final segment is /v/, some allophony occurs
        if word[j] == 'v':

            #If the word is the word <v>, then change nothing
            if word == ['v']:
                pass
            
            #If the final /v/ is preceded by a consonant, then change to [ʋ]
            elif word[j-1] in sk_consonants:
                word[j] = 'ʋ'
                
            #Otherwise change word-final /v/ to [ʊ̯]
            else:
                word[j] = 'ʊ̯'
        
        #Otherwise devoice segment at index j, if possible
        else:
            word[j] = sk_devoicing_dict.get(word[j], word[j])
        
        tr.append(''.join(word))
       
    return ' '.join(tr)    


def syllabify(text):
    """Adds syllabic diacritics to /r/ and /ɫ/ in certain contexts"""
    
    syllabics = ['r', 'ɫ']
    
    #Split text into words
    tr = []
    text = text.split()
    
    #Iterate through words of text
    for word in text:
        w = []
        
        #Iterate through characters of the word
        for i in range(len(word)):
            ch = word[i]
            w.append(ch)
            
            #If the current character is a possibly syllabic consonant, check its context
            if ch in syllabics:
                
                #If word initial and followed by a consonant, make it syllabic
                if i == 0:
                    try:
                        nxt = word[i+1]
                        if nxt in sk_consonants:
                            w.append('̩') #syllabic diacritic
                        else:
                            continue
                    
                    #In case of words consisting of only a possibly syllabic consonant, make it syllabic
                    except IndexError:
                        w.append('̩')
                        
                else:
                    #If the possibly syllabic consonant is between consonants
                    #or word-final following a consonant, make it syllabic
                    if word[i-1] in sk_consonants:
                        try:
                            nxt = word[i+1]
                            if nxt in sk_consonants:
                                w.append('̩')
                            else:
                                continue
                        except IndexError:
                            w.append('̩')
                    else:
                        continue
        tr.append(''.join(w))
    return ' '.join(tr)


def sk_voice_assim(text):
    """Performs voicing assimilation on obstruent clusters"""
    
    tr = []
    
    #Iterate through characters of text
    for i in range(len(text)):
        ch = text[i]
        
        #Check whether current character is an obstruent
        if ch in sk_obstruents:
            try:
                
                #Identify the following segment and its voicing status
                nxt = text[i+1]
                voice = nxt not in sk_voiceless
                
                #If the following segment is an obstruent, prepare to assimilate voicing
                if nxt in sk_obstruents:
                    
                    #/v/ does not trigger voicing assimilation
                    #otherwise assimilate to voicing of following obstruent
                    if nxt != 'v':
                        if voice == False:
                            tr.append(sk_devoicing_dict.get(ch, ch))
                        elif voice == True:
                            tr.append(sk_voicing_dict.get(ch, ch))
                    else:
                        tr.append(ch)
                else:
                    tr.append(ch)
            except IndexError:
                tr.append(ch)
        else:
            tr.append(ch)
    return ''.join(tr)


def fix_chs(text):
    """Corrects specific character sequences involving /t/ and /v/"""
    
    #Delete /t/ when followed by these affricates
    text = re.sub('tʦ', 'ʦ', text)
    text = re.sub('tʧ', 'ʧ', text)
    
    #Allophony of /v/: remain /v/ when preceding obstruents, otherwise /ʋ/
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch == 'v':
            try:
                nxt = text[i+1]
                if nxt in sk_obstruents + [' ']:
                    tr.append('v')
                else:
                    tr.append('ʋ')
            except IndexError:
                tr.append('v')
        else:
            tr.append(ch)
            
    return ''.join(tr)


def count_syllables(word, vowels=sk_vowels):
    """Counts syllables in word"""
    return len([ch for ch in word if ch in vowels+['̩']]) - word.count('̯')
        

def add_stress(text):
    """Adds stress marking to words with >1 syllable"""
    
    #Split text into words
    tr = []
    text = text.split()
    
    #Iterate through words
    for word in text:
        
        #Count number of syllables to word and add stress marking to words
        #with >1 syllable
        syls = count_syllables(word)
        if syls > 1:
            w = []
            i = 0
            while i < len(word):
                ch = word[i]
                if ch in sk_vowels:
                    w.append('ˈ')
                    break
                elif ch in ['r', 'ɫ']:
                    if word[i+1] == '̩': #syllabic
                        w.append('ˈ')
                        break
                    else:
                        w.append(ch)
                        i += 1
                else:
                    w.append(ch)
                    i += 1
            w.extend(word[i:])
            tr.append(''.join(w))
        else:
            tr.append(word)
    return ' '.join(tr)
            

def transcribe_sk(text, stress=True):
    
    #Convert from Slovak orthography to basic IPA
    step1 = sk_g2p(text)
    
    #Perform palatalization
    step2 = palatalize_sk(step1)
    
    #Perform final devoicing
    step3 = final_devoicing(step2)
    
    #Perform voicing assimilation
    step4 = sk_voice_assim(step3)
    
    #Syllabify consonsants in relevant contexts
    step5 = syllabify(step4)
    
    #Fix some character combinations
    step6 = fix_chs(step5)
    
    #Add stress annotation if specified to do so
    if stress == True:
        step7 = add_stress(step6)
        return step7
    else:
        return step6