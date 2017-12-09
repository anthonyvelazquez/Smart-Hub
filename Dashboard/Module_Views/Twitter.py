from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import datetime
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms
import AI.CommandPhrases
from API.Functions import *
from AI.Credentials import *

import twitter
api = twitter.Api(consumer_key='T6VOKns0NMdoMRm3CoaFVdhRb',
                      consumer_secret='LsOCq5dXptdSVZVwp8aWoqPZHTeJEXoWKjZvPlh3gGNC1pvPdX',
                      access_token_key='803818229743439872-zGu2Wi7koZvrTkegzCwuWJk0eKbBBFJ',
                      access_token_secret='DQs1QN33S45nkASiFDF2CxfJduxypjUJbZAW72mIodzon')
class TwitterTimelineView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        # print(api.VerifyCredentials())
        statuses = api.GetHomeTimeline()
        context['status_list'] = statuses
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "This is your Twitter Timeline."
        context['ai_voice'] = profile.ai_voice
        return render(request, "twitter/twitter_timeline.html", context=context)

class TwitterRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "What do you want me to post on Twitter?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "request/simple_request.html", context=context)

class TwitterTweetView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Is this what you want me to post?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "reddit/reddit_dashboard.html", context=context)

class TwitterPostedView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "Is this what you want me to post?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "reddit/reddit_dashboard.html", context=context)


# https://python-twitter.readthedocs.io/en/latest/twitter.html