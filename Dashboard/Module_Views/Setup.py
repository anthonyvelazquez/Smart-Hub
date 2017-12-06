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

class AISetupNameRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.ai_setting_name = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Hello. Lets start off by giving me a name. What do you want my name to be?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "setup/setup.html", context=context)

class AISetupNameView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.ai_setting_name = False
        profile.ai_name = request.session['ai_info']
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Ok my new name will be " + request.session['ai_info']
        context['ai_voice'] = profile.ai_voice
        return render(request, "setup/setup.html", context=context)

class AISetupGenderRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.ai_setting_gender = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Am I a man or a woman?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "setup/setup.html", context=context)

class AISetupGenderView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.ai_setting_gender = False
        profile.ai_gender = request.session['ai_info']
        if "woman" in request.session['ai_info'] or "female" in request.session['ai_info']:
            profile.ai_voice = "UK English Female"
            profile.ai_gender = "female"
        else:
            profile.ai_voice = "UK English Male"
            profile.ai_gender = "male"
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Ok I am now a " + request.session['ai_info']
        context['ai_voice'] = profile.ai_voice
        return redirect('Dashboard')

class ProfileNameSetupView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        if "woman" in request.session['ai_info'] or "female" in request.session['ai_info']:
            profile.ai_voice = "UK English Female"
        else:
            profile.ai_voice = "UK English Male"
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Ok I am now a " + request.session['ai_info']
        context['ai_voice'] = profile.ai_voice
        return redirect('Dashboard')