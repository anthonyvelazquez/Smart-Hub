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

class CurrentWeatherRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.weather_picking_location = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Where do you want me to get the current weather for?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "weather/current_weather.html", context=context)

class CurrentWeatherHereView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.weather_picking_location = False
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "This is the weather for your current location."
        context['ai_voice'] = profile.ai_voice
        return render(request, "weather/current_weather.html", context=context)

class CurrentWeatherSearchView(View):
    def get(self, request, location):
        if "here" in location:
            return redirect('Current_Weather_Here')
        else:
            context = {}
            weather_context = {}
            profile = UserProfile.objects.get(current_profile=True)
            profile.weather_picking_location = False
            profile.save()
            context['current_date'] = datetime.datetime.now()
            GetWeather(weather_context, location)
            context.update(weather_context)
            context['speech_response'] = "This is the current weather for " + context['weather_location']
            context['ai_voice'] = profile.ai_voice
            return render(request, "weather/current_weather.html", context=context)

    #     class DisplayWeatherView(View):
    # def get(self, request):
    #     data = request.session['weather'].replace("show me the weather for ", "")
    #     data = data.replace("show me the weather in ", "")
    #     data = data.replace("what is the weather in ", "")
    #     data = data.replace("what is the weather for ", "")
    #     data = data.replace("what's the weather in ", "")
    #     data = data.replace("what's the weather for ", "")
    #     print(data)
    #     profile = UserProfile.objects.get(current_profile=True)
    #     context = {}
    #     weather_context = {}
    #     context['current_date'] = datetime.datetime.now()
    #     GetWeather(weather_context, data)
    #     context.update(weather_context)
    #     context['speech_response'] = "This is the weather for " + data
    #     context['ai_voice'] = profile.ai_voice
    #     return render(request, "weather.html", context=context)