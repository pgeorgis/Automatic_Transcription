#AUTOMATIC SERBIAN LATIN-CYRILLIC SCRIPT CONVERSION
#Written by Philip Georgis (2020)

import re


#DICTIONARIES OF CYRILLIC/LATIN CHARACTER EQUIVALENCIES 

cyrillic_latin_dict = {'А':'A',
                       'а':'a',
                       'Б':'B',
                       'б':'b',
                       'Ц':'C',
                       'ц':'c',
                       'Ч':'Č',
                       'ч':'č',
                       'Ћ':'Ć',
                       'ћ':'ć',
                       'Д':'D',
                       'д':'d',
                       'Џ':'Dž',
                       'џ':'dž',
                       'Ђ':'Đ',
                       'ђ':'đ',
                       'Е':'E',
                       'е':'e',
                       'Ф':'F',
                       'ф':'f',
                       'Г':'G',
                       'г':'g',
                       'Х':'H',
                       'х':'h',
                       'И':'I',
                       'и':'i',
                       'Ј':'J',
                       'ј':'j',
                       'К':'K',
                       'к':'k',
                       'Л':'L',
                       'л':'l',
                       'Љ':'Lj',
                       'љ':'lj',
                       'М':'M',
                       'м':'m',
                       'Н':'N',
                       'н':'n',
                       'Њ':'Nj',
                       'њ':'nj',
                       'О':'O',
                       'о':'o',
                       'П':'P',
                       'п':'p',
                       'Р':'R',
                       'р':'r',
                       'С':'S',
                       'с':'s',
                       'Ш':'Š',
                       'ш':'š',
                       'Т':'T',
                       'т':'t',
                       'У':'U',
                       'у':'u',
                       'В':'V',
                       'в':'v',
                       'З':'Z',
                       'з':'z',
                       'Ж':'Ž',
                       'ж':'ž',
                       
                       #Non-Serbian Cyrillic characters
                       #(Russian, Ukrainian, Belarusian, Bulgarian)
                       
                       #Soft sign --> apostrophe to mark palatalization
                       'Ь':"’", 
                       'ь':"’", 
                       
                       #Hard sign --> nothing 
                       #(also works for BG <ъ>, corresponds to deleted vowel in Serbian,
                       #e.g. BG <връх> = SR <врх>)
                       'Ъ':'', 
                       'ъ':'', 
                       
                       'Я':'Ja',
                       'я':'ja',
                       'Ё':'Jo',
                       'ё':'jo',
                       'Ю':'Ju',
                       'ю':'ju',
                       'Э':'E',
                       'э':'e',
                       'Щ':'ŠČ', #assumes Russian/Ukrainian transliteration scheme, from Bulgarian it would be 'št'
                       'щ':'šč',
                       'Й':'J',
                       'й':'j',
                       'І': 'I',
                       'і':'i',
                       'Ї':'Ji',
                       'ї':'ji',
                       'Є':'Je',
                       'є':'je',
                       'Ґ':'G',
                       'ґ':'g',
                       'Ў':'W',
                       'ў':'w'}

latin_cyrillic_dict = {'A': 'А',
                       'a': 'а',
                       'B': 'Б',
                       'b': 'б',
                       'C': 'Ц',
                       'c': 'ц',
                       'Č': 'Ч',
                       'č': 'ч',
                       'Ć': 'Ћ',
                       'ć': 'ћ',
                       'D': 'Д',
                       'd': 'д',
                       'Dž': 'Џ',
                       'dž': 'џ',
                       'Đ': 'Ђ',
                       'đ': 'ђ',
                       'E': 'Е',
                       'e': 'е',
                       'F': 'Ф',
                       'f': 'ф',
                       'G': 'Г',
                       'g': 'г',
                       'H': 'Х',
                       'h': 'х',
                       'I': 'И',
                       'i': 'и',
                       'J': 'Ј',
                       'j': 'ј',
                       'K': 'К',
                       'k': 'к',
                       'L': 'Л',
                       'l': 'л',
                       'Lj': 'Љ',
                       'lj': 'љ',
                       'M': 'М',
                       'm': 'м',
                       'N': 'Н',
                       'n': 'н',
                       'Nj': 'Њ',
                       'nj': 'њ',
                       'O': 'О',
                       'o': 'о',
                       'P': 'П',
                       'p': 'п',
                       'R': 'Р',
                       'r': 'р',
                       'S': 'С',
                       's': 'с',
                       'Š': 'Ш',
                       'š': 'ш',
                       'T': 'Т',
                       't': 'т',
                       'U': 'У',
                       'u': 'у',
                       'V': 'В',
                       'v': 'в',
                       'Z': 'З',
                       'z': 'з',
                       'Ž': 'Ж',
                       'ž': 'ж',
                       
                       #Non-native Latin characters
                       'Q': 'К',
                       'q': 'к',
                       'W': 'В',
                       'w': 'в',
                       'X': 'Кс',
                       'x': 'кс',
                       'Y': 'И',
                       'y': 'и'} #better to map 'y' to 'и' rather than to 'ј'

latin_digraph_dict = {'LJ':'Љ',
                      'Lj':'Љ',
                      'lj':'љ',
                      'NJ':'Њ',
                      'Nj':'Њ',
                      'nj':'њ',
                      'DŽ':'Џ',
                      'Dž':'Џ',
                      'dž':'џ',
                      
                      #Non-native digraphs which might appear in texts:
                      'QU':'КВ',
                      'Qu':'Кв',
                      'qu':'кв'}

def word_is_caps(word):
    """Returns True if a word consists of all uppercase letters (all caps)"""
    if word == word.upper():
        return True
    else:
        return False


def convert_to_latin(cyrillic_text):
    """Converts a Serbian Cyrillic text to Serbian Latin script"""
    
    #Split text by lines
    cyrillic_text = cyrillic_text.split('\n')
    
    #Segment the text into words, add a new line character
    cyrillic_text = [line.split() + ['\n'] for line in cyrillic_text]
    
    #Iterate through lines and words and transcribe each individually
    transcribed = []
    for line in cyrillic_text:
        for word in line:
            #Check whether the original word is all uppercase
            all_caps = word_is_caps(word)
            
            #Iterate through the characters of the word and transcribe each into Latin
            tr_word = []
            for ch in word:
                tr_word.append(cyrillic_latin_dict.get(ch, ch))
            
            #Join the characters of the transcribed word
            tr_word = ''.join(tr_word)
            
            #Palatalized segments with equivalents in Serbo-Croatian
            #Will already be partially converted to Latin characters
            palatal_segs = {"N’":'Nj', #Нь --> N’ --> Nj
                            "n’":'nj', #нь --> n’ --> nj
                            "L’":'Lj', #Ль --> L’ --> Lj
                            "l’":'lj', #ль --> l’ --> lj
                            "Č’":'Ć', #Чь --> Č’ --> Ć
                            "č’":'ć', #чь --> č’ --> ć
                            'C’':'Ć', #Ць --> C’ --> Ć
                            'c’':'ć', #ць --> c’ --> ć
                            "Dz’":'Đ', #Дзь --> Dz’ --> Đ
                            "dz’":'đ' #дзь --> dz’ --> đ
                            }
            
            #Convert non-Serbian Cyrillic palatalized segments into Serbian equivalents
            for seg in palatal_segs:
                tr_word = re.sub(seg, palatal_segs[seg], tr_word)
            
            #If the original word was all uppercase, ensure that transcribed
            #word is also all uppercase
            if all_caps == True:
                tr_word = tr_word.upper()
            
            #Add fully transcribed word to list of transcribed words
            transcribed.append(tr_word)
            
    #Return the words of the converted text joined by white spaces
    return ' '.join(transcribed)


def convert_to_cyrillic(latin_text):
    """Converts a Serbian Latin text to Serbian Cyrillic script"""
    
    #Split text by lines
    latin_text = latin_text.split('\n')
    
    #Segment the text into words, add a new line character
    latin_text = [line.split() + ['\n'] for line in latin_text]
    
    #Iterate through lines and words and transcribe each individually
    transcribed = []
    for line in latin_text:
        for word in line:
            tr_word = word[:]
            
            #Check if the word is all uppercase
            all_caps = word_is_caps(word)
            
            #Convert two-character sequences to Cyrillic first
            for digraph in latin_digraph_dict:
                tr_word = re.sub(digraph, latin_digraph_dict[digraph], tr_word)
                
            #Then convert remaining single characters to Cyrillic
            for ch in latin_cyrillic_dict:
                tr_word = re.sub(ch, latin_cyrillic_dict[ch], tr_word)
                        
            #Join together the transcribed characters
            tr_word = ''.join(tr_word)
            
            #If original word was fully uppercase, ensure that the transcribed word is also
            if all_caps == True:
                tr_word = tr_word.upper()
            
            #Add fully transcribed word to list of transcribed words
            transcribed.append(tr_word)
            
    #Return the words of the converted text joined by white spaces
    return ' '.join(transcribed)



def convert_text(text, source_script=None):
    """Converts text automatically in either direction"""
    """If source_script is unspecified (= None), the source script will be detected automatically"""
    
    #Keys for specifying the source script
    cyrillic = ['cyrillic', 'cyr', 'c', 'ćirilica', 'ć', 'ћирилица', 'ћир', 'ћ']
    latin = ['latin', 'lat', 'l', 'latinica', 'латиница', 'лат', 'л']
    cyrillic_keys = ', '.join([f'"{key}"' for key in cyrillic])
    latin_keys = ', '.join([f'"{key}"' for key in latin])
    
    #Try to automatically detect the source script if none is specified
    if source_script == None:
        
        #Determine proportions of characters belonging to each script
        cyrillic_count, latin_count = 0, 0
        count = len(text)
        for ch in text:
            if ch in cyrillic_latin_dict:
                cyrillic_count += 1
            elif ch in latin_cyrillic_dict:
                latin_count += 1
        cyrillic_count /= count
        latin_count /= count
        
        #Set the source as the script representing the majority of characters
        if cyrillic_count > latin_count:
            source = 'cyrillic'
        elif latin_count > cyrillic_count:
            source = 'latin'
        
        #If proportions of Latin and Cyrillic characters in text are equal, raise an error
        else:
            print('Error: unable to determine source script of text! Please specify:')
            print(f'Cyrillic: {cyrillic_keys}')
            print(f'Latin: {latin_keys}')
            raise TypeError
    
    #Otherwise use user-specified source script
    else:
        source = source_script
    
    #Convert the text according to specified or detected source script
    if source.lower() in cyrillic:
        return convert_to_latin(text)
    
    elif source.lower() in latin:
        return convert_to_cyrillic(text)
    
    else:
        print('Error: unrecognized script key. Please use one of the recognized keys:')
        print(f'Cyrillic: {cyrillic_keys}')
        print(f'Latin: {latin_keys}')




def main():
    text = input('Enter Serbo-Croatian text below:\n')
    print('\n')
    print(convert_text(text))
    
        
main()

