from django.urls import path

from . import views

urlpatterns = [
    path('', views.all_agents, name='all-agents'),
]