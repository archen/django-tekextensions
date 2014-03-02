# Core Django imports
from django.conf.urls import patterns, url

# App-specific imports
from tekextensions import views

urlpatterns = patterns('',
                       url(r'^add/(?P<model_name>\w+)/?$', views.add_new_model),
                       )