from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms, Reminders

class SleepView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.sleep_active = True
        profile.save()
        context['alarmlist'] = Alarms.objects.filter(profile=profile)
        context['reminderlist'] = Reminders.objects.filter(profile=profile)
        context['speech_response'] = "Sleep Mode Activated"
        context['ai_voice'] = profile.ai_voice
        return render(request, "sleep.html", context=context)