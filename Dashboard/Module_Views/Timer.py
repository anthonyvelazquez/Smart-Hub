from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import datetime
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile
from dateutil import parser

class TimerSetView(View):
    def get(self, request, timer):
        mode = 0
        # Used for mode 1 which means increase by certain number: 1 = secs, 2 = mins, 3 = hrs
        time_mode = 0
        if "set timer for" in timer:
            data = timer.replace("set timer for ", "")
        elif "set a timer for" in timer:
            data = timer.replace("set a timer for ", "")
        if "second" in data:
            time_mode = 1
        elif "minute" in data:
            time_mode = 2
        elif "hour" in data:
            time_mode = 3
        context = {}
        dt = parser.parse(data)
        profile = UserProfile.objects.get(current_profile=True)
        if time_mode == 1:
            profile.timer_time = datetime.datetime.now() + datetime.timedelta(seconds=dt.second)
        elif time_mode == 2:
            profile.timer_time = datetime.datetime.now() + datetime.timedelta(minutes=dt.minute)
        elif time_mode == 3:
            profile.timer_time = datetime.datetime.now() + datetime.timedelta(hours=dt.hour)
        profile.timer_enabled = True
        profile.save()
        context['timer'] = profile.timer_time
        context['on'] = profile.timer_enabled
        context['speech_response'] = "This is your timer"
        context['ai_voice'] = profile.ai_voice
        return render(request, "misc/timer.html", context=context)

class TimerDoneView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.timer_time = datetime.datetime.now()
        profile.timer_enabled = False
        profile.save()
        context['timer'] = profile.timer_time
        context['on'] = profile.timer_enabled
        context['speech_response'] = "Your timer is done"
        context['ai_voice'] = profile.ai_voice
        return render(request, "misc/timer.html", context=context)

class TimerDisplayView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['timer'] = profile.timer_time
        context['speech_response'] = ""
        context['ai_voice'] = profile.ai_voice
        return render(request, "misc/timer.html", context=context)
