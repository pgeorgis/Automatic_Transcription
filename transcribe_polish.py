#AUTOMATIC GRAPHEME-TO-PHONEME (G2P) TRANSCRIPTION: POLISH
#Written by Philip Georgis (2021)


#Mapping of Polish orthographic characters to IPA symbols
#Any characters not included here have identical IPA representation
polish_ipa = {'ą':'ɔ̃', 
              'c':'ʦ',
              'ć':'ʨ',
              'e':'ɛ',
              'ę':'ɛ̃',
              'g':'ɡ',
              'h':'x',
              'ł':'w',
              'ń':'ɲ',
              'o':'ɔ',
              'ó':'u',
              'r':'ɾ',
              'ś':'ɕ',
              'w':'v',
              'y':'ɨ',
              'ź':'ʑ',
              'ż':'ʐ'} 

#IPA transcriptions for digraphs or certain two-character sequences
polish_digraphs = {'ch':'x',
                   'cz':'t͡ʂ',
                   'dz':'ʣ',
                   'dź':'ʥ',
                   'dż':'d͡ʐ',
                   'ng':'ŋɡ',
                   'nk':'ŋk',
                   'rz':'ř', 
                   #although <rz> and <ż> are pronounced identically, <rz>
                   #exhibits different phonological behavior; thus we temporarily
                   #transcribe <rz> as /ř/ to preserve this distinction
                   'sz':'ʂ'}

#Mapping of voiced consonants to their voiceless counterparts
devoicing_dict = {'b':'p',
                  'd':'t',
                  'ʥ':'ʨ',
                  'ʣ':'ʦ',
                  'd͡ʐ':'t͡ʂ',
                  'g':'k',
                  'ɡ':'k',
                  'ř':'ʂ',
                  'v':'f',
                  'z':'s',
                  'ʐ':'ʂ',
                  'ʑ':'ɕ'}

#Mapping of voiceless consonants to their voiced counterparts
voicing_dict = {'ɕ':'ʑ',
                'f':'v',
                'k':'ɡ',
                'p':'b',
                'ř':'ʐ',
                's':'z',
                'ʂ':'ʐ',
                't':'d',
                'ʦ':'ʣ',
                'ʨ':'ʥ',
                't͡ʂ':'d͡ʐ'} 

#Mapping of consonants to their palatalized counterparts
palatal_dict = {'b':'bʲ',
                'd':'dʲ',
                'ʣ':'ʥ',
                'f':'fʲ',
                'ɡ':'ɡʲ',
                'k':'kʲ',
                'l':'lʲ',
                'm':'mʲ',
                'n':'ɲ',
                'p':'pʲ',
                'ɾ':'ɾʲ',
                's':'ɕ',
                't':'tʲ',
                'ʦ':'ʨ',
                'v':'vʲ',
                'x':'xʲ',
                'z':'ʑ'}

#Designate IPA characters as respective sound types 
#(vowels, consonants, obstruents, voiceless sounds, etc.)
pl_vowels = ['a', 'ɛ', 'i', 'ɔ', 'u', 'ɨ']

pl_consonants = ['b', 'ɕ', 'd', 'ʣ', 'ʥ', 'f', 'ɡ', 'j', 
                 'k', 'l', 'm', 'n', 'ɲ', 'ŋ', 'p', 'ɾ', 
                 'ř', 's', 'ʂ', 't', 'ʦ', 'ʨ', 'v', 'w', 
                 'x', 'z', 'ʑ', 'ʐ']

pl_obstruents = ['b', 'ɕ', 'd', 'ʣ', 'ʥ', 'f', 'ɡ', 'k', 
                 'p', 's', 'ʂ', 't', 'ʦ', 'ʨ', 'v', 'x', 
                 'z', 'ʑ', 'ʐ']

pl_plosives = ['b', 'd', 'ɡ', 'k', 'p', 't']

pl_fricatives = ['ɕ', 'f', 's', 'ʂ', 'v', 'x', 'z', 'ʑ', 'ʐ']

pl_affricates = ['ʣ', 'ʥ', 'd͡ʐ', 'ʦ', 'ʨ', 't͡ʂ']

plos_affr = pl_plosives + pl_affricates

pl_voiceless = ['ɕ', 'f', 'k', 'p', 's', 'ʂ', 't', 'ʦ', 'ʨ', 'x']


#Characters (spaces, punctuation, etc.) which mark the end of a word
ending = [' ', '.', ',', ';', ':', '!', '?', '[', ']', '(', ')', "'", '"'] 



def polish_g2p(text):
    """Converts an orthographic text to a basic IPA representation"""
    
    #Lowercase the text and split it into a list of words
    text = text.lower().split()
    
    #Iterate through words in the text and store their basic transcriptions in tr
    tr = []
    for word in text:
        w = [] #list of transcribed segments in the word
        
        #Iterate through the characters in the orthographic word
        i = 0
        while i < len(word):
            ch = word[i]
            
            #Check whether the current character plus the following character
            #form one of the designated digraphs, e.g. <ch>, <sz>, etc.
            try:
                digr = word[i:i+2]
                
                #If the characters do form a digraph, transcribe it accordingly
                #and skip the next character
                if digr in polish_digraphs:
                    w.append(polish_digraphs[digr])
                    i += 2
                
                #Otherwise transcribe only the single character
                else:
                    w.append(polish_ipa.get(ch, ch))
                    i += 1
            
            #If there is no following character, transcribe only the current character
            except IndexError:
                w.append(polish_ipa.get(ch, ch))
                i += 1
                
        #Add the fully transcribed word to the list of transcribed words
        tr.append(''.join(w))
    
    #Return the list of transcribed words as a single string
    return ' '.join(tr)



def pl_palatalization(text):
    """Carries out palatalization of consonants in the relevant context"""
    tr = []
    
    #Iterate through characters of the text
    i = 0
    while i < len(text):
        ch = text[i]
        
        #Check whether the current character can be palatalized
        if ch in palatal_dict:
            
            #If it can be palatalized, check whether <i> follows (context for palatalization)
            try:
                nxt = text[i+1]
                
                #If the next character is <i>, palatalize the consonant
                if nxt == 'i':
                    tr.append(palatal_dict[ch])
                    
                    #Check whether the character after <i> is another vowel
                    try:
                        nxtnxt = text[i+2]
                        
                        #If the character afer <i> is another vowel, 
                        #transcribe /j/ if the preceding unpalatalized consonant was not one of /n, s, ʦ, ʣ/
                        #then skip 2 indices ahead in order to not transcribe <i>
                        if nxtnxt in pl_vowels:
                            if ch not in ['ʦ', 'ʣ', 's', 'z', 'n']:
                                tr.append('j')
                            i += 2
                        
                        #Otherwise move only 1 index ahead in order to transcribe <i>
                        else:
                            i += 1
                    except IndexError:
                        i += 1
                
                #If <i> does not immediately follow, do not palatalized the character
                else:
                    tr.append(ch)
                    i += 1
            except IndexError:
                tr.append(ch)
                i += 1
        
        #If the current character cannot be palatalized, change nothing
        else:
            tr.append(ch)
            i += 1
            
    #Return the palatalized text as a string
    return ''.join(tr)



def nasalv_allophony(text, final_denasal=False):
    """Carries out context-dependent allophonic changes of nasal vowels;
    If final_denasal == True, word-final nasal vowels are denasalized."""
    
    #Split the text into words, iterate through words of the text
    text = text.split()
    tr = []
    for word in text:
        
        #Iterate through characters in the word
        i = 0
        w = []
        while i < len(word):
            ch = word[i]
            
            #Check whether the current character is a nasal diacritic
            if ch == '̃': #nasal diacritic
                try:
                    nxt = word[i+1]
                    
                    #Nasal vowels are realized as an oral vowel + nasal consonant
                    #when preceding plosives or affricates; the nasal consonant
                    #matches the following consonant in place of articulation
                    if nxt in plos_affr:
                        if nxt in ['p', 'b']:
                            w.append('m')
                        elif nxt in ['t', 'd', 'ʦ', 'ʣ']:
                            w.append('n')
                        elif nxt in ['ʨ', 'ʥ']:
                            w.append('ɲ')
                        elif nxt in ['k', 'ɡ']:
                            w.append('ŋ')
                        else:
                            print(f'Error: {nxt} has not been accounted for in nasal vowel allophony!')
                            raise TypeError
                        i += 1
                    
                    #/ɔ̃/ seems to be de-nasalized before /w/, but not /ɛ̃/;
                    #but both are realized as monophthongs in this position
                    elif nxt == 'w':
                        
                        #Add the nasal diacritic only if the vowel was /ɛ̃/
                        if word[i-1] == 'ɛ':
                            w.append(ch)
                        i += 1
                    
                    #If the underlying nasal vowel is not followed by a plosive,
                    #affricate, or /w/, then denasalize the vowel and add [w̃] to
                    #yield a nasal diphthong composed of an oral vowel and nasal semivowel
                    else:
                        w.append('w̃')
                        i += 1                            
                
                #If the nasal vowel is word-final, treat /ɛ̃/ and /ɔ̃/ separately
                except IndexError:
                    
                    #Only transcribe word-final /ɛ̃/ as [ɛw̃] if final_denasal == False
                    if word[i-1] == 'ɛ':
                        if final_denasal == False:
                            w.append('w̃')
                        i += 1 
                    
                    #/ɔ̃/ is always realized as a nasal diphthong [ɔw̃] word-finally
                    elif word[i-1] == 'ɔ':
                        w.append('w̃')
                        i += 1
                    
                    else:
                        print(f'Error: a phone other than /ɛ, ɔ/ (/{word[i-1]}/) is marked as nasalized!')
                        raise TypeError
            
            #Change nothing if the current character is not a nasal diacritic
            else:
                w.append(ch)
                i += 1
        
        #Add the transcribed word to the list of transcribed words
        tr.append(''.join(w))
        
    #Return the list of transcribed words as a single string
    return ' '.join(tr)



def voicing_assim1(text):
    """Carries out voicing assimilation to a following consonant"""
    tr = []
    
    #Iterate through characters of the text
    i = 0
    while i < len(text):
        ch = text[i]
        
        #Check whether the current character is an obstruent
        if ch in pl_obstruents:
            
            #Check whether the next character is also an obstruent
            #If so, check whether it is voiced or voiceless
            try:
                nxt = text[i+1]
                voice = False
                if nxt in pl_obstruents:
                    
                    #Check that the next character is not /v/
                    #/v/ does not trigger voicing assimilation
                    if nxt != 'v': 
                        if nxt not in pl_voiceless:
                            voice = True
                        
                        #Assimilate the current character to the voicing 
                        #of the following character
                        if voice == False:
                            tr.append(devoicing_dict.get(ch, ch))
                        elif voice == True:
                            tr.append(voicing_dict.get(ch, ch))
                        i += 1
                    
                    #Change nothing if the next character is /v/
                    else:
                        tr.append(ch)
                        i += 1
                        
                #Change nothing if the next character is not an obstruent or does not exist
                else:
                    tr.append(ch)
                    i += 1
            except IndexError:
                tr.append(ch)
                i += 1
        
        #Change nothing if the current character is not an obstruent
        else:
            tr.append(ch)
            i += 1
            
    #Return the transcribed text as a single string
    return ''.join(tr)
                    


def voicing_assim2(text):
    """Carries out voicing assimilation for <rz> and <w> to a preceding obstruent"""
    tr = []
    
    #Iterate through characters of the text
    i = 0
    while i < len(text):
        ch = text[i]
        
        #Check whether the current character is /ř/ or /v/ in non-initial position
        if i != 0:
            if ch in ['ř', 'v']:
                
                #If so, check whether the preceding character was an obstruent
                if text[i-1] in pl_obstruents:
                    
                    #If so, check whether this obstruent was voiced or voiceless
                    voice = True
                    if text[i-1] in pl_voiceless:
                        voice = False
                    
                    #Assimilate the /ř/ or /v/ to the voicing of the preceding obstruent
                    if voice == False:
                        tr.append(devoicing_dict.get(ch, ch))
                    else:
                        tr.append(voicing_dict.get(ch, ch))
                    i += 1
                
                
                #Change nothing if any of the above conditions were not met
                else:
                    tr.append(ch)
                    i += 1
            else:
                tr.append(ch)
                i += 1
        else:
            tr.append(ch)
            i += 1
    
    #Return the transcribed text as a single string
    return ''.join(tr)
            


def pl_finaldevoicing(text):
    """Carries out word-final devoicing"""
    tr = []
    
    #Iterate through words in the text
    text = text.split()
    for word in text:
        w = []
        
        #Iterate backwards from the end of the word, to locate the final consonant
        j = len(word) - 1
        while word[j] in ending: #ignore punctuation
            j -= 1
        
        #Iterate forwards through the characters of the word 
        i = 0
        while i < len(word):
            ch = word[i]
            
            #If the current character is at the index of the final consonant,
            #devoice the current character (if possible)
            if i == j:
                w.append(devoicing_dict.get(ch, ch))
                
            #Otherwise change nothing
            else:
                w.append(ch)
            i += 1
            
        #Add the new transcription to the list of transcribed words
        tr.append(''.join(w))        
    
    #Return the list of transcribed words as a single string
    return ' '.join(tr)



def fix_rz(text):
    """Changes transcription of <rz> from temporary /ř/ to /ʐ/"""
    tr = ''
    for ch in text:
        if ch == 'ř':
            tr += 'ʐ'
        else:
            tr += ch
    return tr


def nasal_lenition(text):
    """Performs lenition on /ɲ/, which becomes /j̃/ when preceding fricatives"""
    tr = text[0]
    if len(text) > 1:
        for i in range(1, len(text)):
            ch = text[i]
            if ch == 'ɲ':
                try:
                    nxt = text[i+1]
                    if nxt in pl_fricatives:
                        tr += 'j̃'
                    else:
                        tr += ch
                except IndexError:
                    tr += ch
            else:
                tr += ch
    return tr


def add_dental(text):
    """Adds dental diacritics to relevant consonants"""
    tr = ''
    for ch in text:
        tr += ch
        if ch in ['s', 'z', 'ʦ', 'ʣ']:
            tr += '̪'
    return tr



def add_stress(text):
    """Adds stress marking to the penultimate vowel of each word in the text"""
    tr = []
    
    #Split the text into words and iterate through the words 
    text = text.split()
    for word in text:
        
        #Split the word into a list of characters
        word = list(word)
        
        #Reverse the list of characters
        word.reverse()
        
        #Iterate through the backwards list of characters and count the number
        #of vowels encountered at each step
        w = []
        i = 0
        vowelcount = 0
        while i < len(word):
            ch = word[i]
            if ch in pl_vowels:
                vowelcount += 1
                
                #Once 2 vowels have been encountered, add stress marking 
                #to the second vowel (penultimate, as we iterate backwards)
                #and break iteration
                if vowelcount == 2:
                    w.append(ch)
                    w.append('ˈ')
                    break
                else:
                    w.append(ch)
                    i += 1
            else:
                w.append(ch)
                i += 1
        
        #If iteration was broken before reaching the beginning of the word,
        #add the rest of the transcription
        if i < (len(word) - 1):
            w.extend(word[i+1:])
        
        #Reverse the transcribed word
        w.reverse()
        
        #Add the transcribed word to the list of transcribed words
        tr.append(''.join(w))
        
    #Return the transcribed text as a single string
    return ' '.join(tr)
    

    
def transcribe_pl(text, final_denasal=False, stress=True):
    """If final_denasal == True, word-final <ę> is not transcribed as nasalized [depends on register];
    e.g. <jagnię> [jˈaɡɲɛw̃] vs. [jˈaɡɲɛ]
    If stress == True, stress annotation is included"""
    
    #Get basic IPA transcription
    step1 = polish_g2p(text)
    
    #Perform palatalization
    step2 = pl_palatalization(step1)
    
    #Carry out nasal vowel allophony
    step3 = nasalv_allophony(step2, final_denasal=final_denasal)
    
    #Devoice word final obstruents
    step4 = pl_finaldevoicing(step3)
    
    #Perform forward voicing assimilation (does not assimilate across word boundaries)
    step5 = voicing_assim1(step4)
    
    #Perform backward voicing assimilation
    step6 = voicing_assim2(step5)
    
    #Change representation of <rz> from temporary /ř/ to /ʐ/
    step7 = fix_rz(step6)
    
    #Perform nasal lenition
    step8 = nasal_lenition(step7)
    
    #Add dental diacritics
    step9 = add_dental(step8)
    
    #Optionally add stress marking
    if stress == True:
        step10 = add_stress(step9)
        return step10
    else:
        return step9

