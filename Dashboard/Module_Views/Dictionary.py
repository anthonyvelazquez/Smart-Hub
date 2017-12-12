from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile
from AI.Credentials import *
from PyDictionary import PyDictionary
dictionary=PyDictionary()


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

class TranslateView(View):
    def get(self, request, word):
        context = {}
        word = word.replace("translate the word ", "")
        profile = UserProfile.objects.get(current_profile=True)
        lang = "Spanish"
        trans = dictionary.translate(word, "es")
        context['word'] = word
        context['trans'] = trans
        context['lang'] = lang
        context['speech_response'] = "The word " + word + " in " + lang + " is " + trans
        context['ai_voice'] = profile.ai_voice
        return render(request, "dictionary/translate.html", context=context)

# https://pypi.python.org/pypi/PyDictionary/1.3.4