from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile
from subprocess import call

class SystemVolumeUpView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['speech_response'] = "Volume Increased"
        context['ai_voice'] = profile.ai_voice
        call(["amixer", "sset", "'Master'", "100%"])        
        return render(request, "mirror.html", context=context)

class SystemVolumeDownView(View):
    def get(self, request):
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['speech_response'] = "Volume Decreased"
        context['ai_voice'] = profile.ai_voice
        call(["amixer", "sset", "'Master'", "0%"])
        return render(request, "mirror.html", context=context)