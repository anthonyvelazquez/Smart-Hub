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

class AlarmRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router accepts the next words as the name for the alarm
        profile.alarm_creating_name = True
        profile.save()
        # Create alarm and store ID so we can edit
        alarm = Alarms.objects.create(profile=profile, alarm_name="Alarm", enabled=True)
        AI.CommandPhrases.Alarm_PK = alarm.pk
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "What do you want the name of your alarm to be?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "alarm/alarm_request.html", context=context)

class AlarmRequestNameView(View):
    def get(self, request, pk, name):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router accepts the next words as the time for the alarm
        profile.alarm_creating_name = False
        profile.alarm_creating_time = True
        profile.save()
        # Grab the alarm from the PK we saved and then set the name
        alarm = Alarms.objects.get(pk=pk)
        alarm.alarm_name = name
        alarm.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "What do you want the time for the alarm to be?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "alarm/alarm_request.html", context=context)

class AlarmRequestTimeView(View):
    def get(self, request, pk, time):
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router finishes and doesnt loop
        profile.alarm_creating_time = False
        profile.save()
        # Grab the alarm from the PK we saved and then set the time
        alarm = Alarms.objects.get(pk=pk)
        from dateutil import parser
        dt = parser.parse(time)
        alarm.alarm_time = datetime.datetime.now()
        alarm.alarm_time = alarm.alarm_time.replace(hour=dt.hour, minute=dt.minute)
        alarm.save()
        request.session['speech_response'] = "I set your alarm."
        return redirect('Dashboard')

class CreateSpecificAlarmView(View):
    def get(self, request):
        data = request.session['command'].replace("make an alarm for ", "")
        data = data.replace("set an alarm for ", "")
        request.session['speech_response'] = "I made an alarm for " + data
        from dateutil import parser
        dt = parser.parse(data)
        profile = UserProfile.objects.get(current_profile=True)
        alarm = Alarms.objects.create(profile=profile, alarm_name="Alarm", enabled=True)
        alarm.alarm_time = datetime.datetime.now()
        alarm.alarm_time = alarm.alarm_time.replace(hour=dt.hour, minute=dt.minute)
        alarm.save()
        return redirect('Dashboard')

class DisplayAlarmView(View):
    def get(self, request, pk):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.alarm_active = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        alarm = Alarms.objects.get(pk=pk)
        context['alarm'] = alarm
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        return render(request, "alarm.html", context=context)

class DisableAlarmView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        request.session['speech_response'] = "I turned off your alarm"
        profile = UserProfile.objects.get(current_profile=True)
        profile.alarm_active = False
        profile.alarm_creating_name = False
        profile.alarm_creating_time = False
        profile.save()
        alarm = Alarms.objects.get(profile=profile, enabled=True)
        alarm.enabled = False
        alarm.save()
        return redirect('Dashboard')

class DeleteAlarmRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router accepts the next words as the name for the alarm
        profile.alarm_deleting_specific = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "What is the name of the alarm you want to delete?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "mirror.html", context=context)

class DeleteSpecificAlarmView(View):
    def get(self, request, name):
        context = {}
        request.session['speech_response'] = "I deleted your alarm named " + name
        profile = UserProfile.objects.get(current_profile=True)
        profile.alarm_deleting_specific = False
        profile.alarm_creating_name = False
        profile.alarm_creating_time = False
        profile.save()
        for alarm in Alarms.objects.filter(profile=profile):
            if alarm.alarm_name in name:
                alarm.delete()
        return redirect('Dashboard')

class DeleteAllAlarmView(View):
    def get(self, request):
        context = {}
        request.session['speech_response'] = "I deleted all your alarms"
        profile = UserProfile.objects.get(current_profile=True)
        profile.alarm_creating_name = False
        profile.alarm_creating_time = False
        profile.save()
        for alarm in Alarms.objects.filter(profile=profile):
            alarm.delete()
        return redirect('Dashboard')