# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms, Reminders

from API.Functions import *
from AI.CommandFilter import *
from AI.Chatbot import *

class TimeView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        weather_context = {}
        commute_context = {}
        holiday_context = {}
        email_context = {}
        apple_context = {}
        start = time.time()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        end = time.time()
        print("Weather:" + str(end - start))
        start = time.time()
        #GetCommuteTimes(profile, commute_context)
        start = time.time()
        GetUnreadEmailsGmail(email_context)
        context.update(email_context)
        end = time.time()
        print("Email:" + str(end - start))
        context['profile'] = profile
        context['current_date'] = datetime.datetime.now()
        context['alarmlist'] = Alarms.objects.filter(profile=profile)
        try:
            context['speech_response'] = request.session['speech_response']
        except KeyError:
            context['speech_response'] = "Dashboard"
        if context['speech_response'] == "":
            context['speech_response'] = "Dashboard"
        context['ai_voice'] = profile.ai_voice
        return render(request, "SmartClock/time.html", context=context)