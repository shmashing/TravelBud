from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='home'),
  url(r'^add$', views.add_travel, name='addPlans'),
  url(r'^(?P<id>\d+)/submit_travel$', views.submit_travel, name='submitTravels'),
  url(r'^destination/(?P<id>\d+)$', views.show_destination, name='travelPage'),
  url(r'^destination/(?P<id>\d+)/addUser$', views.add_user, name='addUser'),
]
