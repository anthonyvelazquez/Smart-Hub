from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
import datetime
from datetime import timedelta
from django.utils import timezone
from Dashboard.models import UserProfile, Alarms
import AI.CommandPhrases
from API.Functions import *
import xmltodict
import re
from random import randint

def DetectBasicGreeting(speech):
    found = False
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = base_dir + '/API/chatbot/greetings_basic.xml'
    fd = open(file,"r")
    doc = xmltodict.parse(fd.read())
    reply_length = len( doc['greeting_basic']['response_list']['response'])
    reply_choices = randint(0,reply_length) - 1
    for phrase in doc['greeting_basic']['human']:
        if speech in phrase:
            return doc['greeting_basic']['response_list']['response'][reply_choices]
    return ""

def DetectSpecificGreeting(speech):
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = base_dir + '/API/chatbot/greetings_specific.xml'
    fd = open(file,"r")
    doc = xmltodict.parse(fd.read())
    for phrase in doc['greeting_specific']['human']:
        if isinstance(phrase, dict):
            if speech in phrase['#text']:
                identifier = phrase['@id']
                print("Specific Greeting Identifier ID: " + identifier)
                for reply in doc['greeting_specific']['response_list']['response']:
                    if isinstance(phrase, dict):
                        if identifier == reply['@id']:
                            return ReplyFormatter(reply['#text'])
    return ""

def DetectAIInformationQuestions(speech):
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = base_dir + '/API/chatbot/ai_information.xml'
    fd = open(file,"r")
    doc = xmltodict.parse(fd.read())
    for phrase in doc['ai_info']['human']:
        if isinstance(phrase, dict):
            if speech in phrase['#text']:
                identifier = phrase['@id']
                print("AI Information Identifier ID: " + identifier)
                for reply in doc['ai_info']['response_list']['response']:
                    if isinstance(phrase, dict):
                        if identifier == reply['@id']:
                            return ReplyFormatter(reply['#text'])
    return ""

def ReplyFormatter(speech):
    profile = UserProfile.objects.get(current_profile=True)
    if "{ ai_name }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.ai_name , speech)
        print("Modified Reply: " + new_reply)
    else:
        new_reply = speech
        print("No Modified Values: " + new_reply)
    return new_reply

def AddBasicGreeting(speech):
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = base_dir + '/API/chatbot/greetings_basic.xml'
    fd = open(file,"r")
    doc = xmltodict.parse(fd.read())
    import xml.etree.ElementTree
    et = xml.etree.ElementTree.parse(file)

    # Append new tag: <a x='1' y='abc'>body text</a>
    # new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'response')
    new_tag = xml.etree.ElementTree.SubElement(et.find('response_list'), 'response')
    new_tag.text = 'New Greeting'
    new_tag.attrib['x'] = '1' # must be str; cannot be an int
    new_tag.attrib['y'] = 'abc'

    # Write back to file
    #et.write('file.xml')
    et.write('file_new.xml')

class ChatbotView(View):
    def get(self, request, speech):
        context = {}
        reply = DetectBasicGreeting(speech)
        if len(reply) == 0:
            print("Basic Greeting Not Detected")
            reply = DetectSpecificGreeting(speech)
        if len(reply) == 0:
            print("Specific Greeting Not Detected")
            reply = DetectAIInformationQuestions(speech)
        if len(reply) == 0:
            print("AI Information Not Detected")
            reply = "I have not been trained for that yet."
        context['speech_response'] = reply
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['ai_voice'] = profile.ai_voice
        return render(request, "mirror.html", context=context)

# http://docs.python-guide.org/en/latest/scenarios/xml/
# xmltodict