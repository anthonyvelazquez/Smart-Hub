from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
import datetime
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms
from coinmarketcap import Market
import AI.CommandPhrases
from API.Functions import *

coinmarketcap = Market()
class CryptoListView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['crypto_list'] = coinmarketcap.ticker(limit=10)
        context['speech_response'] = "These are the top 10 crypto currencies."
        context['ai_voice'] = profile.ai_voice
        return render(request, "crypto/crypto_list.html", context=context)

class CryptoRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.crypto_search_request = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['request_name'] = "Cryptocurrency Search"
        context['speech_response'] = "What crypto currency do you want me to look up?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "request/simple_request.html", context=context)

class CryptoDisplayView(View):
    def get(self, request, coin):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.crypto_search_request = False
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['crypto_list'] = coinmarketcap.ticker()
        found = False
        for crypto in context['crypto_list']:
            if coin in crypto['symbol'] or coin.lower() in crypto['name'].lower():
                found_coin = crypto
                found = True
                context['crypto'] = crypto
                break
        if not found:
            context['speech_response'] = "I could not find that coin in the market."
        else:
            context['speech_response'] = "This is what I found for " + found_coin['name']
        context['ai_voice'] = profile.ai_voice
        return render(request, "crypto/crypto_display.html", context=context)

    # https://github.com/mrsmn/coinmarketcap
    # pip install uber_rides

