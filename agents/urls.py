from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^(?P<agent_pk>[0-9]{0,8})$', views.AgentsView.as_view(), name='agent-views'),
]