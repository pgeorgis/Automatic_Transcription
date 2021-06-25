#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 08:41:27 2020

@author: phgeorgis
"""

nahuatl_ipa = {'ā':'aː',
               'ē':'eː',
               'ī':'iː',
               'ō':'oː',
               'y':'j',
               'z':'s',
               'x':'ʃ',
               'h':'ʔ',
               'c':'k'
               }

nahuatl_digraphs = {'cu':'kʷ',
                    'uc':'kʷ',
                    'tl':'t͡ɬ',
                    'hu':'w',
                    'uh':'w',
                    'ch':'ʧ',
                    'tz':'ʦ',
                    'qu':'k',
                    'ce':'se',
                    'cē':'seː',
                    'ci':'si',
                    'cī':'siː',
                    'ca':'ka',
                    'cā':'kaː',
                    'co':'ko',
                    'cō':'koː'}

nahuatl_voiceless_consonants = ['p', 't', 'k', 'ʔ', 's', 'ʃ', 'ʧ', 'ʦ', 'h', 't͡ɬ']

nahuatl_devoicing = {'m':'m̥',
                     'n':'n̥',
                     'l':'ɬ',
                     'j':'ʃ',
                     'w':'ʍ'}

def transcribe_nahuatl(text):
    text = text.lower()
    tr = []
    i = 0
    while i < len(text):
        ch = text[i]
        try:
            nxt = text[i+1]
            digraph = f'{ch}{nxt}'
            if digraph in nahuatl_digraphs:
                tr.append(nahuatl_digraphs[digraph])
                i += 2
            else:
                tr.append(nahuatl_ipa.get(ch, ch))
                i += 1
        except IndexError:
            tr.append(nahuatl_ipa.get(ch, ch))
            i += 1
    devoiced_tr = []
    for i in range(len(tr)):
        ch = tr[i]
        if ch in nahuatl_devoicing:
            try:
                nxt = tr[i+1]
                if nxt in nahuatl_voiceless_consonants:
                    devoiced_tr.append(nahuatl_devoicing[ch])
                else:
                    devoiced_tr.append(ch)
            except IndexError:
                devoiced_tr.append(nahuatl_devoicing[ch])
        else:
            devoiced_tr.append(ch)
    return ''.join(devoiced_tr)