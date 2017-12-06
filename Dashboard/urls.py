from django.conf.urls import url
from Dashboard import views
from Dashboard.Module_Views.Alarm import *
from Dashboard.Module_Views.Sleep import *
from Dashboard.Module_Views.Reminder import *
from Dashboard.Module_Views.Setup import *
from Dashboard.Module_Views.Email import *
from Dashboard.Module_Views.Apple import *
from Dashboard.Module_Views.LoL import *
from Dashboard.Module_Views.Weather import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^$', views.DashboardView.as_view(), name='Dashboard'),
    # *******************************************
    # Setup
    # *******************************************
    url(r'^Setup/AI/Name/Request$', AISetupNameRequestView.as_view(), name='AI_Setup_Name_Request'),
    url(r'^Setup/AI/Name$', AISetupNameView.as_view(), name='AI_Setup_Name'),
    url(r'^Setup/AI/Gender/Request$', AISetupGenderRequestView.as_view(), name='AI_Setup_Gender_Request'),
    url(r'^Setup/AI/Gender$', AISetupGenderView.as_view(), name='AI_Setup_Gender'),
    url(r'^Profile$', views.ProfileView.as_view(), name='Profile'),
    url(r'^Profile/Create$', views.CreateProfileView.as_view(), name='Profile_Create'),
    # *******************************************
    # Alarm
    # *******************************************
    url(r'^Alarm/Request$', AlarmRequestView.as_view(), name='Alarm_Request'),
    url(r'^Alarm/Request/Name/(?P<pk>[^/]+)/(?P<name>[^/]+)$', AlarmRequestNameView.as_view(), name='Alarm_Request_Set_Name'),
    url(r'^Alarm/Request/Time/(?P<pk>[^/]+)/(?P<time>[^/]+)$', AlarmRequestTimeView.as_view(), name='Alarm_Request_Set_Time'),
    url(r'^Alarm/Request/Specific$', CreateSpecificAlarmView.as_view(), name='Alarm_Create_Specific'),
    url(r'^Alarm/Disable$', DisableAlarmView.as_view(), name='Alarm_Disable'),
    url(r'^Alarm/Delete/All$', DeleteAllAlarmView.as_view(), name='Alarm_Delete_All'),
    url(r'^Alarm/Delete/Request$', DeleteAlarmRequestView.as_view(), name='Alarm_Delete_Request_Name'),
    url(r'^Alarm/Delete/Request/(?P<name>[^/]+)$', DeleteSpecificAlarmView.as_view(), name='Alarm_Delete_Specific'),
    url(r'^Alarm/Display/(?P<pk>[^/]+)$', DisplayAlarmView.as_view(), name='Alarm_Display'),
    # *******************************************
    # Email
    # *******************************************
    url(r'^Email/List/Unread$', EmailUnreadListView.as_view(), name='Email_Unread_List'),
    # *******************************************
    # League of Legends
    # *******************************************
    url(r'^LoL/Me$', SelfLoLProfileView.as_view(), name='LoL_Me'),
    # *******************************************
    # Apple
    # *******************************************
    url(r'^Apple/iPhone/Find$', AppleFindiPhoneView.as_view(), name='Apple_Find_iPhone'),
    url(r'^Apple/iPhone/Find/Ping/(?P<response>[^/]+)$', AppleFindiPhonePingRequestView.as_view(), name='Apple_Find_iPhone_Ping_Request'),
    # *******************************************
    # Weather
    # *******************************************
    url(r'^Weather/Current/Request$', CurrentWeatherRequestView.as_view(), name='Current_Weather_Request'),
    url(r'^Weather/Current/Here$', CurrentWeatherHereView.as_view(), name='Current_Weather_Here'),
    url(r'^Weather/Current/Search/(?P<location>[^/]+)$', CurrentWeatherSearchView.as_view(), name='Current_Weather_Search'),
    # *******************************************
    # Alarm
    # *******************************************
    url(r'^Setup/(?P<profile_id>[^/]+)$', views.SetupView.as_view(), name='Setup'),
    url(r'^Command$', csrf_exempt(views.VoiceCommandView.as_view()), name='Voice_Command'),
    url(r'^Math/Request$', views.MathRequestView.as_view(), name='Math_Request'),
    url(r'^Math/Solve$', views.MathView.as_view(), name='Math'),
    # *******************************************
    # Reminder
    # *******************************************
    url(r'^Reminder/Request$', ReminderRequestView.as_view(), name='Reminder_Request'),
    url(r'^Reminder/Create$', ReminderView.as_view(), name='Reminder'),
    url(r'^Reminder/Delete/All$', DeleteAllReminderView.as_view(), name='Reminder_Delete_All'),
    url(r'^Reminder/Delete/First$', DeleteFirstReminderView.as_view(), name='Reminder_Delete_First'),
    url(r'^Reminder/Delete/Last$', DeleteLastReminderView.as_view(), name='Reminder_Delete_Last'),
    # *******************************************
    # Alarm
    # *******************************************
    url(r'^Mirror$', views.MirrorView.as_view(), name='Mirror'),
    # *******************************************
    # Sleep
    # *******************************************
    url(r'^Sleep$', SleepView.as_view(), name='Sleep'),
    # *******************************************
    # Alarm
    # *******************************************
    url(r'^Search/Request$', views.SearchRequestView.as_view(), name='Search_Request'),
    url(r'^Search/Result$', views.SearchResultView.as_view(), name='Search_Result'),
    url(r'^Conversation$', views.ConversationView.as_view(), name='Conversation'),
]

# https://docs.smart-mirror.io/docs/configure_the_mirror.html#giphy
