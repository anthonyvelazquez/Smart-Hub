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

class EmailUnreadListView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        GetUnreadEmaiLListGmail(context)
        if context['email_count'] > 0:
            context['speech_response'] = "This is a list of your unread emails."
        else:
            context['speech_response'] = "You have no unread emails."
        context['ai_voice'] = profile.ai_voice
        return render(request, "email/email_list.html", context=context)
