from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import datetime
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms
import AI.CommandPhrases
from API.Functions import *
from AI.Credentials import *
import praw

reddit = praw.Reddit(client_id='9-8Sk1mkFnSl8A',
                     client_secret='1TnCOWjYoSEqSlkIeBCd6PGj5rY',
                     user_agent='SmartHub',
                     username=Reddit_Username,
                     password=Reddit_Password)

class RedditDashboardView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        print(reddit.read_only)
        for submission in reddit.subreddit('gaming').hot(limit=10):
            print(submission.title)
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = "This is your Reddit Dashboard."
        context['ai_voice'] = profile.ai_voice
        return render(request, "reddit/reddit_dashboard.html", context=context)



# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html#prerequisites


# import pprint

# # assume you have a Reddit instance bound to variable `reddit`
# submission = reddit.submission(id='39zje0')
# print(submission.title) # to make it non-lazy
# pprint.pprint(vars(submission))
