from django.urls import path

from . import views

urlpatterns = [
    path('', views.AgentsView.as_view(), name='agent-views'),
]