#MODERN GREEK GRAPHEME-TO-PHONEME TRANSCRIPTION
#Written by Philip Georgis, 2021

import re

greek_ipa = {'α':'a',
             'β':'v',
             'γ':'ɣ',
             'δ':'ð',
             'ε':'e',
             'ζ':'z',
             'η':'i',
             'θ':'θ',
             'ι':'i',
             'κ':'k',
             'λ':'l',
             'μ':'m',
             'ν':'n',
             'ξ':'ks',
             'ο':'o',
             'π':'p',
             'ρ':'ɾ',
             'σ':'s',
             'ς':'s',
             'τ':'t',
             'υ':'i',
             'φ':'f',
             'χ':'x',
             'ψ':'ps',
             'ω':'o',
             
             #Accented vowels
             'ά':'ˈa',
             'έ':'ˈe',
             'ή':'ˈi',
             'ί':'ˈi',
             'ϊ':'i',
             'ΐ':'ˈi',
             'ό':'ˈo',
             'ύ':'ˈi',
             'ϋ':'i',
             'ώ':'ˈo'
             }

greek_digraphs = {'αι':'e',
                  'αί':'ˈe',
                  'αυ':'aw', #transcribed as /w/ in order to target it later for voicing assimilation to either /v/ or /f/
                  'αύ':'ˈaw',
                  'ει':'i',
                  'εί':'ˈi',
                  'ευ':'ew',
                  'εύ':'ˈew',
                  'οι':'i',
                  'οί':'ˈi',
                  'ου':'u',
                  'ού':'ˈu',
                  'υι':'i',
                  'υί':'ˈi',
                  
                  'μπ':'ᵐb',
                  'ντ':'ⁿd',
                  'γγ':'ᵑɡ',
                  'γκ':'ᵑɡ',
                  'γχ':'ŋx',
                  'τσ':'ʦ',
                  'τζ':'ʣ'}

gr_palatalization_dict = {#Phonemes palatalized before all front vowels 
                          'k':'c',
                          'ɡ':'ɟ',
                          'x':'ç',
                          'ɣ':'ʝ',
                          
                          #Phonemes palatalized before /jV/
                          'l':'ʎ',
                          'n':'ɲ',
                          'm':'mɲ'}

gr_voicing_dict = {'p':'b',
                   't':'d',
                   'c':'ɟ',
                   'k':'ɡ',
                   'ʦ':'ʣ'}


greek_phones = set(p for tr in list(greek_ipa.values()) + list(greek_digraphs.values()) + list(gr_palatalization_dict.values())
                   for p in tr)
gr_vowels = ['a', 'e', 'i', 'o', 'u']
gr_consonants = [p for p in greek_phones if p not in gr_vowels+['ˈ']]

gr_voiceless = ['p', 't', 'c', 'k', 'ʦ', 'f', 'θ', 's', 'ç', 'x']


def gr2ipa(text):
    #Lowercase the text
    text = text.lower()
    
    #Convert digraphs to IPA first
    for digraph in greek_digraphs:
        text = re.sub(digraph, greek_digraphs[digraph], text)
    
    #Then convert remaining single letters to IPA
    for letter in greek_ipa:
        text = re.sub(letter, greek_ipa[letter], text)
    
    return text


def greek_glides(text):
    #Convert /iV/ to /jV/
    text = list(text)
    for i in range(len(text)):
        ch = text[i]
        if ch == 'i':
            try:
                nxt = text[i+1]
                
                #Check if the next character is a vowel or stress marker (which indicates the following sound is a vowel)
                if nxt in gr_vowels + ["ˈ"]:
                    
                    #Check that the /i/ is not stressed and not word-initial
                    if i > 0:
                        prev = text[i-1]
                        if prev not in ["ˈ", " "]:
                            text[i] = 'j'
                    else:
                        pass
                    
            except IndexError:
                pass
            
    return ''.join(text)
        

def greek_palatalization(text, strong_palatalization=True):
    text = list(text)
    
    for i in range(len(text)):
        ch = text[i]
        
        #Check whether it is a sound which can be palatalized
        if ch in gr_palatalization_dict:
            
            try:
                nxt = text[i+1]
                if nxt == "ˈ":
                    nxt = text[i+2]
                
                #Palatalize velars before all front vowels and glides
                if ch not in ['l', 'm', 'n']: 
                    if nxt in ['i', 'e', 'j']:
                        text[i] = gr_palatalization_dict[ch]
                        
                
                
                else:
                    
                    if strong_palatalization == True:
                    #Palatalize /l, n/ before /i, j/ and /m/ only before /j/
                        if ch != 'm':
                            if nxt in ['i', 'j']:
                                text[i] = gr_palatalization_dict[ch]
                        else:
                            if nxt == 'j':
                                text[i] = gr_palatalization_dict[ch]
                                
                    else:
                        #Otherwise, palatalize /l, m, n/ only before /j/
                        if nxt == 'j':
                            text[i] = gr_palatalization_dict[ch]
                
            except IndexError:
                pass
            

    #Remove redundant /j/
    text = ''.join(text)
    palatalized = list(gr_palatalization_dict.values())
    for p in palatalized:
        text = re.sub(f'{p}j', f'{p}', text)
    
    #Glide hardening: turn remaining /j/ into /ʝ/ or /ç/ according to preceding consonant
    text = list(text)
    for i in range(len(text)):
        ch = text[i]
        
        if ch == 'j':
            prev_ch = text[i-1]
            if prev_ch in gr_voiceless:
                text[i] = 'ç'
                
            #Exception */CɾjV/ --> /CɾiV/
            elif prev_ch == 'ɾ':
                if i > 1:
                    prev_prev_ch = text[i-2]
                    if prev_prev_ch in gr_consonants:
                        text[i] = 'i'
                    else:
                        text[i] = 'ʝ'
                else:
                    text[i] = 'ʝ'
            
            else:
                text[i] = 'ʝ'
    text = ''.join(text)
            
    return text
            
            
def voicing_assimilation(text):
    text = list(text)
    
    for i in range(len(text)):
        ch = text[i]
        
        #Change <w> from <aυ/ευ> to either /v/ or /f/, depending on voicing context 
        if ch == 'w':
            try:
                nxt = text[i+1]
                if nxt in gr_voiceless:
                    text[i] = 'f'
                
                else:
                    text[i] = 'v'
            
            #If word final, convert it to /f/
            except IndexError:
                text[i] = 'f'

        
        #Voice /s/ to /z/ when followed by a voiced consonant
        elif ch == 's':
            try:
                nxt = text[i+1]
                if nxt in gr_consonants:
                    if nxt not in gr_voiceless:
                        text[i] = 'z'
            
            except IndexError:
                pass
        
    return ''.join(text)


def gemination_reduction(text):
    if len(text) > 0:
        reduced_text = [text[0]]
        for i in range(1, len(text)):
            ch = text[i]
            if ch in gr_consonants:
                prev_ch = text[i-1]
                if ch != prev_ch:
                    reduced_text.append(ch)
            else:
                reduced_text.append(ch)
        return ''.join(reduced_text)
    else:
        return text
    

def denasalize_plosives(text):
    #Split text into words
    words = text.split()
    
    for i in range(len(words)):
        word = words[i]
        if word[0] in ['ᵐ', 'ⁿ', 'ᵑ']:
            words[i] = word[1:]
    text = ' '.join(words)
    return text


def word_boundary_voicing(text):
    #Split text into words
    words = text.split()
    
    for i in range(len(words)-1, 0, -1):
        word = words[i]
        prev_word = words[i-1]
        if prev_word in ['tin', 'ton', 
                         'stin', 'ston',
                         'aftˈin', 'aftˈon',
                         'ðen', 'min']:
            if word[0] in gr_voicing_dict:
                word = list(word)
                word[0] = gr_voicing_dict[word[0]]
                
                #Revoice <ξ, ψ> to /ɡz, bz/
                if len(word) > 1:
                    if word[0] in ['b', 'ɡ']:
                        if word[1] == 's':
                            word[1] = 'z'
                
                words[i] = ''.join(word)
                words[i-1] = prev_word[:-1]
    
    return ' '.join(words)
                
        
def transcribe_gr(text, strong_palatalization=True):
    #Step 1: Basic conversion to IPA
    text = gr2ipa(text)
    
    #Step 2: /iV/ --> /jV/
    text = greek_glides(text)
    
    #Step 3: Voicing assimilation of <w> and /s/
    text = voicing_assimilation(text)
    
    #Step 4: Reduce geminate consonants
    text = gemination_reduction(text)
    
    #Step 5: Palatalization and glide hardening
    #If strong_palatalization == True, /l, n/ are also palatalized to /ʎ, ɲ/ before /i/
    text = greek_palatalization(text, strong_palatalization)
    
    #Step 6: Denasalization of word-initial voiced plosives
    text = denasalize_plosives(text)
    
    #Step 7: Revoice plosives across word boundaries following certain grammatical words
    text = word_boundary_voicing(text)
    
    #Retract all /s, z/ sounds
    text = re.sub('s', 's̠', text)
    text = re.sub('z', 'z̠', text)
    
    return text

    