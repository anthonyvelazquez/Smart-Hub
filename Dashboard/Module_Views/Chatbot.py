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
import os
import xml.etree.ElementTree


def SpeechFromXML(speech):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    from sys import platform
    if platform == "linux" or platform == "linux2":
        print("Linux System")
        folder = base_dir + "\\API\\chatbot\\"
    elif platform == "darwin":
        print("Mac System")
        folder = base_dir + "/API/chatbot/"
    elif platform == "win32":
        print("Windows System")
        folder = base_dir + "\\API\\chatbot\\"
    import glob
    # Grab all XML Filenames
    for filename in glob.glob(folder + '*.xml'):
        print("Checking File:" + filename)
        # Open each file and turn to dict
        file = open(filename,"r")
        xmldict = xmltodict.parse(file.read())
        # Get root name
        et = xml.etree.ElementTree.parse(filename)
        root = et.getroot().tag
        # Check human words
        for phrase in xmldict[root]['human']:
            # Check if its a matching conversation or generic
            if isinstance(phrase, dict):
                if speech in phrase['#text']:
                    # Found the match now get the ID so you can match a reply
                    identifier = phrase['@id']
                    print(root + " Identifier ID: " + identifier)
                    # Check every response in response_list for a match
                    # Check if there are multiple replies available that have an ID
                    specific_replies = [] 
                    for reply in xmldict[root]['response_list']['response']:
                        if isinstance(reply, dict):
                            if identifier == reply['@id']:
                                specific_replies.append(reply['#text'])
                    # Get length of list and select random reply
                    length = len(specific_replies)
                    return ReplyFormatter(specific_replies[randint(0, length-1)])
            else:
                if speech in phrase:
                    # Get list of generic replies available
                    generic_replies = []
                    for reply in xmldict[root]['response_list']['response']:
                        if not isinstance(reply, dict):
                            generic_replies.append(reply)
                    # Get length of list and select random reply
                    length = len(generic_replies)
                    return ReplyFormatter(generic_replies[randint(0, length-1)])
    # Didnt find any matches
    return "I have not been trained for that yet"

def ReplyFormatter(speech):
    profile = UserProfile.objects.get(current_profile=True)
    if "{ ai_name }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.ai_name , speech)
        print("Modified Name Reply: " + new_reply)
    elif "{ ai_gender }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.ai_gender , speech)
        print("Modified Gender Reply: " + new_reply)
    elif "{ f_name }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.first_name , speech)
        print("Modified Name Reply: " + new_reply)
    elif "{ l_name }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.last_name , speech)
        print("Modified Name Reply: " + new_reply)
    elif "{ address }" in speech:
        new_reply = re.sub(r'\{[^)]*\}', profile.address , speech)
        print("Modified Address Reply: " + new_reply)
    else:
        new_reply = speech
        print("No Modified Values: " + new_reply)
    return new_reply

def AddBasicGreeting(speech):
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file = base_dir + '/API/chatbot/greetings_basic.xml'
    fd = open(file,"r")
    doc = xmltodict.parse(fd.read())
    et = xml.etree.ElementTree.parse(file)

    # Append new tag: <a x='1' y='abc'>body text</a>
    # new_tag = xml.etree.ElementTree.SubElement(et.getroot(), 'response')
    print("Root Name: " + et.getroot().tag)
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
        reply = SpeechFromXML(speech)
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