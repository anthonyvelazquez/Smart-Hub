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

class NetworkScannerView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        import subprocess
        p = subprocess.Popen('ls', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print line,
        retval = p.wait()
        context['speech_response'] = "There are "
        context['ai_voice'] = profile.ai_voice
        return render(request, "reminder/reminder_request.html", context=context)
