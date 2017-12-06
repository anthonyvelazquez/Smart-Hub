from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from Dashboard.models import UserProfile, Alarms, Reminders

from API.Functions import *
from AI.CommandFilter import *
from AI.Chatbot import *

Testing = False

def PingTry(host):
    import subprocess
    ping = subprocess.Popen(["ping", host], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    out, error = ping.communicate()
    print (out) #This will show me the ping result, I can check the content and see if the host replyed or not
class DashboardView(View):
    def get(self, request):
        #PingTry("192.168.1.1")
        context = {}
        profile = UserProfile.objects.get(current_profile=True)
        if not Testing:
            weather_context = {}
            commute_context = {}
            holiday_context = {}
            email_context = {}
            apple_context = {}
            start = time.time()
            GetProfileWeather(profile, weather_context)
            context.update(weather_context)
            end = time.time()
            print("Weather:" + str(end - start))
            start = time.time()
            #GetCommuteTimes(profile, commute_context)
            context.update(commute_context)
            end = time.time()
            print("Commute:" + str(end - start))
            start = time.time()
            GetHolidays(profile, holiday_context)
            context.update(holiday_context)
            end = time.time()
            print("Holidays:" + str(end - start))
            start = time.time()
            # GetAppleIphoneInformation(profile, apple_context)
            context.update(apple_context)
            end = time.time()
            print("Apple:" + str(end - start))
            start = time.time()
            client = gnewsclient()
            context['headlines'] = client.get_news()
            end = time.time()
            print("Headline:" + str(end - start))
            start = time.time()
            GetUnreadEmailsGmail(email_context)
            context.update(email_context)
            end = time.time()
            print("Email:" + str(end - start))
        context['profile'] = profile
        context['current_date'] = datetime.datetime.now()
        context['alarmlist'] = Alarms.objects.filter(profile=profile)
        context['reminderlist'] = Reminders.objects.filter(profile=profile)
        try:
            context['speech_response'] = request.session['speech_response']
        except KeyError:
            context['speech_response'] = "Dashboard"
        try:
            if request.session['summary']:
                context['speech_response'] = GetDashboardSummarySpeech(profile, context)
        except KeyError:
            context['speech_response'] = "Dashboard"
        context['ai_voice'] = profile.ai_voice
        # context['alarm_url'] = reverse('Alarm_Display')
        #https://stackoverflow.com/questions/45906482/how-to-stream-opencv-frame-with-django-frame-in-realtime
        
        context['test'] = Testing
        return render(request, "index.html", context=context)

class SetupView(View):
    def get(self, request, profile_id):
        context = {}
        profile = UserProfile.objects.get(pk=profile_id)
        if not profile.current_profile:
            profile.current_profile = True
            profile.save()
        context['profile'] = profile
        return render(request, "setup.html", context=context)
    def post(self, request, profile_id):
        data = request.POST
        context = {}
        profile = UserProfile.objects.get(pk=profile_id)
        if data['prof_name']:
            profile.profile_name = data['prof_name']
        if data['f_name']:
            profile.first_name = data['f_name']
        if data['l_name']:
            profile.last_name = data['l_name']
        if data['address']:
            profile.address = data['address']
        if data['loc_1']:
            profile.loc_1 = data['loc_1']
        if data['loc_1_name']:
            profile.loc_1_name = data['loc_1_name']
        if data['loc_2']:
            profile.loc_2 = data['loc_2']
        if data['loc_2_name']:
            profile.loc_2_name = data['loc_2_name']
        profile.save()
        return redirect('Setup', profile_id=profile.pk)

class ProfileView(View):
    def get(self, request):
        context = {}
        context['profilelist'] = UserProfile.objects.all()
        return render(request, "profile.html", context=context)

class ProfileSelectorView(View):
    def get(self, request):
        context = {}
        context['profilelist'] = UserProfile.objects.all()
        return render(request, "profile.html", context=context)    

class CreateProfileView(View):
    def get(self, request):
        UserProfile.objects.create()
        return redirect('Profile')

class MathRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = request.session['speech_response']
        context['ai_voice'] = profile.ai_voice
        return render(request, "mirror.html", context=context)

class MathView(View):
    def get(self, request):
        data = request.session['equation'].replace("what is ", "")
        data = data.replace("what's", "")
        data = data.replace("times", "*")
        data = data.replace("minus", "-")
        data = data.replace("plus", "+")
        data = data.replace("divided by", "/")
        print(data)
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        context['question'] = data
        try:
            context['answer_speech'] = str(eval(data))
            context['answer'] = " = " + context['answer_speech']
            context['answer_speech'] = "The answer is" + context['answer_speech']
        except ZeroDivisionError:
            context['question'] = "Cannot Divide By Zero"
            context['answer_speech'] = "You cannot divide by zero."
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        return render(request, "math.html", context=context)

class MirrorView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = request.session['speech_response']
        context['ai_voice'] = profile.ai_voice
        return render(request, "mirror.html", context=context)

class SearchRequestView(View):
    def get(self, request):
        context = {}
        weather_context = {}
        profile = UserProfile.objects.get(current_profile=True)
        profile.search_active = True
        profile.save()
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = request.session['speech_response']
        context['ai_voice'] = profile.ai_voice
        return render(request, "mirror.html", context=context)

from googleapiclient.discovery import build
import pprint
my_api_key = "AIzaSyA6gpXzXxGQVV43PK1iq6Tdo2WOoffymgc"
my_cse_id = "014442162659748437345:fwfisy_a-pq"

def google_search(search_term, api_key, cse_id, **kwargs):
    # https://developers.google.com/apis-explorer/#p/customsearch/v1/search.cse.list
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

class SearchResultView(View):
    def get(self, request):
        context = {}
        weather_context = {}

        results = google_search(request.session['search'], my_api_key, my_cse_id, num=1, searchType="image")
        # for result in results:
        #     pprint.pprint(result)
        profile = UserProfile.objects.get(current_profile=True)
        context['current_date'] = datetime.datetime.now()
        GetProfileWeather(profile, weather_context)
        context.update(weather_context)
        context['speech_response'] = request.session['speech_response']
        context['ai_voice'] = profile.ai_voice
        context['image_link'] = results[0]['link']
        return render(request, "search.html", context=context)

class VoiceCommandView(View):
    def post(self, request):
        data = request.POST
        profile = UserProfile.objects.get(current_profile=True)
        request.session['summary'] = False
        if profile.ai_setting_name:
            print("AI Setup Active: Name")
            response, request.session['ai_info'] = AISetupCommandRouter(True, 1, profile, data['command'])
        elif profile.ai_setting_gender:
            print("AI Setup Active: Gender")
            response, request.session['ai_info'] = AISetupCommandRouter(True, 2, profile, data['command'])
        elif profile.sleep_active:
            print("Sleep Mode Active: ")
            response, request.session['speech_response'] = SleepCommandRouter(True, profile, data['command'])
        elif profile.alarm_active:
            print("Alarm is Currently Going Off: ")
            response = AlarmCommandRouter(True, profile, data['command'])
        elif profile.apple_iphone_ping_request:
            print("Apple Ping Request Active: ")
            response = AppleCommandRouter(True, profile, data['command'])
        elif profile.search_active:
            print("Search is Active: " + data['command'])
            response, request.session['speech_response'], request.session['search'] = SearchCommandRouter(True, profile, data['command'])
        elif profile.reminder_create_active:
            print("Reminder is Active: " + data['command'])
            response, request.session['reminder'] = ReminderCommandRouter(True, profile, data['command'])
        elif profile.math_request_active:
            print("Math is Active: " + data['command'])
            response, request.session['equation'] = EquationCommandRouter(True, profile, data['command'])
        elif profile.weather_picking_location:
            print("Weather Search Active: " + data['command'])
            response = WeatherCommandRouter(True, data['command'])
        else:
            # if "find my iPhone" in data['command']:
            #     response = {'status': 200, 'message': "Your error", 'url':reverse('iPhone')}
            print("Checking Navigation")
            found, response, request.session['speech_response'] = NavigationCommandRouter(data['command'])
            if not found:
                print("Checking Setup")
                found, response = AISetupCommandRouter(False, 1, profile, data['command'])
            if not found:
                print("Checking Sleep")
                found, response = SleepCommandRouter(False, profile, data['command'])
            if not found:
                print("Checking Alarm")
                found, response = AlarmCommandRouter(False, profile, data['command'])
            if not found:
                print("Checking Search")
                found, response, request.session['speech_response'] = SearchCommandRouter(False, profile, data['command'])
            if not found:
                print("Checking Reminder")
                found, response = ReminderCommandRouter(False, profile, data['command'])
            if not found:
                print("Checking Email")
                found, response = EmailCommandRouter(profile, data['command'])
            if not found:
                print("Checking Apple")
                found, response = AppleCommandRouter(False, profile, data['command'])
            if not found:
                print("Checking Weather")
                found, response = WeatherCommandRouter(False, data['command'])
            # if not found:
            #     print("Checking Equation")
            #     found, response, request.session['speech_response'], request.session['equation'] = EquationCommandRouter(False, profile, data['command'])
            if not found:
                    # *******************************************
                    # A.I. Commands
                    # *******************************************
                if "what's new" in data['command'] or "what is new" in data['command']:
                    request.session['summary'] = True
                    response = {'status': 200, 'message': "Your error", 'url':reverse('Dashboard')}
                    # *******************************************
                    # Chatbot Commands
                    # *******************************************
                else:
                    print("Unknown Command: " + data['command'])
                    response = ChatbotCommandRouter(data['command'])
        import json
        return HttpResponse(json.dumps(response), content_type='application/json')
# https://github.com/clayshieh/PySMS
# https://www.hackster.io/tinkernut/diy-vintage-spotify-radio-using-a-raspberry-pi-bc3322
# https://github.com/tweepy/tweepy
# https://kamranicus.com/guides/raspberry-pi-3-baby-monitor#the-hardware