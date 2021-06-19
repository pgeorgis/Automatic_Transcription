#AUTOMATIC GRAPHEME-TO-PHONEME (G2P) TRANSCRIPTION: CZECH
#Written by Philip Georgis (2021)

#Mapping of Czech orthographic characters to IPA symbols
#Any characters not included here have identical IPA representation
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
             #'ř':'r̝',
             'š':'ʃ',
             'ť':'c',
             'w':'v',
             'x':'ks',
             'ž':'ʒ'}


cz_digraphs = {'au':'au̯',
               'eu':'ɛu̯',
               'ou':'ou̯',
               'ch':'x',
               'dz':'ʣ',
               'dž':'ʤ',
               'qu':'kv',
               'nk':'ŋk',
               'ng':'ŋɡ'}

#Characters which undergo palatalization before <i>, <í>, <ě>
cz_palatal_dict = {'d':'ɟ',
                   't':'c',
                   'n':'ɲ'} 

cz_obstruents = ['b', 'c', 'd', 'f', 'ɡ', 'k', 'p', 's', 't', 'v', 'x', 'z',
                 'ɟ', 'ɦ', 'ʃ', 'ʒ', 'ʦ', 'ʧ', 'ř', 'ʣ', 'ʤ']

cz_consonants = cz_obstruents + ['m', 'n', 'ɲ', 'ŋ', 'r', 'l', 'j']

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
                     'ř':'ř̊'} #includes voiceless diacritic above for ř

cz_voicing_dict = {cz_devoicing_dict[phone]:phone for phone in cz_devoicing_dict}

cz_voiceless = list(cz_voicing_dict.keys())

cz_vowels = ['a', 'i', 'ɛ', 'ɪ', 'o', 'u']

#Characters (spaces, punctuation, etc.) which mark the end of a word
ending = [' ', '.', ',', ';', ':', '!', '?', '[', ']', '(', ')', "'", '"']

def cz_g2p(text):
    text = text.lower()
    text = text.split()
    tr = []
    for word in text:
        w = []
        i = 0
        while i < len(word):
            ch = word[i]
            try:
                digr = word[i:i+2]
                if digr in cz_digraphs:
                    w.append(cz_digraphs[digr])
                    i += 2
                else:
                    w.append(czech_ipa.get(ch, ch))
                    i += 1
            except IndexError:
                w.append(czech_ipa.get(ch, ch))
                i += 1
        tr.append(''.join(w))
    return ' '.join(tr)



def palatalize_cz(text):
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch not in cz_palatal_dict:
            tr.append(ch)
        else:
            try:
                nxt = text[i+1]
                if nxt in ['ě', 'i', 'ɪ']:
                    tr.append(cz_palatal_dict[ch])
                else:
                    tr.append(ch)
            except IndexError:
                tr.append(ch)
    new_tr = []
    for i in range(len(tr)):
        ch = tr[i]
        if ch in ['y', 'ý']:
            if ch == 'y':
                new_tr.append('ɪ')
            else:
                new_tr.append('iː')
        elif ch == 'ě':
            if tr[i-1] in ['m', 'b', 'p', 'f', 'v']:
                if tr[i-1] == 'm':
                    new_tr.append('ɲɛ')
                else:
                    new_tr.append('jɛ')
            else:
                new_tr.append('ɛ')
        else:
            new_tr.append(ch)      
    return ''.join(new_tr)


def final_devoicing(text):
    tr = []
    text = text.split()
    for word in text:
        i = 0
        w = []
        j = len(word) - 1
        while word[j] in ending:
            j -= 1
        while i < len(word):
            ch = word[i]
            if i != j:
                w.append(ch)
            else:
                w.append(cz_devoicing_dict.get(ch, ch))
            i += 1
        tr.append(''.join(w))        
    return ' '.join(tr)    

def syllabify(text):
   #if beginning of word and next ch is consonant
   #if end of word and previous ch is consonant
   #if surrounded by consonants
    tr = []
    text = text.split()
    syllabics = ['r', 'l', 'm', 'n']
    for word in text:
        w = []
        for i in range(len(word)):
            ch = word[i]
            w.append(ch)
            if ch in syllabics:
                if i == 0:
                    try:
                        nxt = word[i+1]
                        if nxt in cz_consonants:
                            if ((ch in ['m', 'n']) and (nxt in ['m', 'n', 'l', 'r', 'ɲ'])):
                                continue
                            else:
                                w.append('̩') #syllabic diacritic
                        else:
                            continue
                    except IndexError:
                        w.append('̩') #in case of words consisting of only a possibly syllabic consonant, make it syllabic
                else:
                    if word[i-1] in cz_consonants:
                        try:
                            nxt = word[i+1]
                            if nxt in cz_consonants:
                                if ((ch in ['m', 'n']) and (nxt in ['m', 'n', 'l', 'r', 'ɲ'])):
                                    continue
                                else:
                                    w.append('̩')
                            else:
                                continue
                        except IndexError:
                            w.append('̩')
                    else:
                        continue
        tr.append(''.join(w))
    return ' '.join(tr)


def cz_voice_assim(text):
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch in cz_obstruents:
            try:
                nxt = text[i+1]
                voice = False
                if nxt in cz_obstruents:
                    if nxt not in ['v', 'ř']:
                        if nxt not in cz_voiceless:
                            voice = True
                        if voice == False:
                            tr.append(cz_devoicing_dict.get(ch, ch))
                        elif voice == True:
                            tr.append(cz_voicing_dict.get(ch, ch))
                    else:
                        tr.append(ch)
                else:
                    tr.append(ch)
            except IndexError:
                tr.append(ch)
        else:
            tr.append(ch)
    new_tr = [tr[0]]
    for i in range(1, len(tr)):
        ch = tr[i]
        if ch == 'ř':
            prev = tr[i-1]
            if prev in cz_voiceless:
                new_tr.append(cz_devoicing_dict[ch])
            else:
                new_tr.append(ch)
        else:
            new_tr.append(ch)
    return ''.join(new_tr)

def fix_chs(text):
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch == 'ř':
            tr.append('r̝')
        elif ch == 't':
            try:
                nxt = text[i+1]
                if nxt in ['ʦ', 'ʧ']:
                    continue #don't add /t/ if it is followed by these affricates
                else:
                    tr.append(ch)
            except IndexError:
                tr.append(ch)
        else:
            tr.append(ch)
    return ''.join(tr)

def add_stress(text):
    tr = []
    text = text.split()
    for word in text:
        w = []
        i = 0
        while i < len(word):
            ch = word[i]
            if ch in cz_vowels:
                w.append('ˈ')
                break
            elif ch in ['r', 'l']:
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
    return ' '.join(tr)
            
            

def transcribe_cz(text, stress=True):
    step1 = cz_g2p(text)
    step2 = palatalize_cz(step1)
    step3 = final_devoicing(step2)
    step4 = cz_voice_assim(step3)
    step5 = syllabify(step4)
    step6 = fix_chs(step5)
    if stress == True:
        step7 = add_stress(step6)
        return step7
    else:
        return step6

