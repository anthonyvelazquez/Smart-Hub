from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile
from AI.Credentials import *
from PyDictionary import PyDictionary
from googletrans import Translator
dictionary=PyDictionary()
translator = Translator()

class DefinitionView(View):
    def get(self, request, word):
        context = {}
        if "what is the definition of" in word:
            word = word.replace("what is the definition of ", "")
        elif "what is the meaning of" in word:
            word = word.replace("what is the meaning of ", "")
        elif "define" or "Define" in word:
            word = word.replace("define ", "")
            word = word.replace("Define ", "")
        profile = UserProfile.objects.get(current_profile=True)
        definition = dictionary.meaning(word)
        first_def = definition[definition.keys()[0]][0]
        def_length = len(definition.keys())
        type_list = []
        def_list = []
        for defs in definition.keys():
            type_list.append(defs)
        for types in type_list:
            def_list.append(definition[types])
        print(type_list)
        print(def_list)
        context['word'] = word
        context['definition_list'] = zip(type_list, def_list)
        context['speech_response'] = "The first definition for " + word + " is " + first_def + ". I will display the rest on the screen."
        context['ai_voice'] = profile.ai_voice
        return render(request, "dictionary/definition.html", context=context)

class SynAntView(View):
    def get(self, request, word):
        context = {}
        word = word.replace("what is the synonym for ", "")
        word = word.replace("what is the antonym for ", "")
        word = word.replace("what are the synonyms for ", "")
        word = word.replace("what are the antonyms for ", "")
        print(word)
        profile = UserProfile.objects.get(current_profile=True)
        syn = dictionary.synonym(word)
        ant = dictionary.antonym(word)
        context['syn'] = syn
        context['ant'] = ant
        context['word'] = word
        context['speech_response'] = "Here are a list of synonyms and antonyms for the word " + word
        context['ai_voice'] = profile.ai_voice
        return render(request, "dictionary/synant.html", context=context)

class TranslateWordView(View):
    def get(self, request, word):
        context = {}
        phrase = word.replace("translate the word ", "")
        word_list = phrase.split()
        profile = UserProfile.objects.get(current_profile=True)
        lang = word_list[-1]
        lang_code = ""
        for code, name in languages:
            if lang.lower() in name.lower():
                lang_code = code
        trans = translator.translate(word_list[0], dest=lang_code)
        context['word'] = word_list[0]
        context['trans'] = trans.text
        context['lang'] = lang
        context['speech_response'] = "The word " + word_list[0] + " in " + lang + " is " + trans.text
        context['ai_voice'] = profile.ai_voice
        return render(request, "dictionary/translate.html", context=context)

class TranslateSentenceView(View):
    def get(self, request, sentence):
        context = {}
        phrase = sentence.replace("translate the sentence ", "")
        word_list = phrase.split()
        profile = UserProfile.objects.get(current_profile=True)
        lang = word_list[-1]
        lang_code = ""
        for code, name in languages:
            if lang.lower() in name.lower():
                lang_code = code
        translation_phrase = ""
        word_section = 0
        for word in word_list:
            if word_section <= len(word_list) - 3:
                translation_phrase = translation_phrase + word + " "
            word_section = word_section + 1
        trans = translator.translate(translation_phrase, dest=lang_code)
        context['word'] = translation_phrase
        context['trans'] = trans.text
        context['lang'] = lang
        context['speech_response'] = "The sentence " + translation_phrase + " in " + lang + " is " + trans.text
        context['ai_voice'] = profile.ai_voice
        return render(request, "dictionary/translate.html", context=context)

# https://pypi.python.org/pypi/PyDictionary/1.3.4
# https://pypi.python.org/pypi/googletrans
# https://gist.github.com/alexanderjulo/4073388


languages = [
    ('aa', 'Afar'),
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('ak', 'Akan'),
    ('sq', 'Albanian'),
    ('am', 'Amharic'),
    ('ar', 'Arabic'),
    ('an', 'Aragonese'),
    ('hy', 'Armenian'),
    ('as', 'Assamese'),
    ('av', 'Avaric'),
    ('ae', 'Avestan'),
    ('ay', 'Aymara'),
    ('az', 'Azerbaijani'),
    ('ba', 'Bashkir'),
    ('bm', 'Bambara'),
    ('eu', 'Basque'),
    ('be', 'Belarusian'),
    ('bn', 'Bengali'),
    ('bh', 'Bihari languages'),
    ('bi', 'Bislama'),
    ('bo', 'Tibetan'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('my', 'Burmese'),
    ('ca', 'Catalan; Valencian'),
    ('cs', 'Czech'),
    ('ch', 'Chamorro'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cv', 'Chuvash'),
    ('kw', 'Cornish'),
    ('co', 'Corsican'),
    ('cr', 'Cree'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('dv', 'Divehi; Dhivehi; Maldivian'),
    ('nl', 'Dutch; Flemish'),
    ('dz', 'Dzongkha'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('ee', 'Ewe'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fj', 'Fijian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('fr', 'French'),
    ('fy', 'Western Frisian'),
    ('ff', 'Fulah'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gv', 'Manx'),
    ('el', 'Greek, Modern (1453-)'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('ha', 'Hausa'),
    ('he', 'Hebrew'),
    ('hz', 'Herero'),
    ('hi', 'Hindi'),
    ('ho', 'Hiri Motu'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('hy', 'Armenian'),
    ('ig', 'Igbo'),
    ('is', 'Icelandic'),
    ('io', 'Ido'),
    ('ii', 'Sichuan Yi; Nuosu'),
    ('iu', 'Inuktitut'),
    ('ie', 'Interlingue; Occidental'),
    ('ia', 'Interlingua (International Auxiliary Language Association)'),
    ('id', 'Indonesian'),
    ('ik', 'Inupiaq'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kn', 'Kannada'),
    ('ks', 'Kashmiri'),
    ('ka', 'Georgian'),
    ('kr', 'Kanuri'),
    ('kk', 'Kazakh'),
    ('km', 'Central Khmer'),
    ('ki', 'Kikuyu; Gikuyu'),
    ('rw', 'Kinyarwanda'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kv', 'Komi'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('kj', 'Kuanyama; Kwanyama'),
    ('ku', 'Kurdish'),
    ('lo', 'Lao'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('li', 'Limburgan; Limburger; Limburgish'),
    ('ln', 'Lingala'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('lu', 'Luba-Katanga'),
    ('lg', 'Ganda'),
    ('mk', 'Macedonian'),
    ('mh', 'Marshallese'),
    ('ml', 'Malayalam'),
    ('mi', 'Maori'),
    ('mr', 'Marathi'),
    ('ms', 'Malay'),
    ('Mi', 'Micmac'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('mi', 'Maori'),
    ('ms', 'Malay'),
    ('my', 'Burmese'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('nr', 'Ndebele, South; South Ndebele'),
    ('nd', 'Ndebele, North; North Ndebele'),
    ('ng', 'Ndonga'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('no', 'Norwegian'),
    ('oc', 'Occitan (post 1500)'),
    ('oj', 'Ojibwa'),
    ('or', 'Oriya'),
    ('om', 'Oromo'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pi', 'Pali'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('rn', 'Rundi'),
    ('ru', 'Russian'),
    ('sg', 'Sango'),
    ('sa', 'Sanskrit'),
    ('si', 'Sinhala; Sinhalese'),
    ('sk', 'Slovak'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('se', 'Northern Sami'),
    ('sm', 'Samoan'),
    ('sn', 'Shona'),
    ('sd', 'Sindhi'),
    ('so', 'Somali'),
    ('st', 'Sotho, Southern'),
    ('es', 'Spanish; Castilian'),
    ('sq', 'Albanian'),
    ('sc', 'Sardinian'),
    ('sr', 'Serbian'),
    ('ss', 'Swati'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ty', 'Tahitian'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('te', 'Telugu'),
    ('tg', 'Tajik'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('ti', 'Tigrinya'),
    ('to', 'Tonga (Tonga Islands)'),
    ('tn', 'Tswana'),
    ('ts', 'Tsonga'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('tw', 'Twi'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('ve', 'Venda'),
    ('vi', 'Vietnamese'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('wo', 'Wolof'),
    ('xh', 'Xhosa'),
    ('yi', 'Yiddish'),
    ('yo', 'Yoruba'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]