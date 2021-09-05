#SPANISH GRAPHEME-TO-PHONEME
#Written by Philip Georgis (2021)

import re
from string import punctuation

#Add Spanish punctuation marks
punctuation += '¡¿«»'

spanish_ipa = {'á':'ˈa',
               'b':'β',
               'c':'k',
               'd':'ð',
               'é':'ˈe',
               'g':'ɣ',
               'h':'',
               'í':'ˈi',
               'j':'X', #needs to remain distinct from <x>
               'ñ':'ɲ',
               'ó':'ˈo',
               'q':'k',
               'r':'ɾ',
               'ú':'ˈu',
               'ü':'w',
               'v':'β',
               'x':'ks',
               'y':'ʝ',
               'z':'θ'
               }

spanish_trigraphs = {'gu(?=[e|é|i|í])':'ɣ',
                     'qu(?=[e|é|i|í])':'k'
                     }

spanish_digraphs = {#True digraphs
                    'ch':'ʧ', 
                    'll':'ʎ', 
                    
                    #<c> and <g> have different realizations depending on the following vowel
                    'c(?=[e|é|i|í])':'θ',
                    'c(?=[a|á|o|ó|u|ú])':'k',
                    'g(?=[e|é|i|í])':'X',
                    
                    #Trill /r/: <rr> or <r> at beginning of words
                    #Capitalize in order to remain distinct from single tap <r> at first
                    'rr':'R',
                    '(^|\W+)r':'R',
                    
                    #Diphthongs 
                    '(?<=[a|á|e|é|o|ó|u|ú])i':'i̯',
                    '(?<=[a|á|e|é])u':'u̯',
                    #<Vy> at end of words (e.g. guay, rey, soy, muy)
                    '(?<=[a|e|o|u])y(?!\w)':'i̯', #e.g. <guay> 
                    
                    #Semivowels/glides
                    #Keep /j/ capitalized to avoid being converted to /x/
                    'i(?=[a|á|e|é|o|ó|u|ú])':'J',
                    'u(?=[a|á|e|é|i|í|o|ó])':'w'
                    }

pause_punctuation = ['.', ',', '!', '¡', '?', '¿', ':', ';', '—']

nasals = ['m', 'n', 'ɲ', 'ŋ']

voiced_obstruent_allophones = {'β':'b', 
                               'ð':'d', 
                               'ɣ':'ɡ', 
                               'ʝ':'ɟ͡ʝ'}

nasal_assimilation = {'p':'m',
                      'b':'m',
                      'f':'ɱ',
                      't':'n',
                      'd':'n',
                      'θ':'n',
                      's':'n',
                      'ʧ':'nʲ',
                      'ɟ':'ɲ',
                      'k':'ŋ',
                      'ɡ':'ŋ',
                      'x':'ŋ'}

voiced_consonants = {'b', 'β', 'd', 'ð', 'ɡ', 'ɣ', 'ɟ', 'ʝ', 
                     'm', 'ɱ', 'n', 'ɲ', 'ŋ', 
                     'l', 'ʎ', 'r', 'ɾ', 
                     'v', 'z'}


#%%
def es2ipa(text):
    """Converts an orthographic text to basic IPA"""
    
    text = text.lower()
    text = text.split()
    
    tr_text = []
    
    for word in text:
        #Transcription of trigraphs
        for trigraph in spanish_trigraphs:
            word = re.sub(trigraph, spanish_trigraphs[trigraph], word)
            
        #Transcription of digraphs
        for digraph in spanish_digraphs:
            word = re.sub(digraph, spanish_digraphs[digraph], word)
        
        #Transcription via single character replacement
        for ch in spanish_ipa:
            word = re.sub(ch, spanish_ipa[ch], word)
        
        #Lowercase everything again
        word = word.lower()
        
        #Add to list of transcribed words
        tr_text.append(word)
    
    text = ' '.join(tr_text)
    
    return text


def es_allophony(text):
    """Carries out several allophonic alternations"""
    
    #Convert fricatives back to stops (or affricate, in the case of /ɟ͡ʝ/)
    #when following nasals
    for fricative in voiced_obstruent_allophones:
        allophone = voiced_obstruent_allophones[fricative]
        for nasal in nasals:
            text = re.sub(f'{nasal}{fricative}', f'{nasal}{allophone}', text)
            text = re.sub(f'{nasal}\s+{fricative}', f'{nasal} {allophone}', text)
    
    #<d> is also /d/ following /l/
    text = re.sub('lð', 'ld', text)
    text = re.sub('l\s+ð', 'l d', text)
    
    #Do the same when appearing after a pause
    #Split the text into words
    text = text.split()
    for i in range(len(text)):
        word = list(text[i])
        if word[0] in voiced_obstruent_allophones:
            
            #If it is not the first word of the text, check whether the previous
            #word ends with pause-triggering punctuation
            #If so, change the fricative to its corresponding stop/affricate
            if i > 0:
                if text[i-1][-1] in pause_punctuation:
                    word[0] = voiced_obstruent_allophones[word[0]]
            
            #If it is the first word, no further checking is necessary,
            #change fricative to stop/affricate
            else:
                word[0] = voiced_obstruent_allophones[word[0]]
        text[i] = ''.join(word)
    text = ' '.join(text)
    
    #Assimilate nasals to place of articulation of following obstruents
    text = list(text)
    for i in range(len(text)-1):
        if text[i] in nasals:
            if text[i+1] in nasal_assimilation:
                text[i] = nasal_assimilation[text[i+1]]
    text = ''.join(text)
    
    #Assimilate /l/ to /lʲ/ preceding post-alveolar /ʧ/
    text = re.sub('l(?=ʧ)', 'lʲ', text)
    
    return text
        
    
def count_syllables(word, vowels=['a', 'e', 'i', 'o', 'u']):
    """Counts syllables in word"""
    return len([ch for ch in word if ch in vowels+['̩']]) - word.count('̯')    
    

def mark_stress(text):
    """Adds stress marking for polysyllabic words"""
    
    text = text.split()
    for i in range(len(text)):
        word = text[i]
        n_syllables = count_syllables(word)
        
        #Don't mark stress for monosyllabic words
        #Remove stress marking from monosyllabic words (e.g. <tú>, <qué>)
        if n_syllables < 2:
            text[i] = ''.join([ch for ch in word if ch != "ˈ"])
        
        #Mark stress for words with at least two syllables
        else:
            #Some words already have stress marked from orthographic accents
            if "ˈ" in word:
                pass
            else:
                #Determine the final segment of the word
                j = -1
                while word[j] in punctuation:
                    j -= 1
                    if abs(j) > len(word):
                        break
                    
                #Skip any words which may consist only of punctuation
                if abs(j) > len(word):
                    pass
                
                #Otherwise assign stress based on final segment
                else:
                    final_seg = word[j]
                    
                    #Words ending in vowels, /n/, and /s/ are stressed on the penultimate syllable
                    if final_seg in {'a', 'e', 'i', 'o', 'u', 'n', 's'}:
                        position = 2
                    
                    #Otherwise stress is on the final syllable
                    #(unless otherwise marked in orthography)
                    else:
                        position = 1
                    
                    #Iterate backwards through word, counting how many 
                    #syllable-bearing units have been encountered
                    #Stop iteration once the appropriate number of vowel positions
                    #have been encountered 
                    vowel_count = 0
                    for k in range(len(word)-1,-1,-1):
                        if word[k] in {'a', 'e', 'i', 'o', 'u'}:
                            vowel_count += 1
                        elif word[k] == '̯':
                            vowel_count -= 1
                        if vowel_count == position:
                            break
                    
                    #Add stress marking to the point where iteration ended
                    word = list(word)
                    word.insert(k, "ˈ")
                    word = ''.join(word)
                    text[i] = word
                    
    return ' '.join(text)


def strip_punctuation(text, punctuation=punctuation):
    """Removes punctuation characters"""
    return ''.join([ch for ch in text if ch not in punctuation])


def has_punctuation(text, punctuation=punctuation):
    """Returns True if the text includes any punctuation characters"""
    for ch in punctuation:
        if ch in text:
            return True
    return False


def fix_y(text):
    """Handles the idiosyncratic behavior of the Spanish word <y> 'and':
        /i/ before pauses and consonantal onsets
        /ʝ/ before vocalic onsets"""
    
    text = text.split()
    for i in range(len(text)):
        word = text[i]
        if strip_punctuation(word).strip() in ['ʝ', 'ɟ͡ʝ']:
            if has_punctuation(word) == True:
                text[i] = re.sub('[ɟ͡]*ʝ', 'i', word)
            else:
                try:
                    nxt_word = strip_punctuation(text[i+1])
                    try:
                        if nxt_word[0] not in {'a', 'e', 'i', 'o', 'u', 'ˈ'}:
                            text[i] = re.sub('[ɟ͡]*ʝ', 'i', word)
                        else:
                            text[i] = re.sub('[ɟ͡]*ʝ', 'ʝ', word)
                    except IndexError:
                        text[i] = re.sub('[ɟ͡]*ʝ', 'i', word)
                            
                except IndexError:
                    text[i] = re.sub('[ɟ͡]*ʝ', 'i', word)
                    
    return ' '.join(text)
        

def voicing_assimilation(text):
    """Voices /f, θ, s/ to /v, ð, z/ when preceding a voiced consonant"""
    
    for voiceless, voiced in zip(['f', 'θ', 's'], ['v', 'ð', 'z']):
        for voiced_consonant in voiced_consonants:
            text = re.sub(f'{voiceless}(?={voiced_consonant})', f'{voiced}', text)
    
    return text
    

def transcribe_es(text, yeismo=True, distincion=True, ceceo=False):
    """Produces a phonetic transcription of  Spanish text.
    Arguments yeismo, distincion, and ceceo control dialect-specific features.
    Default is Standard Peninsular Spanish.
    For Latin American Spanish, set distincion = False."""
    
    text = es2ipa(text)
    
    #Yeísmo: /ʎ/ --> /ʝ/
    if yeismo == True:
        text = re.sub('ʎ', 'ʝ', text)
    
    #Strengthen fricatives /β, ð, ʝ, ɣ/ into stops/affricates after nasals and pauses
    text = es_allophony(text)
    
    #Add lowered diacritics to /β, ð, ɣ/ to mark them as approximants
    text = re.sub('β', 'β̞', text)
    text = re.sub('ð', 'ð̞', text)
    text = re.sub('ɣ', 'ɣ̞', text)
    
    #Convert <y> "and" to /i/, or /ʝ/ when preceding vowels
    text = fix_y(text)

    #Add stress marking
    text = mark_stress(text)
    
    #Distinción (both /s/ and /θ/)
    #Seseo (all /s/), ceceo (all /s̄/, similar to /θ/)
    if distincion == False:
        text = re.sub('θ', 's', text)
    if ceceo == True:
        text = re.sub('s', 's̄', text)
        text = re.sub('θ', 's̄', text)
    
    #Fricative voicing assimilation: /f, θ, s/ --> /v, ð, z/
    text = voicing_assimilation(text)
    
    return text


#%%
#TO ADD:
#nasalization of vowels before syllable-final nasals
#retracted S in Peninsular Spanish
#dental t, d

