import datetime
from datetime import timedelta
from django.utils import timezone
import googlemaps
import holidays
import pyowm
import smtplib
import time
import imaplib
import re
import email
from gnewsclient import gnewsclient
gmaps = googlemaps.Client(key='AIzaSyBrYIZY34HfYPrhUr7pkecChHstvs64nsY')
from pyicloud import PyiCloudService

def GetProfileWeather(profile, context):
    #https://github.com/csparpa/pyowm
    #print(profile.weather_updated)
    if(datetime.datetime.now(timezone.utc) - profile.weather_updated) > timedelta(1):
        print("24hrs have passed since last weather update")
        owm = pyowm.OWM('e7ca91961c67928b30ecda2a78dc9f28')
        # Have a pro subscription? Then use:
        # owm = pyowm.OWM(API_key='your-API-key', subscription_type='pro')
        observation = owm.weather_at_coords(int(gmaps.geocode(profile.address)[0]['geometry']['location']['lat']),int(gmaps.geocode(profile.address)[0]['geometry']['location']['lng']))
        w = observation.get_weather()
        temp = w.get_temperature('fahrenheit')
        profile.weather = temp['temp']
        profile.sunrise = datetime.datetime.fromtimestamp(w.get_sunrise_time())
        profile.sunset = datetime.datetime.fromtimestamp(w.get_sunset_time())
        profile.weather_updated = datetime.datetime.now()
        profile.save()
    context['weather'] = profile.weather
    context['sunrise'] = profile.sunrise
    context['sunset'] = profile.sunset

def GetWeather(context, location):
    owm = pyowm.OWM('e7ca91961c67928b30ecda2a78dc9f28')
    searched_location = gmaps.geocode(location)
    observation = owm.weather_at_coords(int(searched_location[0]['geometry']['location']['lat']),int(searched_location[0]['geometry']['location']['lng']))
    w = observation.get_weather()
    temp = w.get_temperature('fahrenheit')
    temp_c = w.get_temperature('celsius')
    context['weather'] = temp['temp']
    context['sunrise'] = datetime.datetime.fromtimestamp(w.get_sunrise_time())
    context['sunset'] = datetime.datetime.fromtimestamp(w.get_sunset_time())
    context['wind'] = w.get_wind()
    context['cloud'] = w.get_clouds()
    context['rain'] = w.get_rain()
    context['snow'] = w.get_snow()
    context['temp_f'] = temp
    context['temp_c'] = temp_c
    context['status'] = w.get_status()
    context['humidity'] = w.get_humidity()
    context['weather_location'] = searched_location[0]['formatted_address']

def GetCommuteTimes(profile, context):
    now = datetime.datetime.now()
    directions_result = gmaps.directions(profile.address,profile.loc_1,mode="driving",departure_time=now)
    directions_result2 = gmaps.directions(profile.address,profile.loc_2,mode="driving",departure_time=now)
    context['loc_1_time'] = directions_result[0]['legs'][0]['duration']['text']
    context['loc_2_time'] = directions_result2[0]['legs'][0]['duration']['text']
    context['loc_1'] = profile.loc_1_name
    context['loc_2'] = profile.loc_2_name

def GetHolidays(profile, context):
    now = datetime.datetime.now()
    upcoming = []
    for date, name in sorted(holidays.US(state='NJ', years=2017).items()):
        if date > now.date():
            upcoming.append(name)
    context['holidays'] = upcoming

def GetAppleIphoneInformation(profile, context):
        api = PyiCloudService('anthonyhvelazquez@icloud.com', 'Velazquez185934')
        devices = api.devices
        dev_name = []
        dev_batt = []
        count = 0
        for device in devices:
            if "iPhone" in device.status()['deviceDisplayName']:
                print(device)
                print("Dev Count:" + str(count))
                profile.apple_iphone_dev_count = count
                profile.save()
            count = count + 1
            # dev_name.append(device.status()['deviceDisplayName'])
            # dev_batt.append(float(device.status()['batteryLevel']) * 100)
        # if api.requires_2sa:
        #     import click
        #     print "Two-step authentication required. Your trusted devices are:"

        #     devices = api.trusted_devices
        #     for i, device in enumerate(devices):
        #         print "  %s: %s" % (i, device.get('deviceName',
        #             "SMS to %s" % device.get('phoneNumber')))

        #     device = click.prompt('Which device would you like to use?', default=0)
        #     device = devices[device]
        #     if not api.send_verification_code(device):
        #         print "Failed to send verification code"
        #         sys.exit(1)

        #     code = click.prompt('Please enter validation code')
        #     if not api.validate_verification_code(device, code):
        #         print "Failed to verify verification code"
        #         sys.exit(1)
        # https://github.com/picklepete/pyicloud
        context['apple_devices'] = zip(dev_name, dev_batt)
def GetLocationFromLatLong(lat, long):
    return gmaps.reverse_geocode((float(lat), float(long)))
def GetAppleIphoneStatusFromID(profile, context):
        api = PyiCloudService('anthonyhvelazquez@icloud.com', 'Velazquez185934')
        devices = api.devices
        context['iphone_status'] = devices[profile.apple_iphone_dev_count].status()

def GetAppleIphoneLocationFromID(profile, context):
        api = PyiCloudService('anthonyhvelazquez@icloud.com', 'Velazquez185934')
        devices = api.devices
        context['iphone_location'] = devices[profile.apple_iphone_dev_count].location()

def PingAppleIphoneFromID(profile, context):
        api = PyiCloudService('anthonyhvelazquez@icloud.com', 'Velazquez185934')
        devices = api.devices
        context['iphone_location'] = devices[profile.apple_iphone_dev_count].play_sound()
def GetUnreadEmailsGmail(context):
        # https://codehandbook.org/how-to-read-email-from-gmail-using-python/
        ORG_EMAIL   = "@gmail.com"
        FROM_EMAIL  = "anthonyhvelazquez" + ORG_EMAIL
        FROM_PWD    = "velazquez1"
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993
        fromlist = []
        subjlist = []
        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL,FROM_PWD)
            mail.select('inbox')

            type, data = mail.search(None, '(UNSEEN)')

            mail_ids = data[0]

            id_list = mail_ids.split()   
            context['email_count'] = len(id_list)
        #     first_email_id = int(id_list[0])
        #     latest_email_id = int(id_list[-1])
        #     if(len(id_list) > 0):
        #         for i in range(first_email_id, latest_email_id+1):
        #             typ, data = mail.fetch(str(i), '(RFC822)' )
        #             for response_part in data:
        #                 if isinstance(response_part, tuple):
        #                     msg = email.message_from_string(response_part[1].decode('utf-8'))
        #                     email_subject = msg['subject']
        #                     email_from = res1 = re.sub(r'\<[^)]*\>', '', msg['from']) #Removes everything between < and > which is usually the email address
        #                     fromlist.append(email_from)
        #                     subjlist.append(email_subject)
        #     else:
        #         print("No New Emails")
        except Exception as e:
            print(e)
        # context['emaillist'] = zip(fromlist, subjlist)
        # context['emails'] = range(0, 5)

def GetUnreadEmaiLListGmail(context):
        # https://codehandbook.org/how-to-read-email-from-gmail-using-python/
        ORG_EMAIL   = "@gmail.com"
        FROM_EMAIL  = "anthonyhvelazquez" + ORG_EMAIL
        FROM_PWD    = "velazquez1"
        SMTP_SERVER = "imap.gmail.com"
        SMTP_PORT   = 993
        fromlist = []
        subjlist = []
        try:
            mail = imaplib.IMAP4_SSL(SMTP_SERVER)
            mail.login(FROM_EMAIL,FROM_PWD)
            mail.select('inbox')

            type, data = mail.search(None, '(UNSEEN)')

            mail_ids = data[0]

            id_list = mail_ids.split()   
            context['email_count'] = len(id_list)
            first_email_id = int(id_list[0])
            latest_email_id = int(id_list[-1])
            if(len(id_list) > 0):
                for i in range(first_email_id, latest_email_id+1):
                    typ, data = mail.fetch(str(i), '(BODY.PEEK[])' )
                    for response_part in data:
                        if isinstance(response_part, tuple):
                            msg = email.message_from_string(response_part[1].decode('utf-8'))
                            email_subject = msg['subject']
                            email_from = res1 = re.sub(r'\<[^)]*\>', '', msg['from']) #Removes everything between < and > which is usually the email address
                            email_from = msg['from']
                            fromlist.append(email_from)
                            subjlist.append(email_subject)
            else:
                print("No New Emails")
        except Exception as e:
            print(e)
        context['emaillist'] = zip(fromlist, subjlist)
        print("Unread Emails:" + str(len(id_list)))
        for a,b in zip(fromlist, subjlist):
            print("From:" + a)
            print("Sub:" + b)
        context['emails'] = range(0, len(id_list))

def GetDashboardSummarySpeech(profile, context):
    message = "Hello " + profile.first_name + "."
    message = message + "This is your summary for today."
    from dateutil import tz
    print((profile.sunset).astimezone(tz.tzlocal()))
    message = message + "It is " + datetime.datetime.now().strftime("%A %B %d, %Y %I %M %p") + "."
    message = message + "You have " + str(context['email_count']) + "unread emails."
    reminder = str(Reminders.objects.filter(profile=profile).count())
    message = message + "You have " + reminder + " reminders as well."
    message = message + "The temperature is " + str(round(float(profile.weather))) + "degrees farenheit "
    if(float(profile.weather) >= 80):
        message = message + "so it is a bit hot outside. You might want to wear shorts."
    elif(float(profile.weather) <= 50):
        message = message + "so it is a bit cold outside. You might want to wear a jacket or thick sweater."
    else:
        message = message + "so it is normal outside."
    message = message + "Finally, the sun will set at " + ((profile.sunset).astimezone(tz.tzlocal())).strftime("%I %M %p")
    return message

def GetNetworkDevices():
    import subprocess
    nmap = subprocess.Popen(('nmap'), stdout=subprocess.PIPE)
    ipout = nmap.communicate()[0]