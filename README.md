# Automatic_Transcription
Automatic G2P (Grapheme-to-Phoneme) transcription and script conversion tools.
These programs take an orthographic (regular spelling) input in a given language and transcribe it into the International Phonetic Alphabet (IPA). Note that punctuation is preserved in certain, but not all, languages.

Supported G2P languages:
- Classical Nāhuatl
- Czech
- Polish
- Ukrainian

Script conversion:
- Serbo-Croatian (Serbian) Cyrillic/Latin conversion 

Examples of G2P functionality:
e.g. Given a Polish orthographic input text: 
>> text = "Cześć, nazywam się Filip. Przepraszam, nie mówię dobrze po polsku."

>> transcribe_pl(text, final_denasal=True)

't͡ʂɛɕʨ, naz̪ˈɨvam ɕɛ fʲˈilʲip. pʂɛpɾˈaʂam, ɲɛ mˈuvʲjɛ dˈɔbʐɛ pɔ pˈɔls̪ku.'

The text can be of any length, for example using a paragraph from the Nāhuatl Wikipedia:

>> paragraph = "In nāhuatlahtōlli ōpeuh tlahtohquih īca in caxtiltēcah īnhuāllāliz īpan in cematoc tlālli, īnāhuac in caxtillāntlahtōlli iuhqui yancuīc āchcāuh tlahtōlli īpan in Ānāhuac; tēl, in europanēcah, ōtlatequitilih in nāhuatlahtōlli īpampa in teōpixqueh ōtēpeuhqueh in tlācah, quimamah in nāhuatlahtōlli cānin tlein āchtopa ahmo motlahtōā nāhuatlāhtōlli."

>> transcribe_nahuatl(paragraph)

'in naːwat͡ɬaʔtoːlli oːpew t͡ɬaʔtoʔkiʔ iːka in kaʃtiɬteːkaʔ iːnwaːllaːlis iːpan in sematok t͡ɬaːlli, iːnaːwak in kaʃtillaːn̥t͡ɬaʔtoːlli iʍki jankʷiːk aːʧkaːw t͡ɬaʔtoːlli iːpan in aːnaːwak; teːl, in europaneːkaʔ, oːt͡ɬatekitiliʔ in naːwat͡ɬaʔtoːlli iːpam̥pa in teoːpiʃkeʔ oːteːpeʍkeʔ in t͡ɬaːkaʔ, kimamaʔ in naːwat͡ɬaʔtoːlli kaːnin t͡ɬein aːʧtopa aʔmo mot͡ɬaʔtoːaː naːwat͡ɬaːʔtoːlli.'

In Ukrainian, stress must be marked orthographically with an accute accent in order for vowel reduction to be rendered:
>> uk_no_stress = "Північний вітер дув з усієї сили, але чим дужче він дув, тим щильніше кутався мандрівник у своє пальто."

>> transcribe_uk(uk_no_stress)

'pʲiʋnʲiʧnɪi̯ ʋʲitɛr duu̯ z usʲijɛji sɪɫɪ ɑɫɛ ʧɪm duʒʧɛ ʋʲin duu̯ tɪm ʃʧɪɫʲnʲiʃɛ kutɑʋsʲɑ mɑndɾʲiʋnɪk u swɔjɛ pɑɫʲtɔ'

>> uk_with_stress = "Півні́чний ві́тер дув з усіє́ї си́ли, а́ле чим ду́жче він дув, тим щильні́ше ку́тався мандрівни́к у своє́ пальто́."

>> transcribe_uk(uk_with_stress)

'pʲiʋnʲˈiʧnɪi̯ ʋʲˈitɛr duu̯ z ʊsʲijˈɛji sˈɪɫɪ ˈɑɫɛ ʧɪm dˈuʒʧɛ ʋʲin duu̯ tɪm ʃʧɪɫʲnʲˈiʃɛ kˈutɐʋsʲɐ mɐndɾʲiʋnˈɪk u swɔjˈɛ pɐɫʲtˈɔ'
