# Automatic Transcription
Automatic G2P (Grapheme-to-Phoneme) transcription and script conversion tools.
These programs take an orthographic (regular spelling) input in a given language and transcribe it into the International Phonetic Alphabet (IPA). Note that punctuation is preserved in certain, but not all, languages.

## Table of Contents
* [Supported Languages](#supported-languages)
* [General Examples](#general-examples)
* [Ukrainian, Belarusian, Bulgarian](#ukrainian-belarusian-bulgarian)
* [Spanish](#spanish)


# Supported Languages
G2P languages:
- Belarusian
- Bulgarian
- Classical Nāhuatl
- Czech
- Modern Greek
- Polish
- Slovak
- Spanish 
- Ukrainian

Script conversion:
- Serbo-Croatian (Serbian) Cyrillic/Latin conversion 

# General Examples
e.g. Given a Polish orthographic input text: 
>> text = "Cześć, nazywam się Filip. Przepraszam, nie mówię dobrze po polsku, ale chciałbym się nauczyć."

>> transcribe_pl(text, final_denasal=True)

't͡ʂɛɕʨ, naz̪ˈɨvam ɕɛ fʲˈilʲip. pʂɛpɾˈaʂam, ɲɛ mˈuvʲjɛ dˈɔbʐɛ pɔ pˈɔls̪ku, ˈalɛ xʨˈawbɨm ɕɛ naˈut͡ʂɨʨ.'

The text can be of any length, for example using a paragraph from the Nāhuatl Wikipedia:

>> paragraph = "In nāhuatlahtōlli ōpeuh tlahtohquih īca in caxtiltēcah īnhuāllāliz īpan in cematoc tlālli, īnāhuac in caxtillāntlahtōlli iuhqui yancuīc āchcāuh tlahtōlli īpan in Ānāhuac; tēl, in europanēcah, ōtlatequitilih in nāhuatlahtōlli īpampa in teōpixqueh ōtēpeuhqueh in tlācah, quimamah in nāhuatlahtōlli cānin tlein āchtopa ahmo motlahtōā nāhuatlāhtōlli."

>> transcribe_nahuatl(paragraph)

'in naːwat͡ɬaʔtoːlli oːpew t͡ɬaʔtoʔkiʔ iːka in kaʃtiɬteːkaʔ iːnwaːllaːlis iːpan in sematok t͡ɬaːlli, iːnaːwak in kaʃtillaːn̥t͡ɬaʔtoːlli iʍki jankʷiːk aːʧkaːw t͡ɬaʔtoːlli iːpan in aːnaːwak; teːl, in europaneːkaʔ, oːt͡ɬatekitiliʔ in naːwat͡ɬaʔtoːlli iːpam̥pa in teoːpiʃkeʔ oːteːpeʍkeʔ in t͡ɬaːkaʔ, kimamaʔ in naːwat͡ɬaʔtoːlli kaːnin t͡ɬein aːʧtopa aʔmo mot͡ɬaʔtoːaː naːwat͡ɬaːʔtoːlli.'

# Ukrainian, Belarusian, Bulgarian
In Ukrainian, Belarusian, and Bulgarian, stress must be marked orthographically with an accute accent in order for vowel reduction to be rendered:
>> uk_no_stress = "Північний вітер дув з усієї сили, але чим дужче він дув, тим щильніше кутався мандрівник у своє пальто."

>> transcribe_uk(uk_no_stress)

'pʲiʋnʲiʧnɪi̯ ʋʲitɛr duu̯ z usʲijɛji sɪɫɪ ɑɫɛ ʧɪm duʒʧɛ ʋʲin duu̯ tɪm ʃʧɪlʲnʲiʃɛ kutɑʋsʲɑ mɑndɾʲiʋnɪk u swɔjɛ pɑlʲtɔ'

>> uk_with_stress = "Півні́чний ві́тер дув з усіє́ї си́ли, а́ле чим ду́жче він дув, тим щильні́ше ку́тався мандрівни́к у своє́ пальто́."

>> transcribe_uk(uk_with_stress)

'pʲiʋnʲˈiʧnɪi̯ ʋʲˈitɛr duu̯ z ʊsʲijˈɛji sˈɪɫɪ ˈɑɫɛ ʧɪm dˈuʒʧɛ ʋʲin duu̯ tɪm ʃʧɪlʲnʲˈiʃɛ kˈutɐʋsʲɐ mɐndɾʲiʋnˈɪk u swɔjˈɛ pɐlʲtˈɔ'

# Spanish
The Spanish G2P functionality transcribes according to standard Peninsular Spanish by default:
>> spanish_text = "El sol demostró entonces al viento que la suavidad y el amor de los abrazos son más poderosos que la furia y la fuerza."

>> transcribe_es(spanish_text)

'el sol demostɾˈo entˈonθes al β̞jˈento ke la swaβ̞ið̞ˈað̞ ʝ el amˈoɾ ð̞e los aβ̞ɾˈaθos son mas poð̞eɾˈosos ke la fˈuɾja i la fwˈeɾθa.'

Latin American Spanish can be yielded by setting "distincion" to False:
>> transcribe_es(spanish_text, distincion=False)

'el sol demostɾˈo entˈonses al β̞jˈento ke la swaβ̞ið̞ˈað̞ ʝ el amˈoɾ ð̞e los aβ̞ɾˈasos son mas poð̞eɾˈosos ke la fˈuɾja i la fwˈeɾsa.'

Other dialectal features such as lack of yeísmo (neutralization of /ʎ/ and /ʝ/) and ceceo can also be transcribed via the "yeismo" and "ceceo" arguments (defaults: yeismo=True, ceceo=False).
