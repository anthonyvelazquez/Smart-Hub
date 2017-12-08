from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms
# from uber_rides.session import Session
# from uber_rides.client import UberRidesClient

class UberView(View):
    def get(self, request):
        context = {}
        # import ipdb; ipdb.set_trace()
        # session = Session(server_token="xGWJMYoHAo-jtiwSixmj5oFe_2EqGjct9uXwxNaJ")
        # client = UberRidesClient(session)
        # response = client.get_products(37.77, -122.41)
        # products = response.json.get('products')
        # product_id = products[0].get('product_id')
        # estimate = client.estimate_ride(
        #     product_id=product_id,
        #     start_latitude=37.77,
        #     start_longitude=-122.41,
        #     end_latitude=37.79,
        #     end_longitude=-122.41,
        #     seat_count=2
        # )
        # fare = estimate.json.get('fare')
        # response = client.get_price_estimates(
        #     start_latitude=37.770,
        #     start_longitude=-122.411,
        #     end_latitude=37.791,
        #     end_longitude=-122.405,
        #     seat_count=2
        # )

        # estimate = response.json.get('prices')

        profile = UserProfile.objects.get(current_profile=True)
        profile.save()
        context['speech_response'] = "Sleep Mode Activated"
        context['ai_voice'] = profile.ai_voice
        return render(request, "sleep.html", context=context)

    # https://github.com/uber/rides-python-sdk
    # pip install uber_rides
