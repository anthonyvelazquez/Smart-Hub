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
        word = word.replace("what is the definition of ", "")
        profile = UserProfile.objects.get(current_profile=True)
        definition = dictionary.meaning(word)
        first_def = definition[definition.keys()[0]][0]
        context['speech_response'] = "The first definition for " + word + " is " + first_def + ". I will display the rest on the screen."
        context['ai_voice'] = profile.ai_voice
        return render(request, "lol/lol_me.html", context=context)

# https://pypi.python.org/pypi/PyDictionary/1.3.4