from django.urls import path
from apps.hosts.views.idc import IDCAddView


urlpatterns = [
    path('idcs/add', IDCAddView.as_view()),
]
