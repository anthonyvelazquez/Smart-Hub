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

class AppleFindiPhoneView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.apple_iphone_ping_request = True
        profile.save()
        GetAppleIphoneInformation(profile, context)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        GetAppleIphoneStatusFromID(profile, context)
        GetAppleIphoneLocationFromID(profile, context)
        context['location'] = GetLocationFromLatLong(context['iphone_location']['latitude'],context['iphone_location']['longitude'])[0]['address_components']
        context.update(weather_context)
        context['speech_response'] = "This is your phones location. Do you want me to ping it?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "apple/find_iphone.html", context=context)

class AppleFindiPhonePingRequestView(View):
    def get(self, request, response):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.apple_iphone_ping_request = False
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        GetAppleIphoneStatusFromID(profile, context)
        GetAppleIphoneLocationFromID(profile, context)
        context['location'] = GetLocationFromLatLong(context['iphone_location']['latitude'],context['iphone_location']['longitude'])[0]['address_components']
        context.update(weather_context)
        if "yes" in response:
            context['speech_response'] = "I am currently pinging your phone."
            PingAppleIphoneFromID(profile, context)
        else:
            context['speech_response'] = "Ok."
        context['ai_voice'] = profile.ai_voice
        return render(request, "apple/find_iphone.html", context=context)