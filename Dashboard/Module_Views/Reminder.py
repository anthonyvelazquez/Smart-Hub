from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
import datetime
from datetime import timedelta
from django.utils import timezone
from Dashboard.models import UserProfile, Alarms, Reminders
import AI.CommandPhrases
from API.Functions import *

class ReminderRequestNameView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router accepts the next words as the name for the reminder
        profile.reminder_create_active = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "What do you want a reminder for?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "reminder/reminder_request.html", context=context)

class ReminderRequestTimeView(View):
    def get(self, request, name):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router accepts the next words as the time for the reminder
        profile.reminder_create_active = False
        profile.reminder_time_create_active = True
        profile.save()
        AI.CommandPhrases.Reminder_Name = name
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "When do you want me to remind you?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "reminder/reminder_request.html", context=context)

class ReminderView(View):
    def get(self, request, time):
        from dateutil import parser
        dt = parser.parse(time)
        request.session['speech_response'] = "Ok I made a reminder."
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router finishes and doesnt loop
        profile.reminder_time_create_active = False
        profile.save()
        reminder = Reminders.objects.create(profile=profile, reminder_name=AI.CommandPhrases.Reminder_Name)
        reminder.reminder_time = datetime.datetime.now()
        reminder.reminder_time = reminder.reminder_time.replace(day=dt.day, hour=dt.hour, minute=dt.minute)
        reminder.save()
        return redirect('Dashboard')

class DeleteAllReminderView(View):
    def get(self, request):
        profile = UserProfile.objects.get(current_profile=True)
        for reminder in Reminders.objects.filter(profile=profile):
            reminder.delete()
        request.session['speech_response'] = "I deleted all your reminders."
        return redirect('Dashboard')

class DeleteFirstReminderView(View):
    def get(self, request):
        profile = UserProfile.objects.get(current_profile=True)
        reminder = Reminders.objects.filter(profile=profile).first()
        reminder.delete()
        request.session['speech_response'] = "I deleted your first reminder."
        return redirect('Dashboard')

class DeleteLastReminderView(View):
    def get(self, request):
        profile = UserProfile.objects.get(current_profile=True)
        reminder = Reminders.objects.filter(profile=profile).last()
        reminder.delete()
        request.session['speech_response'] = "I deleted your last reminder."
        return redirect('Dashboard')

class CreateSpecificReminderView(View):
    def get(self, request, reminder):
        data = reminder.replace("quick reminder ", "")
        request.session['speech_response'] = "I made a reminder that says " + data
        profile = UserProfile.objects.get(current_profile=True)
        reminder = Reminders.objects.create(profile=profile, reminder_name=data)
        reminder.reminder_time = datetime.datetime.now()
        reminder.save()
        return redirect('Dashboard')