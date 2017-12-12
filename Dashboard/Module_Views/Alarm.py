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
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router finishes and doesnt loop
        profile.alarm_creating_time = False
        profile.alarm_creating_mode = True
        profile.save()
        # Grab the alarm from the PK we saved and then set the time
        alarm = Alarms.objects.get(pk=pk)
        from dateutil import parser
        dt = parser.parse(time)
        alarm.alarm_time = datetime.datetime.now()
        alarm.alarm_time = alarm.alarm_time.replace(hour=dt.hour, minute=dt.minute)
        alarm.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "When do you want the alarm for?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "alarm/alarm_request.html", context=context)

class AlarmRequestModeView(View):
    def get(self, request, pk, mode):
        profile = UserProfile.objects.get(current_profile=True)
        # Set the profile so the command router finishes and doesnt loop
        profile.alarm_creating_mode = False
        profile.save()
        # Grab the alarm from the PK we saved and then set the time
        alarm = Alarms.objects.get(pk=pk)
        if "daily" in mode:
            alarm.daily = True
        elif "weekly" in mode:
            alarm.weekly = True
        elif "tomorrow" in mode:
            alarm.alarm_time = alarm.alarm_time + datetime.timedelta(days=1)
        alarm.save()
        request.session['speech_response'] = "I set your " + mode + " alarm."
        return redirect('Dashboard')

class CreateQuickAlarmView(View):
    def get(self, request, alarm):
        data = alarm.replace("quick alarm ", "")
        request.session['speech_response'] = "I made an alarm for " + data
        from dateutil import parser
        dt = parser.parse(data)
        profile = UserProfile.objects.get(current_profile=True)
        alarm = Alarms.objects.create(profile=profile, alarm_name="Alarm", enabled=True)
        alarm.alarm_time = datetime.datetime.now()
        # The current hour is older than the hour they want
        if alarm.alarm_time.hour > dt.hour:
            alarm.alarm_time = alarm.alarm_time + datetime.timedelta(days=1)
        # Same hour but its later than the alarm time
        elif alarm.alarm_time.hour == dt.hour and alarm.alarm_time.minute > dt.minute:
            alarm.alarm_time = alarm.alarm_time + datetime.timedelta(days=1)
        alarm.alarm_time = alarm.alarm_time.replace(hour=dt.hour, minute=dt.minute)
        alarm.save()
        return redirect('Dashboard')

class CreateSpecificAlarmView(View):
    def get(self, request, alarm):
        mode = 0
        # Used for mode 1 which means increase by certain number: 1 = secs, 2 = mins, 3 = hrs
        time_mode = 0
        if "set an alarm in" in alarm:
            mode = 1
        elif "set an alarm for" in alarm:
            mode = 2
        elif "set a repeating alarm for" in alarm:
            mode = 3
        elif "wake me up at" in alarm:
            mode = 4
        data2 = alarm.replace("wake me up at ", "")
        from dateutil import parser
        profile = UserProfile.objects.get(current_profile=True)
        alarm_obj = Alarms.objects.create(profile=profile, alarm_name="Alarm", enabled=True)
        alarm_obj.alarm_time = datetime.datetime.now()
        if mode == 1:
            data = alarm.replace("set an alarm in ", "")
            if "second" in data:
                time_mode = 2
            elif "minute" in data:
                time_mode = 2
            elif "hour" in data:
                time_mode = 3
            dt = parser.parse(data)
            request.session['speech_response'] = "I made an alarm for " + data
        elif mode == 2:
            data = alarm.replace("set an alarm for ", "")
            dt = parser.parse(data)
            request.session['speech_response'] = "I made an alarm for " + data
        elif mode == 3:
            data = alarm.replace("set a repeating alarm for ", "")
            dt = parser.parse(data)
            alarm_obj.daily = True
            request.session['speech_response'] = "I made a repeating alarm for " + data
        elif mode == 4:
            data = alarm.replace("wake me up at ", "")
            dt = parser.parse(data)
            request.session['speech_response'] = "I will wake you up at " + data
        
        # Check if alarm should be today or tomorrow
        if mode != 1:
            if alarm_obj.alarm_time.hour < dt.hour:
                alarm_obj.alarm_time = alarm_obj.alarm_time + datetime.timedelta(days=1)
            elif alarm_obj.alarm_time.hour == dt.hour and alarm_obj.alarm_time.minute < dt.minute:
                alarm_obj.alarm_time = alarm_obj.alarm_time + datetime.timedelta(days=1)
        if mode == 1:
            if time_mode == 1:
                alarm_obj.alarm_time = alarm_obj.alarm_time + datetime.timedelta(seconds=dt.second)
            elif time_mode == 2:
                alarm_obj.alarm_time = alarm_obj.alarm_time + datetime.timedelta(minutes=dt.minute)
            elif time_mode == 3:
                alarm_obj.alarm_time = alarm_obj.alarm_time + datetime.timedelta(hours=dt.hour)
        else:
            alarm_obj.alarm_time = alarm_obj.alarm_time.replace(hour=dt.hour, minute=dt.minute)
        alarm_obj.save()
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
        alarm.going_off = True
        alarm.save()
        context['alarm'] = alarm
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Your alarm called " + alarm.alarm_name + "is going off."
        context['ai_voice'] = profile.ai_voice
        return render(request, "alarm.html", context=context)

class DisableAlarmView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.alarm_active = False
        profile.sleep_active = False
        profile.save()
        alarm = Alarms.objects.get(profile=profile, going_off=True)
        alarm.going_off = False
        if alarm.daily:
            now = datetime.datetime.now()
            alarm.alarm_time = alarm.alarm_time + datetime.timedelta(days=1)
            request.session['speech_response'] = "I reset your daily alarm"
        elif alarm.weekly:
            now = datetime.datetime.now()
            alarm.alarm_time = alarm.alarm_time + datetime.timedelta(weeks=1)
            request.session['speech_response'] = "I reset your weekly alarm"
        else:
            request.session['speech_response'] = "I turned off your alarm"
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
        context['request_name'] = "Alarm Deletion"
        context['speech_response'] = "What is the name of the alarm you want to delete?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "request/simple_request.html", context=context)

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