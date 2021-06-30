#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  8 15:30:56 2020

@author: phgeorgis
"""

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


sk_digraphs = {'ia':'ɪ̯a',
               'ie':'ɪ̯ɛ',
               'iu':'ɪ̯u',
               'au':'au̯',
               'eu':'ɛu̯',
               'ou':'ɔʊ̯',
               'ch':'x',
               'dz':'ʣ',
               'dž':'ʤ',
               'qu':'kv',
               'nk':'ŋk',
               'ng':'ŋɡ',
               'mf':'ɱf',
               'mv':'ɱv'}

sk_palatal_dict = {'d':'ɟ',
                   't':'c',
                   'n':'ɲ', 
                   'l':'ʎ'}

sk_obstruents = ['b', 'c', 'd', 'f', 'ɡ', 'k', 'p', 's', 't', 'v', 'x', 'z',
                 'ɟ', 'ɦ', 'ʃ', 'ʒ', 'ʦ', 'ʧ', 'ʣ', 'ʤ']

sk_consonants = sk_obstruents + ['m', 'n', 'ɲ', 'ŋ', 'r', 'ɫ', 'ʎ', 'j', 'ʋ']

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

sk_voicing_dict = {sk_devoicing_dict[phone]:phone for phone in sk_devoicing_dict}

sk_voiceless = list(sk_voicing_dict.keys())

sk_vowels = ['a', 'i', 'ɛ', 'æ', 'ɔ', 'u', 'ʊ', 'ɪ']

ending = [' ', '.', ',', ';', ':', '!', '?', '[', ']', '(', ')', "'", '"']

def sk_g2p(text):
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
                if digr in sk_digraphs:
                    w.append(sk_digraphs[digr])
                    i += 2
                else:
                    w.append(slovak_ipa.get(ch, ch))
                    i += 1
            except IndexError:
                w.append(slovak_ipa.get(ch, ch))
                i += 1
        tr.append(''.join(w))
    return ' '.join(tr)



def palatalize_sk(text):
    tr = []
    text = text.split()
    exceptions = ['jɛdɛn', 'tɛn', 'tɛlɛfɔːn'] #words that don't follow the palatalization rule
    #how to deal with inflections of these words?
    for word in text:
        if word not in exceptions:
            w = []
            for i in range(len(word)):
                ch = word[i]
                if ch not in sk_palatal_dict:
                    w.append(ch)
                else:
                    try:
                        nxt = word[i+1]
                        if nxt in ['ɛ', 'i', 'ɪ']:
                            w.append(sk_palatal_dict[ch])
                        else:
                            w.append(ch)
                    except IndexError:
                        w.append(ch)
            tr.append(''.join(w))
        else:
            tr.append(word)
    tr = ' '.join(tr)
    new_tr = []
    for i in range(len(tr)):
        ch = tr[i]
        if ch in ['y', 'ý']:
            if ch == 'y':
                new_tr.append('i')
            else:
                new_tr.append('iː')
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
                if ch == 'v':
                    if word == 'v':
                        w.append('v')
                    elif word[i-1] in sk_consonants:
                        w.append('ʋ')
                    else:
                        w.append('ʊ̯')
                else:    
                    w.append(sk_devoicing_dict.get(ch, ch))
            i += 1
        tr.append(''.join(w))        
    return ' '.join(tr)    

def syllabify(text):
    tr = []
    text = text.split()
    syllabics = ['r', 'ɫ']
    for word in text:
        w = []
        for i in range(len(word)):
            ch = word[i]
            w.append(ch)
            if ch in syllabics:
                if i == 0:
                    try:
                        nxt = word[i+1]
                        if nxt in sk_consonants:
                            w.append('̩') #syllabic diacritic
                        else:
                            continue
                    except IndexError:
                        w.append('̩') #in case of words consisting of only a possibly syllabic consonant, make it syllabic
                else:
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
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch in sk_obstruents:
            try:
                nxt = text[i+1]
                voice = False
                if nxt in sk_obstruents:
                    if nxt != 'v':
                        if nxt not in sk_voiceless:
                            voice = True
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
    tr = []
    for i in range(len(text)):
        ch = text[i]
        if ch == 't':
            try:
                nxt = text[i+1]
                if nxt in ['ʦ', 'ʧ']:
                    continue #don't add /t/ if it is followed by these affricates
                else:
                    tr.append(ch)
            except IndexError:
                tr.append(ch)
        elif ch == 'v':
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

def count_syllables(word):
    syl_count = 0
    for i in range(len(word)):
        ch = word[i]
        if ch in sk_vowels:
            try:
                nxt = word[i+1]
                if nxt != '̯':
                    syl_count += 1
            except IndexError:
                syl_count += 1
        else:
            try:
                nxt = word[i+1]
                if nxt == '̩':
                    syl_count += 1
            except IndexError:
                pass
    return syl_count
        

def add_stress(text):
    tr = []
    text = text.split()
    for word in text:
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
    step1 = sk_g2p(text)
    step2 = palatalize_sk(step1)
    step3 = final_devoicing(step2)
    step4 = sk_voice_assim(step3)
    step5 = syllabify(step4)
    step6 = fix_chs(step5)
    if stress == True:
        step7 = add_stress(step6)
        return step7
    else:
        return step6