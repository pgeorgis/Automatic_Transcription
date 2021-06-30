#GRAPHEME-TO-PHONEME TRANSCRIPTION FOR UKRAINIAN
#Written by Philip Georgis (2021)
#Transcriptions primarily follow the conventions given in the following publications:
#"Illustrations of the IPA: Ukrainian" (Pompino-Marschall et al., 2017)
#and
#"Ukrainian vowel phones in the IPA context" (Vakulenko, 2018)

import re
from string import punctuation

#Note that due to stress-dependent vowel reduction in Ukrainian, this G2P conversion
#yields the correct transcriptions only when stress is marked in the orthographic form
#e.g. <голова́>, <язи́к>
stress_mark = '́'

#Ukrainian Cyrillic alphabet to basic IPA conversion
uk_ipa_dict = {'а':'ɑ',
               'б':'b',
               'в':'ʋ',
               'г':'ɦ', 
               'ґ':'ɡ', 
               'д':'d', 
               'е':'ɛ', 
               'є':'ʲɛ',
               'ж':'ʒ', 
               'з':'z', 
               'и':'ɪ', 
               'і':'ʲi', #used after consonants 
               'ї':'ji', #used after vowels 
               'й':'j', 
               'к':'k', 
               'л':'ɫ', 
               'м':'m', 
               'н':'n', 
               'о':'ɔ', 
               'п':'p', 
               'р':'r', 
               'с':'s', 
               'т':'t', 
               'у':'u', 
               'ф':'f', 
               'х':'x', 
               'ц':'ʦ',
               'ч':'ʧ', 
               'ш':'ʃ',
               'щ':'ʃʧ', 
               'ь':'ʲ',
               'ю':'ʲu',
               'я':'ʲɑ'
               }

#Characters (versions of apostrophe) which mark non-palatalization of preceding consonant
apostrophes = ["ʼ", "'", "’"]
punctuation = set(ch for ch in punctuation if ch not in apostrophes)

uk_vowels = ['ɑ', 'ɐ', 'ɛ', 'e', 'ɪ', 'i', 'ɔ', 'o', 'u', 'ʊ']

vowel_reduction_dict = {'ɑ':'ɐ',
                        'ɛ':'e',
                        'i':'e',
                        'ɔ':'o',
                        'u':'ʊ'}

uk_voiceless = ['k', 'p', 's', 't', 'f', 'x', 'ʦ', 'ʧ', 'ʃ']


def uk2ipa(text):
    """Performs preliminary conversion from Ukrainian Cyrillic to IPA"""
    #Lower-case the text
    text = text.lower()
    
    #Remove punctuation
    text = ''.join([ch for ch in text if ch not in punctuation])
    
    #Convert two-character sequences first
    tr = re.sub('дз', 'ʣ', text)
    
    #Then convert other single characters
    tr = ''.join([uk_ipa_dict.get(ch, ch) for ch in tr])
    
    return tr


def uk_palatalization(text):
    """Performs palatalization of relevant consonants"""
    
    #Most palatalization other than of <л, р> will already be marked from <ь, є, і, ю, я>
    #Change from dark /ɫ/ to light /l/
    tr = re.sub('ɫʲ', 'lʲ', text)
    #Change from trill to tap when palatalized
    tr = re.sub('rʲ', 'ɾʲ', tr)
    
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
                
    #Change /ʲi/ at beginning of words <і> to /i/
    #Change other /ʲ/ at beginning of words to /j/
    tr = ''.join(new_tr)
    words = tr.split()
    final_tr = []
    for word in words:
        if word[:2] == 'ʲi':
            final_tr.append(word[1:])
        elif word[0] == 'ʲ':
            final_tr.append('j'+word[1:])
        else:
            final_tr.append(word)
    
    #Join the split words back together
    tr = ' '.join(final_tr)
                
    return tr


def uk_allophony(text):
    """Carries out allophonic changes to phonemes <в> /ʋ/, <й> /j/, and г /ɦ/"""
    
    #Becomes [w] when preceding rounded back vowels [ɔ, u]
    text = re.sub('ʋɔ', 'wɔ', text)
    text = re.sub('ʋu', 'wu', text)
    
    #Becomes devoiced labio-velar approximant [ʍ] 
    #when preceding a voiceless consonant and not preceded by a vowel
    text = list(text)
    for i in range(len(text)):
        ch = text[i]
        if ch == 'ʋ':
            if ((i == 0) or (text[i-1] not in uk_vowels)):
                try:
                    nxt = text[i+1]
                    if nxt in uk_voiceless:
                        text[i] = 'ʍ'         
                except IndexError:
                    pass
    text = ''.join(text)
    
    #/ʋ/ becomes [u̯] word-finally, and /j/ becomes [i̯]
    words = text.split()
    for w in range(len(words)):
        word = words[w]
        word = re.sub('ʋ$', 'u̯', word)
        word = re.sub('j$', 'i̯', word)
        words[w] = word
    
    #/ɦ/ is devoiced to /x/ when preceding /k/
    text = ' '.join(words)
    text = re.sub('ɦk', 'xk', text)
    
    return text
    


def uk_vowel_reduction(text):
    """Performs first vowel reduction on vowels /ɑ, u/
    and adjusts stress marking (stress marking is required)"""
    
    #Reduce each word's vowels separately
    words = text.split()
    for w in range(len(words)):
        word = list(words[w])
        
        #Only reduce vowels in which stress is marked (i.e., don't reduce vowels in monosyllabic words)
        if stress_mark in word:
            stressed_indices = []
        
            for i in range(len(word)):
                ch = word[i]
                if ch in uk_vowels:
                    try:
                        #Check whether the following character is the stress marking
                        nxt = word[i+1]
                        
                        #If the vowel is stressed, do not reduce it and add its index to list
                        #of stressed indices
                        if nxt == stress_mark:
                            stressed_indices.append(i)
                        
                        #If not stressed, then reduce the vowel if it is one of /ɑ, u/
                        else:
                            if ch in ['ɑ', 'u']:
                                word[i] = vowel_reduction_dict.get(ch, ch)
                                
                    
                    #If the current character is a vowel and it is not followed by 
                    #another character, by default this means it is not stressed,
                    #so reduce it it is one of /ɑ, u/
                    except IndexError:
                        if ch in ['ɑ', 'u']:
                            word[i] = vowel_reduction_dict.get(ch, ch)
        
            #Then iterate through stress indices and remove stress accent mark and
            #add preceding stress IPA diacritic instead
            for i in stressed_indices:
                word[i] = "ˈ" + word[i]
                word[i+1] = ''
            reduced_word = [ch for ch in word if ch != '']       
    
            #Then iterate through the word again and check for stressed /u, i/
            #Unstressed /ɔ, ɛ/ reduce/harmonize to /o, e/ when preceding stressed /u, i/
            #Iterate backwards from start of stressed /u, i/ to locate immediately preceding 
            #/ɔ, ɛ/ and reduce these
            if "ˈu" in reduced_word:
                stressed_u = re.compile("ˈu")
                indices = [(m.start(0), m.end(0)) for m in re.finditer(stressed_u, ''.join(reduced_word))][0]
                start, end = indices
                for j in range(start-1,-1,-1):
                    if reduced_word[j] == 'ɔ':
                        reduced_word[j] = vowel_reduction_dict.get(reduced_word[j], reduced_word[j])
                        break
            
            elif "ˈi" in reduced_word:
                stressed_i = re.compile("ˈi")
                indices = [(m.start(0), m.end(0)) for m in re.finditer(stressed_i, ''.join(reduced_word))][0]
                start, end = indices
                for j in range(start-1,-1,-1):
                    if reduced_word[j] == 'ɛ':
                        reduced_word[j] = vowel_reduction_dict.get(reduced_word[j], reduced_word[j])
                        break
            
            words[w] = ''.join(reduced_word)
            
    
    text = ' '.join(words)
    
    return text


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
                if ((prev_ch in uk_vowels) and (nxt_ch in uk_vowels)):
                    tr[i] = 'j'
                
                #Or if the /ʲ/ appears after an apostrophe (marking non-palatalization of preceding consonant),
                #change to /j/
                elif prev_ch in apostrophes:
                    tr[i] = 'j'
                
            #No need to change anything if it is the final character of a word
            except IndexError:
                pass
    tr = ''.join(tr)
    return tr


def remove_apostrophe(text):
    """Remove apostrophes ("ʼ"), which mark that the preceding consonant is not palatalized"""
    
    return ''.join([ch for ch in text if ch not in apostrophes])


def transcribe_uk(text):
    #Convert Ukrainian Cyrillic into preliminary IPA
    step1 = uk2ipa(text)
    
    #Perform palatalization
    step2 = uk_palatalization(step1)
    
    #Perform allophonic changes to consonants
    step3 = uk_allophony(step2)
    
    #Perform vowel reduction
    step4 = uk_vowel_reduction(step3)
    
    #Adjust representation of palatalizing vowels
    step5 = adjust_soft_vowels(step4)

    #Remove non-palatalizing apostrophes
    step6 = remove_apostrophe(step5)
    
    return step6



    