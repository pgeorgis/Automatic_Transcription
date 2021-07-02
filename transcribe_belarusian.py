#GRAPHEME-TO-PHONEME TRANSCRIPTION FOR BELARUSIAN
#Written by Philip Georgis (2021)
#Transcriptions primarily follow the conventions given in:
#"Illustrations of the IPA: Belarusian" (Bird & Litvin, 2020)

import re
from string import punctuation

#Note that Belarusian has unpredictable, mobile stress and thus stress can 
#only be marked in the IPA transcriptions when marked orthographically 
#using the '́' (accute accent) stress mark
#e.g. <галава́>
stress_mark = '́'

#Belarusian Cyrillic alphabet to basic IPA conversion
be_ipa_dict = {'а':'a',
               'б':'b',
               'в':'v',
               'г':'ʁ', 
               'д':'d', 
               'е':'ʲe',
               'ё':'ʲɵ',
               'ж':'ʐ', 
               'з':'z',
               'і':'ʲi',
               'й':'j', 
               'к':'k', 
               'л':'l', 
               'м':'m', 
               'н':'n', 
               'о':'o', 
               'п':'p', 
               'р':'r', 
               'с':'s', 
               'т':'t', 
               'у':'u',
               'ў':'w',
               'ф':'f', 
               'х':'x', 
               'ц':'ʦ',
               'ч':'ʧ', 
               'ш':'ʂ',
               'ы':'ɨ',
               'ь':'ʲ',
               'э':'ɛ',
               'ю':'ʲʉ',
               'я':'ʲæ'
               }

#List of Belarusian vowels
be_vowels = ['a', 'æ', 'ɛ', 'e', 'ɨ', 'i', 'o', 'ɵ', 'u', 'ʉ']


#Dictionary of voiced obstruents with their devoiced counterparts
be_devoicing_dict = {'b':'p',
                     'v':'f',
                     'ʁ':'ʁ̥',
                     'd':'t',
                     'ʐ':'ʂ',
                     'z':'s',
                     'ʣ':'ʦ',
                     'ʤ':'ʧ'}

#Dictionary of voiceless obstruents with their voiced counterparts
be_voicing_dict = {be_devoicing_dict[voiced]:voiced for voiced in be_devoicing_dict}


#List of Belarusian obstruents
be_obstruents = list(be_devoicing_dict.keys()) + list(be_voicing_dict.keys()) + ['k']


def be2ipa(text):
    """Performs preliminary conversion from Belarusian Cyrillic to IPA"""
    #Lower-case the text
    text = text.lower()
    
    #Remove punctuation
    text = ''.join([ch for ch in text if ch not in punctuation])
    
    #Convert two-character sequences first
    tr = re.sub('дз', 'ʣ', text)
    tr = re.sub('дж', 'ʤ', tr)
    
    #Then convert other single characters
    tr = ''.join([be_ipa_dict.get(ch, ch) for ch in tr])
    
    return tr


def be_palatalization(text):
    """Performs palatalization of relevant consonants"""
    
    #Most palatalization other than of <г, р> will already be marked from <ь, е, і, ю, я>
    #The palatalized equivalent of /ʁ/ <г> is /ɣʲ/
    tr = re.sub('ʁʲ', 'ɣʲ', text)
    #No palatalization of <р> /r/ in Belarusian, unlike Russian and Ukrainian
    tr = re.sub('rʲ', 'r', tr)
    
    #Ensure that sequences of two identical consonants, the latter of which is palatalized, 
    #are both palatalized
    new_tr = []
    for i in range(len(tr)):
        ch = tr[i]
        try:
            nxt_ch = tr[i+1]
            
            #Check whether the next character is the same as the current character
            if nxt_ch == ch:
                try:
                    #If so, check whether 2 characters ahead is /ʲ/, i.e. if the next character is palatalized
                    nxtnxt_ch = tr[i+2]
                    if nxtnxt_ch == 'ʲ':
                        #If so, also palatalize the current character
                        new_tr.append(ch)
                        new_tr.append('ʲ')
                    
                    #Otherwise don't change anything
                    else:
                        new_tr.append(ch)
                
                #If the following character is the last (and not palatalized), don't change anything
                except IndexError:
                    new_tr.append(ch)
            
            #If they aren't the same phoneme, then change nothing
            else:
                new_tr.append(ch)
        
        #If there is no next character, don't change anything
        except IndexError:
            new_tr.append(ch)
                
    #Change /ʲ/ at beginning of words to /j/
    tr = ''.join(new_tr)
    words = tr.split()
    final_tr = []
    for word in words:
        if word[0] == 'ʲ':
            final_tr.append('j'+word[1:])
        else:
            final_tr.append(word)
    
    #Join the split words back together
    tr = ' '.join(final_tr)
                
    return tr


def be_stress(text):
    """Adjusts stress marking (stress marking is required for this to work)"""
    
    #Reduce each word's vowels separately
    words = text.split()
    for w in range(len(words)):
        word = list(words[w])
        
        #Only mark stress in word where stress is marked orthographically
        if stress_mark in word:
            stressed_indices = []
        
            for i in range(len(word)):
                ch = word[i]
                if ch in be_vowels:
                    try:
                        #Check whether the following character is the stress marking
                        nxt = word[i+1]
                        
                        #If the vowel is stressed, add its index to list of stressed indices
                        if nxt == stress_mark:
                            stressed_indices.append(i)                                
                    
                    #If the current character is a vowel and it is not followed by 
                    #another character, this means it is not stressed: change nothing
                    except IndexError:
                        pass
        
            #Then iterate through stress indices and remove stress accent mark and
            #add preceding stress IPA diacritic instead
            for i in stressed_indices:
                word[i] = "ˈ" + word[i]
                word[i+1] = ''
            words[w] = ''.join([ch for ch in word if ch != ''])
            
    
    text = ' '.join(words)
    
    return text

def be_vowel_reduction(text):
    """Performs vowel reduction of /a/ to [ʌ] in pre-stressed syllables, not 
    immediately preceding the stressed syllable"""
    
    #Split the text into words
    words = text.split()
    
    #Check if each word has stress marking, otherwise don't try to reduce anything
    for w in range(len(words)):
        word = words[w]
        if "ˈ" in word:
            #Get the index of stress marking
            stress_index = word.index("ˈ")
            
            #Iterate backwards through the word and count the observed vowels
            vowel_indices = []
            vowel_count = 0
            for j in range(stress_index-1,-1,-1):
                ch = word[j]
                if ch in be_vowels:
                    vowel_count += 1
                    #If the vowel is /a/ and it was at least 2 vowels prior 
                    #to stress, save its index
                    if ch == 'a': #Note source is ambiguous about whether this also affects allophone [æ]
                        if vowel_count >= 2:
                            vowel_indices.append(j)
            
            #Reduce the vowels whose indices were saved to [ʌ]
            phones = list(word)
            for index in vowel_indices:
                phones[index] = 'ʌ'
            
            #Join the phones back together
            word = ''.join(phones)
            words[w] = word
    
    return ' '.join(words)


def adjust_soft_vowels(text):
    """Changes intervocalic /ʲ/ to /j/"""
    
    tr = list(text)
    for i in range(1, len(tr)):
        ch = tr[i]
        if ch == 'ʲ':
            try:
                prev_ch = tr[i-1]
                nxt_ch = tr[i+1]
                
                #If the /ʲ/ appears between two vowels, change it to /j/
                if ((prev_ch in be_vowels) and (nxt_ch in be_vowels)):
                    tr[i] = 'j'
                
                
            #No need to change anything if it is the final character of a word
            except IndexError:
                pass
    tr = ''.join(tr)
    return tr


def be_final_devoicing(text):
    """Performs word-final obstruent devoicing"""
    
    #Split the text into words
    words = text.split()
    
    #Iterate through the words and devoice the final sound, if possible
    for w in range(len(words)):
        word = words[w]
        phones = list(word)
        
        #If the final character is not "ʲ", directly try to devoice this character
        if phones[-1] != "ʲ":
            phones[-1] = be_devoicing_dict.get(phones[-1], phones[-1])
        
        #Otherwise try to devoice the character precending "ʲ"
        else:
            phones[-2] = be_devoicing_dict.get(phones[-2], phones[-2])
        
        words[w] = ''.join(phones)
    
    return ' '.join(words)


def be_obstruent_assimilation(text):
    """Performs voicing and palatalization assimilation on obstruent sequences"""
    
    #Split the text into characters
    text = list(text)
    
    #Iterate backwards through the text
    for i in range(len(text)-1,-1,-1):
        ch = text[i]
        
        #Check whether the current segment is an obstruent
        if ch in be_obstruents:
            
            #Try to find the next segment
            try:
                if text[i+1] != 'ʲ':
                    j = i+1
                else:
                    j = i+2
                nxt = text[j]
                
                #Check whether the next segment is an obstruent
                if nxt in be_obstruents:
                    
                    #If so, check whether it is voiced or voiceless
                    voiced = nxt in be_devoicing_dict.keys()
                    
                    #Assimilate voicing of current obstruent to next obstruent's voicing
                    if voiced == True:
                        text[i] = be_voicing_dict.get(ch, ch)
                    else:
                        text[i] = be_devoicing_dict.get(ch, ch)
                    
                    #Then check whether it is palatalized
                    try:
                        nxtnxt = text[j+1]
                        palatalized = nxtnxt == 'ʲ'
                        
                        #If the next segment is palatalized but the current segment is not,
                        #palatalize also the current segment
                        if palatalized == True:
                            if j == i+1:
                                
                                #But never palatalize the "hard" consonants
                                if ch not in ['ʂ', 'ʐ', 'ʧ', 'ʤ']:
                                    text.insert(j, 'ʲ')
                        
                    except IndexError:
                        pass
            
                    
            #If there is no following segment, change nothing
            except IndexError:
                pass
    
    return ''.join(text)
    


def transcribe_be(text):
    #Convert Belarusian Cyrillic into preliminary IPA
    step1 = be2ipa(text)
    
    #Perform extra palatalization steps
    step2 = be_palatalization(step1)
    
    #Mark stress if in orthography
    step3 = be_stress(step2)
    
    #Reduce /a/ vowels in pre-stress syllables
    step4 = be_vowel_reduction(step3)
    
    #Adjust representation of palatalizing vowels
    step5 = adjust_soft_vowels(step4)

    #Perform final obstruent devoicing
    step6 = be_final_devoicing(step5)
    
    #Perform obstruent voicing/palatalization assimilation
    step7 = be_obstruent_assimilation(step6)
    
    return step7



    