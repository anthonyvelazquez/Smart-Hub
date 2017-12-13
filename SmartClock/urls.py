from django.conf.urls import url
from SmartClock import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^Time$', views.TimeView.as_view(), name='Time'),
   
]

# https://docs.smart-mirror.io/docs/configure_the_mirror.html#giphy
