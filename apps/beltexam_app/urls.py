from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r"^$", views.landing),
    url(r"^main$", views.landing),
    url(r"^register$", views.register),
    url(r"^login$", views.login),
    url(r"^success$", views.success),
    url(r"^logout$", views.logout),
    url(r"^travels$", views.travels),
    url(r"^travels/add$", views.travelsadd),
    url(r"^travels/jointrip$", views.jointrip),
    url(r"^travels/addprocess$", views.travelsaddprocess),
    url(r"^travels/destination/(?P<id>\d+)$", views.destination),
]