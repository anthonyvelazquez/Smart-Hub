from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
import datetime
from datetime import timedelta
from django.utils import timezone
from Dashboard.models import UserProfile, Emails
import AI.CommandPhrases
from API.Functions import *

class EmailUnreadListView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.unread_email_request = True
        profile.save()
        for email in Emails.objects.filter(profile=profile, unread=True):
            email.delete()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        GetUnreadEmaiLListGmail(context)
        email_count = 1
        for email_id in context['id_list']:
            Emails.objects.create(profile=profile, email_number=email_count, unread=True, email_id=email_id.decode("utf-8"))
            email_count = email_count + 1
        if context['email_count'] > 0:
            context['speech_response'] = "This is a list of your unread emails. Which email number do you want to open?"
        else:
            context['speech_response'] = "You have no unread emails."
        context['ai_voice'] = profile.ai_voice
        return render(request, "email/email_list.html", context=context)

class EmailAllListView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.all_email_request = True
        profile.save()
        for email in Emails.objects.filter(profile=profile, unread=False):
            email.delete()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        GetAllEmaiLListGmail(context)
        email_count = 1
        for email_id in context['id_list']:
            Emails.objects.create(profile=profile, email_number=email_count, unread=False, email_id=email_id)
            email_count = email_count + 1
        if context['email_count'] > 0:
            context['speech_response'] = "This is a list of all your recent emails. Which email number do you want to open?"
        else:
            context['speech_response'] = "You have no emails."
        context['ai_voice'] = profile.ai_voice
        return render(request, "email/email_list.html", context=context)

class SpecificEmailUnreadView(View):
    def get(self, request, number):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.unread_email_request = False
        profile.save()
        email = Emails.objects.get(profile=profile, email_number=number, unread=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        GetUnreadEmailFromID(context, email.email_id)
        context['speech_response'] = "I opened your unread email."
        context['ai_voice'] = profile.ai_voice
        return render(request, "email/email_display.html", context=context)

class SpecificEmailAllView(View):
    def get(self, request, number):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.all_email_request = False
        profile.save()
        email = Emails.objects.get(profile=profile, email_number=number, unread=False)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        GetAllEmailFromID(context, email.email_id)
        context['speech_response'] = "I opened your email."
        context['ai_voice'] = profile.ai_voice
        return render(request, "email/email_display.html", context=context)