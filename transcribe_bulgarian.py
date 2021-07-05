#BULGARIAN GRAPHEME-TO-PHONEME CONVERSION
#Based on phonological descriptions in:
#'Bulgarian: Illustrations of the IPA' (Ternes & Vladimirova-Buhtz, 1990)
#'The Sound System of Standard Bulgarian' (Sabev, 2000)
#<http://www.personal.rdg.ac.uk/~llsroach/phon2/b_phon/b_phon.htm>
#Written by Philip Georgis (2021)

#Notes about limitations:
# 1) Bulgarian exhibits both variable stress and vowel reduction in unstressed syllables.
#   In order to yield the correct transcriptions, the orthographic form must be
#   annotated with stress, using the accute accent '́'.
#
# 2) Bulgarian verbs ending in stressed <a, я> are pronounced with the vowel
#   /ɤ/ instead of /a/, as if spelled with <ъ>. This G2P tool operates only 
#   on the orthography and has no way of recognizing the POS of input. Thus,
#   the transcription for such verbs would need to be corrected through some form
#   of post-processing.

import re
from string import punctuation
stress_mark = '́'

#Bulgarian Cyrillic alphabet to basic IPA conversion
bg_ipa_dict = {'а':'a',
               'б':'b',
               'в':'v',
               'г':'ɡ',
               'д':'d',
               'е':'ɛ',
               'ж':'ʒ',
               'з':'z',
               'и':'i',
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
               'щ':'ʃt',
               'ъ':'ɤ',
               'ь':'j',
               'ю':'ju',
               'я':'ja'}


#Lists and dictionaries of relevant Bulgarian segment types
bg_obstruents = ['p', 'b', 't', 'd', 'c', 'ɟ', 'k', 'ɡ', 
                 'ʦ', 'ʣ', 'ʧ', 'ʤ', 
                 'f', 'v', 's', 'z', 'ʃ', 'ʒ', 'x', 'ɣ']

bg_consonants = bg_obstruents + ['ɫ', 'l', 'm', 'n', 'r'] #not including /j/

bg_devoicing_dict = {'b':'p', 
                     'd':'t',
                     'ɡ':'k',
                     'ʣ':'ʦ',
                     'ʤ':'ʧ',
                     'v':'f',
                     'z':'s',
                     'ʒ':'ʃ',
                     'ɣ':'x'}

bg_voicing_dict = {bg_devoicing_dict[seg]:seg for seg in bg_devoicing_dict}
bg_voiced_obstruents = list(bg_devoicing_dict.keys())
bg_voiceless_obstruents = list(bg_devoicing_dict.values())

#Dictionary of vowels and their reduced equivalents
bg_vowel_reduction_dict = {'a':'ɐ', 'ɤ':'ɐ', 'ɔ':'o'}


def bg2ipa(text):
    """Performs preliminary conversion from Bulgarian Cyrillic to IPA"""
    #Lower-case the text
    text = text.lower()
    
    #Remove punctuation
    text = ''.join([ch for ch in text if ch not in punctuation])
    
    #Convert two-character sequences first
    tr = re.sub('дз', 'ʣ', text)
    tr = re.sub('дж', 'ʤ', tr)
    
    #Then convert other single characters
    tr = ''.join([bg_ipa_dict.get(ch, ch) for ch in tr])
    
    #Convert dark /ɫ/ to light /l/ before front vowels /i/ and /ɛ/
    tr = re.sub('ɫi', 'li', tr)
    tr = re.sub('ɫɛ', 'lɛ', tr)
    tr = re.sub('ɫj', 'lj', tr)
    
    return tr



def bg_vowel_reduction(text):
    """Marks stress in IPA and performs vowel reduction of 
    /a, ɤ, ɔ/ in unstressed syllables"""
    
    #First split the text into words
    words = text.split()
    
    #Then iterate through the list of words and reduce the vowels in each, if stress is marked
    tr = []
    for word in words:
        if stress_mark in word:
            tr_word = []
            stress_i = word.index(stress_mark)
            stressed_vowel_i = stress_i - 1
            for i in range(len(word)):
                ch = word[i]
                if i == stress_i:
                    pass
                elif i != stressed_vowel_i:
                    tr_word.append(bg_vowel_reduction_dict.get(ch, ch))
                else:
                    stressed_vowel = "ˈ" + word[stressed_vowel_i]
                    tr_word.append(stressed_vowel)
            tr.append(''.join(tr_word))
        
        #Don't reduce vowels if the stress is not marked for this word
        else:
            tr.append(word)
    
    return ' '.join(tr)
    

def bg_voicing_assimilation(text):
    """Devoices word-final obstruents and then regressively assimilates 
    sequences of obstruents according to the voicing of the final obstruent
    (except when the final obstruent is /v/)"""
    
    #First split the text into words
    words = text.split()
    
    #Iterate backwards through words of text and perform final devoicing 
    #and voicing assimilation on each, with voicing assimilation across word boundaries
    tr = []
    for j in range(len(words)-1,-1,-1):
        word = words[j]
        word_tr = list(word) 
        for i in range(len(word_tr)-1,-1,-1): 
            ch = word_tr[i] 
            if ch in bg_obstruents: 
                try:
                    nxt_ch = word_tr[i+1]
                    if nxt_ch in bg_obstruents:
                        if nxt_ch != 'v':
                            voicing = nxt_ch in bg_voiced_obstruents
                            if voicing == True:
                                word_tr[i] == bg_voicing_dict.get(ch, ch)
                            else:
                                word_tr[i] = bg_devoicing_dict.get(ch, ch)
                                
                #If the final segment of the word, try to assimilate voicing
                #with the first segment of the following word. 
                
                except IndexError:
                    try: 
                        nxt_word = words[j+1]
                        nxt_word_seg1 = nxt_word[0]
                        if nxt_word_seg1 in bg_obstruents:
                            if nxt_word_seg1 != 'v':
                                voicing = nxt_word_seg1 in bg_voiced_obstruents
                                if voicing == True:
                                    word_tr[i] == bg_voicing_dict.get(ch, ch)
                                else:
                                    word_tr[i] = bg_devoicing_dict.get(ch, ch)
                            
                    #If there is no following word in the text, then devoice.
                    except IndexError:
                        
                        #Unless the word is <в> /v/, then leaved voiced in citation form
                        if word != 'v':
                            word_tr[i] = bg_devoicing_dict.get(ch, ch)
                        else:
                            word_tr[i] = 'v'
                        
        tr.insert(0, ''.join(word_tr))
        
    return ' '.join(tr)


def bg_palatalization(text):
    """Performs palatalization of all consonants preceding /j/, /Cj/ --> /Cʲ/,
    and also of velar stops preceding the front vowels /i, ɛ/"""
    
    #First palatalize the velar stops before front vowels
    tr = re.sub('ki', 'kʲi', text)
    tr = re.sub('kɛ', 'kʲɛ', tr)
    tr = re.sub('ɡi', 'ɡʲi', tr)
    tr = re.sub('ɡɛ', 'ɡʲɛ', tr)
    
    #Then convert /j/ following consonants to /ʲ/
    palatalized = [tr[0]]
    if len(tr) > 1:
        for i in range(1, len(tr)):
            ch = tr[i]
            if ch == 'j':
                prev_ch = tr[i-1]
                if prev_ch in bg_consonants:
                    palatalized.append('ʲ')
                else:
                    palatalized.append('j')
            else:
                palatalized.append(ch)
    return ''.join(palatalized)
    
    

def transcribe_bg(text, palatalization=True):
    """If palatalization is set to True, /Cj/ sequences will be transcribed as
    palatalized rather than as sequences of a consonant followed by /j/;
    the velar stops /k/ and /ɡ/ will also be palatalized before front vowels"""
    
    #Step 1: Convert Bulgarian Cyrillic to basic IPA
    step1 = bg2ipa(text)
    
    #Step 2: Perform vowel reduction in unstressed syllables
    step2 = bg_vowel_reduction(step1)
    
    #Step 3: Perform regressive voicing assimilation on obstruents
    step3 = bg_voicing_assimilation(step2)
    
    if palatalization == True:
        step4 = bg_palatalization(step3)
        
        return step4
    
    else:
        return step3
    
    
    