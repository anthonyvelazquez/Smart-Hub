from django.db import models

# Create your models here.
class UserProfile(models.Model):
    profile_name = models.TextField(default="New Profile")
    first_name = models.TextField(null=True, default=None, blank=True)
    last_name = models.TextField(null=True, default=None, blank=True)
    age = models.TextField(null=True, default=None, blank=True)
    address = models.TextField(null=True, default=None, blank=True)
    current_profile = models.BooleanField(default=False)
    
    ai_voice = models.TextField(null=True, default=None, blank=True)
    ai_name = models.TextField(null=True, default=None, blank=True)
    ai_gender = models.TextField(null=True, default=None, blank=True)
    ai_setting_name = models.BooleanField(default=False)
    ai_setting_gender = models.BooleanField(default=False)
    ai_setting_volume = models.TextField(null=True, default=None, blank=True)

    alarm_active = models.BooleanField(default=False)
    alarm_creating_name = models.BooleanField(default=False)
    alarm_creating_time = models.BooleanField(default=False)
    alarm_deleting_specific = models.BooleanField(default=False)
    
    reminder_create_active = models.BooleanField(default=False)
    math_request_active = models.BooleanField(default=False)
    sleep_active = models.BooleanField(default=False)
    search_active = models.BooleanField(default=False)

    apple_iphone_dev_count = models.IntegerField(null=True, default=None, blank=True)
    apple_iphone_ping_request = models.BooleanField(default=False)

    crypto_search_request = models.BooleanField(default=False)

    unread_email_request = models.BooleanField(default=False)
    all_email_request = models.BooleanField(default=False)

    uber_car_request = models.BooleanField(default=False)
    uber_car_seat_request = models.BooleanField(default=False)
    uber_address_request = models.BooleanField(default=False)

    #Commute
    loc_1 = models.TextField(null=True, default=None, blank=True)
    loc_2 = models.TextField(null=True, default=None, blank=True)
    loc_1_name = models.TextField(null=True, default=None, blank=True)
    loc_2_name = models.TextField(null=True, default=None, blank=True)
    loc_1_time = models.TextField(null=True, default=None, blank=True)
    loc_2_time = models.TextField(null=True, default=None, blank=True)
    commute_updated = models.DateTimeField(null=True, default=None, blank=True)
    #Weather and Times
    weather = models.TextField(null=True, default=None, blank=True)
    weather_updated = models.DateTimeField(null=True, default=None, blank=True)
    sunrise = models.DateTimeField(null=True, default=None, blank=True)
    sunset = models.DateTimeField(null=True, default=None, blank=True)
    weather_picking_location = models.BooleanField(default=False)

class Alarms(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, default=None, blank=True)
    alarm_name = models.TextField(null=True, default=None, blank=True)
    alarm_time = models.DateTimeField(null=True, default=None, blank=True)
    enabled = models.BooleanField(default=False)

class Reminders(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, default=None, blank=True)
    reminder_name = models.TextField(null=True, default=None, blank=True)
    reminder_time = models.DateTimeField(null=True, default=None, blank=True)

class Emails(models.Model):
    profile = models.ForeignKey(UserProfile, null=True, default=None, blank=True)
    # What user sees
    email_number = models.TextField(null=True, default=None, blank=True)
    # What Gmail needs
    email_id = models.TextField(null=True, default=None, blank=True)
    unread = models.BooleanField(default=False)