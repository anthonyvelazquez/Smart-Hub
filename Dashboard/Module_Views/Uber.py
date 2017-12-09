from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from API.Functions import *
import AI.CommandPhrases
session = Session(server_token="xGWJMYoHAo-jtiwSixmj5oFe_2EqGjct9uXwxNaJ")
client = UberRidesClient(session)

class UberCarTypeRequestView(View):
    def get(self, request):
       
        profile = UserProfile.objects.get(current_profile=True)
        profile.uber_car_request = True
        profile.save()
        latitude, longitude = GetLatLongFromLocation(profile.address)   
        response = client.get_products(latitude, longitude)
        products = response.json.get('products')
        product_id = products[0].get('product_id')
        # estimate = client.estimate_ride(
        #     product_id=product_id,
        #     start_latitude=37.77,
        #     start_longitude=-122.41,
        #     end_latitude=37.79,
        #     end_longitude=-122.41,
        #     seat_count=2
        # )
        # fare = estimate.json.get('fare')
        response = client.get_price_estimates(
            start_latitude=37.770,
            start_longitude=-122.411,
            end_latitude=37.791,
            end_longitude=-122.405,
            seat_count=2
        )
        estimate = response.json.get('prices')
        context = {}
        weather_context = {}
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['vehicle_list'] = products
        context['speech_response'] = "What type of Uber do you need?"
        context['ai_voice'] = profile.ai_voice
        return render(request, "uber/uber_list.html", context=context)

class UberSeatRequestView(View):
    def get(self, request, car):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.uber_car_request = False
        profile.uber_car_seat_request = True
        profile.save()
        AI.CommandPhrases.Uber_Car = car
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['request_name'] = "Number of Uber seats needed"
        context['speech_response'] = "How many seats do you need"
        context['ai_voice'] = profile.ai_voice
        return render(request, "request/simple_request.html", context=context)

class UberAddressRequestView(View):
    def get(self, request, seat):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.uber_car_seat_request = False
        profile.uber_address_request = True
        profile.save()
        AI.CommandPhrases.Uber_Seats = seat
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['request_name'] = "Uber Destination Needed"
        context['speech_response'] = "Where do you want to go"
        context['ai_voice'] = profile.ai_voice
        return render(request, "request/simple_request.html", context=context)

class UberEstimateView(View):
    def get(self, request, address):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.uber_address_request = False
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        latitude, longitude = GetLatLongFromLocation(profile.address)   
        des_latitude, des_longitude = GetLatLongFromLocation(address)   
        response = client.get_products(latitude, longitude)
        products = response.json.get('products')
        product_id = ""
        for product in products:
            if (product['display_name']).lower() in AI.CommandPhrases.Uber_Car.lower():
                product_id = product.get('product_id')
                break
        response = client.get_price_estimates(
            start_latitude=latitude,
            start_longitude=longitude,
            end_latitude=des_latitude,
            end_longitude=des_longitude,
            seat_count=int(AI.CommandPhrases.Uber_Seats)
        )
        estimate = response.json.get('prices')
        for car in estimate:
            if AI.CommandPhrases.Uber_Car.lower() in (car['display_name']).lower():
                context['car'] = car
                break
        context['speech_response'] = "This is an estimate cost for your uber."
        context['ai_voice'] = profile.ai_voice
        return render(request, "uber/uber_estimate.html", context=context)

    # https://github.com/uber/rides-python-sdk
    # pip install uber_rides
